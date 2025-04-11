import requests
from api_keys import TMDB_API_KEY

BASE_URL = "https://api.themoviedb.org/3"

def get_genres():
    url = f"{BASE_URL}/genre/tv/list"
    params = {"api_key": TMDB_API_KEY, "language": "en-US"}
    response = requests.get(url, params=params)
    return response.json()['genres']


def search_dramas_by_genre_keywords(keywords, region='US'):
    url = f"{BASE_URL}/search/tv"
    params = {
        "api_key": TMDB_API_KEY,
        "query": keywords,
        "language": "en-US",
        "region": region,
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])


def get_netflix_dramas_by_genre(genre_id, region='US'):
    url = f"{BASE_URL}/discover/tv"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre_id,
        "with_watch_providers": "8",  # Netflix
        "watch_region": region,
        "sort_by": "popularity.desc",
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    return response.json().get("results", [])
