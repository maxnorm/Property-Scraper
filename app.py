import os

from src.bot import Bot
from src.model.UrlProvider import UrlProvider
from src.utils.csv_utils import add_to_csv, create_property_csv, add_images_to_csv, create_images_csv
from dotenv import load_dotenv
from src.utils.load_sitemap import load_sitemaps
import logging
from concurrent.futures import ThreadPoolExecutor


def process_url(url):
    """
    Process a URL and add the property to the CSV file.
    :param url:
    :return:
    """
    bot = Bot(proxied=True)
    try:
        prop = bot.get_property(url)
        bot.close()

        add_to_csv([prop.get_csv_data()], os.getenv("PROPERTY_FILE"))
        add_images_to_csv(prop.images, prop.id, os.getenv("IMAGES_FILE"))
    except Exception as e:
        bot.close()
        logging.error(f"An error occurred while processing the property:\n"
                      f"URL: {url}\n"
                      f"Error: {e}")


def start():
    """
    Start the bot.
    """
    pre_start()
    url_dispenser = UrlProvider()

    max_threads = int(os.getenv("MAX_THREADS", 5))

    with ThreadPoolExecutor(max_threads) as executor:
        while True:
            current_url = url_dispenser.next()
            if current_url is None:
                logging.info("No more URLs to process.")
                break

            logging.info(f"Processing URL: {current_url}")
            executor.submit(process_url, current_url)


def pre_start():
    """Prepare the environment for the bot."""
    create_property_csv()
    create_images_csv()
    load_sitemaps()


if __name__ == '__main__':
    load_dotenv()

    logging.basicConfig(
        filename='bot.log',
        encoding='utf-8',
        filemode='a',
        format='{asctime} | {levelname} - {message}',
        style='{',
        datefmt='%Y-%m-%d %H:%M:%S',
        level = logging.INFO
    )

    Bot.active_headless()

    max_threads = int(os.getenv("MAX_THREADS", 5))
    print(f"MAX: {max_threads} threads.")

    start()

