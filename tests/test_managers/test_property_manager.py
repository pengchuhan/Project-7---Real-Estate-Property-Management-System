import unittest
from real_estate.managers import PropertyManager
from real_estate.models import Property, PropertyType, PropertyStatus

class TestPropertyManager(unittest.TestCase):
    def setUp(self):
        # 初始化 PropertyManager
        self.property_manager = PropertyManager()
        # 创建一些房产对象
        self.property1 = Property(1, "123 Main St", 250000.0, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        self.property2 = Property(2, "456 Elm St", 300000.0, PropertyType.APARTMENT, PropertyStatus.AVAILABLE)
        self.property3 = Property(3, "789 Oak St", 150000.0, PropertyType.APARTMENT, PropertyStatus.SOLD, owner="John Doe")
        # 添加房产到管理器
        self.property_manager.add_property(self.property1)
        self.property_manager.add_property(self.property2)
        self.property_manager.add_property(self.property3)

    def test_add_property(self):
        """测试添加房产"""
        new_property = Property(4, "101 Pine St", 400000.0, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        self.property_manager.add_property(new_property)
        self.assertIn(new_property.property_ID, self.property_manager.properties)

    def test_remove_property(self):
        """测试移除房产"""
        self.property_manager.remove_property(1)
        self.assertNotIn(1, self.property_manager.properties)
        self.assertNotIn(1, self.property_manager.tree.get_keys())

    def test_update_status(self):
        """测试更新房产状态"""
        # 设置房产所有者
        self.property_manager.properties[2].owner = "Bob Smith"
        # 更新房产状态为 SOLD
        self.property_manager.update_status(2, PropertyStatus.SOLD)
        # 检查房产状态是否更新为 SOLD
        self.assertEqual(self.property_manager.properties[2].status, PropertyStatus.SOLD)
        # 尝试将已售出的房产状态更新为 AVAILABLE，应抛出 ValueError
        with self.assertRaises(ValueError):
            self.property_manager.update_status(2, PropertyStatus.AVAILABLE)
        # 尝试将可用房产的所有者设置为 None，应抛出 ValueError
        self.property_manager.properties[1].owner = None
        with self.assertRaises(ValueError):
            self.property_manager.update_status(1, PropertyStatus.SOLD)

    def test_search_properties(self):
        """测试搜索房产"""
        results = self.property_manager.search_properties(price_range=(100000, 300000), property_type=PropertyType.APARTMENT)
        self.assertEqual(len(results), 2)
        for property_obj in results:
            self.assertTrue(100000 <= property_obj.price <= 300000)
            self.assertEqual(property_obj.property_type, PropertyType.APARTMENT)

if __name__ == "__main__":
    unittest.main()