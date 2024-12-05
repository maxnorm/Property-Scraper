import os
import time
import random
import pandas as pd
from src.bot import Bot
from src.utils.download import download_daily_sitemap
import logging
from concurrent.futures import ThreadPoolExecutor

def load_sitemaps():
    """
    Load the sitemap from the provided URL.
    Only load the sitemap if it does not exist in the data/sitemaps folder.
    :return:
    """
    load_global_sitemap()
    time.sleep(5)
    if not os.path.exists(os.getenv("SITEMAP_FOLDER")):
        daily_urls = pd.read_csv(os.getenv("SITEMAP_FILE"))

        max_threads = int(os.getenv("MAX_THREADS", 5))
        with ThreadPoolExecutor(max_threads) as executor:
            for url in daily_urls["url"]:
                executor.submit(load_sitemap, url)

    else:
        print("Daily Sitemaps already exists.")


def load_sitemap(url):
    """
    Load the sitemap from the provided URL.
    :param url: The URL of the sitemap.
    """
    try:
        bot = Bot()
        sitemap = bot.get_daily_sitemap(url)
        download_daily_sitemap(url, sitemap)
        time.sleep(random.randint(1, 10))
        bot.close()
        time.sleep(random.randint(1, 10))
    except Exception as e:
        logging.error(f"An error occurred while loading the daily sitemap: {e}")


def load_global_sitemap():
    """
    Load the global sitemap from the provided URL.
    Only load the sitemap if it does not exist in the data/sitemaps folder.
    :return:
    """
    if not os.path.exists(os.getenv("SITEMAP_FILE")):
        try:
            bot = Bot()
            sitemap = bot.get_global_sitemap(os.getenv("C_SITEMAP_URL"))
            sitemap.to_csv(os.getenv("SITEMAP_FILE"), index=False)
            bot.close()
        except Exception as e:
            print(f"An error occurred while loading the global sitemap: {e}")
    else:
        print("Global sitemap already exists.")
