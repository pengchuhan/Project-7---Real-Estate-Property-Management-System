import unittest
import os
import shutil
import tempfile
from real_estate.utils.loader import load_dataset
from real_estate.managers.client_manager import ClientManager
from real_estate.managers.property_manager import PropertyManager
from real_estate.models.property import PropertyStatus, PropertyType, Property
from real_estate.models.client import Client
from typing import Tuple
import csv


def count_properties(tree) -> int:
    """辅助函数，统计 AVL 树里节点数量"""
    count = 0
    def inorder(node):
        nonlocal count
        if not node:
            return
        inorder(node.left)
        count += 1
        inorder(node.right)
    inorder(tree.root)
    return count


def get_all_keys(tree):
    """辅助函数，获取 AVL 树中所有的 key"""
    keys = []
    def inorder(node):
        if not node:
            return
        inorder(node.left)
        keys.append(node.key)
        inorder(node.right)
    inorder(tree.root)
    return keys


class TestLoader(unittest.TestCase):
    def setUp(self):
        # 创建临时数据目录
        self.test_dir = tempfile.mkdtemp()

        # 自定义文件名
        self.clients_file = os.path.join(self.test_dir, "test_client.csv")
        self.properties_file = os.path.join(self.test_dir, "test_property.csv")

        # 写入客户端数据
        with open(self.clients_file, "w", newline='', encoding='utf-8') as f:
            f.write(
                "client_ID,name,contact_info,property_type,budget\n"
                "1,Alice,alice@example.com,HOUSE,350000\n"
                "2,Bob,bob@example.com,APARTMENT,250000\n"
                "3,Charlie,charlie@example.com,HOUSE,400000\n"
            )

        # 写入房产数据
        with open(self.properties_file, "w", newline='', encoding='utf-8') as f:
            f.write(
                "property_ID,address,price,property_type,status\n"
                "1,123 Main St,250000.0,HOUSE,AVAILABLE\n"
                "2,456 Oak St,300000.0,APARTMENT,AVAILABLE\n"
                "3,789 Pine St,400000.0,HOUSE,AVAILABLE\n"
                "4,101 Maple St,500000.0,APARTMENT,SOLD\n"
            )

    def tearDown(self):
        # 清理临时数据目录
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_dataset(self):
        """测试加载自定义CSV数据集"""
        client_mgr, prop_mgr = load_dataset(
            data_dir=self.test_dir,
            client_filename="test_client.csv",
            property_filename="test_property.csv"
        )

        # 验证客户端数量
        self.assertEqual(client_mgr.clients.size(), 3)

        # 验证房产数量
        self.assertEqual(count_properties(prop_mgr.tree), 4)

        # 验证是否包含正确的price作为key
        keys = get_all_keys(prop_mgr.tree)
        self.assertIn(250000.0, keys)
        self.assertIn(500000.0, keys)


if __name__ == "__main__":
    unittest.main()
