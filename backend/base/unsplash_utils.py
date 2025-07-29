# In base/unsplash_utils.py

import requests
from django.core.cache import cache # <-- 1. Import Django's cache framework

# --- THE API KEY IS DIRECTLY IN THE CODE AS YOU REQUESTED ---
UNSPLASH_ACCESS_KEY = 'bRSY6Ar9PUb1986rvzrDGYSX2ZUpbq7JF1x_mapdeTk'

def fetch_unsplash_image(query):
    """
    Fetches an image URL from the Unsplash API for a given query.
    Includes caching to reduce API calls and error handling to prevent crashes.
    """
    # Create a unique, safe key for the cache based on the query
    cache_key = f"unsplash_image_{query.lower().replace(' ', '_')}"
    
    # First, try to get the result from the cache
    cached_url = cache.get(cache_key)
    if cached_url:
        print(f"CACHE HIT: Found image for '{query}' in cache.")
        return cached_url

    # If not in cache, proceed to call the API
    print(f"CACHE MISS: Calling Unsplash API for '{query}'.")
    
    url = "https://api.unsplash.com/search/photos"
    headers = {"Accept-Version": "v1"}
    params = {
        "query": query,
        "client_id": UNSPLASH_ACCESS_KEY, # Use the key defined above
        "per_page": 1,
        "orientation": "squarish"
    }

    # --- THIS IS THE CRITICAL FIX ---
    # Wrap the entire network request in a try...except block.
    try:
        # Set a timeout to prevent requests from hanging
        response = requests.get(url, headers=headers, params=params, timeout=5)
        
        # Raise an exception for bad responses (like 403 for rate limits)
        response.raise_for_status() 

        data = response.json()
        
        # Safely check if the 'results' list is not empty
        if data.get("results"):
            image_url = data["results"][0]["urls"]["small"]
            
            # On a successful API call, store the result in the cache for 1 hour.
            cache.set(cache_key, image_url, timeout=3600)
            
            return image_url

    except requests.exceptions.RequestException as e:
        # This block will catch any network-related error and prevent the server from crashing.
        print(f"!!! UNSPLASH API ERROR for query '{query}': {e}")
        # Return None on failure.
        return None 

    # If the API call was successful but there were no image results, return None.
    return None