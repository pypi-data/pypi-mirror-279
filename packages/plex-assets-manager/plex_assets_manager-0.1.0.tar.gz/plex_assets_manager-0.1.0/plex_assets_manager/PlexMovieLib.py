import sys
from plexapi.server import PlexServer 
from Movie import Movie
import os
from shutil import move, Error
from pathlib import Path
from utils import *
import random
import time
from datetime import datetime
from conf import *
import subprocess

class PlexMovieLib:
    def __init__(self, plex_token = PLEX_API_TOKEN, plex_url=PLEX_URL, movies_library=MOVIES_LIBRARY, log=LOG, quiet=QUIET):
        self.plex = PlexServer(plex_url, plex_token)
        self.movies = self.plex.library.section(movies_library)
        self.movies_path = self.movies.locations[0]
        self.quiet=quiet
        self.id = self.movies.key
        if log:
            self.log_file = open("log.txt",'w+',encoding="utf-8")
        else:
            self.log_file = sys.stdout
        self.subtitle_download_count, self.last_run_date = self.load_subtitle_download_count()

    def printText(self,text):
        if not self.quiet:
            print(text,file=self.log_file)

    #function to force a Plex Media Scan of the library
    def force_plex_scan(self):
        pms = PMS if PMS != '' else get_default_plex_media_scanner()
        force_scan_command=[pms, '--refresh', '--force', '--section', str(self.id)]
        try:
            result = subprocess.run(force_scan_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            print(f"Force scan output: {result.stdout}")
        except subprocess.CalledProcessError as e:
            print(f"Force Scan failed with error: {e.stderr}")


    def reorganize_folders(self):
        self.force_plex_scan()
        for movie in self.movies.all():
            m=Movie(movie)    

            title_validchars = m.getTitleValidChars()
            correct_folder_name = f"{title_validchars} ({m.year})"
            correct_folder_path = self.movies_path  + "/" + correct_folder_name
            self.printText(f"\n\n{correct_folder_name}\nOld location :\n{m.folder_path}\nNew location :\n{correct_folder_path}")
            
            if m.folder_path == correct_folder_path:
                self.printText("Already exists in correct folder. Exiting")
        
            elif m.folder_path == self.movies_path:
                self.printText("files are in base location. moving following files") 
                os.makedirs(correct_folder_path,exist_ok=True)
                for file in os.scandir(m.folder_path):
                    filePath = Path(file.path)
                    filename = (filePath).stem                  
                    if file.is_file():
                        if filename.find(m.filename) == 0:
                            self.printText(f"Object filename is: {file.path}")
                            try:
                                move(file.path,correct_folder_path)
                                self.printText("Folder moved")
                            except Error:
                                pass
            else:
                try:
                    move(m.folder_path,correct_folder_path)
                    self.printText("Folder moved")
                except FileNotFoundError:
                    pass


    def rename_movie_files(self):
        self.force_plex_scan()
        for movie in self.movies.all():
            m=Movie(movie)    
            correct_movie_filename = m.get_correct_filename()
            self.printText(f"\n\nMovie : {correct_movie_filename}\nCurrent Name : {m.filename}")
            
            for file in os.scandir(m.folder_path):
                filePath = Path(file.path)
                filename = filePath.stem  
                if file.is_file():
                    if filename.find(m.filename) == 0:
                        correct_filename = filename.replace(m.filename,correct_movie_filename)
                        correct_filepath = m.folder_path + "/" + correct_filename + filePath.suffix
                        self.printText(f"\nObject's filename is: {file.path}\nCorrected filepath is: {correct_filepath}")
                        try:
                            os.rename(file.path,correct_filepath)
                        except PermissionError:
                            self.printText('chflags nouchg "{}"'.format(file.path))
                            os.system('chflags nouchg "{}"'.format(file.path))
                            os.rename(file.path,correct_filepath)
                        self.printText("Rename completed")


    def download_all_trailers(self):
        self.force_plex_scan()
        for movie in self.movies.all():
            m=Movie(movie) 
            self.printText(f"Now processing {m.title}")
            stop_code = m.download_trailers()

            if stop_code == 0:
                self.printText(f"Trailer already exists")
            else:
                self.printText(f"\n\n{m.title} ({m.year}): ")
                if stop_code==1:
                    self.printText(f"Trailer found for {m.title}")
                else:
                    self.printText(f"Trailer not found for {m.title}")
                    if stop_code==2:
                        self.printText(f"Trailer found for {m.originalTitle}")
                    elif stop_code ==3:
                        self.printText(f"Trailer not found for {m.originalTitle}")               
            time.sleep(random.randint(1,MAX_SLEEP_DURATION))


    def load_subtitle_download_count(self):
        if os.path.exists(SUB_DOWNLOAD_TRACK_FILE):
            with open(SUB_DOWNLOAD_TRACK_FILE, "r") as file:
                data = file.read().strip().split(',')
                last_run_date = data[0]
                download_count = int(data[1])
                if last_run_date == datetime.now().strftime('%Y-%m-%d'):
                    return download_count, last_run_date
        return 0, datetime.now().strftime('%Y-%m-%d')

    def save_subtitle_download_count(self):
        with open(SUB_DOWNLOAD_TRACK_FILE, "w") as file:
            file.write(f"{self.last_run_date},{self.subtitle_download_count}")


    def download_all_subtitles(self):
        self.force_plex_scan()
        for movie in self.movies.all():
            if self.subtitle_download_count >= MAX_DAILY_SUB_DOWNLOADS:
                self.printText("Maximum daily subtitle downloads reached.")
                break
            try:
                m = Movie(movie)
                self.printText(f"Checking subtitles for {m.title}")
                if m.is_subtitle_present():
                    self.printText(f"Subtitles already present for {m.title}")
                else:
                    self.printText(f"Downloading subtitles for {m.title}")
                    if m.download_subtitles():
                        self.printText(f"Subtitles downloaded for {m.title}")
                        self.subtitle_download_count += 1
                    else:
                        self.printText(f"Subtitles not found for {m.title}")
            except Exception as e:
                self.printText(f"Error while downloading subtitles for {m.title}: {str(e)}")




