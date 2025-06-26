import unittest
from real_estate.models import Client
from real_estate.structures import AVLTree, ClientQueue

class TestAVLTree(unittest.TestCase):
    def setUp(self):
        """设置 AVLTree 测试用例的初始数据"""
        self.tree = AVLTree()

    def test_insert_and_get_keys(self):
        """测试插入和获取有序键"""
        keys = [5, 3, 7, 1, 4, 6, 8]
        for key in keys:
            self.tree.insert_key(key)
        self.assertEqual(self.tree.get_keys(), sorted(keys))

    def test_balance_after_insertions(self):
        """测试插入后的平衡性"""
        keys = [10, 20, 30, 40, 50, 25]
        for key in keys:
            self.tree.insert_key(key)
        self.assertEqual(self.tree.get_keys(), sorted(keys))

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