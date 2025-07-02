from real_estate.managers import ClientManager, PropertyManager
from real_estate.utils.loader import load_dataset
from PyQt5.QtWidgets import QApplication
import sys
from real_estate.gui.interface import RealEstateGUI

def main():
    # 指定数据文件的路径和文件名
    data_dir = "datasets"  # 数据文件所在的目录
    client_filename = "client_requests_dataset.csv"  # 客户数据文件名
    property_filename = "real_estate_properties_dataset.csv"  # 房产数据文件名

    # 加载数据集
    client_manager, property_manager = load_dataset(data_dir, client_filename, property_filename)

    # 处理客户端请求
    while not client_manager.clients.is_empty():
        client = client_manager.clients.dequeue()  # 直接移除队列顶部的客户端
        print(f"Processing client request: {client}")

        # 获取所有房产（中序遍历）
        properties = property_manager.tree.search_by_price_range(float('-inf'), float('inf'))

        # 查找符合预算的房产
        matches = client_manager.match_properties(properties, client)
        if matches:
            print(f"Matching properties for client {client.client_ID}:")
            for client_match, matched_properties in matches:
                for property in matched_properties:
                    print(f"  - {property}")
        else:
            print(f"No matching properties for client {client.client_ID}.")

        # 客户购买房产
        if matches:
            property_to_buy = matches[0][1][0]
            client_manager.buy_property(client, property_to_buy.property_ID, property_manager)
            print(f"Client {client.client_ID} has bought property {property_to_buy.property_ID}.")
        else:
            print(f"Client {client.client_ID} did not buy any property.")
            client_manager.remove_client(client.client_ID)  # 没买也移除

def main():
    app = QApplication(sys.argv)
    gui = RealEstateGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()