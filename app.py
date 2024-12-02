import os

import pandas as pd

from src.bot import Bot
from src.model.UrlDispenser import UrlDispenser
from src.utils.csv_utils import add_to_csv, create_property_csv, add_images_to_csv, create_images_csv
from dotenv import load_dotenv
from src.utils.load_sitemap import load_sitemap


def process_url(url, error_df):
    """
    Process a URL and add the property to the CSV file.
    :param url:
    :param error_df:
    :return:
    """
    try:
        bot = Bot()
        prop = bot.get_property(url)
        add_to_csv([prop.get_csv_data()], os.getenv("PROPERTY_FILE"))
        add_images_to_csv(prop.images, prop.id, os.getenv("IMAGES_FILE"))
        bot.close()
    except Exception as e:
        print(f"An error occurred while processing the property: {url}")

        new_row = pd.DataFrame([{"url": url, "error": str(e)}])
        error_df = pd.concat([error_df, new_row], ignore_index=True)

    return error_df


def start():
    """
    Start the bot.
    """
    pre_start()
    url_dispenser = UrlDispenser()

    error_df = pd.DataFrame(columns=["url", "error"])

    while True:
        current_url = url_dispenser.next()

        if current_url is None:
            print("All URLs have been processed.")
            break

        error_df = process_url(current_url, error_df)

    error_df.to_csv("data/errors.csv", index=False)


def pre_start():
    """Prepare the environment for the bot."""
    create_property_csv()
    create_images_csv()
    load_sitemap()


if __name__ == '__main__':
    load_dotenv()
    start()
