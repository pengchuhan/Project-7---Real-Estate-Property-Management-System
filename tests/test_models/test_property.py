import unittest
from real_estate.models import Property, PropertyType, PropertyStatus

class TestProperty(unittest.TestCase):
    def setUp(self):
        """设置测试用例的初始数据"""
        self.property1 = Property(
            property_ID=1,
            address="123 Main St",
            price=250000.0,
            property_type=PropertyType.HOUSE,
            status=PropertyStatus.AVAILABLE,
            owner=None
        )
        self.property2 = Property(
            property_ID=3,
            address="789 Oak St",
            price=150000.0,
            property_type=PropertyType.APARTMENT,
            status=PropertyStatus.SOLD,
            owner="John Doe"
        )
        self.property3 = Property(
            property_ID=1,
            address="123 Main St",
            price=250000.0,
            property_type=PropertyType.HOUSE,
            status=PropertyStatus.AVAILABLE,
            owner=None
        )

    def test_property_initialization(self):
        """测试 Property 类的初始化"""
        self.assertEqual(self.property1.property_ID, 1)
        self.assertEqual(self.property1.address, "123 Main St")
        self.assertEqual(self.property1.price, 250000.0)
        self.assertEqual(self.property1.property_type, PropertyType.HOUSE)
        self.assertEqual(self.property1.status, PropertyStatus.AVAILABLE)
        self.assertIsNone(self.property1.owner)

        self.assertEqual(self.property2.property_ID, 3)
        self.assertEqual(self.property2.address, "789 Oak St")
        self.assertEqual(self.property2.price, 150000.0)
        self.assertEqual(self.property2.property_type, PropertyType.APARTMENT)
        self.assertEqual(self.property2.status, PropertyStatus.SOLD)
        self.assertEqual(self.property2.owner, "John Doe")

    def test_property_repr(self):
        """测试 Property 类的 __repr__ 方法"""
        expected_repr1 = "<Property 1 | 123 Main St | $250000.00 | HOUSE | AVAILABLE | Owner: None | Features: 无>"
        expected_repr2 = "<Property 3 | 789 Oak St | $150000.00 | APARTMENT | SOLD | Owner: John Doe | Features: 无>"
        self.assertEqual(repr(self.property1), expected_repr1)
        self.assertEqual(repr(self.property2), expected_repr2)

    def test_property_eq(self):
        """测试 Property 类的 __eq__ 方法"""
        self.assertTrue(self.property1 == self.property3)
        self.assertFalse(self.property1 == self.property2)
        self.assertFalse(self.property1 == "not a property")

    def test_property_lt(self):
        """测试 Property 类的 __lt__ 方法"""
        self.assertTrue(self.property1 < self.property2)
        self.assertFalse(self.property2 < self.property1)
        with self.assertRaises(TypeError):
            self.property1 < "not a property"

if __name__ == "__main__":
    unittest.main()