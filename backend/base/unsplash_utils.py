import requests

UNSPLASH_ACCESS_KEY = 'bRSY6Ar9PUb1986rvzrDGYSX2ZUpbq7JF1x_mapdeTk'

def fetch_unsplash_image(query):
    url = "https://api.unsplash.com/search/photos"
    headers = {"Accept-Version": "v1"}
    params = {
        "query": query,
        "client_id": UNSPLASH_ACCESS_KEY,
        "per_page": 1,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data["results"]:
            return data["results"][0]["urls"]["small"]
    return None
