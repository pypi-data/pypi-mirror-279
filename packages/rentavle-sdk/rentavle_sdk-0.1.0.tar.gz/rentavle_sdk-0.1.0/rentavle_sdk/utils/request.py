import requests

def get(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print("HTTP GET request failed:", error)
        raise error
