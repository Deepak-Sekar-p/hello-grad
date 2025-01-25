import requests
import json
import os
from github import Github

# Use the correct environment variable name for GitHub authentication
GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
REPO_NAME = "Deepak-Sekar-p/hello-grad"
DATA_FILE_PATH = "data/uk_postcodes.json"

def fetch_postcode_data():
    url = "https://api.ordnancesurvey.co.uk/opendata/downloads/products/PostcodeBoundaries/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch postcode data")

def update_github_file(data):
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
    except Exception:
        repo.create_file(
            DATA_FILE_PATH,
            "Create postcode data file",
            json.dumps(data, indent=4)
        )
    print("Postcode data updated successfully.")

if __name__ == "__main__":
    postcode_data = fetch_postcode_data()
    update_github_file(postcode_data)
