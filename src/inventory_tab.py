# """
# Inventory Management Tab
# Handles product management, search, and inventory operations
# """

# from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
#                              QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
#                              QHeaderView, QMessageBox, QDialog, QFormLayout,
#                              QSpinBox, QDoubleSpinBox, QTextEdit, QComboBox,
#                              QGroupBox, QSplitter)
# from PyQt5.QtCore import Qt, pyqtSignal
# from PyQt5.QtGui import QFont, QIcon
# from .currency_utils import format_currency, get_currency_symbol
# # QR Code generation will be handled locally to avoid import issues

# class ProductDialog(QDialog):
#     """Dialog for adding/editing products"""
    
#     def __init__(self, parent=None, product_data=None):
#         super().__init__(parent)
#         self.product_data = product_data
#         self.init_ui()
        
#     def init_ui(self):
#         """Initialize the dialog UI"""
#         self.setWindowTitle("Add Product" if not self.product_data else "Edit Product")
#         self.setModal(True)
#         self.setMinimumWidth(400)
        
#         layout = QVBoxLayout(self)
        
#         # Form layout
#         form_layout = QFormLayout()
        
#         # Barcode field
#         self.barcode_edit = QLineEdit()
#         if self.product_data:
#             self.barcode_edit.setText(self.product_data.get('barcode', ''))
#             self.barcode_edit.setReadOnly(True)
#         form_layout.addRow("Barcode:", self.barcode_edit)
        
#         # Name field
#         self.name_edit = QLineEdit()
#         if self.product_data:
#             self.name_edit.setText(self.product_data.get('name', ''))
#         form_layout.addRow("Name:", self.name_edit)
        
#         # Description field
#         self.description_edit = QTextEdit()
#         self.description_edit.setMaximumHeight(80)
#         if self.product_data:
#             self.description_edit.setText(self.product_data.get('description', ''))
#         form_layout.addRow("Description:", self.description_edit)
        
#         # Category field
#         self.category_edit = QComboBox()
#         self.category_edit.setEditable(True)
#         categories = ["Electronics", "Clothing", "Food", "Books", "Home & Garden", "Sports", "Other"]
#         self.category_edit.addItems(categories)
#         if self.product_data:
#             self.category_edit.setCurrentText(self.product_data.get('category', ''))
#         form_layout.addRow("Category:", self.category_edit)
        
#         # Cost price field
#         self.cost_price_edit = QDoubleSpinBox()
#         self.cost_price_edit.setMaximum(999999.99)
#         self.cost_price_edit.setDecimals(2)
#         self.cost_price_edit.setPrefix(get_currency_symbol())
#         if self.product_data:
#             self.cost_price_edit.setValue(self.product_data.get('cost_price', 0))
#         form_layout.addRow("Cost Price:", self.cost_price_edit)
        
#         # Selling price field
#         self.selling_price_edit = QDoubleSpinBox()
#         self.selling_price_edit.setMaximum(999999.99)
#         self.selling_price_edit.setDecimals(2)
#         self.selling_price_edit.setPrefix(get_currency_symbol())
#         if self.product_data:
#             self.selling_price_edit.setValue(self.product_data.get('selling_price', 0))
#         form_layout.addRow("Selling Price:", self.selling_price_edit)
        
#         # Quantity field
#         self.quantity_edit = QSpinBox()
#         self.quantity_edit.setMaximum(999999)
#         if self.product_data:
#             self.quantity_edit.setValue(self.product_data.get('quantity', 0))
#         form_layout.addRow("Quantity:", self.quantity_edit)
        
#         # Minimum quantity field
#         self.min_quantity_edit = QSpinBox()
#         self.min_quantity_edit.setMaximum(999999)
#         if self.product_data:
#             self.min_quantity_edit.setValue(self.product_data.get('min_quantity', 0))
#         form_layout.addRow("Min Quantity:", self.min_quantity_edit)
        
#         layout.addLayout(form_layout)
        
#         # Buttons
#         button_layout = QHBoxLayout()
        
