import requests
import json

class NewsClient:
    def __init__(self):
        self.base_url = None  
        self.logged_in = False
        self.username = None

    def login(self, url):
        self.base_url = url
        username = input("Enter username: ")
        password = input("Enter password: ")
        payload = {"username": username, "password": password}
        headers = {'Content-Type': 'application/json'}  # Specify JSON content type
        response = requests.post(f"{self.base_url}/api/login/", data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            print("Login successful.")
            self.logged_in = True
            self.username = username
        else:
            print("Login failed. Please check your credentials.")

    def logout(self):
        if not self.logged_in:
            print('You are not logged in')
            return
        response = requests.post(f"{self.base_url}/api/logout/")
        if response.status_code == 200:
            self.logged_in = False
            print("Logout successful.")
        else:
            print("Logout failed.")

    def post_story(self):
        if not self.logged_in:
            print("Please log in first.")
            return
        
        headline = input("Enter story headline: ")
        category = input("Enter story category: ")
        region = input("Enter story region: ")
        details = input("Enter story details: ")
        author = self.username
        
        payload = {
            "headline": headline,
            "category": category,
            "region": region,
            "details": details,
            "author": author
        }
        response = requests.post(f"{self.base_url}/api/stories/", json=payload)
        if response.status_code == 201:
            data = response.json()
            unique_key = data.get('unique_key')
            print(f"Story posted successfully. Unique key: {unique_key}")
        else:
            print("Failed to post story.")

    def get_news(self, agency=None, cat=None, reg=None, date=None):
        response = requests.get("https://newssites.pythonanywhere.com/api/directory/")
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    for agency_info in data:
                        if not isinstance(agency_info, dict):
                            print("Invalid data format for agency info. Skipping.")
                            continue
                        agency_code = agency_info.get('agency_code')
                        if agency and agency_code != agency:
                            continue
                        agency_url = agency_info.get('url')
                        news_url = f"{agency_url}/api/stories"
                        
                        # Construct payload for news request
                        payload = {}
                        if cat:
                            payload['story_cat'] = cat
                        if reg:
                            payload['story_region'] = reg
                        if date:
                            payload['story_date'] = date

                        news_response = requests.get(news_url, params=payload)
                        
                        if news_response.status_code == 200:
                            news_data = news_response.json()
                            if isinstance(news_data, list):
                                print(f"\n=== News from {agency_code} ===\n")
                                for news_item in news_data:
                                    if not isinstance(news_item, dict):
                                        print("Invalid data format for news item. Skipping.")
                                        continue
                                    print(f"Headline: {news_item.get('headline')}")
                                    print(f"Category: {news_item.get('story_cat')}")
                                    print(f"Region: {news_item.get('story_region')}")
                                    print(f"Date: {news_item.get('story_date')}")
                                    print(f"Details: {news_item.get('story_details')}\n")
                            else:
                                print(f"No news found from {agency_code}.")
                        else:
                            print(f"Failed to fetch news from {agency_code}: {news_response.text}")
            except Exception as e:
                print(f"Error occurred: {e}")
        else:
            print(f"Failed to fetch agencies: {response.text}")

    def register_agency(self, agency_name, url, agency_code):
        if not self.logged_in:
            print("Please log in first.")
            return
        
        payload = {
            "agency_name": agency_name,
            "url": url,
            "agency_code": agency_code
        }
        headers = {'Content-Type': 'application/json'}  
        response = requests.post(f"{self.base_url}/api/directory/", json=payload, headers=headers)
        if response.status_code == 201:
            print("Agency registered successfully.")
        else:
            print(f"Failed to register agency: {response.text}")

    def list_agencies(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print("\n=== Agencies ===\n")
                for agency in data:
                    print(f"Agency Name: {agency.get('agency_name')}")
                    print(f"URL: {agency.get('url')}")
                    print(f"Agency Code: {agency.get('agency_code')}\n")
            else:
                print("No agencies found.")
        else:
            print(f"Failed to fetch agencies: {response.text}")

    def delete_story(self, story_key):
        if not self.logged_in:
            print("Please log in first.")
            return
        response = requests.delete(f"{self.base_url}api/stories/{story_key}/")
        if response.status_code == 200:
            print("Story deleted successfully.")
        else:
            print(f"Failed to delete story: {response.text}")

client = NewsClient()
debug=False

while True:
    command = input("Enter command (login, logout, post, news, list, delete, exit): ").lower()
    
    if command == "login":
        url = input("Enter login URL: ")
        client.login(url)
    elif command == "logout":
        client.logout()
    elif command == "post":
        client.post_story()
    elif command == "news":
        agency = input("Enter news agency code (optional): ")
        cat = input("Enter news category (optional): ")
        reg = input("Enter region (optional): ")
        date = input("Enter date (optional): ")
        client.get_news(agency, cat, reg, date)
    elif command == "list":
        url = input("Enter directory URL: ")
        client.list_agencies(url)
    elif command == "delete":
        story_key = input("Enter story key to delete: ")
        client.delete_story(story_key)
    elif command == "exit":
        break
    else:
        print("Invalid command. Please try again.")