import os
import requests
import json
from github import Github

# Retrieve GitHub token from environment variables
GITHUB_TOKEN = os.getenv("PAT_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Ensure PAT_TOKEN is set in GitHub secrets.")

# GitHub repository details
REPO_NAME = "Deepak-Sekar-p/hello-grad"
DATA_FILE_PATH = "data/uk_postcodes.json"

def fetch_postcode_data():
    """
    Fetch postcode data from Postcodes.io API (no API key required).
    """
    url = "https://api.postcodes.io/postcodes?q=London"
    print(f"Fetching postcode data from: {url}")

    response = requests.get(url, timeout=60)

    if response.status_code == 404:
        raise Exception("Error 404: API endpoint not found.")
    elif response.status_code != 200:
        raise Exception(f"Failed to fetch postcode data: {response.status_code} {response.text}")

    return response.json()

def update_github_file(data):
    """
    Update postcode data in GitHub repository.
    """
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)

    with open(DATA_FILE_PATH, 'w') as f:
        json.dump(data, f, indent=4)

    try:
        contents = repo.get_contents(DATA_FILE_PATH)
        repo.update_file(
            DATA_FILE_PATH,
            "Update postcode data",
            json.dumps(data, indent=4),
            contents.sha
        )
        print("Postcode data updated successfully.")
    except Exception:
        repo.create_file(
            DATA_FILE_PATH,
            "Create postcode data file",
            json.dumps(data, indent=4)
        )
        print("Postcode data file created successfully.")

if __name__ == "__main__":
    try:
        postcode_data = fetch_postcode_data()
        update_github_file(postcode_data)
    except Exception as e:
        print(f"Error encountered: {e}")
