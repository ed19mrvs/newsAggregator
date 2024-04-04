from django.contrib import admin
from .models import Author, Story

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'username','password')  # Display these fields in the admin list view

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('headline', 'category', 'region', 'author', 'date', 'details')