#         self.save_button = QPushButton("Save")
#         self.save_button.clicked.connect(self.accept)
#         button_layout.addWidget(self.save_button)
        
#         self.cancel_button = QPushButton("Cancel")
#         self.cancel_button.clicked.connect(self.reject)
#         button_layout.addWidget(self.cancel_button)
        
#         layout.addLayout(button_layout)
        
#     def get_product_data(self):
#         """Get the entered product data"""
#         return {
#             'barcode': self.barcode_edit.text().strip(),
#             'name': self.name_edit.text().strip(),
#             'description': self.description_edit.toPlainText().strip(),
#             'category': self.category_edit.currentText().strip(),
#             'cost_price': self.cost_price_edit.value(),
#             'selling_price': self.selling_price_edit.value(),
#             'quantity': self.quantity_edit.value(),
#             'min_quantity': self.min_quantity_edit.value()
#         }

# class InventoryTab(QWidget):
#     """Inventory management tab"""
    
#     def __init__(self, db_manager):
#         super().__init__()
#         self.db_manager = db_manager
#         self.init_ui()
#         self.refresh_data()
        
#     def init_ui(self):
#         """Initialize the user interface"""
#         layout = QVBoxLayout(self)
        
#         # Search and filter section
#         search_group = QGroupBox("Search & Filter")
#         search_layout = QHBoxLayout()
        
#         self.search_edit = QLineEdit()
#         self.search_edit.setPlaceholderText("Search by name, barcode, or category...")
#         self.search_edit.textChanged.connect(self.filter_products)
#         search_layout.addWidget(self.search_edit)
        
#         self.category_filter = QComboBox()
#         self.category_filter.addItem("All Categories")
#         self.category_filter.addItems(["Electronics", "Clothing", "Food", "Books", "Home & Garden", "Sports", "Other"])
#         self.category_filter.currentTextChanged.connect(self.filter_products)
#         search_layout.addWidget(self.category_filter)
        
#         search_group.setLayout(search_layout)
#         layout.addWidget(search_group)
        
#         # Buttons section
#         button_layout = QHBoxLayout()
        
#         self.add_button = QPushButton("➕ Add Product")
#         self.add_button.clicked.connect(self.add_product)
#         button_layout.addWidget(self.add_button)
        
#         self.edit_button = QPushButton("✏️ Edit Product")
#         self.edit_button.clicked.connect(self.edit_product)
#         self.edit_button.setEnabled(False)
#         button_layout.addWidget(self.edit_button)
        
#         self.delete_button = QPushButton("🗑️ Delete Product")
#         self.delete_button.clicked.connect(self.delete_product)
#         self.delete_button.setEnabled(False)
#         button_layout.addWidget(self.delete_button)
        
#         self.refresh_button = QPushButton("🔄 Refresh")
#         self.refresh_button.clicked.connect(self.refresh_data)
#         button_layout.addWidget(self.refresh_button)
        
#         button_layout.addStretch()
        
#         layout.addLayout(button_layout)
        
#         # Products table
#         self.products_table = QTableWidget()
#         self.products_table.setColumnCount(8)
#         self.products_table.setHorizontalHeaderLabels([
#             "ID", "Barcode", "Name", "Category", "Cost Price", "Selling Price", "Quantity", "Status"
#         ])
        
#         # Set table properties
#         header = self.products_table.horizontalHeader()
#         header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
#         header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Barcode
#         header.setSectionResizeMode(2, QHeaderView.Stretch)           # Name
#         header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Category
#         header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Cost Price
#         header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Selling Price
#         header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Quantity
#         header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Status
        
#         self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
#         self.products_table.setAlternatingRowColors(True)
#         self.products_table.itemSelectionChanged.connect(self.on_selection_changed)
        
#         layout.addWidget(self.products_table)
        
#         # Status bar
#         self.status_label = QLabel("Ready")
#         layout.addWidget(self.status_label)
        
#     def refresh_data(self):
#         """Refresh the products table"""
#         try:
#             products = self.db_manager.get_all_products()
#             self.populate_table(products)
#             self.status_label.setText(f"Loaded {len(products)} products")
#         except Exception as e:
#             self.status_label.setText(f"Error loading products: {str(e)}")
    
