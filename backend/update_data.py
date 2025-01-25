import requests
import json
import os
from github import Github

# GitHub token for authentication
GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Ensure PAT_TOKEN is set in GitHub secrets.")

# API Key for Ordnance Survey (if required)
API_KEY = os.getenv("ORDNANCE_SURVEY_API_KEY")

# GitHub repository details
REPO_NAME = "Deepak-Sekar-p/hello-grad"
DATA_FILE_PATH = "data/uk_postcodes.json"

def fetch_postcode_data():
    """
    Fetch postcode data from Ordnance Survey API.
    """
    url = "https://api.ordnancesurvey.co.uk/opendata/downloads/products/PostcodeBoundaries/latest"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    print(f"Fetching postcode data from: {url}")
    response = requests.get(url, headers=headers, timeout=60)

    if response.status_code != 200:
        print(f"Error: Failed to fetch data from {url}")
        print(f"Response Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        raise Exception("Failed to fetch postcode data")

    return response.json()

def update_github_file(data):
    """
    Update postcode data in GitHub repository.
    """
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    try:
        contents = repo.get_contents(DATA_FILE_PATH)
        repo.update_file(
            DATA_FILE_PATH,
            "Update postcode data",
            json.dumps(data, indent=4),
            contents.sha
        )
        print("Postcode data updated successfully.")
    except Exception as e:
        # If the file does not exist, create it
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
