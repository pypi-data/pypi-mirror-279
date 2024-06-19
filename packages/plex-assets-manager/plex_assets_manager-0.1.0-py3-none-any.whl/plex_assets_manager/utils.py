import yt_dlp as youtube_dl
import requests
from conf import *
import os
import platform

#function to get OS name
def get_os():
    os_name = platform.system()
    if os_name == 'Darwin':
        return 'macOS'
    elif os_name == 'Windows':
        return 'Windows'
    else:
        return 'Other'

#function to get location of PLex Media Scanner based on OS
def get_default_plex_media_scanner():
    os_name = platform.system()
    if os_name == 'Darwin':
        return PMS_DEFAULT_OSX
    elif os_name == 'Windows':
        return PMS_DEFAULT_WIN
    else :
        return ''



#function to search a <search_title> on youtube and download it to <folder path> and name it <filename>.ext
def download_movie_trailers(search_title, filename, folder_path, min_views=MIN_VIEWS, max_filesize_MB=MAX_FILESIZE_MB, min_filesize_MB=MIN_FILESIZE_MB):
    try:
        # Generate YouTube search query
        query = f"ytsearch:{search_title} trailer"
        max_filesize = max_filesize_MB * 1024 * 1024
        min_filesize = min_filesize_MB * 1024 * 1024

        output_filename = f"{filename} -trailer.%(ext)s"
        output_filepath = os.path.join(folder_path, output_filename)

        # Prepare options for downloading
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'outtmpl': output_filepath,
            'min_views':min_views,
            'max_filesize': max_filesize,
            'min_filesize': min_filesize,
            'quiet':True
        }

        # Download the trailers
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([query])

    except youtube_dl.DownloadError as e:
        print("Download Error:", e)

def download_subtitle_from_opensubtitles(movie_title, year, folder_path):
    headers = {
        'Api-Key': OPENSUBTITLES_API_KEY,
    }
    params = {
        'query': movie_title,
        'year': year,
        'languages': 'en',
        'limit': 1,
    }
    response = requests.get('https://api.opensubtitles.com/api/v1/subtitles', headers=headers, params=params)
    response.raise_for_status()
    results = response.json()

    if results['total_count'] > 0:
        file_id = results['data'][0]['attributes']['files'][0]['file_id']
        download_link_response = requests.get(f'https://api.opensubtitles.com/api/v1/download', headers=headers, params={'file_id': file_id})
        download_link_response.raise_for_status()
        download_link = download_link_response.json()['link']

        subtitle_response = requests.get(download_link)
        subtitle_response.raise_for_status()
        subtitle_path = os.path.join(folder_path, f"{movie_title} ({year}).srt")
        
        with open(subtitle_path, 'wb') as subtitle_file:
            subtitle_file.write(subtitle_response.content)
        return True
    return False