#     def populate_table(self, products):
#         """Populate the table with products data"""
#         self.products_table.setRowCount(len(products))
        
#         for row, product in enumerate(products):
#             # ID
#             self.products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            
#             # Barcode
#             barcode_item = QTableWidgetItem(product['barcode'] or '')
#             self.products_table.setItem(row, 1, barcode_item)
            
#             # Name
#             self.products_table.setItem(row, 2, QTableWidgetItem(product['name']))
            
#             # Category
#             self.products_table.setItem(row, 3, QTableWidgetItem(product['category'] or ''))
            
#             # Cost Price
#             cost_item = QTableWidgetItem(format_currency(product['cost_price']))
#             cost_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
#             self.products_table.setItem(row, 4, cost_item)
            
#             # Selling Price
#             selling_item = QTableWidgetItem(format_currency(product['selling_price']))
#             selling_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
#             self.products_table.setItem(row, 5, selling_item)
            
#             # Quantity
#             quantity_item = QTableWidgetItem(str(product['quantity']))
#             quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
#             self.products_table.setItem(row, 6, quantity_item)
            
#             # Status
#             status = self.get_status_text(product['quantity'], product['min_quantity'])
#             status_item = QTableWidgetItem(status)
#             status_item.setTextAlignment(Qt.AlignCenter)
            
#             # Color coding for status
#             if "Low Stock" in status:
#                 status_item.setBackground(Qt.yellow)
#             elif "Out of Stock" in status:
#                 status_item.setBackground(Qt.red)
#             elif "In Stock" in status:
#                 status_item.setBackground(Qt.green)
            
#             self.products_table.setItem(row, 7, status_item)
    
#     def get_status_text(self, quantity, min_quantity):
#         """Get status text based on quantity"""
#         if quantity == 0:
#             return "Out of Stock"
#         elif min_quantity > 0 and quantity <= min_quantity:
#             return f"Low Stock ({quantity})"
#         else:
#             return "In Stock"
    
#     def filter_products(self):
#         """Filter products based on search text and category"""
#         search_text = self.search_edit.text().lower()
#         category_filter = self.category_filter.currentText()
        
#         for row in range(self.products_table.rowCount()):
#             name = self.products_table.item(row, 2).text().lower()
#             barcode = self.products_table.item(row, 1).text().lower()
#             category = self.products_table.item(row, 3).text()
            
#             # Check if row matches search criteria
#             matches_search = (search_text in name or 
#                             search_text in barcode or 
#                             search_text in category.lower())
            
#             matches_category = (category_filter == "All Categories" or 
#                               category == category_filter)
            
#             # Show/hide row based on filters
#             self.products_table.setRowHidden(row, not (matches_search and matches_category))
    
#     def on_selection_changed(self):
#         """Handle table selection changes"""
#         has_selection = len(self.products_table.selectedItems()) > 0
#         self.edit_button.setEnabled(has_selection)
#         self.delete_button.setEnabled(has_selection)
    
#     def add_product(self, barcode=None):
#         """Add a new product"""
#         dialog = ProductDialog(self)
#         if barcode:
#             dialog.barcode_edit.setText(barcode)
        
#         if dialog.exec_() == QDialog.Accepted:
#             product_data = dialog.get_product_data()
            
#             # Validate data
#             if not product_data['name']:
#                 QMessageBox.warning(self, "Validation Error", "Product name is required")
#                 return
            
#             if product_data['cost_price'] <= 0 or product_data['selling_price'] <= 0:
#                 QMessageBox.warning(self, "Validation Error", "Prices must be greater than 0")
#                 return
            
#             # Add to database
#             if self.db_manager.add_product(product_data):
#                 self.refresh_data()
#                 QMessageBox.information(self, "Success", "Product added successfully")
#             else:
#                 QMessageBox.warning(self, "Error", "Failed to add product")
    
#     def edit_product(self):
#         """Edit selected product"""
#         current_row = self.products_table.currentRow()
#         if current_row < 0:
#             return
        
