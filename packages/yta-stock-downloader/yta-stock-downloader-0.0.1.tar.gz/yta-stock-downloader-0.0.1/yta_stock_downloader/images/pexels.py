from ytageneralutils.file_downloader import download_image

import requests
import os

HEADERS = {
    'content-type': 'application/json',
    'Accept-Charset': 'UTF-8',
    'Authorization': os.getenv('PEXELS_API_KEY')
}

def search_images(query, locale = 'es-ES', per_page = 25):
    """
    Makes a search of Pexels images and returns the results
    """
    pexels_search_videos_url = 'https://api.pexels.com/v1/search'

    params = {
        'query': query,
        'orientation': 'landscape',   # landscape | portrait | square
        'size': 'large',   # large | medium | small
        'locale': locale, # 'es-ES' | 'en-EN' ...
        'per_page': per_page
    }

    r = requests.get(pexels_search_videos_url, params = params, headers = HEADERS)

    return r.json()['photos']

def download_first(query, output_filename):
    photos = search_images(query)

    if len(photos) == 0:
        return None

    url = photos[0]['src']['landscape']

    download_image(url, output_filename)