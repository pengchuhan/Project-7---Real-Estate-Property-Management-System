import unittest
from real_estate.models import Client
from real_estate.structures import AVLTree, ClientQueue
from real_estate.models.property import Property, PropertyType, PropertyStatus

class TestAVLTree(unittest.TestCase):
    def setUp(self):
        """设置 AVLTree 测试用例的初始数据"""
        self.tree = AVLTree()
    
    def create_fake_property(self, property_id, price):
        return Property(
            property_ID=property_id,
            address=f"Address {property_id}",
            price=price,
            property_type=PropertyType.HOUSE,
            status=PropertyStatus.AVAILABLE
        )

    def test_insert_and_get_keys(self):
        """测试插入和获取有序键"""
        keys = [(5, 105), (3, 103), (7, 107), (1, 101), (4, 104), (6, 106), (8, 108)]
        for price, prop_id in keys:
            prop = self.create_fake_property(prop_id, price)
            self.tree.insert_key((price, prop_id), prop)

        # 获取中序遍历的 key 列表
        inorder_keys = []

        def inorder(node):
            if node:
                inorder(node.left)
                inorder_keys.append(node.key)
                inorder(node.right)

        inorder(self.tree.root)

        expected = sorted(keys)
        self.assertEqual(inorder_keys, expected)


    def test_balance_after_insertions(self):
        """测试AVL树插入后是否平衡"""
        keys = [(10, 110), (20, 120), (30, 130), (40, 140), (50, 150), (25, 125)]
        for price, prop_id in keys:
            prop = self.create_fake_property(prop_id, price)
            self.tree.insert_key((price, prop_id), prop)

        # 判断是否平衡
        def is_balanced(node):
            if not node:
                return True
            balance = abs(self.tree.balance_factor(node))
            return balance <= 1 and is_balanced(node.left) and is_balanced(node.right)

        self.assertTrue(is_balanced(self.tree.root))


if __name__ == "__main__":
    unittest.main()
class TestClientQueue(unittest.TestCase):
    def setUp(self):
        """设置 ClientQueue 测试用例的初始数据"""
        self.queue = ClientQueue()
        self.client1 = Client(client_ID=1, name="Alice Johnson", contact_info="alice@example.com", budget=350000.0)
        self.client2 = Client(client_ID=2, name="Bob Smith", contact_info="bob@example.com", budget=400000.0)

    def test_enqueue_and_dequeue(self):
        """测试入队和出队"""
        self.queue.enqueue(self.client1)
        self.queue.enqueue(self.client2)
        self.assertEqual(self.queue.size(), 2)
        self.assertEqual(self.queue.dequeue(), self.client1)
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.dequeue(), self.client2)
        self.assertTrue(self.queue.is_empty())

    def test_is_empty(self):
        """测试队列是否为空"""
        self.assertTrue(self.queue.is_empty())
        self.queue.enqueue(self.client1)
        self.assertFalse(self.queue.is_empty())

    def test_no_duplicates(self):
        """测试队列不允许重复客户端"""
        self.queue.enqueue(self.client1)
        self.queue.enqueue(self.client1)  # 尝试添加重复客户端
        self.assertEqual(self.queue.size(), 1)  # 队列大小应该仍然是1

if __name__ == "__main__":
    unittest.main()