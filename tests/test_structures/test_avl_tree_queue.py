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

    def test_insert_ll_rotation(self):
        tree = AVLTree()
        tree.insert_key(30, "A")
        tree.insert_key(20, "B")
        tree.insert_key(10, "C")  # LL型，触发右旋
        self.assertEqual(tree.root.key, 20)

    def test_insert_rr_rotation(self):
        tree = AVLTree()
        tree.insert_key(10, "A")
        tree.insert_key(20, "B")
        tree.insert_key(30, "C")  # RR型，触发左旋
        self.assertEqual(tree.root.key, 20)


    def test_delete_node_with_two_children(self):
        tree = AVLTree()
        tree.insert_key(20, "A")
        tree.insert_key(10, "B")
        tree.insert_key(30, "C")
        tree.insert_key(25, "D")
        tree.delete(tree.root, 20)  # 根节点有两个孩子
        self.assertNotEqual(tree.root.key, 20)

    
    def test_find_by_id(self):
        tree = AVLTree()
        node1 = Property(1, "a", 100, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        node2 = Property(2, "b", 200, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        tree.insert_key(100, node1)
        tree.insert_key(200, node2)
        found = tree._find_by_id(tree.root, 2)
        self.assertIsNotNone(found)
        not_found = tree._find_by_id(tree.root, 999)
        self.assertIsNone(not_found)

    def test_search_by_price_range(self):
        tree = AVLTree()
        node1 = Property(1, "a", 100, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        node2 = Property(2, "b", 200, PropertyType.HOUSE, PropertyStatus.AVAILABLE)
        tree.insert_key(100, node1)
        tree.insert_key(200, node2)
        results = tree.search_by_price_range(50, 150)
        self.assertIn(node1, results)
        self.assertNotIn(node2, results)

    def test_insert_duplicate_key(self):
        tree = AVLTree()
        prop1 = self.create_fake_property(101, 10)
        prop2 = self.create_fake_property(102, 10)
        tree.insert_key((10, 101), prop1)
        tree.insert_key((10, 101), prop2)  # duplicate, should be ignored
        # 只会有一个节点
        self.assertEqual(tree.size(), 1)
        self.assertEqual(tree.root.property, prop1)

    def test_delete_nonexistent_key(self):
        tree = AVLTree()
        prop = self.create_fake_property(201, 20)
        tree.insert_key((20, 201), prop)
        # 删除一个不存在的key，树不变
        tree.delete_key((999, 999))
        self.assertEqual(tree.size(), 1)
        self.assertEqual(tree.root.property, prop)
        
    def test_queue_singleton_pop(self):
        q = ClientQueue()
        c = Client(99, "Single", "s@x.com", 1000)
        q.enqueue(c)
        item = q.dequeue()
        self.assertEqual(item, c)
        self.assertTrue(q.is_empty())

    def test_queue_peek_empty(self):
        q = ClientQueue()
        self.assertIsNone(q.peek())

    def test_tree_size(self):
        tree = AVLTree()
        self.assertEqual(tree.size(), 0)
        tree.insert_key((1,1), self.create_fake_property(1,1))
        self.assertEqual(tree.size(), 1)




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

    def test_dequeue_empty(self):
        """测试空队列dequeue返回None"""
        self.assertIsNone(self.queue.dequeue())

    def test_peek(self):
        """测试peek返回队首和空队列"""
        # 空队列
        self.assertIsNone(self.queue.peek())
        # 非空队列
        self.queue.enqueue(self.client1)
        self.assertEqual(self.queue.peek(), self.client1)

    def test_contains(self):
        """测试in运算符"""
        self.queue.enqueue(self.client1)
        self.assertIn(self.client1, self.queue)
        self.assertNotIn(self.client2, self.queue)

    def test_move_front_to_rear_empty_and_single(self):
        """测试move_front_to_rear空队列和单元素队列"""
        # 空队列应无异常
        self.queue.move_front_to_rear()
        self.assertTrue(self.queue.is_empty())
        # 单元素时move，内容不变
        self.queue.enqueue(self.client1)
        self.queue.move_front_to_rear()
        self.assertEqual(self.queue.size(), 1)
        self.assertEqual(self.queue.peek(), self.client1)

    def test_to_list(self):
        """测试to_list方法"""
        self.assertEqual(self.queue.to_list(), [])
        self.queue.enqueue(self.client1)
        self.queue.enqueue(self.client2)
        self.assertEqual(self.queue.to_list(), [self.client1, self.client2])


if __name__ == "__main__":
    unittest.main()