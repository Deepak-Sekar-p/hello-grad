import os
import requests
import zipfile
import io
import json
from github import Github

# Retrieve GitHub token from environment variables
GITHUB_TOKEN = os.getenv("PAT_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Ensure PAT_TOKEN is set in GitHub secrets.")

# GitHub repository details
REPO_NAME = "Deepak-Sekar-p/hello-grad"
DATA_FILE_PATH = "data/uk_postcodes.json"

# ONS Postcode Directory ZIP file URL (replace with the updated URL from the portal)
ONS_ZIP_URL = "https://www.arcgis.com/sharing/rest/content/items/2cc9b1e28d0a4c748391526ddf426b16/data"

def download_and_extract_zip(url):
    """
    Download and extract the ZIP file containing the ONS Postcode Directory.
    """
    response = requests.get(url)
    if response.status_code == 200:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            for filename in z.namelist():
                if filename.endswith(".csv"):
                    print(f"Extracting: {filename}")
                    with z.open(filename) as f:
                        return f.read().decode("utf-8")
    else:
        raise Exception(f"Failed to download file: {response.status_code} {response.text}")

def process_postcode_csv(csv_content):
    """
    Process the ONS CSV data to extract relevant postcode information.
    """
    lines = csv_content.splitlines()
    headers = lines[0].split(",")
    postcode_index = headers.index("pcds")  # Postcode column
    lat_index = headers.index("lat")       # Latitude column
    long_index = headers.index("long")     # Longitude column
    
    postcodes = []
    for line in lines[1:]:  # Skip the header
        columns = line.split(",")
        postcodes.append({
            "postcode": columns[postcode_index],
            "latitude": float(columns[lat_index]),
            "longitude": float(columns[long_index]),
        })
    return postcodes

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
        print("Downloading ONS Postcode Directory...")
        csv_data = download_and_extract_zip(ONS_ZIP_URL)
        print("Processing postcode data...")
        postcode_data = process_postcode_csv(csv_data)
        print("Updating GitHub repository...")
        update_github_file(postcode_data)
    except Exception as e:
        print(f"Error encountered: {e}")
