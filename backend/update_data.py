import requests
import json
import os
from github import Github

# Constants
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # GitHub token for authentication
REPO_NAME = "Deepak-Sekar-p/hello-grad"
DATA_FILE_PATH = "uk_postcodes.json"

# Function to fetch postcode data from an open API (e.g., Ordnance Survey, OpenData)
def fetch_postcode_data():
    url = "https://api.ordnancesurvey.co.uk/opendata/downloads/products/PostcodeBoundaries/latest"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch postcode data")

# Function to update the data file on GitHub
def update_github_file(data):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Get the existing content
    try:
        contents = repo.get_contents(DATA_FILE_PATH)
        repo.update_file(
            DATA_FILE_PATH,
            "Update postcode data",
            json.dumps(data, indent=4),
            contents.sha
        )
    except Exception:
        # If the file does not exist, create it
        repo.create_file(
            DATA_FILE_PATH,
            "Create postcode data file",
            json.dumps(data, indent=4)
        )
    print("Postcode data updated successfully.")

if __name__ == "__main__":
    try:
        postcode_data = fetch_postcode_data()
        update_github_file(postcode_data)
    except Exception as e:
        print(f"Error: {e}")
