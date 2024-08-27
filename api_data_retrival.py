from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = result.json()  
    token = json_result['access_token']
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search" 
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = result.json()  

    if "artists" in json_result and "items" in json_result["artists"]:
        items = json_result["artists"]["items"]
        if len(items) == 0:
            print("No artist with this name exists...")
            return None
        return items[0]
    else:
        print("No artist data found in response...")
        return None

token = get_token()

# Example search
artist_name = "Kendrick Lamar" 
artist_info = search_for_artist(token, artist_name)
print(artist_info)
