import requests


BASE_URL = "https://api.github.com"


def get_headers():

    return {
        "Accept": "application/vnd.github+json"
    }


def get_profile(username):

    url = f"{BASE_URL}/users/{username}"

    response = requests.get(
        url,
        headers=get_headers(),
        timeout=10
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()


def get_repositories(username):

    url = f"{BASE_URL}/users/{username}/repos"

    params = {
        "per_page": 100,
        "sort": "updated"
    }

    response = requests.get(
        url,
        headers=get_headers(),
        params=params,
        timeout=10
    )

    if response.status_code == 404:
        return None

    response.raise_for_status()

    return response.json()