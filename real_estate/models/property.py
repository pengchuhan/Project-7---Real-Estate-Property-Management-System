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
        self.views = 0
        self.inquiries = 0

    def add_view(self):
        self.views += 1

    def add_inquiry(self):
        self.inquiries += 1

    def reset_interest(self):
        self.views = 0
        self.inquiries = 0

    def __repr__(self):
        owner_str = self.owner if self.owner else "None"
        features_str = '无'
        if hasattr(self, 'features') and self.features:
            features_str = ','.join(self.features)
        return (f"<Property {self.property_ID} | {self.address} | ${self.price:.2f} | "
                f"{self.property_type.name} | {self.status.name} | Owner: {owner_str} | Features: {features_str}>")

    def __eq__(self, other):
        if isinstance(other, Property):
            return self.property_ID == other.property_ID
        return False

    def __lt__(self, other):
        if not isinstance(other, Property):
            raise TypeError("Cannot compare Property with non-Property object")
        return self.property_ID < other.property_ID
