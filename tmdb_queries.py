import json
import requests
from api_keys import TMDB_API_KEY

# setups
BASE_URL = "https://api.themoviedb.org/3"
HEADERS = {
    "accept": "application/json",
    "Authorization": f"Bearer {TMDB_API_KEY}"
}


""" 
@return list of dict (json format)
"""
def get_languages():
    url = f"{BASE_URL}/configuration/languages"
    response = requests.get(url, headers=HEADERS)
    return response.json()


""" 
@return list of dict (json format)
"""
def get_genres():
    url = f"{BASE_URL}/genre/tv/list?language=en"
    response = requests.get(url, headers=HEADERS)
    return response.json()["genres"]


""" 
@param original language(str), result page(str), region(str)
@return list of dict (json format)
"""
def get_netflix_kdramas_cdramas(lang="", page="1", region='US'):
    url = f"{BASE_URL}/discover/tv"
    params = {
        "with_watch_providers": "8",  # Netflix
        "watch_region": region,
        "sort_by": "popularity.desc",
        "with_original_language": lang,
        "page": page
    }
    response = requests.get(url, headers=HEADERS, params=params)
    return response.json().get("results", [])


""" 
@param int
@return list of strings
"""
def get_poster_image(id):
    url = f"{BASE_URL}/tv/{id}/images"

    response = requests.get(url, headers=HEADERS)
    paths = response.json()["backdrops"]

    image_paths = []
    image_path = "https://image.tmdb.org/t/p/w500"
    for i in range(0, len(paths)):
        image_url = image_path + paths[i]['file_path']
        image_paths.append(image_url)
        
    return image_paths


""" 
@param int
@return string
"""
def get_drama_title(id):
    url = f"{BASE_URL}/tv/{id}"
    response = requests.get(url, headers=HEADERS)

    return response.json()['name']


""" 
@param int
@return list of int
"""
def get_drama_genre_id(id):
    url = f"{BASE_URL}/tv/{id}"
    response = requests.get(url, headers=HEADERS)
    genres = response.json()['genres']
    result = []
    for i in range(0, len(genres)):
        result.append(genres[i]['id'])

    return result


""" 
@param int
@return list of dict (json format)
"""
def get_drama_keywords(id):
    url = f"{BASE_URL}/tv/{id}/keywords"
    response = requests.get(url, headers=HEADERS)

    return response.json()['results']


""" 
Generate a combined list of kdramas and cdramas, then
populate to json file.
"""
# generating full list of kdramas and cdramas
def generate_list():
    kdrama_list = []
    for i in range(0, 15):
        kdrama_list += get_netflix_kdramas_cdramas("ko", str(i+1))
    # print(len(kdrama_list))

    cdrama_list = []
    for i in range(0, 5):
        cdrama_list += get_netflix_kdramas_cdramas("zh", str(i+1))
    # print(len(cdrama_list))

    drama_list = kdrama_list + cdrama_list
    print(f'Drama list completed. Total: {len(drama_list)}')

    # populate to json file
    json.dump(drama_list, open('data/drama_list.json', 'w'))
