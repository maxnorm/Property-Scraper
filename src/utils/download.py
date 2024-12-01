import os
import requests


def download_image(filename, image_url, folder):
    """Download the image from the provided URL."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            file_path = os.path.join(folder, f"{filename}.jpg")
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path
        else:
            print(f"Failed to download image: {image_url}")
            return None
    except Exception as e:
        print(f"Error downloading image: {e}")
        return None
