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
        file_names.reverse()
        return file_names

    def __load_current_file(self):
        if self.file_index >= len(self.files):
            self.urls = []
            return

        file_name = self.files[self.file_index]
        file_path = os.path.join(os.getenv("SITEMAP_FOLDER"), file_name)

        try:
            df = pd.read_csv(file_path)
            if "url" in df.columns and not df["url"].empty:
                self.urls = df["url"].tolist()
                self.index = 0  # Reset URL index
                return
        except Exception as e:
            print(f"Error loading {file_name}: {e}")

        self.file_index += 1
        self.__load_current_file()

    def next(self):
        """
        Get the next URL from the dispenser.
        :return: The next URL.
        """
        while self.file_index < len(self.files):
            if self.index < len(self.urls):
                url = self.urls[self.index]
                self.index += 1
                return url

            self.file_index += 1
            self.index = 0
            self.__load_current_file()

        return None
