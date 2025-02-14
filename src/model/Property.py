import uuid
from src.enum.feature import Feature


def get_property_columns():
    """
    Get the columns for the property CSV file.
    :return: The columns for the property CSV file.
    """
    return [
        "id", "category", "price", "rooms", "beds", "baths",
        "description", "address", "lot_area", "liveable_area",
        "year_built", "building_style", "walkscore", "property_use",
        "total_parking", "fireplace", "nb_units", "residential_units",
        "main_unit", "gross_revenue", "additional_features", "pool",
        "zoning", "net_area", "type_coproperty"
    ]


class Property:
    """
    Property class to store information about a property
    """
    def __init__(self, listing_id, category, address, price=None,
                 rooms=None, beds=None, baths=None, description=None):
        print(hash(listing_id))
        self.id = hash(listing_id)
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
        self.property_use = None
        self.total_parking = None
        self.fireplace = None
        self.nb_units = None
        self.residential_units = None
        self.main_unit = None
        self.gross_revenue = None
        self.additional_features = None
        self.pool = None
        self.zoning = None
        self.net_area = None
        self.type_coproperty = None
        self.images = []

    def set_images(self, images):
        """
        Set the images for the property.
        :param images:
        """
        self.images = images

    def add_feature(self, key, value):
        """
        Add a feature to the property.
        :param key:
        :param value:
        """
        match key:
            case Feature.BUILDING_STYLE.value:
                self.building_style = value
            case Feature.YEAR_BUILT.value:
                self.year_built = value
            case Feature.LOT_AREA.value:
                self.lot_area = value
            case Feature.LIVEABLE_AREA.value:
                self.liveable_area = value
            case Feature.PROPERTY_USE.value:
                self.property_use = value
            case Feature.TOTAL_PARKING.value:
                self.total_parking = value
            case Feature.FIREPLACE.value:
                self.fireplace = value
            case Feature.NB_UNITS.value:
                self.nb_units = value
            case Feature.RESIDENTIAL_UNITS.value:
                self.residential_units = value
            case Feature.MAIN_UNIT.value:
                self.main_unit = value
            case Feature.GROSS_REVENUE.value:
                self.gross_revenue = value
            case Feature.ADDITIONAL_FEATURES.value:
                self.additional_features = value
            case Feature.POOL.value:
                self.pool = value
            case Feature.ZONING.value:
                self.zoning = value
            case Feature.NET_AREA.value:
                self.net_area = value
            case Feature.TYPE_COPROPERTY.value:
                self.type_coproperty = value
            case _:
                pass

    def get_csv_data(self):
        """
        Get the data for the property in CSV format.
        :return: The data for the property in CSV format.
        """
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
            "walkscore": self.walkscore,
            "property_use": self.property_use,
            "total_parking": self.total_parking,
            "fireplace": self.fireplace,
            "nb_units": self.nb_units,
            "residential_units": self.residential_units,
            "main_unit": self.main_unit,
            "gross_revenue": self.gross_revenue,
            "additional_features": self.additional_features,
            "pool": self.pool,
            "zoning": self.zoning,
            "net_area": self.net_area,
            "type_coproperty": self.type_coproperty
        }

    def __str__(self):
        return f"Property ID: {self.id}"
