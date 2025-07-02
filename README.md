# README

## Introduction to the Real Estate Property Management System

### Overview

This project aims to develop a comprehensive real estate property management system designed to efficiently manage and optimize the organization, retrieval, and assignment of properties to clients. The system leverages advanced data structures, specifically AVL Trees for managing property listings and Queues for handling client requests, to ensure balanced and efficient data handling.

### Key Features

1. **Property Management with AVL Trees**
   - **Efficient Storage and Retrieval**: Properties are stored in an AVL Tree, a self-balancing binary search tree, which ensures that operations like insertion, deletion, and searching are performed in logarithmic time.
   - **Balanced Structure**: The AVL Tree maintains balance through rotations, ensuring optimal performance even as the dataset grows.
   - **Property Representation**: Each property is represented by a class that includes attributes such as `property_ID`, `address`, `price`, `property_type`, `status`, and `owner`.

2. **Client Request Management with Queues**
   - **First-Come, First-Served Handling**: Client requests are managed using a Queue data structure, ensuring that requests are processed in the order they are received.
   - **Client Representation**: Each client is represented by a class that includes attributes such as `client_ID`, `name`, `contact_info`, and `budget`.
   - **Request Processing**: The system processes client requests efficiently, matching clients with properties that fit their budget and preferences.

3. **Robust Search and Matching Capabilities**
   - **Search by Criteria**: The system supports searching for properties based on various criteria, including price range, property type, and location.
   - **Matching Properties**: The system can match properties to clients based on their budget and preferences, facilitating efficient property assignments.

4. **Data Consistency and Validation**
   - **Status Management**: The system ensures data consistency by validating property statuses. For example, a property cannot be marked as available if it has an owner, and a sold property must have an owner.
   - **Error Handling**: The system includes robust error handling to manage invalid operations and ensure data integrity.

5. **Dataset Integration**
   - **CSV File Support**: The system includes functionality to load property and client data from CSV files, facilitating easy integration with existing datasets.
   - **Initialization**: The `load_dataset` function initializes the AVL Tree and client request queue with data from the provided CSV files.

## Directory Structure

```
real_estate_project/
├── real_estate/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── property.py
│   │   └── client.py
│   ├── structures/
│   │   ├── __init__.py
│   │   ├── avl_tree.py
│   │   └── client_queue.py
│   ├── managers/
│   │   ├── __init__.py
│   │   ├── property_manager.py
│   │   └── client_manager.py
│   ├── utils/
|   |   ├── __init__.py
│   |   └── loader.py
|   └── gui/
│       └── interface.py
├── tests/
│   ├── __init__.py
│   ├── test_models/
│   │   ├── test_property.py
│   │   └── test_client.py
│   ├── test_structures/
│   │   |── test_avl_tree_queue.py
|   |   └── test_avl_queue.py
│   └── test_managers/
│       ├── test_property_manager.py
│       └── test_client_manager.py
├── datasets/
│   ├── real_estate_properties_dataset.csv
│   └── client_requests_dataset.csv
├── main.py
├── README.md
└── requirements.txt
```


## Part 1 – Building the Software Toolbox

### Task 1: Defining the Data Structure

#### Property Representation
- **Property Class**: The `Property` class is defined in `real_estate/models/property.py`. It contains attributes like `property_ID`, `address`, `price`, `property_type`, `status`, and `owner`. The `property_type` and `status` attributes are implemented using enumerations (`PropertyType` and `PropertyStatus`) to ensure valid values.
- **Utility Methods**: The class includes `__repr__` for string representation, `__eq__` for equality comparison based on `property_ID`, and `__lt__` for less-than comparison, which is useful for AVL Tree operations.

#### Client Representation
- **Client Class**: The `Client` class is defined in `real_estate/models/client.py`. It contains attributes like `client_ID`, `name`, `contact_info`, and `budget`.
- **Utility Methods**: The class includes `__repr__` for string representation.

#### AVL Tree for Property Management
- **AVL Tree Class**: The `AVLTree` class is implemented in `real_estate/structures/avl_tree.py`. It supports basic AVL Tree operations like insertion, deletion, and balancing through rotations.
- **AVL Node Class**: The `AVLNode` class is used to represent each node in the AVL Tree, storing the property and balancing information.

#### Queue for Client Requests
- **Client Queue Class**: The `ClientQueue` class is implemented in `real_estate/structures/client_queue.py`. It manages client requests using a first-come, first-served approach, with methods for enqueueing and dequeueing clients.

### Task 2: Property Management Utilities

#### Adding and Removing Properties
- **Property Manager Class**: The `PropertyManager` class in `real_estate/managers/property_manager.py` provides methods to add and remove properties from the AVL Tree.
- **Updating Property Status**: The `update_status` method allows changing the status of a property while ensuring consistency (e.g., a sold property must have an owner).
- **Searching Properties**: The `search_properties` method allows searching for properties based on criteria like price range, property type, and location.

### Task 3: Client Request Management

#### Managing Client Requests
- **Client Manager Class**: The `ClientManager` class in `real_estate/managers/client_manager.py` provides methods to manage client requests.
- **Adding and Removing Requests**: Methods to add and remove client requests from the queue.
- **Matching Properties**: The `match_properties` method finds properties that match a client's budget.
- **Buying Properties**: The `buy_property` method allows a client to buy a property, updating the property's status and owner, and removing the client from the queue.

### Task 4: Loading the Dataset

#### Dataset Loading
- **Loader Function**: The `load_dataset` function in `real_estate/utils/loader.py` reads CSV files (`client_requests_dataset.csv` and `real_estate_properties_dataset.csv`) and initializes the AVL Tree and client request queue with the given data.
- **File Paths**: The function assumes the datasets are located in the `datasets` directory relative to the project root.

### Testing

#### Unit Tests
- **Test Classes**: Unit tests are implemented in the `tests` directory, covering all the implemented methods.
- **Running Tests**: Tests can be run using the `unittest` framework by executing the test scripts (e.g., `test_avl_tree_queue.py`, `test_client_manager.py`).


### Usage

1. **Install Dependencies**: Ensure all required packages are installed (`pip install -r requirements.txt`).
2. **Load Data**: Run the `load_dataset` function to initialize the AVL Tree and client request queue with data from the CSV files.
3. **Run Program**: Execute the `main.py` script to process client requests and manage properties.

This project provides a structured approach to managing real estate properties and client requests using AVL Trees and queues, ensuring efficient data handling and consistency.