from ..models import Client, Property, PropertyType, PropertyStatus
from ..structures.client_queue import ClientQueue
from ..managers.client_manager import ClientManager
from ..managers.property_manager import PropertyManager
import csv
import os
from typing import Tuple

def load_dataset(data_dir: str, client_filename: str, property_filename: str) -> Tuple[ClientManager, PropertyManager]:
    client_manager = ClientManager()
    property_manager = PropertyManager()

    # 加载客户端数据
    clients_file = os.path.join(data_dir, client_filename)
    print(f"Checking clients file: {clients_file}")
    if not os.path.exists(clients_file):
        print(f"Clients file not found: {clients_file}")
        raise FileNotFoundError(f"Dataset file not found: {clients_file}")
    try:
        with open(clients_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Processing client: client_ID={row['client_ID']}, name={row['name']}, contact_info={row['contact_info']}, property_type={row['property_type']}, budget={row['budget'].strip()}")
                client = Client(
                    client_ID=int(row["client_ID"]),
                    name=row["name"],
                    contact_info=row["contact_info"],
                    budget=float(row["budget"].strip()),
                    property_type=PropertyType[row["property_type"]] if row["property_type"] and row["property_type"] != "None" else None
                )
                client_manager.add_client(client)
                print(f"Added client with ID: {client.client_ID}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"Error parsing clients file: {e}")

    # 加载房产数据
    properties_file = os.path.join(data_dir, property_filename)
    print(f"Checking properties file: {properties_file}")
    if not os.path.exists(properties_file):
        print(f"Properties file not found: {properties_file}")
        raise FileNotFoundError(f"Dataset file not found: {properties_file}")
    try:
        with open(properties_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Processing property: property_ID={row['property_ID']}, address={row['address']}, price={row['price']}, property_type={row['property_type']}, status={row['status']}, owner={row.get('owner', '')}")
                owner = None if not row.get('owner', '').strip() else row['owner']
                property_obj = Property(
                    property_ID=int(row["property_ID"]),
                    address=row["address"],
                    price=float(row["price"]),
                    property_type=PropertyType[row["property_type"]],
                    status=PropertyStatus[row["status"]],
                    owner=owner
                )
                property_manager.add_property(property_obj)
                print(f"Added property with ID: {property_obj.property_ID}")
    except (KeyError, ValueError) as e:
        raise ValueError(f"Error parsing properties file: {e}")

    return client_manager, property_manager