import unittest
from real_estate.managers import ClientManager, PropertyManager
from real_estate.models import Client, Property, PropertyType, PropertyStatus


class TestClientManager(unittest.TestCase):
    def setUp(self):
        # 初始化 ClientManager
        self.client_manager = ClientManager()
        # 创建一些客户端对象
        self.client1 = Client(client_ID=1, name="Alice Johnson", contact_info="alice@example.com", budget=350000.0, property_type=PropertyType.HOUSE)
        self.client2 = Client(client_ID=2, name="Bob Smith", contact_info="bob@example.com", budget=400000.0, property_type=PropertyType.APARTMENT)
        self.client3 = Client(client_ID=3, name="Charlie Davis", contact_info="charlie@example.com", budget=250000.0, property_type=PropertyType.COMMERCIAL)

        # 添加客户端
        self.client_manager.add_client(self.client1)
        self.client_manager.add_client(self.client2)
        self.client_manager.add_client(self.client3)

        # 初始化 PropertyManager
        self.property_manager = PropertyManager()

        # 创建房产
        self.property1 = Property(1, "123 Main St", 250000.0, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        self.property2 = Property(2, "456 Elm St", 300000.0, PropertyType.APARTMENT, PropertyStatus.AVAILABLE)
        self.property3 = Property(3, "789 Oak St", 150000.0, PropertyType.APARTMENT, PropertyStatus.SOLD, owner="John Doe")
        self.property4 = Property(4, "321 Pine St", 500000.0, PropertyType.HOUSE, PropertyStatus.AVAILABLE)  # 超预算的房产

        # 添加房产
        self.property_manager.add_property(self.property1)
        self.property_manager.add_property(self.property2)
        self.property_manager.add_property(self.property3)
        self.property_manager.add_property(self.property4)

    def test_add_client(self):
        """测试添加客户端"""
        new_client = Client(client_ID=4, name="Diana Wilson", contact_info="diana@example.com", budget=300000.0, property_type=PropertyType.LAND)
        self.client_manager.add_client(new_client)
        self.assertEqual(self.client_manager.clients.size(), 4)

    def test_find_client_by_id(self):
        """测试按 ID 查找客户端"""
        found = self.client_manager.find_client_by_id(1)
        self.assertEqual(found, self.client1)

        not_found = self.client_manager.find_client_by_id(999)
        self.assertIsNone(not_found)

    def test_remove_client(self):
        """测试移除客户端"""
        removed = self.client_manager.remove_client(1)
        self.assertTrue(removed)
        self.assertIsNone(self.client_manager.find_client_by_id(1))

        # 测试移除不存在的客户
        removed_non_exist = self.client_manager.remove_client(999)
        self.assertFalse(removed_non_exist)

    def test_match_properties(self):
        """测试匹配符合预算的房产"""
        properties = self.property_manager.search_properties()

        # client1 寻找 HOUSE，预算 350000
        matches = self.client_manager.match_properties(properties, current=self.client1)
        self.assertEqual(len(matches), 1)
        matched_props = matches[0][1]
        self.assertIn(self.property1, matched_props)
        self.assertNotIn(self.property4, matched_props)  # property4 超预算
        self.assertNotIn(self.property2, matched_props)  # 类型不匹配

        # client2 寻找 APARTMENT，预算 400000
        matches2 = self.client_manager.match_properties(properties, current=self.client2)
        self.assertEqual(len(matches2), 1)
        matched_props2 = matches2[0][1]
        self.assertIn(self.property2, matched_props2)
        self.assertNotIn(self.property3, matched_props2)  # property3 已售

        # client3 寻找 COMMERCIAL，没有任何房产匹配
        matches3 = self.client_manager.match_properties(properties, current=self.client3)
        self.assertEqual(matches3, [])  # 无匹配

    def test_buy_property(self):
        """测试客户端购买房产"""
        # 正常购买
        self.client_manager.buy_property(self.client1, self.property1.property_ID, self.property_manager)
        prop = self.property_manager.find_property_by_id(self.property1.property_ID)
        self.assertEqual(prop.status, PropertyStatus.SOLD)
        self.assertEqual(prop.owner, self.client1.name)

        # 确认 client1 已从队列中移除
        self.assertIsNone(self.client_manager.find_client_by_id(self.client1.client_ID))

        # 尝试购买已售房产，应该报错
        with self.assertRaises(ValueError):
            self.client_manager.buy_property(self.client2, self.property1.property_ID, self.property_manager)

        # 尝试购买预算不足的房产
        with self.assertRaises(ValueError):
            self.client_manager.buy_property(self.client3, self.property4.property_ID, self.property_manager)

    def test_peek(self):
        """测试peek方法"""
        first_client = self.client_manager.peek()
        self.assertEqual(first_client, self.client1)

        # 移除所有客户后，peek返回None
        self.client_manager.remove_client(self.client1.client_ID)
        self.client_manager.remove_client(self.client2.client_ID)
        self.client_manager.remove_client(self.client3.client_ID)
        self.assertIsNone(self.client_manager.peek())


if __name__ == "__main__":
    unittest.main()
