import sys
import os
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QTextEdit, QListWidget, QTabWidget,
    QMenu, QAction, QToolTip, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsTextItem, QGraphicsItem, QMessageBox, QSizePolicy, QHeaderView, QAbstractScrollArea, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QColor, QBrush, QCursor, QFont, QPen
from PyQt5.QtCore import Qt

# matplotlib集成
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from ..managers.client_manager import ClientManager
from ..managers.property_manager import PropertyManager
from ..utils.loader import load_dataset
from ..models import PropertyType, PropertyStatus, Property, Client
from ..structures.avl_tree import AVLTree
from .dialogs import AddClientDialog, AddPropertyDialog

# Tree Node for AVL Tree visualization
class TreeNodeItem(QGraphicsEllipseItem):
    def __init__(self, node, x, y, gui_ref, radius=48):
        super().__init__(x - radius, y - radius, 2 * radius, 2 * radius)
        self.node = node
        self.gui_ref = gui_ref
        self.radius = radius
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable, True)
        # 淡蓝色填充，蓝色边
        self.setBrush(QBrush(QColor("#d0e8ff")))
        self.setPen(QPen(QColor("#d0e8ff"), 3))
        self.setZValue(1)

        prop = node.property

        # 编号（大号居中）
        self.id_text = QGraphicsTextItem(str(prop.property_ID), self)
        self.id_text.setFont(QFont('Segoe UI', 19, QFont.Bold))
        self.id_text.setDefaultTextColor(QColor("#0d233a"))
        # 价格（小号居中，偏下）
        price_str = f"¥{int(prop.price)}"
        self.price_text = QGraphicsTextItem(price_str, self)
        self.price_text.setFont(QFont('Segoe UI', 11, QFont.Normal))
        self.price_text.setDefaultTextColor(QColor("#1565c0"))

        # 居中编号
        id_rect = self.id_text.boundingRect()
        self.id_text.setPos(
            self.rect().center().x() - id_rect.width() / 2,
            self.rect().center().y() - id_rect.height() / 1.9
        )
        # 价格在圈内偏下
        price_rect = self.price_text.boundingRect()
        self.price_text.setPos(
            self.rect().center().x() - price_rect.width() / 2,
            self.rect().center().y() + self.radius/2.2 - price_rect.height() / 2
        )

    def hoverEnterEvent(self, event):
        self.setBrush(QBrush(QColor("#90caf9")))  # highlight
        prop = self.node.property
        info = f"""ID: {prop.property_ID}\nAddress: {prop.address}\nPrice: {prop.price:.2f}\nType: {prop.property_type.name}\nStatus: {prop.status.name}"""
        QToolTip.showText(event.screenPos(), info.strip())

    def hoverLeaveEvent(self, event):
        self.setBrush(QBrush(QColor("#d0e8ff")))

    def contextMenuEvent(self, event):
        menu = QMenu()
        delete_action = QAction("Delete Property", menu)
        delete_action.triggered.connect(self.delete_node)
        menu.addAction(delete_action)
        menu.exec_(event.screenPos().toPoint())

    def delete_node(self):
        prop = self.node.property
        self.gui_ref.log(f"Deleting property {prop.property_ID} from AVL and manager")
        self.gui_ref.property_manager.remove_property(prop.property_ID)
        self.gui_ref.refresh_views()

    # 美化 draw avl node
    def _draw_avl_node(self, node, x, y, offset):
        if not node:
            return
        node_item = TreeNodeItem(node, x, y, self)
        self.tree_scene.addItem(node_item)
        # 连线加粗且美观
        pen = QPen(QColor("#82c0f3"), 4, Qt.SolidLine)
        if node.left:
            self.tree_scene.addLine(x, y + node_item.radius, x - offset, y + 90 - node_item.radius, pen)
            self._draw_avl_node(node.left, x - offset, y + 90, offset / 1.55)
        if node.right:
            self.tree_scene.addLine(x, y + node_item.radius, x + offset, y + 90 - node_item.radius, pen)
            self._draw_avl_node(node.right, x + offset, y + 90, offset / 1.55)

