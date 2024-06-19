from pathlib import Path
import re
import os
from utils import download_movie_trailers, download_subtitle_from_opensubtitles

class Movie:
    def __init__(self,movie):
        self.title = movie.title
        self.year = movie.year
        self.originalTitle = movie.originalTitle
        path = Path(movie.locations[0])
        self.folder_path = str(path.parent)
        self.filename=str(path.stem)
    
    def getTitleValidChars(self):
        return re.sub('[/?%*|"<>:]+', "-", self.title)

    def getOriginalTitleValidChars(self):
        if self.originalTitle == None or self.originalTitle.strip() == '':
            return ''
        else:
            return " (" + re.sub('[/?%*|"<>:]+', "-", self.originalTitle) + ")"

    def get_correct_filename(self):
        title_validchars=self.getTitleValidChars()
        year=self.year
        originalTitle_validchars=self.getOriginalTitleValidChars()
        return f"{title_validchars} ({year}){originalTitle_validchars}"
    
    def is_trailer_present(self):
        for file in os.listdir(self.folder_path):
            file_name, file_ext = os.path.splitext(file)
            if file_name.endswith("-trailer"):
                return True
        return False
    
    def download_trailers(self):
        if self.is_trailer_present():
            return 0
        else:
            filename = self.get_correct_filename()
            # try searching <title> on youtube for trailers, and download
            search_title = f"{self.title} ({self.year})"
            download_movie_trailers(search_title, filename, self.folder_path)
            if self.is_trailer_present():
                return 1
            else:
                # if <title> doesnt work, try <original title>
                if self.originalTitle != None and self.originalTitle.strip() != '':
                    search_title = f"{self.originalTitle} ({self.year})"
                    download_movie_trailers(search_title, filename, self.folder_path) 
                    if self.is_trailer_present():
                        return 2
                    else:
                        return 3
                else:
                    return 4
                
    def is_subtitle_present(self):
        for file in os.listdir(self.folder_path):
            file_ext = os.path.splitext(file)[1]
            if file_ext.lower() in ['.srt', '.sub']:
                return True
        return False

    def download_subtitles(self):
        if self.is_subtitle_present():
            return True
        else:
            if download_subtitle_from_opensubtitles(self.title, self.year, self.folder_path):
                return True
            elif self.originalTitle and self.originalTitle.strip():
                if download_subtitle_from_opensubtitles(self.originalTitle, self.year, self.folder_path):
                    return True
            return False
                
