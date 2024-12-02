from enum import Enum


class Feature(Enum):
    """
    Enum for all the characteristics label of a property
    """
    BUILDING_STYLE = "Style de bâtiment"
    YEAR_BUILT = "Année de construction"
    LOT_AREA = "Superficie du terrain"
    LIVEABLE_AREA = "Superficie habitable"
    PROPERTY_USE = "Utilisation de la propriété"
    TOTAL_PARKING = "Stationnement total"
    FIREPLACE = "Foyer / Poêle"
    NB_UNITS = "Nombre d’unités"
    RESIDENTIAL_UNITS = "Unités résidentielles"
    MAIN_UNIT = "Unité principale"
    GROSS_REVENUE = "Revenus bruts potentiels"
    ADDITIONAL_FEATURES = "Caractéristiques additionnelles"
    POOL = "Piscine"
    ZONING = "Zonage"
    NET_AREA = "Superficie nette"
    TYPE_COPROPERTY = "Type de copropriété"
