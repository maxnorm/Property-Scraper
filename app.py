import random
import pandas as pd

from src.bot import Bot
from src.utils.parse_xml import parse_xml
from src.utils.csv_utils import add_to_csv, create_property_csv, add_images_to_csv, create_images_csv


def start():
    create_property_csv()
    create_images_csv()

    error_df = pd.DataFrame(columns=["url", "error"])

    for i in range(5):
        current_url = random_test_url()
        try:
            bot = Bot()
            prop = bot.get_property(current_url)
            add_to_csv([prop.get_csv_data()], f"data/properties.csv")
            add_images_to_csv(prop.images, prop.id, f"data/images.csv")
        except Exception as e:
            print(f"An error occurred while processing the property: {current_url}")

            new_row = pd.DataFrame([{"url": current_url, "error": str(e)}])
            error_df = pd.concat([error_df, new_row], ignore_index=True)

    error_df.to_csv("data/errors.csv", index=False)

def random_test_url():
    urls = parse_xml("daily-file.xml")
    random_index = random.randint(0, len(urls) - 1)
    return urls[random_index]


if __name__ == '__main__':
    start()
