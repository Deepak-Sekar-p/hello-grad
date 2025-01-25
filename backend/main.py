from fastapi import FastAPI
import requests
import json
from cachetools import cached, TTLCache

app = FastAPI()

GITHUB_RAW_URL = "https://raw.githubusercontent.com/yourusername/hello-grad-webapp/main/data/uk_postcodes.json"
cache = TTLCache(maxsize=1, ttl=3600)

@cached(cache)
def fetch_postcode_data():
    response = requests.get(GITHUB_RAW_URL)
    if response.status_code == 200:
        return json.loads(response.text)
    return []

@app.get("/api/postcodes")
async def get_postcodes():
    postcodes = fetch_postcode_data()
    return {"data": postcodes}

@app.get("/")
async def root():
    return {"message": "Welcome to the Hello Grad UK Postcode API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
