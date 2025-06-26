from ..models import Property, PropertyStatus, PropertyType
from ..structures.avl_tree import AVLTree

class PropertyManager:
    def __init__(self):
        self.properties = {}  # 映射 ID 到 Property 对象
        self.tree = AVLTree()  # 存储 Property ID，用于快速查找

    def add_property(self, property_obj):
        if isinstance(property_obj, Property):
            self.properties[property_obj.property_ID] = property_obj
            self.tree.insert_key(property_obj.property_ID)

    def remove_property(self, property_id):
        if property_id in self.properties:
            del self.properties[property_id]
            self.tree.delete_key(property_id)
            return True
        return False

    def update_status(self, property_id, new_status):
        if property_id in self.properties:
            property_obj = self.properties[property_id]
            if new_status == PropertyStatus.SOLD and not property_obj.owner:
                raise ValueError("A sold property must have an owner.")
            if new_status == PropertyStatus.AVAILABLE and property_obj.owner:
                raise ValueError("An available property cannot have an owner.")
            property_obj.status = new_status
            return True
        return False

    def search_properties(self, price_range=None, property_type=None, location=None):
        if price_range is not None and (not isinstance(price_range, tuple) or len(price_range) != 2):
            raise ValueError("price_range must be a tuple of (min, max)")
        results = []
        for property_obj in self.properties.values():
            if (price_range is None or price_range[0] <= property_obj.price <= price_range[1]) and \
               (property_type is None or property_obj.property_type == property_type) and \
               (location is None or property_obj.address == location):
                results.append(property_obj)
        return results