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

    def match_properties(self, properties):
        matching = []
        current_node = self.clients.front
        while current_node:
            client = current_node.data
            matched = [
                p for p in properties
                if p.price <= client.budget
                and p.status == PropertyStatus.AVAILABLE
                and p.property_type == client.property_type
            ]
            if matched:
                matching.append((client, matched))
            current_node = current_node.next
        return matching


    def match_properties_advanced(self, properties, client):
        """
        根据客户详细偏好为其匹配房产，返回按匹配分数排序的房产列表。
        匹配分数考虑预算、类型、位置、特征等。
        """
        results = []
        for prop in properties:
            # 如果价格超过预算，不计分，直接跳过
            if prop.price > client.budget:
                continue
            score = 0
            # 预算匹配
            if prop.price <= client.budget:
                score += 30
            # 类型匹配
            if prop.property_type == client.property_type:
                score += 20
            # 区域匹配
            if hasattr(prop, 'address') and client.preferred_neighborhoods:
                for n in client.preferred_neighborhoods:
                    if n in prop.address:
                        score += 20
                        break
            # 特征匹配
            if hasattr(prop, 'features') and client.preferred_features:
                matched = set(client.preferred_features) & set(getattr(prop, 'features', []))
                score += 10 * len(matched)
            # 状态可售
            if hasattr(prop, 'status') and getattr(prop, 'status', None).name == 'AVAILABLE':
                score += 10
            if score > 0:
                results.append((score, prop))
        # 按分数降序排序
        results.sort(reverse=True, key=lambda x: x[0])
        return results

    def buy_property(self, client, property_id, property_manager):
        if not client:
            raise ValueError("Client not found.")

        property_obj = None

        if property_id is not None:
            property_obj = property_manager.find_property_by_id(property_id)
            if not property_obj:
                raise ValueError("Property not found.")
            if property_obj.status != PropertyStatus.AVAILABLE:
                raise ValueError(f"Property '{property_obj.property_ID}' is not available.")
            if property_obj.property_type != client.property_type:
                raise ValueError("Property type does not match client's preference.")
            if client.budget < property_obj.price:
                raise ValueError("Insufficient budget.")

            property_obj.status = PropertyStatus.SOLD
            property_obj.owner = client.name

        else:
            matches = property_manager.search_properties(
                price_range=(0, client.budget),
                property_type=client.property_type
            )
            matches = [p for p in matches if p.status == PropertyStatus.AVAILABLE]

            if not matches:
                raise ValueError("No available properties match the client's criteria.")

            matches.sort(key=lambda p: p.price)
            property_obj = matches[0]

        property_obj.status = PropertyStatus.SOLD
        property_obj.owner = client.name
        client.budget -= property_obj.price



        return property_obj  # 不再移除队列中的客户




    def peek(self):
        if not self.clients.is_empty():
            return self.clients.front.data
        return None