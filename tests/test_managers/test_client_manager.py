import unittest
from real_estate.managers import ClientManager, PropertyManager
from real_estate.models import Client, Property, PropertyType, PropertyStatus

class TestClientManager(unittest.TestCase):
    def setUp(self):
        # 初始化 ClientManager
        self.client_manager = ClientManager()
        # 创建一些客户端对象，包含 property_type
        self.client1 = Client(client_ID=1, name="Alice Johnson", contact_info="alice@example.com", budget=350000.0, property_type=PropertyType.HOUSE)
        self.client2 = Client(client_ID=2, name="Bob Smith", contact_info="bob@example.com", budget=400000.0, property_type=PropertyType.APARTMENT)
        self.client3 = Client(client_ID=3, name="Charlie Davis", contact_info="charlie@example.com", budget=250000.0, property_type=PropertyType.COMMERCIAL)
        # 添加客户端到管理器
        self.client_manager.add_client(self.client1)
        self.client_manager.add_client(self.client2)
        self.client_manager.add_client(self.client3)
        
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

    def test_add_client(self):
        """测试添加客户端"""
        new_client = Client(client_ID=4, name="Diana Wilson", contact_info="diana@example.com", budget=300000.0, property_type=PropertyType.LAND)
        self.client_manager.add_client(new_client)
        self.assertEqual(self.client_manager.clients.size(), 4)

    def test_find_client_by_id(self):
        """测试按 ID 查找客户端"""
        found = self.client_manager.find_client_by_id(1)
        self.assertEqual(found, self.client1)
        self.assertIsNone(self.client_manager.find_client_by_id(999))

    def test_remove_client(self):
        """测试移除客户端"""
        self.client_manager.remove_client(1)
        self.assertIsNone(self.client_manager.find_client_by_id(1))

    def test_match_properties(self):
        """测试匹配符合预算的房产"""
        properties = [self.property1, self.property2, self.property3]
        # 仅匹配 client1 的 HOUSE 类型房产
        matches = self.client_manager.match_properties(properties, 0, 400000, current=self.client1)
        self.assertEqual(len(matches), 1)  # 应仅匹配 property1 (HOUSE)
        self.assertEqual(matches[0][0], self.client1)
        self.assertIn(self.property1, matches[0][1])  # 匹配 property1
        self.assertNotIn(self.property2, matches[0][1])  # 不匹配 APARTMENT

    def test_buy_property(self):
        """测试客户端购买房产"""
        # 传递 client 对象而非 client_ID
        self.client_manager.buy_property(self.client1, self.property1.property_ID, self.property_manager)
        self.assertEqual(self.property_manager.properties[self.property1.property_ID].status, PropertyStatus.SOLD)
        self.assertEqual(self.property_manager.properties[self.property1.property_ID].owner, self.client1.name)
        self.assertIsNone(self.client_manager.find_client_by_id(self.client1.client_ID))

if __name__ == "__main__":
    unittest.main()