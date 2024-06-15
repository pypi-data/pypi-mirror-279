import requests

def get(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print("HTTP GET request failed:", error)
        raise error
