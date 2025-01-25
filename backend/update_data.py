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

# List of all UK postcode areas
POSTCODE_AREAS = [
    "AB", "AL", "B", "BA", "BB", "BD", "BH", "BL", "BN", "BR", "BS", "BT", "CA", "CB",
    "CF", "CH", "CM", "CO", "CR", "CT", "CV", "CW", "DA", "DD", "DE", "DG", "DH", "DL",
    "DN", "DT", "DY", "E", "EC", "EH", "EN", "EX", "FK", "FY", "G", "GL", "GU", "GY",
    "HA", "HD", "HG", "HP", "HR", "HS", "HU", "HX", "IG", "IM", "IP", "IV", "KA", "KT",
    "KW", "KY", "L", "LA", "LD", "LE", "LL", "LN", "LS", "LU", "M", "ME", "MK", "ML",
    "N", "NE", "NG", "NN", "NP", "NR", "NW", "OL", "OX", "PA", "PE", "PH", "PL", "PO",
    "PR", "RG", "RH", "RM", "S", "SA", "SE", "SG", "SK", "SL", "SM", "SN", "SO", "SP",
    "SR", "SS", "ST", "SW", "SY", "TA", "TD", "TF", "TN", "TQ", "TR", "TS", "TW", "UB",
    "W", "WA", "WC", "WD", "WF", "WN", "WR", "WS", "WV", "YO", "ZE"
]

def fetch_all_postcodes():
    """
    Fetch postcode data area by area using Postcodes.io API.
    """
    all_postcodes = []

    for area in POSTCODE_AREAS:
        url = f"https://api.postcodes.io/postcodes?q={area}"
        print(f"Fetching postcode data for area: {area}")
        response = requests.get(url, timeout=60)

        if response.status_code == 200:
            data = response.json()
            if data.get("status") == 200 and data.get("result"):
                all_postcodes.extend(data["result"])
            else:
                print(f"No results found for area {area}")
        else:
            print(f"Failed to fetch postcode data for {area}: {response.status_code} {response.text}")

    return all_postcodes

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
        postcode_data = fetch_all_postcodes()
        update_github_file(postcode_data)
    except Exception as e:
        print(f"Error encountered: {e}")
