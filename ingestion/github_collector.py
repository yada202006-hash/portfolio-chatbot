import os
import requests
from dotenv import load_dotenv
load_dotenv()

class GitHubCollector:
    def __init__(self):
        self.username = os.getenv("GITHUB_USERNAME")
        self.base_url = "https://api.github.com"
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_user_profile(self):
        url=f"{self.base_url}/users/{self.username}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching user profile for {self.username}")
            return None

    def get_user_repositories(self):
        repositories = []
        page = 1
        while True:
            url = f"{self.base_url}/users/{self.username}/repos?page={page}&per_page=100"
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                repos = response.json()
                if not repos:
                    break
                repositories.extend(repos)
                page += 1
            else:
                print(f"Error fetching repositories for {self.username}")
                break
        return repositories

    def get_readme(self,repo_name):
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/readme"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

        else:
            print(f"Error fetching README for repository {repo_name}")
            return None

    def get_languages(self,repo_name):
        url = f"{self.base_url}/repos/{self.username}/{repo_name}/languages"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching languages for repository {repo_name}")
            return None
    