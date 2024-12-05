import os
import requests
from datetime import datetime


def download_image(filename, image_url, folder):
    """Download the image from the provided URL."""
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        proxies = {
            "http": os.getenv("PROXY_HTTP"),
            "https": os.getenv("PROXY_HTTPS")
        }
        response = requests.get(image_url, stream=True, proxies=proxies)
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

def download_daily_sitemap(url, df):
    """Download the daily sitemap from the provided URL."""
    if not os.path.exists("data/sitemaps"):
        os.makedirs("data/sitemaps")

    path = url.split("/")[-1]
    path = path.replace(".xml", "")

    if "daily" in path:
        path = path.replace("daily", f"{datetime.now().strftime('%Y-%m-%d')}")

    file_path = f"data/sitemaps/{path}.csv"

    df.to_csv(file_path, index=False)
    print(f"Downloaded sitemap: {file_path}")

