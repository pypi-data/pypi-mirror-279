from ytageneralutils.tmp_processor import create_tmp_filename
from ytageneralutils.file_downloader import download_video
from random import choice

import os
import requests

HEADERS = {
    'content-type': 'application/json',
    'Accept-Charset': 'UTF-8',
    'Authorization': os.getenv('PEXELS_API_KEY')
}

def download_first(query, ignore_ids = [], output_filename = None):
    """
    Searches for the provided 'query', gets the valid results and selects
    the first video that is not included in 'ignore_ids'. If available, it
    downloads that video with the provided 'output_filename' or a temporary
    generated file.

    This method returns an object containing 'id' and 'output_filename' if  
    downloaded, or None if not.
    """
    video = __get_first(query, ignore_ids)

    if not video:
        return None
    
    return __download(video, output_filename)

def download_random(query, ignore_ids = [], output_filename = None):
    """
    Searches for the provided 'query', gets the valid results and selects a
    random video that is not included in 'ignore_ids'. If available, it
    downloads that video with the provided 'output_filename' or a temporary
    generated file.

    This method returns an object containing 'id' and 'output_filename' if  
    downloaded, or None if not.
    """
    video = __get_random(query, ignore_ids)

    if not video:
        return None
    
    return __download(video, output_filename)

def __download(video, output_filename = None):
    """
    Downloads the provided video and returns an object containing 'id'
    and 'output_filename' if downloaded, or None if not.
    """
    if not output_filename:
        output_filename = create_tmp_filename('pexels_video.mp4')
    
    output_filename = download_video(video['url'], output_filename)

    return {
        'id': video['id'],
        'output_filename': output_filename
    }

def __get_first(query, ignore_ids = []):
    """
    Searchss for the provided 'query', gets the valid results and selects 
    the first video that is not included in 'ignore_ids'.

    This method returns a video (containing 'id', 'url', 'width', 'height'
    and 'fps') if found, or None if not.
    """
    videos = __get_videos(query, ignore_ids)

    if len(videos) == 0:
        return None
    
    return videos[0]

def __get_random(query, ignore_ids = []):
    """
    Searchss for the provided 'query', gets the valid results and selects a
    random video that is not included in 'ignore_ids'.

    This method returns a video (containing 'id', 'url', 'width', 'height'
    and 'fps') if found, or None if not.
    """
    videos = __get_videos(query, ignore_ids)

    if len(videos) == 0:
        return None
    
    return choice(videos)

def __get_videos(query, ignore_ids = []):
    """
    This method returns only valid videos found for the provided 'query'. We consider
    valid videos those ones that have a FullHD quality and a aspect ratio close to
    16 / 9, so we can apply some resizing without too much lose. This search will skip
    the videos with any of the 'ignore_ids'.

    This method returns an array of videos (if found) that contains, for each video,
    the main video 'id', 'url', 'width', 'height' and 'fps'. The main video 'id' is
    obtained for avoiding repetitions.
    """
    videos = search_videos(query)

    best_video_files = []
    if len(videos) > 0:
        for video in videos:
            if video['id'] in ignore_ids:
                continue

            best_video_file = __get_best_video_file(video['video_files'])
            if best_video_file:
                best_video_files.append({
                    'id': video['id'],
                    'url': best_video_file['link'],
                    'width': best_video_file['width'],
                    'height': best_video_file['height'],
                    'fps': best_video_file['fps']
                })

    return best_video_files

def __get_best_video_file(video_files):
    """
    Makes some iterations over received video_files to check the best
    quality video that is hd with the higher 'width' and 'height' values,
    but only accepting (by now) 16/9 format.
    It returns the video if found, or None if there is no valid video available.
    """
    # TODO: This need work
    best_video_file = None
    for video_file in video_files:
        aspect_ratio = video_file['width'] / video_file['height']
        if aspect_ratio < 1.6 or aspect_ratio > 1.95:
            # TODO: We avoid, by now, not valid for resizing
            continue

        # Landscape valid aspect_ratio is 1.7777777777777777 which is 16/9 format
        # Vertical valid aspect ratio is 0.5626 which is 9/16 format
        # TODO: Implement an option to receive vertical format instead of landscape
        if video_file['quality'] != 'sd' and (video_file['width'] > 1920 or video_file['height'] > 1080):
            # This video is valid, lets check if it is the best one
            if best_video_file == None:
                # No previous best_video_file, so this one is the new one
                best_video_file = video_file
            else:
                if best_video_file['width'] < video_file['width']:
                    # More quality, so preserve the new one as best_video
                    best_video_file = video_file

    return best_video_file
    
def search_videos(query, locale = 'es-ES', per_page = 25):
    """
    Makes a search of Pexels videos and returns the results
    """
    pexels_search_videos_url = 'https://api.pexels.com/videos/search'

    params = {
        'query': query,
        'locale': locale, # 'es-ES' | 'en-EN' ...
        'per_page': per_page
    }

    r = requests.get(pexels_search_videos_url, params = params, headers = HEADERS)

    return r.json()['videos']