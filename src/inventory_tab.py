"""
Inventory Management Tab
Handles product management, search, and inventory operations
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QMessageBox, QDialog, QFormLayout,
                             QSpinBox, QDoubleSpinBox, QTextEdit, QComboBox,
                             QGroupBox, QSplitter)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
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
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Barcode field
        self.barcode_edit = QLineEdit()
        if self.product_data:
            self.barcode_edit.setText(self.product_data.get('barcode', ''))
            self.barcode_edit.setReadOnly(True)
        form_layout.addRow("Barcode:", self.barcode_edit)
        
        # Name field
        self.name_edit = QLineEdit()
        if self.product_data:
            self.name_edit.setText(self.product_data.get('name', ''))
        form_layout.addRow("Name:", self.name_edit)
        
        # Description field
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        if self.product_data:
            self.description_edit.setText(self.product_data.get('description', ''))
        form_layout.addRow("Description:", self.description_edit)
        
        # Category field
        self.category_edit = QComboBox()
        self.category_edit.setEditable(True)
        categories = ["Electronics", "Clothing", "Food", "Books", "Home & Garden", "Sports", "Other"]
        self.category_edit.addItems(categories)
        if self.product_data:
            self.category_edit.setCurrentText(self.product_data.get('category', ''))
        form_layout.addRow("Category:", self.category_edit)
        
        # Cost price field
        self.cost_price_edit = QDoubleSpinBox()
        self.cost_price_edit.setMaximum(999999.99)
        self.cost_price_edit.setDecimals(2)
        self.cost_price_edit.setPrefix(get_currency_symbol())
        if self.product_data:
            self.cost_price_edit.setValue(self.product_data.get('cost_price', 0))
        form_layout.addRow("Cost Price:", self.cost_price_edit)
        
        # Selling price field
        self.selling_price_edit = QDoubleSpinBox()
        self.selling_price_edit.setMaximum(999999.99)
        self.selling_price_edit.setDecimals(2)
        self.selling_price_edit.setPrefix(get_currency_symbol())
        if self.product_data:
            self.selling_price_edit.setValue(self.product_data.get('selling_price', 0))
        form_layout.addRow("Selling Price:", self.selling_price_edit)
        
        # Quantity field
        self.quantity_edit = QSpinBox()
        self.quantity_edit.setMaximum(999999)
        if self.product_data:
            self.quantity_edit.setValue(self.product_data.get('quantity', 0))
        form_layout.addRow("Quantity:", self.quantity_edit)
        
        # Minimum quantity field
        self.min_quantity_edit = QSpinBox()
        self.min_quantity_edit.setMaximum(999999)
        if self.product_data:
            self.min_quantity_edit.setValue(self.product_data.get('min_quantity', 0))
        form_layout.addRow("Min Quantity:", self.min_quantity_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
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
        layout = QVBoxLayout(self)
        
        # Search and filter section
        search_group = QGroupBox("Search & Filter")
        search_layout = QHBoxLayout()
        
        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Search by name, barcode, or category...")
        self.search_edit.textChanged.connect(self.filter_products)
        search_layout.addWidget(self.search_edit)
        
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")
        self.category_filter.addItems(["Electronics", "Clothing", "Food", "Books", "Home & Garden", "Sports", "Other"])
        self.category_filter.currentTextChanged.connect(self.filter_products)
        search_layout.addWidget(self.category_filter)
        
        search_group.setLayout(search_layout)
        layout.addWidget(search_group)
        
        # Buttons section
        button_layout = QHBoxLayout()
        
        self.add_button = QPushButton("➕ Add Product")
        self.add_button.clicked.connect(self.add_product)
        button_layout.addWidget(self.add_button)
        
        self.edit_button = QPushButton("✏️ Edit Product")
        self.edit_button.clicked.connect(self.edit_product)
        self.edit_button.setEnabled(False)
        button_layout.addWidget(self.edit_button)
        
        self.delete_button = QPushButton("🗑️ Delete Product")
        self.delete_button.clicked.connect(self.delete_product)
        self.delete_button.setEnabled(False)
        button_layout.addWidget(self.delete_button)
        
        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.clicked.connect(self.refresh_data)
        button_layout.addWidget(self.refresh_button)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Products table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(8)
        self.products_table.setHorizontalHeaderLabels([
            "ID", "Barcode", "Name", "Category", "Cost Price", "Selling Price", "Quantity", "Status"
        ])
        
        # Set table properties
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
        self.products_table.itemSelectionChanged.connect(self.on_selection_changed)
        
        layout.addWidget(self.products_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
    def refresh_data(self):
        """Refresh the products table"""
        try:
            products = self.db_manager.get_all_products()
            self.populate_table(products)
            self.status_label.setText(f"Loaded {len(products)} products")
        except Exception as e:
            self.status_label.setText(f"Error loading products: {str(e)}")
    
    def populate_table(self, products):
        """Populate the table with products data"""
        self.products_table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            # ID
            self.products_table.setItem(row, 0, QTableWidgetItem(str(product['id'])))
            
            # Barcode
            barcode_item = QTableWidgetItem(product['barcode'] or '')
            self.products_table.setItem(row, 1, barcode_item)
            
            # Name
            self.products_table.setItem(row, 2, QTableWidgetItem(product['name']))
            
            # Category
            self.products_table.setItem(row, 3, QTableWidgetItem(product['category'] or ''))
            
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
            self.products_table.setItem(row, 6, quantity_item)
            
            # Status
            status = self.get_status_text(product['quantity'], product['min_quantity'])
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)
            
            # Color coding for status
            if "Low Stock" in status:
                status_item.setBackground(Qt.yellow)
            elif "Out of Stock" in status:
                status_item.setBackground(Qt.red)
            elif "In Stock" in status:
                status_item.setBackground(Qt.green)
            
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
            QMessageBox.Yes | QMessageBox.No
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
