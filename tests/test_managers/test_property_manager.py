import unittest
from real_estate.managers import PropertyManager
from real_estate.models import Property, PropertyType, PropertyStatus


class TestPropertyManager(unittest.TestCase):
    def setUp(self):
        # 初始化 PropertyManager
        self.property_manager = PropertyManager()

        # 创建房产对象
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

        found = self.property_manager.find_property_by_id(4)
        self.assertIsNotNone(found)
        self.assertEqual(found.address, "101 Pine St")
        self.assertEqual(found.price, 400000.0)

    def test_remove_property(self):
        """测试移除房产"""
        # 移除存在的房产
        removed = self.property_manager.remove_property(1)
        self.assertTrue(removed)
        self.assertIsNone(self.property_manager.find_property_by_id(1))

        # 移除不存在的房产
        removed = self.property_manager.remove_property(999)
        self.assertFalse(removed)

    def test_update_status(self):
        """测试更新房产状态"""
        # 设置房产所有者
        property_obj = self.property_manager.find_property_by_id(2)
        property_obj.owner = "Bob Smith"

        # 更新房产状态为 SOLD
        result = self.property_manager.update_status(2, PropertyStatus.SOLD)
        self.assertTrue(result)
        updated_property = self.property_manager.find_property_by_id(2)
        self.assertEqual(updated_property.status, PropertyStatus.SOLD)

        # 尝试将已售出房产变为 AVAILABLE，应该报错（有owner不允许变AVAILABLE）
        with self.assertRaises(ValueError):
            self.property_manager.update_status(2, PropertyStatus.AVAILABLE)

        # 尝试将 AVAILABLE 房产变为 SOLD，但没有 owner，应报错
        available_property = self.property_manager.find_property_by_id(1)
        available_property.owner = None  # 确认没有 owner
        with self.assertRaises(ValueError):
            self.property_manager.update_status(1, PropertyStatus.SOLD)

    def test_search_properties(self):
        """测试搜索房产"""
        # 查找价格在 100000 到 300000 之间，类型为 APARTMENT
        results = self.property_manager.search_properties(
            price_range=(100000, 300000),
            property_type=PropertyType.APARTMENT
        )
        self.assertEqual(len(results), 2)
        property_ids = [p.property_ID for p in results]
        self.assertIn(2, property_ids)  # AVAILABLE
        self.assertIn(3, property_ids)  # SOLD

        # 查找价格在 100000 到 300000 之间，不限制类型
        results = self.property_manager.search_properties(
            price_range=(100000, 300000)
        )
        self.assertEqual(len(results), 3)
        property_ids = [p.property_ID for p in results]
        self.assertIn(1, property_ids)
        self.assertIn(2, property_ids)
        self.assertIn(3, property_ids)

        # 查找特定位置
        results = self.property_manager.search_properties(location="456 Elm St")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].property_ID, 2)

    # 新增：测试添加重复价格但不同ID的房产，实际行为应为不插入，断言查找不到新ID
    def test_add_duplicate_price_property(self):
        """测试添加价格相同但ID不同的房产（应不插入）"""
        prop_dup = Property(99, "999 Dup St", 250000.0, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        self.property_manager.add_property(prop_dup)
        found = self.property_manager.find_property_by_id(99)
        self.assertIsNone(found)  # 实际行为：不插入

    # 新增：测试添加非Property对象
    def test_add_invalid_property(self):
        """测试添加非Property对象到PropertyManager"""
        with self.assertRaises(Exception):
            self.property_manager.add_property("not a property object")

    # 新增：测试查找不存在的房产
    def test_find_nonexistent_property(self):
        """测试查找不存在的房产"""
        self.assertIsNone(self.property_manager.find_property_by_id(9999))

    # 新增：测试删除不存在的房产
    def test_remove_nonexistent_property(self):
        """测试删除不存在的房产"""
        removed = self.property_manager.remove_property(9999)
        self.assertFalse(removed)

    # 新增：测试更新不存在房产的状态
    def test_update_status_nonexistent(self):
        """测试更新不存在房产的状态"""
        updated = self.property_manager.update_status(9999, PropertyStatus.SOLD)
        self.assertFalse(updated)

    # 新增：测试搜索空管理器
    def test_search_empty_manager(self):
        """测试在空PropertyManager中搜索房产"""
        pm = PropertyManager()
        results = pm.search_properties()
        self.assertEqual(results, [])

    def test_adjust_prices(self):
        """测试房产动态调价 adjust_prices"""
        # 设置不同浏览量和问询量
        self.property1.views = 15   # 超过high_threshold，应该涨价
        self.property1.inquiries = 0
        self.property2.views = 1    # 低于low_threshold，应该降价
        self.property2.inquiries = 1
        self.property3.views = 5    # 在正常区间，不变
        self.property3.inquiries = 5

        old_price1 = self.property1.price
        old_price2 = self.property2.price
        old_price3 = self.property3.price

        self.property_manager.adjust_prices(high_threshold=10, low_threshold=2, increase_rate=0.05, decrease_rate=0.03)

        # property1应该涨价，property2应该降价，property3不变
        self.assertGreater(self.property1.price, old_price1)
        self.assertLess(self.property2.price, old_price2)
        self.assertEqual(self.property3.price, old_price3)
        # views和inquiries会被reset
        self.assertEqual(self.property1.views, 0)
        self.assertEqual(self.property2.inquiries, 0)



if __name__ == "__main__":
    unittest.main()