import unittest
from real_estate.structures.avl_tree import AVLTree
from real_estate.structures.client_queue import ClientQueue
from real_estate.models.client import Client

class TestAVLTreeAndClientQueue(unittest.TestCase):
    def test_avl_tree(self):
        """测试 AVLTree"""
        tree = AVLTree()
        tree.insert_key(5)
        tree.insert_key(3)
        tree.insert_key(7)
        tree.insert_key(2)
        tree.insert_key(4)
        tree.insert_key(6)
        tree.insert_key(8)
        print("AVLTree keys:", tree.get_keys())  # 预期: [2, 3, 4, 5, 6, 7, 8]
        tree.display()  # 打印树状结构

    def test_client_queue(self):
        """测试 ClientQueue"""
        queue = ClientQueue()
        client1 = Client(1, "Alice", "alice@example.com", 350000.0)
        client2 = Client(2, "Bob", "bob@example.com", 400000.0)
        queue.enqueue(client1)
        queue.enqueue(client2)
        print("Queue size:", queue.size())  # 预期: 2
        print("Dequeued:", queue.dequeue())  # 预期: <Client 1 | Alice | ...>
        self.assertEqual(queue.size(), 1)

if __name__ == "__main__":
    unittest.main()