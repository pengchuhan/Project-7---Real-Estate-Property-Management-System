from ..models import Client, Property, PropertyStatus
from ..structures.client_queue import ClientQueue

class ClientManager:
    def __init__(self):
        self.clients = ClientQueue()

    def add_client(self, client):
        if isinstance(client, Client):
            self.clients.enqueue(client)

    def find_client_by_id(self, client_id):
        temp_queue = ClientQueue()
        found = None
        while not self.clients.is_empty():
            current = self.clients.dequeue()
            temp_queue.enqueue(current)
            if current.client_ID == client_id:
                found = current
        while not temp_queue.is_empty():
            self.clients.enqueue(temp_queue.dequeue())
        return found

    def remove_client(self, client_id):
        temp_queue = ClientQueue()
        found = False
        while not self.clients.is_empty():
            client = self.clients.dequeue()
            if client.client_ID == client_id:
                found = True
            else:
                temp_queue.enqueue(client)
        while not temp_queue.is_empty():
            self.clients.enqueue(temp_queue.dequeue())
        return found

    def match_properties(self, properties, min_budget, max_budget, current=None):
        matched = []
        if current is None:
            current = self.peek()
        if current:
            # 匹配所有价格 ≤ 预算的房产，并确保类型和状态匹配
            matched_properties = [p for p in properties 
                                 if p.price <= current.budget 
                                 and p.status == PropertyStatus.AVAILABLE 
                                 and p.property_type == current.property_type]
            if matched_properties:
                matched.append((current, matched_properties))
        return matched

    def buy_property(self, client, property_id, property_manager):
        if not client:
            raise ValueError("Client not found.")
        if property_id not in property_manager.properties:
            raise ValueError("Property not found.")
        property_obj = property_manager.properties[property_id]
        if property_obj.status == PropertyStatus.SOLD:
            raise ValueError("Property is already sold.")
        if client.budget < property_obj.price:
            raise ValueError("Insufficient budget.")
        property_obj.status = PropertyStatus.SOLD
        property_obj.owner = client.name
        self.remove_client(client.client_ID)

    def peek(self):
        if not self.clients.is_empty():
            return self.clients.front.data
        return None