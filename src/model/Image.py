import uuid


def get_images_columns():
    """
    Get the columns for the property CSV file.
    :return: The columns for the property CSV file.
    """
    return [
        "id", "path", "label", "property_id"
    ]


class Image:
    """
    A class to represent an image.
    """
    def __init__(self, path, label):
        self.id = str(uuid.uuid4())
        self.path = path
        self.label = label

    def get_csv_data(self):
        return {
            "id": self.id,
            "path": self.path,
            "label": self.label
        }

    def __str__(self):
        return f"Image: {self.label} - {self.path}"
