import os

import requests
from dotenv import load_dotenv


load_dotenv()


TMDB_API_KEY = os.getenv("API_KEY")

TMDB_BASE_URL = "https://api.themoviedb.org/3"

TMDB_IMAGE_BASE_URL = "https://image.tmdb.org/t/p"


if not TMDB_API_KEY:
    raise RuntimeError(
        "TMDB_API_KEY is not configured."
    )


def get_movie_details(movie_id):

    url = f"{TMDB_BASE_URL}/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return {
            "id": data.get("id"),
            "title": data.get("title"),
            "overview": data.get("overview"),
            "release_date": data.get("release_date"),
            "rating": data.get("vote_average"),
            "poster_path": data.get("poster_path")
        }

    except requests.RequestException as exc:

        print(
            f"TMDB request failed for "
            f"movie {movie_id}: {exc}"
        )

        return None


def get_poster_url(
    poster_path,
    size="w500"
):

    if not poster_path:
        return None

    return (
        f"{TMDB_IMAGE_BASE_URL}/"
        f"{size}{poster_path}"
    )