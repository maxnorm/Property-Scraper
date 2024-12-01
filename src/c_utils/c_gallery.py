import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.model.Image import Image
from src.utils.download import download_image


def open_gallery(driver):
    """Open the gallery of images on the current property page."""
    try:
        photo_container_xpath = "//div[contains(@class, 'primary-photo-container')]"
        photo_container = driver.find_element(By.XPATH, photo_container_xpath)
        gallery_anchor = photo_container.find_element(By.TAG_NAME, "a")
        gallery_anchor.click()
        time.sleep(2)  # Wait for the gallery to open
    except Exception as e:
        print(f"Failed to open the gallery: {e}")


def get_images_url(driver):
    """Browse through the gallery and  get the images url."""
    count = 1
    count_to = get_total_images(driver)
    images = set()

    while True:
        try:
            if count > count_to:
                break

            # Find the current image element and download it
            image = driver.find_element(By.ID, "fullImg")
            image_url = image.get_attribute("src")
            label = get_image_label(driver)

            if image_url and image_url not in images:
                images.add(Image(image_url, label))
                count += 1

            # Click the arrow to navigate to the next image
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)
            time.sleep(1)  # Wait for the next image to load

        except Exception as e:
            print(f"No more images or encountered an error: {e}")
            break

    return images


def get_total_images(driver):
    """Get the total number of images in the gallery.
    HTML structure:
    <div class="description">
        <strong>1/20</strong>
        " [Image Label]"
    </div>
    :param driver: The Selenium WebDriver instance.
    :return: The total number of images in the gallery.
    """
    description = get_image_description(driver)
    strong_text = description.find_element(By.TAG_NAME, "strong").text
    count_to = strong_text.split("/")[1]
    return int(count_to)


def get_image_label(driver):
    """Get the label of the current image."""
    description = get_image_description(driver)
    strong_text = description.find_element(By.TAG_NAME, "strong").text
    full_text = description.text

    # Remove the "1/20" part from the full text to get the label
    label = full_text.replace(strong_text, "").strip()
    return label


def get_image_description(driver):
    """Get the description of the current image."""
    gallery = driver.find_element(By.ID, "gallery")
    img_wrapper = gallery.find_element(By.CLASS_NAME, "image-wrapper")
    description = img_wrapper.find_element(By.CLASS_NAME, "description")
    return description
