#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file
"""

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

PLEX_API_TOKEN  = os.getenv('PLEX_API_TOKEN')
OPENSUBTITLES_API_KEY  = os.getenv('OPENSUBTITLES_API_KEY')

LOG = True
QUIET = False


PLEX_URL = "http://127.0.0.1:32400"

# actual path to Plex Media Scanner if known
PMS = ''

MOVIES_LIBRARY = 'Movies'

#youtube trailer download conf
MIN_VIEWS=10000
MAX_FILESIZE_MB=100
MIN_FILESIZE_MB=1
MAX_SLEEP_DURATION=15

# max daily subtitle downloads
MAX_DAILY_SUB_DOWNLOADS = 20
SUB_DOWNLOAD_TRACK_FILE = "sub_download_tracker.txt"

# default path to Plex Media Scanner for diffrent OS
PMS_DEFAULT_OSX = "/Applications/Plex Media Server.app/Contents/MacOS/Plex Media Scanner"
PMS_DEFAULT_WIN = "C:\Program Files (x86)\Plex\Plex Media Server\Plex Media Scanner.exe"


