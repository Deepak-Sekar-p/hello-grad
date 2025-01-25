import os
import requests
import json
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
REPO_NAME = "Deepak-Sekar-p/hello-grad"
DATA_FILE_PATH = "data/uk_postcodes.json"

def fetch_postcode_data():
    url = "https://api.ordnancesurvey.co.uk/opendata/downloads/products/PostcodeBoundaries/latest"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch postcode data: {response.status_code} {response.text}")

    return response.json()

def update_github_file(data):
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    # Ensure data directory exists
    os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)

    # Check if file exists in repo
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
        # If file does not exist, create it
        with open(DATA_FILE_PATH, 'w') as f:
            json.dump(data, f, indent=4)
        repo.create_file(
            DATA_FILE_PATH,
            "Create postcode data file",
            json.dumps(data, indent=4)
        )
        print("Postcode data file created successfully.")

if __name__ == "__main__":
    postcode_data = fetch_postcode_data()
    update_github_file(postcode_data)
