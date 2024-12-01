import pandas as pd
from src.model.Property import get_property_columns
from src.model.Image import get_images_columns
import os


def add_to_csv(data, path):
    """Add data to a CSV file."""
    df = pd.DataFrame(data)
    df.to_csv(path, mode='a', header=False, index=False)


def add_images_to_csv(images, property_id, path):
    """Add images to the images CSV file."""
    data = [image.get_csv_data() for image in images]
    df = pd.DataFrame(data)
    df["property_id"] = property_id
    df.to_csv(path, mode='a', header=False, index=False)


def create_images_csv():
    """Create the images CSV file."""
    if not os.path.exists("data/images.csv"):
        os.makedirs("data/images.csv")
    df = pd.DataFrame(columns=get_images_columns())
    df.to_csv("data/images.csv", index=False)


def create_property_csv():
    """Create the properties CSV file."""
    # Ensure the "data" directory exists
    os.makedirs("data", exist_ok=True)

    # Create the properties CSV file
    file_path = "data/properties.csv"
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=get_property_columns())
        df.to_csv(file_path, index=False)
        print(f"Created file: {file_path}")
    else:
        print(f"File already exists: {file_path}")


def create_images_csv():
    """Create the images CSV file."""
    # Ensure the "data" directory exists
    os.makedirs("data", exist_ok=True)

    # Create the images CSV file
    file_path = "data/images.csv"
    if not os.path.exists(file_path):
        df = pd.DataFrame(columns=get_images_columns())
        df.to_csv(file_path, index=False)
        print(f"Created file: {file_path}")
    else:
        print(f"File already exists: {file_path}")