# Main GUI class
class RealEstateGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Real Estate Management System")
        self.setMinimumSize(1400, 900)
        self.client_manager = ClientManager()
        self.property_manager = PropertyManager()
        self.avl_tree = AVLTree()
        self.favorites = set()
        self.apply_styles()
        self._build_menu()
        self._build_tabs()
        self.load_initial_data()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #f5f6fa, stop: 1 #e6e9f0);
                font-family: 'Segoe UI', Arial, sans-serif;
                font-size: 22px;
            }
            QPushButton {
                background-color: #0984e3;
                color: white;
                padding: 10px 18px;
                border-radius: 6px;
                min-width: 110px;
                font-size: 19px;
                margin-right: 12px;
            }
            QPushButton:hover {
                background-color: #74b9ff;
            }
            QLineEdit, QComboBox {
                border: 1px solid #ccc;
                padding: 6px;
                border-radius: 4px;
                font-size: 18px;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f0f4ff;
                font-size: 18px;
            }
            QHeaderView::section {
                background-color: #dde6f7;
                font-weight: bold;
                font-size: 18px;
                border: 1px solid #dee2e6;
                padding: 4px;
            }
            QListWidget {
                font-size: 18px;
                background: #fff;
                border: 1px solid #ccc;
            }
            QToolTip {
                background-color: #ffffff;
                color: #2d3436;
                border: 1px solid #0984e3;
                padding: 6px;
                border-radius: 4px;
                font-size: 18px;
            }
        """)

    def _build_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        file_menu.addAction("Exit", self.close)
        view_menu = menubar.addMenu("View")
        view_menu.addAction("Refresh", self.refresh_views)
        help_menu = menubar.addMenu("Help")
        help_menu.addAction("About", lambda: QMessageBox.information(self, "About", "Real Estate System v1.0"))

    def _build_tabs(self):
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self._build_main_tab()
        self._build_tree_tab()
        self._build_analytics_tab()
    
    def _build_analytics_tab(self):
        tab = QWidget()
        self.analytics_layout = QVBoxLayout(tab)

        # Chart controls
        chart_btns = QHBoxLayout()
        btn_type_dist = QPushButton("Property Type Distribution")
        btn_type_dist.clicked.connect(self.plot_property_type_distribution)
        chart_btns.addWidget(btn_type_dist)

        btn_type_avg = QPushButton("Avg Price by Type")
        btn_type_avg.clicked.connect(self.plot_property_type_avg_price)
        chart_btns.addWidget(btn_type_avg)

        btn_status = QPushButton("Transaction Rate")
        btn_status.clicked.connect(self.plot_transaction_rate)
        chart_btns.addWidget(btn_status)

        btn_hot = QPushButton("Top 10 Most Viewed")
        btn_hot.clicked.connect(self.plot_hot_properties)
        chart_btns.addWidget(btn_hot)

        self.analytics_layout.addLayout(chart_btns)
        self.analytics_chart_area = QVBoxLayout()
        self.analytics_layout.addLayout(self.analytics_chart_area)
        self.tabs.addTab(tab, "Analytics")

    def _clear_analytics_chart_area(self):
        while self.analytics_chart_area.count():
            item = self.analytics_chart_area.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    def plot_property_type_distribution(self):
        props = self.property_manager.search_properties()
        from collections import Counter
        type_counts = Counter([p.property_type.name for p in props])
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(type_counts.values(), labels=type_counts.keys(), autopct='%1.1f%%', startangle=90, colors=["#90caf9", "#b2dfdb", "#ffe082", "#ef9a9a"])
        ax.set_title("Property Type Distribution")
        self._show_chart(fig)

    def plot_property_type_avg_price(self):
        props = self.property_manager.search_properties()
        type_price = {}
        type_count = {}
        for p in props:
            t = p.property_type.name
            type_price[t] = type_price.get(t, 0) + p.price
            type_count[t] = type_count.get(t, 0) + 1
        type_avg = {t: type_price[t]/type_count[t] for t in type_price if type_count[t]}
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(type_avg.keys(), type_avg.values(), color="#64b5f6")
        ax.set_title("Average Price by Type")
        ax.set_ylabel("Average Price")
        self._show_chart(fig)

    def plot_transaction_rate(self):
        props = self.property_manager.search_properties()
        type_total = {}
        type_sold = {}
        for p in props:
            t = p.property_type.name
            type_total[t] = type_total.get(t, 0) + 1
            if p.status == PropertyStatus.SOLD:
                type_sold[t] = type_sold.get(t, 0) + 1
        type_rate = {t: (type_sold.get(t, 0) / type_total[t]) * 100 for t in type_total}
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(type_rate.keys(), type_rate.values(), color="#81c784")
        ax.set_title("Transaction Rate (%) by Type")
        ax.set_ylabel("Transaction Rate (%)")
        ax.set_ylim(0, 100)
        self._show_chart(fig)

    def plot_hot_properties(self):
        props = self.property_manager.search_properties()
        top_props = sorted(props, key=lambda p: p.views, reverse=True)[:10]
        labels = [f"{p.address[:10]}...({p.property_ID})" for p in top_props]
        views = [p.views for p in top_props]
        fig, ax = plt.subplots(figsize=(8, 5))
        bars = ax.barh(labels, views, color="#ffb74d")
        ax.set_title("Top 10 Most Viewed Properties")
        ax.set_xlabel("Views")
        ax.invert_yaxis()
        self._show_chart(fig)

    def _show_chart(self, fig):
        self._clear_analytics_chart_area()
        canvas = FigureCanvas(fig)
        self.analytics_chart_area.addWidget(canvas)
        fig.tight_layout()
        canvas.draw()

    def _build_main_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 客户队列区（在上）
        client_group = QVBoxLayout()
        lbl_client = QLabel("Client Queue")
        lbl_client.setFont(QFont('Segoe UI', 16, QFont.Bold))
        client_group.addWidget(lbl_client, alignment=Qt.AlignLeft)
        self.client_list = QListWidget()
        self.client_list.setMinimumHeight(110)
        self.client_list.itemClicked.connect(self.show_client_details)
        client_group.addWidget(self.client_list)
        btn_del_client = QPushButton("Delete Selected Client")
        btn_del_client.clicked.connect(self.delete_selected_client)
        btn_del_client.setMinimumHeight(70)
        btn_del_client.setStyleSheet("margin-top:10px;margin-bottom:8px;")
        client_group.addWidget(btn_del_client, alignment=Qt.AlignLeft)
        layout.addLayout(client_group, 1)

        # 房产列表区（在下）
        prop_group = QVBoxLayout()
        lbl_prop = QLabel("Property List")
        lbl_prop.setFont(QFont('Segoe UI', 16, QFont.Bold))
        prop_group.addWidget(lbl_prop, alignment=Qt.AlignLeft)
        self.property_table = QTableWidget()
        self.property_table.setColumnCount(7)
        self.property_table.setHorizontalHeaderLabels(["Price", "ID", "Address", "Type", "Status", "Owner", "Actions"])
        self.property_table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.property_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.property_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.property_table.setMinimumHeight(340)
        self.property_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        prop_group.addWidget(self.property_table)
        layout.addLayout(prop_group, 5)

        # Controls
        controls = QHBoxLayout()
        self.input_search = QLineEdit()
        self.input_search.setPlaceholderText("Search by address or price range (e.g. 100000-500000)")
        controls.addWidget(self.input_search)

        btn_search = QPushButton("Search")
        btn_search.clicked.connect(self.search_property)
        controls.addWidget(btn_search)

        btn_match = QPushButton("Match and Buy")
        btn_match.clicked.connect(self.match_and_buy)
        controls.addWidget(btn_match)

        btn_add_prop = QPushButton("Add Property")
        btn_add_prop.clicked.connect(self.add_property)
        controls.addWidget(btn_add_prop)

        btn_add_client = QPushButton("Add Client")
        btn_add_client.clicked.connect(self.add_client)
        controls.addWidget(btn_add_client)

        layout.addLayout(controls)

        # Log panel
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(QLabel("Log Output"))
        layout.addWidget(self.log_output)

        self.tabs.addTab(tab, "Main")

    def _build_tree_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.tree_view = QGraphicsView()
        self.tree_scene = QGraphicsScene()
        self.tree_view.setScene(self.tree_scene)
        btn_refresh = QPushButton("Refresh AVL Tree")
        btn_refresh.clicked.connect(self.refresh_tree_view)
        layout.addWidget(btn_refresh)
        layout.addWidget(self.tree_view)
        self.tabs.addTab(tab, "AVL Tree")

    def refresh_tree_view(self):
        self.tree_scene.clear()
        if not self.avl_tree.root:
            self.tree_scene.addText("Empty Tree")
            return
        width = max(1600, self.tree_view.width())
        height = max(800, self.tree_view.height())
        self._draw_avl_node(self.avl_tree.root, width // 2, 60, width // 6)
        self.tree_view.setSceneRect(0, 0, width, height)
        self.tree_view.centerOn(width // 2, 0)


    def _draw_avl_node(self, node, x, y, offset):
        if not node:
            return
        node_item = TreeNodeItem(node, x, y, self)
        self.tree_scene.addItem(node_item)
        label = QGraphicsTextItem(str(node.property.property_ID))
        label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        label.setPos(x - 15, y - 15)
        self.tree_scene.addItem(label)
        if node.left:
            self.tree_scene.addLine(x, y+20, x - offset, y + 80-20)
            self._draw_avl_node(node.left, x - offset, y + 80, offset / 1.6)
        if node.right:
            self.tree_scene.addLine(x, y+20, x + offset, y + 80-20)
            self._draw_avl_node(node.right, x + offset, y + 80, offset / 1.6)

    def match_and_buy(self):
        if self.client_manager.clients.is_empty():
            self.log("No clients in queue")
            return
        client = self.client_manager.clients.peek()
        try:
            property_obj = self.client_manager.buy_property(client, None, self.property_manager)
            self.client_manager.clients.dequeue()
            self.log(f"Client {client.name} purchased property {property_obj.property_ID} ({property_obj.address})")
        except ValueError as e:
            self.log(f"Match failed for {client.name}: {str(e)}")
            self.client_manager.clients.move_front_to_rear()
        self.refresh_views()

    def log(self, message):
        self.log_output.append(f"[INFO] {message} - {self.get_current_time()}")

    def get_current_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def load_initial_data(self):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        data_dir = os.path.join(base_dir, 'datasets')
        client_file = 'client_requests_dataset.csv'
        property_file = 'real_estate_properties_dataset.csv'
        self.client_manager, self.property_manager = load_dataset(data_dir, client_file, property_file)
        self.refresh_views()

    def refresh_views(self):
        self.client_list.clear()
        for c in self.client_manager.clients.to_list():
            text = f"{c.client_ID} | {c.name} | {c.contact_info} | Budget: {c.budget:.2f} | Type: {c.property_type.name if c.property_type else 'None'}"
            self.client_list.addItem(text)

        props = self.property_manager.search_properties()
        self.populate_property_table(props)

        self.avl_tree = AVLTree()
        for p in props:
            self.avl_tree.insert_key((p.price, p.property_ID), p)
        self.refresh_tree_view()

    def populate_property_table(self, props):
        self.property_table.setRowCount(0)
        self.property_table.setRowCount(len(props))
        # 可选：调整每列宽度，Actions列更宽
        for i in range(6):
            self.property_table.setColumnWidth(i, 180)
        self.property_table.setColumnWidth(6, 400)

        for row, prop in enumerate(props):
            self.property_table.setItem(row, 0, QTableWidgetItem(f"{prop.price:.2f}"))
            self.property_table.setItem(row, 1, QTableWidgetItem(str(prop.property_ID)))
            self.property_table.setItem(row, 2, QTableWidgetItem(prop.address))
            self.property_table.setItem(row, 3, QTableWidgetItem(prop.property_type.name))
            self.property_table.setItem(row, 4, QTableWidgetItem(prop.status.name))
            self.property_table.setItem(row, 5, QTableWidgetItem(prop.owner or "None"))

            actions = QWidget()
            layout = QHBoxLayout()
            btn_fav = QPushButton("Favorite" if prop.property_ID not in self.favorites else "Unfavorite")
            btn_fav.setMinimumWidth(120)
            btn_fav.clicked.connect(lambda _, pid=prop.property_ID: self.toggle_favorite(pid))
            btn_view = QPushButton("Request Viewing")
            btn_view.setMinimumWidth(130)
            btn_view.clicked.connect(lambda _, pid=prop.property_ID: self.request_viewing(pid))
            btn_delete = QPushButton("Delete")
            btn_delete.setMinimumWidth(100)
            btn_delete.setStyleSheet("background-color:#ee5d5d;")
            btn_delete.clicked.connect(lambda _, pid=prop.property_ID: self.delete_property(pid))
            layout.addWidget(btn_fav)
            layout.addWidget(btn_view)
            layout.addWidget(btn_delete)
            layout.setSpacing(16)
            layout.setContentsMargins(0, 0, 0, 0)
            actions.setLayout(layout)
            self.property_table.setCellWidget(row, 6, actions)

    def request_viewing(self, property_id):
        prop = self.property_manager.find_property_by_id(property_id)
        if prop:
            prop.add_view()
            self.log(f"Viewing requested for property {property_id} ({prop.address})")
        else:
            self.log(f"Property {property_id} not found.")

    def toggle_favorite(self, property_id):
        if property_id in self.favorites:
            self.favorites.remove(property_id)
            self.log(f"Unfavorited property {property_id}")
        else:
            self.favorites.add(property_id)
            self.log(f"Favorited property {property_id}")
        self.refresh_views()
    
    def delete_property(self, property_id):
        confirm = QMessageBox.question(self, "Confirm Deletion", f"Delete property {property_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.property_manager.remove_property(property_id)
            self.log(f"Deleted property {property_id}")
            self.refresh_views()

    def delete_selected_client(self):
        selected = self.client_list.currentItem()
        if not selected:
            self.log("No client selected")
            return
        client_id = int(selected.text().split('|')[0].strip())
        confirm = QMessageBox.question(self, "Confirm", f"Delete client {client_id}?", QMessageBox.Yes | QMessageBox.No)
        if confirm == QMessageBox.Yes:
            self.client_manager.remove_client(client_id)
            self.log(f"Deleted client {client_id}")
            self.refresh_views()

    def add_property(self):
        dialog = AddPropertyDialog(self)
        if dialog.exec_():
            prop = dialog.get_data()
            if prop:
                self.property_manager.add_property(prop)
                self.refresh_views()

    def add_client(self):
        dialog = AddClientDialog(self)
        if dialog.exec_():
            client = dialog.get_data()
            if client:
                self.client_manager.add_client(client)
                self.refresh_views()

    def show_client_details(self, item):
        client_id = int(item.text().split('|')[0].strip())
        client = self.client_manager.find_client_by_id(client_id)
        if client:
            QToolTip.showText(self.client_list.mapToGlobal(self.client_list.pos()),
                              f"Client: {client.name}\nContact: {client.contact_info}\nBudget: {client.budget:.2f}\nType: {client.property_type.name if client.property_type else 'None'}")

    def show_property_details(self, item):
        row = self.property_table.currentRow()
        prop_id = int(self.property_table.item(row, 1).text())
        prop = self.property_manager.find_property_by_id(prop_id)
        if prop:
            QToolTip.showText(self.property_table.mapToGlobal(self.property_table.pos()),
                              f"Property ID: {prop.property_ID}\nAddress: {prop.address}\nPrice: {prop.price:.2f}\nType: {prop.property_type.name}\nStatus: {prop.status.name}\nOwner: {prop.owner or 'None'}")

    def analyze_market(self):
        props = self.property_manager.search_properties()
        if not props:
            self.log("No data to analyze")
            return
        avg = sum(p.price for p in props) / len(props)
        counts = {}
        for p in props:
            counts[p.property_type.name] = counts.get(p.property_type.name, 0) + 1
        self.log(f"Avg Price: {avg:.2f}, Distribution: {counts}")

    def search_property(self):
        query = self.input_search.text().strip()
        results = []
        if '-' in query:
            try:
                low, high = map(float, query.split('-'))
                results = self.property_manager.search_properties(price_range=(low, high))
            except:
                self.log("Invalid price range")
        else:
            results = [p for p in self.property_manager.search_properties() if query in p.address]
        self.populate_property_table(results)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealEstateGUI()
    window.show()
    sys.exit(app.exec())
