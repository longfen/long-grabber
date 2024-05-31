import os
import sys
import requests
import random
import string

def generate_random_name(length=10):
    """Generate a random name for the repository."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def create_github_repository(repo_name, github_token):
    """Create a new GitHub repository."""
    headers = {"Authorization": f"token {github_token}"}
    data = {"name": repo_name, "private": False}
    response = requests.post("https://api.github.com/user/repos", json=data, headers=headers)
    return response.json().get("html_url")

def upload_to_github(files_path, github_repo_url):
    """Upload files to the GitHub repository."""
    os.chdir(files_path)
    os.system("git init")
    os.system("git add .")
    os.system("git commit -m 'Automated upload'")
    os.system(f"git remote add origin {github_repo_url}")
    os.system("git push -u origin master")

def main():
    # Generate a random repository name
    repo_name = generate_random_name()

    # Replace with your GitHub personal access token
    github_token = "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"

    # Create a new GitHub repository
    github_repo_url = create_github_repository(repo_name, github_token)

    # Upload files to the GitHub repository
    files_path = "C:/path/to/your/files"
    upload_to_github(files_path, github_repo_url)

    print("Files uploaded to:", github_repo_url)

if __name__ == "__main__":
    main()
