import os
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import src.c_utils.c_gallery as c_gallery
from src.model.Property import Property
from src.utils.images_processing import process_images
import re
import pandas as pd
from src.utils.parse_sitemaps import parse_global_sitemap, parse_daily_sitemap


class Bot:
    headless = False

    @staticmethod
    def active_headless():
        """
        Activate the headless mode for the bot.
        """
        Bot.headless = True

    def __init__(self):
        # Setting up the Chrome driver
        service = Service(driverpath=os.getenv('DRIVER_PATH'))
        options = webdriver.ChromeOptions()

        if self.headless:
            options.add_argument('--headless')

        options.add_argument('--log-level=2')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920x1080')

        self.driver = webdriver.Chrome(service=service, options=options)
        self.__stealth()

        self.driver.delete_all_cookies()

        self.driver.implicitly_wait(10)

    def __stealth(self):
        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    def __proxy(self):
        # TODO Implement proxy settings
        pass

    def accept_cookies(self):
        try:
            self.driver.find_element(By.ID, "didomi-notice-agree-button").click()
        except Exception as e:
            print(f"Cookie notice not found or already accepted: {e}")


    def get_property(self, url):
        """
        Get the property information from the given URL.
        :param url: The URL of the property.
        :return: The Property object.
        """
        self.driver.get(url)
        self.accept_cookies()

        head_info = self.driver.find_element(By.CLASS_NAME, "house-info")

        category = head_info.find_element(By.CSS_SELECTOR, '[data-id="PageTitle"]')
        category = category.text.replace(" à vendre", "")

        address = head_info.find_element(By.CSS_SELECTOR, "[itemprop='address']").text

        meta_price = head_info.find_element(By.CSS_SELECTOR, "[itemprop='price']")
        price = meta_price.get_attribute("content")

        description_section = self.driver.find_element(By.CLASS_NAME, "description")

        teaser = description_section.find_element(By.CLASS_NAME, "teaser")
        try:
            rooms = teaser.find_element(By.CLASS_NAME, "piece").text
            rooms = int(rooms.split(" ")[0])
        except NoSuchElementException:
            rooms = None

        try:
            beds = teaser.find_element(By.CLASS_NAME, "cac").text
            beds = int(beds.split(" ")[0])
        except NoSuchElementException:
            beds = None

        try:
            baths = teaser.find_element(By.CLASS_NAME, "sdb").text
            baths = int(baths.split(" ")[0])
        except NoSuchElementException:
            baths = None

        description_content = self.driver.find_element(By.CLASS_NAME, "property-description")
        description = description_content.find_element(By.CSS_SELECTOR, "[itemprop='description']").text

        prop = Property(category, address, price, rooms, beds, baths, description)

        characteristics = description_section.find_elements(By.CLASS_NAME, "carac-container")
        for characteristic in characteristics:
            try:
                walkscore = characteristic.find_element(By.CLASS_NAME, "walkscore")
                prop.walkscore = int(walkscore.text)
                continue
            except NoSuchElementException:
                pass

            key = characteristic.find_element(By.CLASS_NAME, "carac-title").text
            value = characteristic.find_element(By.CLASS_NAME, "carac-value").text
            prop.add_feature(key, value)

        c_gallery.open_gallery(self.driver)
        images = c_gallery.get_images_url(self.driver)
        images = process_images(images, prop.id)
        prop.set_images(images)

        return prop

    def __get_sitemap(self, url):
        """
        Get the sitemap from the given URL.
        :param url: The URL of the sitemap.
        :return: The sitemap content.
        """
        self.driver.get(url)
        sitemapindex = self.driver.find_elements(By.CLASS_NAME, "folder")

        urls = []
        for sitemap in sitemapindex:
            loc = sitemap.text.split("\n")[1]
            match = re.search(r"<loc>(.*?)</loc>", loc)

            # Check if a match is found and extract the URL
            if match:
                url = match.group(1)
                urls.append(url)

        df = pd.DataFrame(urls, columns=["url"])
        return df

    def get_global_sitemap(self, url):
        """
        Get the global sitemap from the given URL.
        :param url: The URL of the global sitemap.
        :return: The sitemap content.
        """
        results = self.__get_sitemap(url)
        return parse_global_sitemap(results)

    def get_daily_sitemap(self, url):
        """
        Get the daily sitemap from the given URL.
        :param url: The URL of the daily sitemap.
        :return: The sitemap content.
        """
        results = self.__get_sitemap(url)
        return parse_daily_sitemap(results)

    def close(self):
        """
        Close the Chrome driver.
        """
        self.driver.close()




