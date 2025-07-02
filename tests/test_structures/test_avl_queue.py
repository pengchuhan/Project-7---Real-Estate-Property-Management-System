import unittest
from real_estate.structures.avl_tree import AVLTree
from real_estate.structures.client_queue import ClientQueue
from real_estate.models.client import Client
from real_estate.models.property import Property, PropertyType, PropertyStatus


class TestAVLTreeAndClientQueue(unittest.TestCase):
    def setUp(self):
        """初始化AVLTree和ClientQueue"""
        self.tree = AVLTree()
        self.queue = ClientQueue()

    def create_property(self, property_id, price):
        """辅助函数：创建Property对象"""
        return Property(
            property_ID=property_id,
            address=f"Address {property_id}",
            price=price,
            property_type=PropertyType.HOUSE,
            status=PropertyStatus.AVAILABLE
        )

    def test_avl_tree(self):
        """测试 AVLTree 插入并打印"""
        keys = [(5, 105), (3, 103), (7, 107), (2, 102), (4, 104), (6, 106), (8, 108)]
        for price, prop_id in keys:
            prop = self.create_property(prop_id, price)
            self.tree.insert_key((price, prop_id), prop)

        print("\n=== AVL Tree Structure ===")
        self.tree.display_horizontal()

        # 中序遍历验证
        inorder_keys = []

        def inorder(node):
            if node:
                inorder(node.left)
                inorder_keys.append(node.key)
                inorder(node.right)

        inorder(self.tree.root)
        expected = sorted(keys)
        self.assertEqual(inorder_keys, expected)

        print("In-order keys:", inorder_keys)

    def test_client_queue(self):
        """测试 ClientQueue 入队和出队"""
        client1 = Client(1, "Alice", "alice@example.com", 350000.0, property_type=PropertyType.HOUSE)
        client2 = Client(2, "Bob", "bob@example.com", 400000.0, property_type=PropertyType.APARTMENT)

        self.queue.enqueue(client1)
        self.queue.enqueue(client2)

        print("Queue size after enqueue:", self.queue.size())  # 预期: 2

        dequeued_client = self.queue.dequeue()
        print("Dequeued client:", dequeued_client)  # 预期: client1

        self.assertEqual(dequeued_client, client1)
        self.assertEqual(self.queue.size(), 1)


if __name__ == "__main__":
    unittest.main()
