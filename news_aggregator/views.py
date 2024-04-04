from django.http import JsonResponse, HttpResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from .models import Story, Author
import json
from datetime import datetime
import pytz 
import random
import string

from django.utils import timezone  # Import timezone

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            author = Author.objects.get(username=username)
        except Author.DoesNotExist:
            return HttpResponse("User does not exist", status=401)

        if author.password == password:
            request.session['logged_in_user'] = username
            return HttpResponse("Login successful", status=200)
        else:
            return HttpResponse("Login failed. Invalid credentials.", status=401)
    else:
        return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def logout_user(request):
    if request.method == 'POST':
        return HttpResponse("Logout successful", status=200)
    else:
        return HttpResponse("Method not allowed", status=405)

import json
from uuid import uuid4
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from .models import Story

@csrf_exempt
def post_story(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            headline = data.get('headline')
            category = data.get('category')
            region = data.get('region')
            details = data.get('details')
            author = data.get('author')
            current_date = timezone.now()
            
            # Generate a random unique key
            unique_key = int(''.join(random.choices(string.digits, k=5)))
            
            # Create the Story object with the generated unique key
            story = Story.objects.create(
                unique_key=unique_key,
                headline=headline,
                category=category,
                region=region,
                details=details,
                author=author,
                date=current_date
            )
            response_data = {
                "message": "Story posted successfully",
                "unique_key": unique_key
            }
            return HttpResponse(json.dumps(response_data), content_type="application/json", status=201)
        except Exception as e:
            print(f"Exception occurred: {str(e)}")  # Print the exception message
            return HttpResponse(f"Unable to post story: {str(e)}", status=503)
    else:
        return HttpResponseNotAllowed(['POST'])

    

def get_stories(request):
    if request.method == 'GET':
        # Retrieve the parameters from the request
        category = request.GET.get('story_cat')
        region = request.GET.get('story_region')
        date = request.GET.get('story_date')

        # Prepare filter parameters for the query
        filter_params = {}

        # Handle category parameter
        if category != '*':
            filter_params['category'] = category

        # Handle region parameter
        if region != '*':
            filter_params['region'] = region

        # Handle date parameter
        if date != '*':
            try:
                filter_params['date__gte'] = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            except ValueError:
                return HttpResponse("Invalid date format. Please provide dates in YYYY-MM-DD format or use '*' as a wildcard.", status=400)

        # Retrieve stories based on the filter parameters
        stories = Story.objects.filter(**filter_params)

        if stories:
            # Serialize the stories
            serialized_stories = [{
                'headline': story.headline,
                'story_cat': story.category,
                'story_region': story.region,
                'author': story.author,
                'story_date': story.date.strftime('%Y-%m-%d'),
                'story_details': story.details
            } for story in stories]

            return JsonResponse({'stories': serialized_stories}, status=200)
        else:
            return HttpResponse("No stories found", status=404)
    else:
        return HttpResponseNotAllowed(['GET'])
    
@csrf_exempt
def delete_story(request, key):
    if request.method == 'DELETE':
        try:
            print('HERE1')
            # Attempt to delete the story with the given key
            story = Story.objects.get(unique_key=key)
            print('HERE2')
            story.delete()
            return HttpResponse("Story deleted successfully", status=200)
        except Story.DoesNotExist:
            return HttpResponse("Story not found", status=404)
        except Exception as e:
            return HttpResponse(f"Failed to delete story: {str(e)}", status=503)
    else:
        return HttpResponseNotAllowed(['DELETE'])

