from .property import PropertyType

class Client:
    def __init__(self, client_ID: int, name: str, contact_info: str, budget: float, property_type: PropertyType = None):
        self.client_ID = client_ID
        self.name = name
        self.contact_info = contact_info
        self.budget = budget
        self.property_type = property_type 

    def __repr__(self):
        property_type_str = self.property_type.name if self.property_type else "None"
        return f"<Client {self.client_ID} | {self.name} | Contact: {self.contact_info} | Property Type: {property_type_str} | Budget: ${self.budget:.2f}>"