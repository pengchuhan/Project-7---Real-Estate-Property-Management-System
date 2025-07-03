
# Real Estate Property Management System

## Overview

This project is a modern real estate property management system that leverages **AVL trees** for efficient property storage and search, **queues** for client request management, and a **PyQt-based GUI** for interactive operation and visualization. The design prioritizes **data integrity, maintainability, extensibility, and usability**.


## Features

* **Efficient Property Management:**
  Properties are managed using an AVL Tree, guaranteeing O(log n) performance for insertion, deletion, and search.

* **Robust Client Request Handling:**
  Client requests are managed in a FIFO queue, ensuring fair and clear processing.

* **Dynamic Pricing:**
  The system adjusts property prices based on real-time interest (views & inquiries).

* **Advanced Matching:**
  Matches clients to properties using a weighted, multi-criteria scoring algorithm.

* **Clean GUI:**
  A user-friendly PyQt5 interface provides visualization (AVL tree, tables), search, analytics, and real-time feedback.

* **Data Integrity & Validation:**
  Strict checks prevent inconsistent property status or client actions.

* **Complete Unit Testing:**
  High code coverage with edge-case tests ensures reliability.


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
|   |   ├── dialogs.py
│       └── interface.py
├── tests/
│   ├── __init__.py
│   ├── test_models/
|   |   ├── __init__.py
│   │   ├── test_property.py
│   │   └── test_client.py
│   ├── test_structures/
|   |   ├── __init__.py
│   │   |── test_avl_tree_queue.py
|   |   └── test_avl_queue.py
│   |── test_managers/
|   |   ├── __init__.py
│   |   ├── test_property_manager.py
│   |   └── test_client_manager.py
|   └── test_utils/
|       ├── __init__.py
│       └── test_loader.py
├── datasets/
│   ├── real_estate_properties_dataset.csv
│   └── client_requests_dataset.csv
├── main.py
├── README.md
└── requirements.txt
```

## 1. Core Architecture

### 1.1 Data Structures

* **Property (`models/property.py`):**

  * Stores all essential property information and statistics (views, inquiries).
  * Enforces status consistency (e.g., `SOLD` requires owner).

* **Client (`models/client.py`):**

  * Stores client info, budget, property type, and preferences.

* **AVLTree (`structures/avl_tree.py`):**

  * Self-balancing tree for property storage.
  * Efficient add/remove/search by price/ID.

* **ClientQueue (`structures/client_queue.py`):**

  * FIFO queue for managing client requests.

### 1.2 Managers & Decoupling

* **PropertyManager:**

  * All AVLTree operations for properties.
  * Status updates with validation, dynamic pricing, and criteria search.

* **ClientManager:**

  * All queue operations for clients.
  * Smart property matching and atomic transactions.

* **Loose Coupling:**

  * Business logic is encapsulated in managers, not in raw data structures.
  * Promotes modularity, reusability, and testability.

### 1.3 GUI Interface

* **Dialogs (`gui/dialogs.py`):**
  For adding/editing properties and clients with validation.

* **Main Interface (`gui/interface.py`):**
  Tab-based GUI for:

  * Viewing/editing/searching properties and clients
  * AVL tree visualization
  * Data analytics (charts, tables)
  * Real-time logs and interaction


## 2. Key Algorithms

* **AVL Tree Balancing:**
  Automatic left/right/left-right/right-left rotations keep the tree balanced for fast operations.

* **Client–Property Matching:**
  Multi-factor scoring: type, budget, features, location, and property status. Advanced method ranks properties by how well they fit client preferences.

* **Dynamic Pricing:**
  Periodically increases price for hot properties (high views/inquiries), decreases for low demand.

* **Transactional Operations:**
  Buying a property is atomic: checks budget, type, status, and updates all fields together.

* **Data Validation & Robustness:**

  * Adding/removing/updating strictly checks all invariants.
  * Invalid actions (buying unavailable property, budget mismatch) raise clear exceptions.


## 3. GUI & Visualization

* **User-Friendly:**
  Search, edit, add, and remove properties and clients via the GUI.
* **AVL Tree Visualization:**
  Real-time graphical rendering of tree structure.
* **Analytics:**
  Built-in charts (Matplotlib): property type distribution, avg price by type, transaction rates, most viewed properties.


## 4. Testing & Quality

* **Unit Tests:**
  All key methods tested (structures, managers, loaders, etc.)
* **Edge-Case Testing:**
  Duplicate client/property, invalid operations, empty cases.
* **Visualization in Tests:**
  Console/graphical display of tree and queue for inspection.
* **Coverage:**
  High code coverage with all branches covered.


## 5. Usage

### 5.1 Requirements

* Python 3.7+
* PyQt5
* matplotlib

Install dependencies:

```bash
pip install -r requirements.txt
```

### 5.2 Running

* To run with GUI:

  ```bash
  python -m real_estate.gui.interface
  ```
* To run tests:

  ```bash
  python -m unittest discover tests
  ```

### 5.3 Dataset

* Place your property and client CSV files under the `datasets/` directory.
* The app will auto-load on startup.



## 6. Optimization & Future Work

* **Optimized Data Structures:**
  Removed redundancy, all logic flows through AVLTree/Queue and managers.

* **GUI Enhancements:**
  Analytics, visualization, real-time feedback.

* **Planned:**

  * Integration with real estate APIs
  * Smarter ML-based recommendations
  * Email/SMS notification system
  * Advanced reporting and data analysis



## 7. Acknowledgements

Special thanks to open source contributors and PyQt5/matplotlib documentation.

