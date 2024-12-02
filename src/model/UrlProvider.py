import pandas as pd
import os
from pathlib import Path


class UrlProvider:
    def __init__(self):
        self.files = self.__load_filenames()
        self.urls = None
        self.file_index = 0
        self.index = 0
        self.__load_current_file()

    def __load_filenames(self):
        folder_path = Path(os.getenv("SITEMAP_FOLDER"))
        file_names = [file.name for file in folder_path.iterdir() if file.is_file()]
        return file_names

    def __load_current_file(self):
        file_path = os.path.join(os.getenv("SITEMAP_FOLDER"), self.files[self.index])
        urls = pd.read_csv(file_path)
        self.file_index += 1
        self.urls = urls["url"]

    def next(self):
        """
        Get the next URL from the dispenser.
        :return: The next URL.
        """
        if self.file_index >= len(self.files):
            return None
        if self.index >= len(self.urls):
            self.index = 0
            self.__load_current_file()
        url = self.urls[self.index]
        self.index += 1
        return url
