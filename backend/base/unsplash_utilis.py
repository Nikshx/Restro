import requests
from django.conf import settings

UNSPLASH_ACCESS_KEY = settings.UNSPLASH_ACCESS_KEY

def fetch_unsplash_image(query):
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Accept-Version": "v1",
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }
    params = {
        "query": query,
        "per_page": 1,
        "orientation": "landscape"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data["results"]:
        return data["results"][0]["urls"]["regular"]
    return None
