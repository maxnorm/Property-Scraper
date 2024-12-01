from PIL import Image
from src.utils.download import download_image
import os
from src.utils.calculate_size import calculate_directory_size, format_size


def compress_image(image_path, folder, quality=85):
    output_path = os.path.join(os.path.splitext(os.path.basename(image_path))[0] + ".webp")
    output_path = f"{folder}/{output_path}"
    img = Image.open(image_path)
    img.save(output_path, "WEBP", optimize=True, quality=quality)
    os.remove(image_path)
    return output_path

def process_images(images, property_id):
    count = 1
    folder = f"data/images/{property_id}"
    for image in images:
        filename = f"{count}"
        path = download_image(filename, image.path, folder)
        path = compress_image(path, folder)
        image.path = path
        count += 1

    total_size = calculate_directory_size(folder)
    formatted_size = format_size(total_size)
    print(f"Total size of images: {formatted_size}")

    return images

def delete_image(image_path):
    os.remove(image_path)

