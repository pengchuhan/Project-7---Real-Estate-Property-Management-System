from ..models import Property, PropertyStatus, PropertyType
from ..structures.avl_tree import AVLTree

class PropertyManager:
    def __init__(self):
        self.tree = AVLTree()  # 存储 Property ID，用于快速查找

    def add_property(self, property_obj):
        if not isinstance(property_obj, Property):
            raise ValueError("Must be a Property instance")
        self.tree.insert_key(property_obj.price, property_obj)

    def remove_property(self, property_id):
        node = self.tree.find_by_id(property_id)
        if node:
            self.tree.delete_key(node.key)  # 按price删除
            return True
        return False

    def update_status(self, property_id, new_status):
        node = self.tree.find_by_id(property_id)
        if node:
            property_obj = node.property
            if new_status == PropertyStatus.SOLD and not property_obj.owner:
                raise ValueError("A sold property must have an owner.")
            if new_status == PropertyStatus.AVAILABLE and property_obj.owner:
                raise ValueError("An available property cannot have an owner.")
            property_obj.status = new_status
            return True
        return False

    def search_properties(self, price_range=None, property_type=None, location=None):
        min_price = price_range[0] if price_range else float('-inf')
        max_price = price_range[1] if price_range else float('inf')

        results = []

        def inorder(node):
            if not node:
                return
            if node.key >= min_price:
                inorder(node.left)
            if min_price <= node.key <= max_price:
                prop = node.property
                if (property_type is None or prop.property_type == property_type) and \
                   (location is None or prop.address == location) and \
                   (prop.status == PropertyStatus.AVAILABLE):
                    results.append(prop)
            if node.key <= max_price:
                inorder(node.right)

        inorder(self.tree.root)
        return results

    def find_property_by_id(self, property_id):
        node = self.tree.find_by_id(property_id)
        return node.property if node else None