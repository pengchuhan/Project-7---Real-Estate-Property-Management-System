from enum import Enum
from typing import Optional


class PropertyType(Enum):
    APARTMENT = "Apartment"
    HOUSE = "House"
    COMMERCIAL = "Commercial"
    LAND = "Land"


class PropertyStatus(Enum):
    AVAILABLE = "Available"
    SOLD = "Sold"


class Property:
    def __init__(self, property_ID: int, address: str, price: float,
                 property_type: PropertyType, status: PropertyStatus,
                 owner: Optional[str] = None):
        self.property_ID = property_ID
        self.address = address
        self.price = price
        self.property_type = property_type
        self.status = status
        self.owner = owner

    def __repr__(self):
        owner_str = self.owner if self.owner else "None"
        return (f"<Property {self.property_ID} | {self.address} | ${self.price:.2f} | "
                f"{self.property_type.name} | {self.status.name} | Owner: {owner_str}>")

    def __eq__(self, other):
        if isinstance(other, Property):
            return self.property_ID == other.property_ID
        return False

    def __lt__(self, other):
        if not isinstance(other, Property):
            raise TypeError("Cannot compare Property with non-Property object")
        return self.property_ID < other.property_ID 