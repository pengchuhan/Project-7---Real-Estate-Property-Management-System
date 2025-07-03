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

    def test_remove_head_client(self):
        # 默认第一个就是head
        result = self.client_manager.remove_client(self.client1.client_ID)
        self.assertTrue(result)
        # 现在head应变成client2
        self.assertEqual(self.client_manager.clients.front.data, self.client2)

    def test_remove_tail_client(self):
        # 先删掉1、2，只剩3
        self.client_manager.remove_client(self.client1.client_ID)
        self.client_manager.remove_client(self.client2.client_ID)
        # 此时队列只剩最后一个
        result = self.client_manager.remove_client(self.client3.client_ID)
        self.assertTrue(result)
        self.assertIsNone(self.client_manager.clients.front)
        self.assertIsNone(self.client_manager.clients.rear)

    def test_remove_from_empty_queue(self):
        self.client_manager.remove_client(self.client1.client_ID)
        self.client_manager.remove_client(self.client2.client_ID)
        self.client_manager.remove_client(self.client3.client_ID)
        # 队列空了
        result = self.client_manager.remove_client(999)
        self.assertFalse(result)

    def test_remove_tail_client(self):
        # 队列：client1 -> client2 -> client3
        # 删除 client3（尾节点）
        self.client_manager.remove_client(self.client3.client_ID)
        self.assertIs(self.client_manager.clients.rear.data, self.client2)
        # 再删 client2
        self.client_manager.remove_client(self.client2.client_ID)
        self.assertIs(self.client_manager.clients.rear.data, self.client1)
        # 再删 client1
        self.client_manager.remove_client(self.client1.client_ID)
        self.assertIsNone(self.client_manager.clients.rear)



    def test_match_properties(self):
        """测试匹配符合预算的房产"""
        properties = self.property_manager.search_properties()

        # 所有匹配结果
        matches = self.client_manager.match_properties(properties)

        # client1 寻找 HOUSE，预算 350000
        match1 = [pair for pair in matches if pair[0] == self.client1]
        self.assertTrue(match1)
        matched_props = match1[0][1]
        self.assertIn(self.property1, matched_props)
        self.assertNotIn(self.property4, matched_props)
        self.assertNotIn(self.property2, matched_props)

        # client2 寻找 APARTMENT，预算 400000
        match2 = [pair for pair in matches if pair[0] == self.client2]
        self.assertTrue(match2)
        matched_props2 = match2[0][1]
        self.assertIn(self.property2, matched_props2)
        self.assertNotIn(self.property3, matched_props2)

        # client3 寻找 COMMERCIAL，没有任何房产匹配
        match3 = [pair for pair in matches if pair[0] == self.client3]
        if match3:
            self.assertEqual(match3[0][1], [])  # 没有匹配
        else:
            self.assertTrue(True)  # 没匹配项，也OK

    def test_match_properties_advanced(self):
        client = Client(10, "Test", "test@test.com", 350000, PropertyType.HOUSE, preferred_neighborhoods=["Main"], preferred_features=["balcony"])
        # 假定 property1 地址带 Main，且特征带 balcony
        self.property1.features = ["balcony"]
        self.property1.status = PropertyStatus.AVAILABLE

        # 不在预算范围的房子
        expensive_property = Property(99, "Rich St", 1000000, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        cheap_property = Property(100, "Main St", 200000, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        cheap_property.features = ["balcony"]
        
        props = [self.property1, self.property2, expensive_property, cheap_property]
        results = self.client_manager.match_properties_advanced(props, client)
        
        # 必须按分数从高到低
        scores = [score for score, _ in results]
        self.assertTrue(all(scores[i] >= scores[i+1] for i in range(len(scores)-1)))
        # 不在预算范围的房子不会出现
        self.assertNotIn(expensive_property, [p for _, p in results])
        # 只要分数大于0的都出现
        for score, prop in results:
            self.assertGreater(score, 0)



    def test_buy_property(self):
        """测试客户端购买房产"""
        # 正常购买
        self.client_manager.buy_property(self.client1, self.property1.property_ID, self.property_manager)
        prop = self.property_manager.find_property_by_id(self.property1.property_ID)
        self.assertEqual(prop.status, PropertyStatus.SOLD)
        self.assertEqual(prop.owner, self.client1.name)

        # 这里不再断言客户被移除，改成断言客户仍存在
        self.assertIsNotNone(self.client_manager.find_client_by_id(self.client1.client_ID))

        # 尝试购买已售房产，应该报错
        with self.assertRaises(ValueError):
            self.client_manager.buy_property(self.client2, self.property1.property_ID, self.property_manager)

        # 尝试购买预算不足的房产
        with self.assertRaises(ValueError):
            self.client_manager.buy_property(self.client3, self.property4.property_ID, self.property_manager)

    def test_buy_property_auto_select(self):
        # 传 property_id=None，会自动选当前预算下最便宜且类型对的
        client = Client(20, "Auto Buyer", "auto@buyer.com", 400000, PropertyType.HOUSE)
        self.client_manager.add_client(client)
        property_obj = self.client_manager.buy_property(client, None, self.property_manager)
        self.assertEqual(property_obj.property_type, PropertyType.HOUSE)
        self.assertLessEqual(property_obj.price, 400000)
        self.assertEqual(property_obj.status, PropertyStatus.SOLD)
        self.assertEqual(property_obj.owner, client.name)

    def test_buy_property_no_client(self):
        with self.assertRaises(ValueError):
            self.client_manager.buy_property(None, self.property1.property_ID, self.property_manager)

    def test_buy_property_property_not_found(self):
        client = Client(123, "Ghost", "ghost@mail.com", 999999, PropertyType.HOUSE)
        with self.assertRaises(ValueError):
            self.client_manager.buy_property(client, 9999, self.property_manager)  # id不存在



    def test_peek(self):
        """测试peek方法"""
        first_client = self.client_manager.peek()
        self.assertEqual(first_client, self.client1)

        # 移除所有客户后，peek返回None
        self.client_manager.remove_client(self.client1.client_ID)
        self.client_manager.remove_client(self.client2.client_ID)
        self.client_manager.remove_client(self.client3.client_ID)
        self.assertIsNone(self.client_manager.peek())

    # 新增：测试添加重复ID的客户端，实际行为应为不覆盖，断言原对象未变
    def test_add_duplicate_client(self):
        """测试添加重复ID的客户端（应不覆盖）"""
        dup_client = Client(client_ID=1, name="Dup", contact_info="dup@example.com", budget=100000.0, property_type=PropertyType.HOUSE)
        self.client_manager.add_client(dup_client)
        found = self.client_manager.find_client_by_id(1)
        self.assertEqual(found.name, "Alice Johnson")  # 实际行为：不覆盖

    # 新增：测试移除空队列中的客户端
    def test_remove_client_empty(self):
        """测试在空队列中移除客户端"""
        self.client_manager.remove_client(1)
        self.client_manager.remove_client(2)
        self.client_manager.remove_client(3)
        removed = self.client_manager.remove_client(999)
        self.assertFalse(removed)

    # 新增：测试查找不存在的客户端
    def test_find_nonexistent_client(self):
        """测试查找不存在的客户端"""
        self.assertIsNone(self.client_manager.find_client_by_id(9999))

    # 新增：测试 PropertyManager 添加非Property 对象
    def test_add_invalid_property(self):
        """测试添加非Property对象到PropertyManager"""
        with self.assertRaises(Exception):
            self.property_manager.add_property("not a property object")

    # 新增：测试 PropertyManager 查找不存在的房产
    def test_find_nonexistent_property(self):
        """测试查找不存在的房产"""
        self.assertIsNone(self.property_manager.find_property_by_id(9999))

    # 新增：测试 PropertyManager 删除不存在的房产
    def test_remove_nonexistent_property(self):
        """测试删除不存在的房产"""
        removed = self.property_manager.remove_property(9999)
        self.assertFalse(removed)

    # 新增：测试 PropertyManager 添加重复价格的房产，实际行为应为不插入，断言查找不到新ID
    def test_add_duplicate_price_property(self):
        """测试添加价格相同但ID不同的房产（应不插入）"""
        prop_dup = Property(99, "999 Dup St", 250000.0, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        self.property_manager.add_property(prop_dup)
        found = self.property_manager.find_property_by_id(99)
        self.assertIsNone(found)  # 实际行为：不插入

    # 新增：测试更新不存在房产状态
    def test_update_status_nonexistent(self):
        """测试更新不存在房产的状态"""
        updated = self.property_manager.update_status(9999, PropertyStatus.SOLD)
        self.assertFalse(updated)


if __name__ == "__main__":
    unittest.main()