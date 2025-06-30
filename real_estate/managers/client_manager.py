from ..models import Client, Property, PropertyStatus
from ..structures.client_queue import ClientQueue

class ClientManager:
    def __init__(self):
        self.clients = ClientQueue()

    def add_client(self, client):
        if isinstance(client, Client):
            self.clients.enqueue(client)

    def find_client_by_id(self, client_id):
        current_node = self.clients.front
        while current_node:
            if current_node.data.client_ID == client_id:
                return current_node.data
            current_node = current_node.next
        return None

    def remove_client(self, client_id):
        current = self.clients.front
        prev = None
        while current:
            if current.data.client_ID == client_id:
                if prev is None:
                    # 删除头节点
                    self.clients.front = current.next
                    if self.clients.front is None:
                        self.clients.rear = None
                else:
                    prev.next = current.next
                    if current.next is None:
                        # 如果是尾节点
                        self.clients.rear = prev
                self.clients._size -= 1
                return True
            prev = current
            current = current.next
        return False

    def match_properties(self, properties, current):
        matching = []
        for client in [current]:
            matched = [
                p for p in properties
                if p.price <= client.budget
                and p.status == PropertyStatus.AVAILABLE
                and p.property_type == client.property_type
            ]
            if matched:
                matching.append((client, matched))
        return matching

    def buy_property(self, client, property_id, property_manager):
        if not client:
            raise ValueError("Client not found.")
        property_obj = None

        if property_id is not None:
            property_obj = property_manager.find_property_by_id(property_id)
            if not property_obj:
                raise ValueError("Property not found.")
            if property_obj.status == PropertyStatus.SOLD:
                raise ValueError("Property is already sold.")
            if client.budget < property_obj.price:
                raise ValueError("Insufficient budget.")
            if property_obj.property_type != client.property_type:
                raise ValueError("Property type does not match client's preference.")

        else:
            # 没有指定 property_id，自动选择最便宜的符合条件的
            available_properties = property_manager.search_properties(
            price_range=(0, client.budget),
            property_type=client.property_type
        )

            if not available_properties:
                raise ValueError("No available properties match the client's criteria.")

            available_properties.sort(key=lambda p: p.price)
            property_obj = available_properties[0]

        property_obj.status = PropertyStatus.SOLD
        property_obj.owner = client.name

        self.remove_client(client.client_ID)

        return property_obj


    def peek(self):
        if not self.clients.is_empty():
            return self.clients.front.data
        return None