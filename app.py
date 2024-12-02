import datetime
import random
import time

import pandas as pd

from src.bot import Bot
from src.utils.csv_utils import add_to_csv, create_property_csv, add_images_to_csv, create_images_csv
from dotenv import load_dotenv
from src.utils.download import download_daily_sitemap

def pre_start():
    create_property_csv()
    create_images_csv()

    load_sitemap()

def load_sitemap():
    daily_urls = pd.read_csv("data/sitemap.csv")

    for url in daily_urls["url"]:
        try:
            bot = Bot()
            sitemap = bot.get_daily_sitemap(url)
            download_daily_sitemap(url, sitemap)
            time.sleep(random.randint(1, 10))
            time.sleep(random.randint(1, 10))
        except Exception as e:
            print(f"An error occurred while loading the sitemap {url}")
            print(e)



def start():
    pre_start()

    error_df = pd.DataFrame(columns=["url", "error"])

    for i in range(5):
        current_url = "" #TODO: Get the current URL from the sitemap
        try:
            bot = Bot()
            prop = bot.get_property(current_url)
            add_to_csv([prop.get_csv_data()], f"data/properties.csv")
            add_images_to_csv(prop.images, prop.id, f"data/images.csv")
            bot.close()
        except Exception as e:
            print(f"An error occurred while processing the property: {current_url}")

            new_row = pd.DataFrame([{"url": current_url, "error": str(e)}])
            error_df = pd.concat([error_df, new_row], ignore_index=True)

    error_df.to_csv("data/errors.csv", index=False)


if __name__ == '__main__':
    load_dotenv()
    start()
