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

    def get_news(self, params=None):
        if params is None:
            params = {}

        response = requests.get(f"{self.base_url}/api/news/", params=params)

        if response.status_code == 200:
            data = response.json().get('news')
            if data:
                print("\n=== News ===\n")
                for idx, news_item in enumerate(data, start=1):
                    print(f"News {idx}:")
                    print(f"  Headline: {news_item.get('headline')}")
                    print(f"  Category: {news_item.get('category')}")
                    print(f"  Region: {news_item.get('region')}")
                    print(f"  Date: {news_item.get('date')}")
                    print(f"  Details: {news_item.get('details')}\n")
            else:
                print("No news found.")
        else:
            print(f"Failed to fetch news: {response.text}")

    def list_agencies(self):
        response = requests.get(f"{self.base_url}api/directory/")
        if response.status_code == 200:
            data = response.json().get('agency_list')
            if data:
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

while True:
    command = input("Enter command (login, logout, post, news, list, delete, exit): ").lower()
    
    if command == "login":
        url = input("Enter login URL: ")
        client.login(url)
    elif command == "logout":
        client.logout()
    elif command == "post":
        client.post_story()
    elif command.startswith("news"):
        # Parse command options
        params = {}
        options = command.split()[1:]
        for option in options:
            key, value = option.split("=")
            params[key.strip("-")] = value
        client.get_news(params)
    elif command == "list":
        client.list_agencies()
    elif command == "delete":
        story_key = input("Enter story key to delete: ")
        client.delete_story(story_key)
    elif command == "exit":
        break
    else:
        print("Invalid command. Please try again.")
