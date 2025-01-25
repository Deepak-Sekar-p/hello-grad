from fastapi import FastAPI
import requests
import json
from cachetools import cached, TTLCache
import os

app = FastAPI()

# GitHub raw URL where postcode data is stored
GITHUB_RAW_URL = "https://raw.githubusercontent.com/Deepak-Sekar-p/hello-grad/main/data/uk_postcodes.json"

# Ensure GitHub token is set correctly
GITHUB_TOKEN = os.getenv("PAT_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GitHub token not found. Ensure PAT_TOKEN is set in GitHub secrets.")

# Cache data for 1 hour
cache = TTLCache(maxsize=1, ttl=3600)

@cached(cache)
def fetch_postcode_data():
    """
    Fetch postcode data from GitHub and cache it.
    """
    response = requests.get(GITHUB_RAW_URL, headers={"Authorization": f"token {GITHUB_TOKEN}"})
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch postcode data: {response.status_code} {response.text}")

    return json.loads(response.text)

@app.get("/api/postcodes")
async def get_postcodes():
    """
    Endpoint to serve postcode data.
    """
    postcodes = fetch_postcode_data()
    return {"data": postcodes}

@app.get("/")
async def root():
    return {"message": "Welcome to the Hello Grad UK Postcode API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
