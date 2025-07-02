# dialogs.py

from PyQt5.QtWidgets import (
    QDialog, QLineEdit, QFormLayout, QComboBox,
    QDialogButtonBox, QMessageBox
)
from ..models import PropertyType, PropertyStatus, Property, Client

class AddPropertyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Property")
        self.setFixedSize(400, 300)
        layout = QFormLayout()

        self.id_input = QLineEdit()
        self.address_input = QLineEdit()
        self.price_input = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems([pt.name for pt in PropertyType])
        self.status_combo = QComboBox()
        self.status_combo.addItems([ps.name for ps in PropertyStatus])
        self.owner_input = QLineEdit()
        self.owner_input.setPlaceholderText("Optional")

        layout.addRow("Property ID:", self.id_input)
        layout.addRow("Address:", self.address_input)
        layout.addRow("Price:", self.price_input)
        layout.addRow("Type:", self.type_combo)
        layout.addRow("Status:", self.status_combo)
        layout.addRow("Owner:", self.owner_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        try:
            property_id = int(self.id_input.text())
            address = self.address_input.text().strip()
            price = float(self.price_input.text())
            property_type = PropertyType[self.type_combo.currentText()]
            status = PropertyStatus[self.status_combo.currentText()]
            owner = self.owner_input.text().strip() or None
            return Property(property_id, address, price, property_type, status, owner)
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input: {e}")
            return None

class AddClientDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Client")
        self.setFixedSize(400, 250)
        layout = QFormLayout()

        self.id_input = QLineEdit()
        self.name_input = QLineEdit()
        self.contact_input = QLineEdit()
        self.budget_input = QLineEdit()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["None"] + [pt.name for pt in PropertyType])

        layout.addRow("Client ID:", self.id_input)
        layout.addRow("Name:", self.name_input)
        layout.addRow("Contact Info:", self.contact_input)
        layout.addRow("Budget:", self.budget_input)
        layout.addRow("Preferred Type:", self.type_combo)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_data(self):
        try:
            client_id = int(self.id_input.text())
            name = self.name_input.text().strip()
            contact = self.contact_input.text().strip()
            budget = float(self.budget_input.text())
            property_type = (
                PropertyType[self.type_combo.currentText()]
                if self.type_combo.currentText() != "None"
                else None
            )
            return Client(client_id, name, contact, budget, property_type)
        except ValueError as e:
            QMessageBox.critical(self, "Input Error", f"Invalid input: {e}")
            return None
