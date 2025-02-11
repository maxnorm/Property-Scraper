import os
import argparse

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
    logging.info(f"Processing URL: {url}")
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
                break

            executor.submit(process_url, current_url)
        logging.info("No more URLs to process.")


def pre_start():
    """Prepare the environment for the bot."""
    create_property_csv()
    create_images_csv()
    load_sitemaps()


def parse_arguments():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="WebScraper for real estate properties.",
        epilog="2025, alchemists",
        add_help=True
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode on the server")
    parser.add_argument("--headful", action="store_true", help="Disable headless mode")

    return parser.parse_args()


if __name__ == '__main__':
    load_dotenv()
    args = parse_arguments()

    if args.headful:
        Bot.active_headful()

    logging.basicConfig(
        filename='bot.log',
        encoding='utf-8',
        filemode='a',
        format='{asctime} | {levelname} - {message}',
        style='{',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )

    max_threads = int(os.getenv("MAX_THREADS", 5))
    print(f"MAX: {max_threads} threads.")

    start()