#         # Get product data from table
#         product_id = int(self.products_table.item(current_row, 0).text())
#         product_data = {
#             'id': product_id,
#             'barcode': self.products_table.item(current_row, 1).text(),
#             'name': self.products_table.item(current_row, 2).text(),
#             'category': self.products_table.item(current_row, 3).text(),
#             'cost_price': float(self.products_table.item(current_row, 4).text().replace(get_currency_symbol(), '').replace(',', '')),
#             'selling_price': float(self.products_table.item(current_row, 5).text().replace(get_currency_symbol(), '').replace(',', '')),
#             'quantity': int(self.products_table.item(current_row, 6).text()),
#             'min_quantity': 0  # Default value
#         }
        
#         dialog = ProductDialog(self, product_data)
#         if dialog.exec_() == QDialog.Accepted:
#             updated_data = dialog.get_product_data()
#             updated_data['id'] = product_id
            
#             # Update in database
#             if self.db_manager.update_product(updated_data):
#                 self.refresh_data()
#                 QMessageBox.information(self, "Success", "Product updated successfully")
#             else:
#                 QMessageBox.warning(self, "Error", "Failed to update product")
    
#     def delete_product(self):
#         """Delete selected product"""
#         current_row = self.products_table.currentRow()
#         if current_row < 0:
#             return
        
#         product_id = int(self.products_table.item(current_row, 0).text())
#         product_name = self.products_table.item(current_row, 2).text()
        
#         reply = QMessageBox.question(
#             self, "Confirm Delete", 
#             f"Are you sure you want to delete '{product_name}'?",
#             QMessageBox.Yes | QMessageBox.No
#         )
        
#         if reply == QMessageBox.Yes:
#             if self.db_manager.delete_product(product_id):
#                 self.refresh_data()
#                 QMessageBox.information(self, "Success", "Product deleted successfully")
#             else:
#                 QMessageBox.warning(self, "Error", "Failed to delete product")
    
#     def show_product_details(self, product):
#         """Show product details (called from main window)"""
#         # Find the product in the table and select it
#         for row in range(self.products_table.rowCount()):
#             if self.products_table.item(row, 1).text() == product['barcode']:
#                 self.products_table.selectRow(row)
#                 self.products_table.scrollToItem(self.products_table.item(row, 0))
#                 break
    
#     def add_new_product(self, barcode):
#         """Add new product with barcode (called from main window)"""
#         self.add_product(barcode)
    
#     def import_data(self):
#         """Import data from file (placeholder)"""
#         QMessageBox.information(self, "Import", "Import functionality will be implemented here")

