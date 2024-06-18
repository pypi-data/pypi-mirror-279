from ytageneralutils.file_downloader import download_image

import urllib.parse
import requests
import os

PIXABAY_API_KEY = os.getenv('PIXABAY_API_KEY')

def __get_url(query):
    params = {
        'key': PIXABAY_API_KEY,
        'q': query,
        'image_type': 'photo'
    }

    return 'https://pixabay.com/api/?' + urllib.parse.urlencode(params)

def download_first(query, output_filename):
    """
    Downloads the first available image found with the provided seach 'query'.
    It is downloaded in the maxium quality available and stored with the 
    'output_filename' provided.
    """
    response = requests.get(__get_url(query), timeout = 10)
    response = response.json()

    # TODO: Check 'output_filename' is valid

    if response['total'] == 0:
        return None
    
    image = response['hits'][0]
    url = image['largeImageURL']

    return download_image(url, output_filename)