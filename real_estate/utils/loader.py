from ..models import Client, Property, PropertyType, PropertyStatus
from ..structures.client_queue import ClientQueue
from ..structures.avl_tree import AVLTree
from ..managers.client_manager import ClientManager
from ..managers.property_manager import PropertyManager
import csv
import os
from typing import Tuple

def load_dataset() -> Tuple[ClientManager, PropertyManager]:
    """
    读取 datasets 中的 CSV 文件并初始化 ClientManager 和 PropertyManager.

    Returns:
        Tuple[ClientManager, PropertyManager]: 一个包含 ClientManager 和 PropertyManager 实例的元组.

    Raises:
        FileNotFoundError: 如果数据集文件不存在。
        ValueError: 如果 CSV 数据格式错误。
    """
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # 回到 real_estate_project 根目录
    data_dir = os.path.join(base_path, "datasets")
    client_manager = ClientManager()
    property_manager = PropertyManager()

    # 加载客户端数据
    # 加载客户端数据
    clients_file = os.path.join(data_dir, "client_requests_dataset.csv")
    print(f"Checking clients file: {clients_file}")
    if not os.path.exists(clients_file):
        print(f"Clients file not found: {clients_file}")
        raise FileNotFoundError(f"Dataset file not found: {clients_file}")
    try:
        with open(clients_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 修改此行，格式化输出具体字段
                print(f"Processing client: client_ID={row['client_ID']}, name={row['name']}, contact_info={row['contact_info']}, property_type={row['property_type']}, budget={row['budget'].strip()}")
                client = Client(
                    client_ID=int(row["client_ID"]),
                    name=row["name"],
                    contact_info=row["contact_info"],
                    budget=float(row["budget"].strip()),
                    property_type=PropertyType[row["property_type"]]
                )
                client_manager.add_client(client)
                print(f"Added client with ID: {client.client_ID}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"Error parsing clients file: {e}")

    # 加载房产数据
    properties_file = os.path.join(data_dir, "real_estate_properties_dataset.csv")
    print(f"Checking properties file: {properties_file}")
    if not os.path.exists(properties_file):
        print(f"Properties file not found: {properties_file}")
        raise FileNotFoundError(f"Dataset file not found: {properties_file}")
    try:
        with open(properties_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # 修改此行，格式化输出具体字段
                print(f"Processing property: property_ID={row['property_ID']}, address={row['address']}, price={row['price']}, property_type={row['property_type']}, status={row['status']}")
                property_obj = Property(
                    property_ID=int(row["property_ID"]),
                    address=row["address"],
                    price=float(row["price"]),
                    property_type=PropertyType[row["property_type"]],
                    status=PropertyStatus[row["status"]]
                )
                property_manager.add_property(property_obj)
                print(f"Added property with ID: {property_obj.property_ID}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"Error parsing properties file: {e}")

    return client_manager, property_manager