"""
Inventory Management Tab
Handles product management, search, and inventory operations
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QDialog, QFormLayout,
                             QSpinBox, QDoubleSpinBox, QTextEdit, QComboBox,
                             QGroupBox, QSplitter, QFrame, QSizePolicy, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon, QPalette, QColor, QPixmap
from .currency_utils import format_currency, get_currency_symbol
# QR Code generation will be handled locally to avoid import issues

class ProductDialog(QDialog):
    """Dialog for adding/editing products"""
    
    def __init__(self, parent=None, product_data=None):
        super().__init__(parent)
        self.product_data = product_data
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        self.setWindowTitle("Add Product" if not self.product_data else "Edit Product")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f7;
            }
            QLabel {
                font-weight: bold;
                color: #2c3e50;
            }
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton#cancelButton {
                background-color: #95a5a6;
            }
            QPushButton#cancelButton:hover {
                background-color: #7f8c8d;
            }
            QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #3498db;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # Barcode field
        self.barcode_edit = QLineEdit()
        self.barcode_edit.setPlaceholderText("Enter product barcode")
        if self.product_data:
            self.barcode_edit.setText(self.product_data.get('barcode', ''))
            self.barcode_edit.setReadOnly(True)
        form_layout.addRow("Barcode:", self.barcode_edit)
        
        # Name field
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter product name")
        if self.product_data:
            self.name_edit.setText(self.product_data.get('name', ''))
        form_layout.addRow("Name:", self.name_edit)
        
        # Description field
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlaceholderText("Enter product description")
        if self.product_data:
            self.description_edit.setText(self.product_data.get('description', ''))
        form_layout.addRow("Description:", self.description_edit)
        
        # Category field
        self.category_edit = QComboBox()
        self.category_edit.setEditable(True)
        categories = ["Electronics", "Clothing", "Food", "Books", "Home & Garden", "Sports", "Other"]
        self.category_edit.addItems(categories)
        self.category_edit.setPlaceholderText("Select or enter category")
        if self.product_data:
            self.category_edit.setCurrentText(self.product_data.get('category', ''))
        form_layout.addRow("Category:", self.category_edit)
        
        # Price row
        price_layout = QHBoxLayout()
        
        # Cost price field
        cost_group = QVBoxLayout()
        cost_label = QLabel("Cost Price:")
        self.cost_price_edit = QDoubleSpinBox()
        self.cost_price_edit.setMaximum(999999.99)
        self.cost_price_edit.setDecimals(2)
        self.cost_price_edit.setPrefix(get_currency_symbol())
        if self.product_data:
            self.cost_price_edit.setValue(self.product_data.get('cost_price', 0))
        cost_group.addWidget(cost_label)
        cost_group.addWidget(self.cost_price_edit)
        price_layout.addLayout(cost_group)
        
        # Selling price field
        selling_group = QVBoxLayout()
        selling_label = QLabel("Selling Price:")
        self.selling_price_edit = QDoubleSpinBox()
        self.selling_price_edit.setMaximum(999999.99)
        self.selling_price_edit.setDecimals(2)
        self.selling_price_edit.setPrefix(get_currency_symbol())
        if self.product_data:
            self.selling_price_edit.setValue(self.product_data.get('selling_price', 0))
        selling_group.addWidget(selling_label)
        selling_group.addWidget(self.selling_price_edit)
        price_layout.addLayout(selling_group)
        
        form_layout.addRow("Pricing:", price_layout)
        
        # Quantity row
        quantity_layout = QHBoxLayout()
        
        # Quantity field
        quantity_group = QVBoxLayout()
        quantity_label = QLabel("Quantity:")
        self.quantity_edit = QSpinBox()
        self.quantity_edit.setMaximum(999999)
        if self.product_data:
            self.quantity_edit.setValue(self.product_data.get('quantity', 0))
        quantity_group.addWidget(quantity_label)
        quantity_group.addWidget(self.quantity_edit)
        quantity_layout.addLayout(quantity_group)
        
        # Minimum quantity field
        min_quantity_group = QVBoxLayout()
        min_quantity_label = QLabel("Min Quantity:")
        self.min_quantity_edit = QSpinBox()
        self.min_quantity_edit.setMaximum(999999)
        if self.product_data:
            self.min_quantity_edit.setValue(self.product_data.get('min_quantity', 0))
        min_quantity_group.addWidget(min_quantity_label)
        min_quantity_group.addWidget(self.min_quantity_edit)
        quantity_layout.addLayout(min_quantity_group)
        
        form_layout.addRow("Inventory:", quantity_layout)
        
        layout.addLayout(form_layout)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        layout.addWidget(separator)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
        self.save_button = QPushButton("Save Product")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
    def get_product_data(self):
        """Get the entered product data"""
        return {
            'barcode': self.barcode_edit.text().strip(),
            'name': self.name_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'category': self.category_edit.currentText().strip(),
            'cost_price': self.cost_price_edit.value(),
            'selling_price': self.selling_price_edit.value(),
            'quantity': self.quantity_edit.value(),
            'min_quantity': self.min_quantity_edit.value()
        }

class InventoryTab(QWidget):
    """Inventory management tab"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.init_ui()
        self.refresh_data()
        
    def init_ui(self):
        """Initialize the user interface"""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # Header section
        header_layout = QHBoxLayout()
        
        title = QLabel("Inventory Management")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #2c3e50;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        self.refresh_button = QPushButton(" Refresh")
        self.refresh_button.setIcon(QIcon.fromTheme("view-refresh"))
        self.refresh_button.clicked.connect(self.refresh_data)
        header_layout.addWidget(self.refresh_button)
        
        main_layout.addLayout(header_layout)
        
        # Search and filter section
        search_group = QGroupBox("Search & Filter")
        search_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #bdc3c7;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #3498db;
            }
        """)
        search_layout = QGridLayout()
        search_layout.setVerticalSpacing(10)
        search_layout.setHorizontalSpacing(15)
        
        search_label = QLabel("Search:")
        search_label.setStyleSheet("font-weight: bold;")
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by name, barcode, or category...")
        self.search_edit.textChanged.connect(self.filter_products)
        self.search_edit.setClearButtonEnabled(True)
        search_layout.addWidget(search_label, 0, 0)
        search_layout.addWidget(self.search_edit, 0, 1)
        
        category_label = QLabel("Category:")
        category_label.setStyleSheet("font-weight: bold;")
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")
        self.category_filter.addItems(["Electronics", "Clothing", "Food", "Books", "Home & Garden", "Sports", "Other"])
        self.category_filter.currentTextChanged.connect(self.filter_products)
        search_layout.addWidget(category_label, 1, 0)
        search_layout.addWidget(self.category_filter, 1, 1)
        
        search_group.setLayout(search_layout)
        main_layout.addWidget(search_group)
        
        # Action buttons section
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.add_button = QPushButton(" Add Product")
        self.add_button.setIcon(QIcon.fromTheme("list-add"))
        self.add_button.clicked.connect(self.add_product)
        self.add_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #219653;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
            QPushButton:disabled {
                background-color: #aab7b8;
            }
        """)
        button_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton(" Edit Product")
        self.edit_button.setIcon(QIcon.fromTheme("document-edit"))
        self.edit_button.clicked.connect(self.edit_product)
        self.edit_button.setEnabled(False)
        self.edit_button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #aab7b8;
            }
        """)
        button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton(" Delete Product")
        self.delete_button.setIcon(QIcon.fromTheme("edit-delete"))
        self.delete_button.clicked.connect(self.delete_product)
        self.delete_button.setEnabled(False)
        self.delete_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
            QPushButton:disabled {
                background-color: #aab7b8;
            }
        """)
        button_layout.addWidget(self.delete_button)
        
        button_layout.addStretch()
        
        # Add import/export buttons
        self.import_button = QPushButton(" Import")
        self.import_button.setIcon(QIcon.fromTheme("document-import"))
        self.import_button.clicked.connect(self.import_data)
        button_layout.addWidget(self.import_button)
        
        self.export_button = QPushButton(" Export")
        self.export_button.setIcon(QIcon.fromTheme("document-export"))
        # self.export_button.clicked.connect(self.export_data)
        button_layout.addWidget(self.export_button)
        
        main_layout.addLayout(button_layout)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(8)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Barcode", "Name", "Category", "Cost Price", "Selling Price", "Quantity", "Status"
        ])
        
        # Set table properties
        self.products_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #d0d0d0;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
                alternate-background-color: #f8f9f9;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 6px;
                border: none;
                font-weight: bold;
            }
            QTableWidget::item:selected {
                background-color: #d6eaf8;
                color: #2c3e50;
            }
        """)
        
        header = self.products_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Barcode
        header.setSectionResizeMode(2, QHeaderView.Stretch)           # Name
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Cost Price
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Selling Price
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Quantity
        header.setSectionResizeMode(7, QHeaderView.ResizeToContents)  # Status
        
        self.products_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setSortingEnabled(True)
        self.products_table.itemSelectionChanged.connect(self.on_selection_changed)
        self.products_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        main_layout.addWidget(self.products_table)
        
        # Status bar
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_frame.setStyleSheet("background-color: #ecf0f1; border-top: 1px solid #bdc3c7;")
        status_layout = QHBoxLayout(status_frame)
        status_layout.setContentsMargins(10, 5, 10, 5)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #7f8c8d;")
        status_layout.addWidget(self.status_label)
        
        status_layout.addStretch()
        
        # Add summary statistics
        self.summary_label = QLabel("")
        self.summary_label.setStyleSheet("color: #7f8c8d;")
        status_layout.addWidget(self.summary_label)
        
        main_layout.addWidget(status_frame)
        
    def refresh_data(self):
        """Refresh the products table"""
        try:
            products = self.db_manager.get_all_products()
            self.populate_table(products)
            self.update_summary(products)
            self.status_label.setText(f"Loaded {len(products)} products")
        except Exception as e:
            self.status_label.setText(f"Error loading products: {str(e)}")
    
    def update_summary(self, products):
        """Update the summary statistics in the status bar"""
        total_products = len(products)
        total_value = sum(p['quantity'] * p['cost_price'] for p in products)
        low_stock = sum(1 for p in products if p['quantity'] > 0 and p['quantity'] <= p.get('min_quantity', 0))
        out_of_stock = sum(1 for p in products if p['quantity'] == 0)
        
        self.summary_label.setText(
            f"Total Value: {format_currency(total_value)} | "
            f"Products: {total_products} | "
            f"Low Stock: {low_stock} | "
            f"Out of Stock: {out_of_stock}"
        )
    
    def populate_table(self, products):
        """Populate the table with products data"""
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            # ID
            id_item = QTableWidgetItem(str(product['id']))
            id_item.setTextAlignment(Qt.AlignCenter)
            self.products_table.setItem(row, 0, id_item)
            
            # Barcode
            barcode_item = QTableWidgetItem(product['barcode'] or 'N/A')
            barcode_item.setTextAlignment(Qt.AlignCenter)
            self.products_table.setItem(row, 1, barcode_item)
            
            # Name
            name_item = QTableWidgetItem(product['name'])
            self.products_table.setItem(row, 2, name_item)
            
            # Category
            category_item = QTableWidgetItem(product['category'] or 'Uncategorized')
            category_item.setTextAlignment(Qt.AlignCenter)
            self.products_table.setItem(row, 3, category_item)
            
            # Cost Price
            cost_item = QTableWidgetItem(format_currency(product['cost_price']))
            cost_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.products_table.setItem(row, 4, cost_item)
            
            # Selling Price
            selling_item = QTableWidgetItem(format_currency(product['selling_price']))
            selling_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.products_table.setItem(row, 5, selling_item)
            
            # Quantity
            quantity_item = QTableWidgetItem(str(product['quantity']))
            quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Color code based on quantity
            min_quantity = product.get('min_quantity', 0)
            if product['quantity'] == 0:
                quantity_item.setBackground(QColor(255, 230, 230))  # Light red for out of stock
            elif min_quantity > 0 and product['quantity'] <= min_quantity:
                quantity_item.setBackground(QColor(255, 255, 230))  # Light yellow for low stock
            
            self.products_table.setItem(row, 6, quantity_item)
            
            # Status
            status = self.get_status_text(product['quantity'], product.get('min_quantity', 0))
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)
            
            # Color coding for status
            if "Low Stock" in status:
                status_item.setBackground(QColor(255, 255, 230))  # Light yellow
                status_item.setForeground(QColor(230, 126, 34))   # Dark orange text
            elif "Out of Stock" in status:
                status_item.setBackground(QColor(255, 230, 230))  # Light red
                status_item.setForeground(QColor(231, 76, 60))    # Dark red text
            elif "In Stock" in status:
                status_item.setBackground(QColor(230, 245, 230))  # Light green
                status_item.setForeground(QColor(39, 174, 96))    # Dark green text
            
            self.products_table.setItem(row, 7, status_item)
    
    def get_status_text(self, quantity, min_quantity):
        """Get status text based on quantity"""
        if quantity == 0:
            return "Out of Stock"
        elif min_quantity > 0 and quantity <= min_quantity:
            return f"Low Stock ({quantity})"
        else:
            return "In Stock"
    
    def filter_products(self):
        """Filter products based on search text and category"""
        search_text = self.search_edit.text().lower()
        category_filter = self.category_filter.currentText()
        
        for row in range(self.products_table.rowCount()):
            name = self.products_table.item(row, 2).text().lower()
            barcode = self.products_table.item(row, 1).text().lower()
            category = self.products_table.item(row, 3).text()
            
            # Check if row matches search criteria
            matches_search = (search_text in name or 
                            search_text in barcode or 
                            search_text in category.lower())
            
            matches_category = (category_filter == "All Categories" or 
                              category == category_filter)
            
            # Show/hide row based on filters
            self.products_table.setRowHidden(row, not (matches_search and matches_category))
        
        # Update status label with filtered count
        visible_count = sum(1 for row in range(self.products_table.rowCount()) 
                          if not self.products_table.isRowHidden(row))
        self.status_label.setText(f"Showing {visible_count} of {self.products_table.rowCount()} products")
    
    def on_selection_changed(self):
        """Handle table selection changes"""
        has_selection = len(self.products_table.selectedItems()) > 0
        self.edit_button.setEnabled(has_selection)
        self.delete_button.setEnabled(has_selection)
    
    def add_product(self, barcode=None):
        """Add a new product"""
        dialog = ProductDialog(self)
        if barcode:
            dialog.barcode_edit.setText(barcode)
        
        if dialog.exec_() == QDialog.Accepted:
            product_data = dialog.get_product_data()
            
            # Validate data
            if not product_data['name']:
                QMessageBox.warning(self, "Validation Error", "Product name is required")
                return
            
            if product_data['cost_price'] <= 0 or product_data['selling_price'] <= 0:
                QMessageBox.warning(self, "Validation Error", "Prices must be greater than 0")
                return
            
            # Add to database
            if self.db_manager.add_product(product_data):
                self.refresh_data()
                QMessageBox.information(self, "Success", "Product added successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to add product")
    
    def edit_product(self):
        """Edit selected product"""
        current_row = self.products_table.currentRow()
        if current_row < 0:
            return
        
        # Get product data from table
        product_id = int(self.products_table.item(current_row, 0).text())
        product_data = {
            'id': product_id,
            'barcode': self.products_table.item(current_row, 1).text(),
            'name': self.products_table.item(current_row, 2).text(),
            'category': self.products_table.item(current_row, 3).text(),
            'cost_price': float(self.products_table.item(current_row, 4).text().replace(get_currency_symbol(), '').replace(',', '')),
            'selling_price': float(self.products_table.item(current_row, 5).text().replace(get_currency_symbol(), '').replace(',', '')),
            'quantity': int(self.products_table.item(current_row, 6).text()),
            'min_quantity': 0  # Default value
        }
        
        dialog = ProductDialog(self, product_data)
        if dialog.exec_() == QDialog.Accepted:
            updated_data = dialog.get_product_data()
            updated_data['id'] = product_id
            
            # Update in database
            if self.db_manager.update_product(updated_data):
                self.refresh_data()
                QMessageBox.information(self, "Success", "Product updated successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to update product")
    
    def delete_product(self):
        """Delete selected product"""
        current_row = self.products_table.currentRow()
        if current_row < 0:
            return
        
        product_id = int(self.products_table.item(current_row, 0).text())
        product_name = self.products_table.item(current_row, 2).text()
        
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            f"Are you sure you want to delete '{product_name}'?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db_manager.delete_product(product_id):
                self.refresh_data()
                QMessageBox.information(self, "Success", "Product deleted successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete product")
    
    def show_product_details(self, product):
        """Show product details (called from main window)"""
        # Find the product in the table and select it
        for row in range(self.products_table.rowCount()):
            if self.products_table.item(row, 1).text() == product['barcode']:
                self.products_table.selectRow(row)
                self.products_table.scrollToItem(self.products_table.item(row, 0))
                break
    
    def add_new_product(self, barcode):
        """Add new product with barcode (called from main window)"""
        self.add_product(barcode)
    
    def import_data(self):
        """Import data from file (placeholder)"""
        QMessageBox.information(self, "Import", "Import functionality will be implemented here")