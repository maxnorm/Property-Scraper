import uuid


def get_property_columns():
    """
    Get the columns for the property CSV file.
    :return: The columns for the property CSV file.
    """
    return [
        "id", "category", "price", "rooms", "beds", "baths",
        "description", "address", "lot_area", "liveable_area",
        "year_built", "building_style", "walkscore"
    ]


class Property:
    """
    Property class to store information about a property
    """
    def __init__(self, category, address, price=None,
                 rooms=None, beds=None, baths=None, description=None):
        self.id = str(uuid.uuid4())
        self.category = category
        self.address = address
        self.price = price
        self.rooms = rooms
        self.beds = beds
        self.baths = baths
        self.description = description
        self.lot_area = None
        self.year_built = None
        self.building_style = None
        self.liveable_area = None
        self.walkscore = None
        self.images = []

    def set_images(self, images):
        self.images = images

    def add_characteristic(self, key, value):
        match key:
            case "Style de bâtiment":
                self.building_style = value
            case "Année de construction":
                self.year_built = value
            case "Superficie du terrain":
                self.lot_area = value
            case "Superficie habitable":
                self.liveable_area = value
            case _:
                pass

    def get_csv_data(self):
        return {
            "id": self.id,
            "category": self.category,
            "price": self.price,
            "rooms": self.rooms,
            "beds": self.beds,
            "baths": self.baths,
            "description": self.description,
            "address": self.address,
            "lot_area": self.lot_area,
            "liveable_area": self.liveable_area,
            "year_built": self.year_built,
            "building_style": self.building_style,
            "walkscore": self.walkscore
        }

    def __str__(self):
        return (f"Property ID: {self.id}\n"
                f"Category: {self.category}\n"
                f"Address: {self.address}\n"
                f"Price: {self.price}\n"
                f"Rooms: {self.rooms}\n"
                f"Beds: {self.beds}\n"
                f"Baths: {self.baths}\n"
                f"Lot Area: {self.lot_area}\n"
                f"Liveable Area: {self.liveable_area}\n"
                f"Year Built: {self.year_built}\n"
                f"Building Style: {self.building_style}\n"
                f"Walkscore: {self.walkscore}\n"
                f"Description: {self.description}")
