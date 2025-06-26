import unittest
from real_estate.models import Client

class TestClient(unittest.TestCase):
    def setUp(self):
        """设置测试用例的初始数据"""
        self.client1 = Client(
            client_ID=1,
            name="Alice Johnson",
            contact_info="alice@example.com",
            budget=350000.0
        )
        self.client2 = Client(
            client_ID=2,
            name="Bob Miller",
            contact_info="bob@example.com",
            budget=250000.0
        )

    def test_client_initialization(self):
        self.assertEqual(self.client1.client_ID, 1)
        self.assertEqual(self.client1.name, "Alice Johnson")
        self.assertEqual(self.client1.contact_info, "alice@example.com")
        self.assertEqual(self.client1.budget, 350000.0)

        self.assertEqual(self.client2.client_ID, 2)
        self.assertEqual(self.client2.name, "Bob Miller")
        self.assertEqual(self.client2.contact_info, "bob@example.com")
        self.assertEqual(self.client2.budget, 250000.0)

    def test_client_repr(self):
        expected_repr1 = "<Client 1 | Alice Johnson | Contact: alice@example.com | Property Type: None | Budget: $350000.00>"
        expected_repr2 = "<Client 2 | Bob Miller | Contact: bob@example.com | Property Type: None | Budget: $250000.00>"
        self.assertEqual(repr(self.client1), expected_repr1)
        self.assertEqual(repr(self.client2), expected_repr2)

if __name__ == "__main__":
    unittest.main()