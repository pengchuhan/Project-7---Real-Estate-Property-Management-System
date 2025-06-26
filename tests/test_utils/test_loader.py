import unittest
import os
import shutil
import tempfile
from real_estate.utils.loader import load_dataset
from real_estate.managers.client_manager import ClientManager
from real_estate.managers.property_manager import PropertyManager

class TestLoader(unittest.TestCase):
    def setUp(self):
        # 创建临时数据目录
        self.test_dir = tempfile.mkdtemp()
        self.clients_file = os.path.join(self.test_dir, "client_requests_dataset.csv")
        self.properties_file = os.path.join(self.test_dir, "real_estate_properties_dataset.csv")

        # 写入测试数据
        with open(self.clients_file, "w", newline='', encoding='utf-8') as f:
            f.write("client_ID,name,contact_info,property_type,budget\n1,Alice,alice@example.com,HOUSE, 350000\n2,Bob,bob@example.com,APARTMENT, 250000")
        with open(self.properties_file, "w", newline='', encoding='utf-8') as f:
            f.write("property_ID,address,price,property_type,status\n1,123 Main St,250000.0,HOUSE,AVAILABLE\n2,456 Oak St,300000.0,APARTMENT,AVAILABLE")

    def tearDown(self):
        # 清理临时数据目录
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_load_dataset(self):
        """测试加载数据集"""
        # 临时修改 load_dataset 路径以使用测试数据
        original_base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        os.chdir(self.test_dir)
        try:
            client_mgr, prop_mgr = load_dataset()
            self.assertEqual(client_mgr.clients.size(), 5)  # 期望加载 5 个客户端
            self.assertEqual(len(prop_mgr.properties),10 )  # 期望加载 10 个房产
            self.assertIn(1, prop_mgr.tree.get_keys())
            self.assertIn(2, prop_mgr.tree.get_keys())
        finally:
            os.chdir(original_base_path)

if __name__ == "__main__":
    unittest.main()