# """
# Sales Tab
# Handles sales transactions and sales history
# """

# from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
#                               QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
#                               QHeaderView, QMessageBox, QDialog, QFormLayout,
#                               QSpinBox, QDoubleSpinBox, QComboBox, QGroupBox,
#                               QDateEdit, QTextEdit)
# from PyQt5.QtCore import Qt, QDate
# from PyQt5.QtGui import QFont
# from datetime import datetime, timedelta
# from .currency_utils import format_currency, get_currency_symbol

# class SaleDialog(QDialog):
#     """Dialog for recording a sale"""
    
#     def __init__(self, parent=None, db_manager=None):
#         super().__init__(parent)
#         self.db_manager = db_manager
#         self.selected_product = None
#         self.init_ui()
        
#     def init_ui(self):
#         """Initialize the dialog UI"""
#         self.setWindowTitle("Record Sale")
#         self.setModal(True)
#         self.setMinimumWidth(400)
        
#         layout = QVBoxLayout(self)
        
#         # Product selection section
#         product_group = QGroupBox("Product Selection")
#         product_layout = QVBoxLayout()
        
#         # Barcode input
#         barcode_layout = QHBoxLayout()
#         self.barcode_edit = QLineEdit()
#         self.barcode_edit.setPlaceholderText("Enter barcode or scan...")
#         self.barcode_edit.returnPressed.connect(self.search_product)
#         barcode_layout.addWidget(QLabel("Barcode:"))
#         barcode_layout.addWidget(self.barcode_edit)
        
#         self.search_button = QPushButton("Search")
#         self.search_button.clicked.connect(self.search_product)
#         barcode_layout.addWidget(self.search_button)
#         product_layout.addLayout(barcode_layout)
        
#         # Product info display
#         self.product_info_label = QLabel("No product selected")
#         self.product_info_label.setStyleSheet("padding: 10px; border: 1px solid gray; background-color: #f0f0f0;")
#         product_layout.addWidget(self.product_info_label)
        
#         product_group.setLayout(product_layout)
#         layout.addWidget(product_group)
        
#         # Sale details section
#         sale_group = QGroupBox("Sale Details")
#         sale_layout = QFormLayout()
        
#         # Quantity
#         self.quantity_edit = QSpinBox()
#         self.quantity_edit.setMinimum(1)
#         self.quantity_edit.setMaximum(999999)
#         self.quantity_edit.valueChanged.connect(self.calculate_total)
#         sale_layout.addRow("Quantity:", self.quantity_edit)
        
#         # Unit price
#         self.unit_price_edit = QDoubleSpinBox()
#         self.unit_price_edit.setMaximum(999999.99)
#         self.unit_price_edit.setDecimals(2)
#         self.unit_price_edit.setPrefix(get_currency_symbol())
#         self.unit_price_edit.valueChanged.connect(self.calculate_total)
#         sale_layout.addRow("Unit Price:", self.unit_price_edit)
        
#         # Total price
#         self.total_price_label = QLabel(f"{get_currency_symbol()}0.00")
#         self.total_price_label.setStyleSheet("font-weight: bold; font-size: 14px; color: green;")
#         sale_layout.addRow("Total Price:", self.total_price_label)
        
#         # Notes
#         self.notes_edit = QTextEdit()
#         self.notes_edit.setMaximumHeight(60)
#         sale_layout.addRow("Notes:", self.notes_edit)
        
#         sale_group.setLayout(sale_layout)
#         layout.addWidget(sale_group)
        
#         # Buttons
#         button_layout = QHBoxLayout()
        
#         self.save_button = QPushButton("Record Sale")
#         self.save_button.clicked.connect(self.accept)
#         self.save_button.setEnabled(False)
#         button_layout.addWidget(self.save_button)
        
#         self.cancel_button = QPushButton("Cancel")
#         self.cancel_button.clicked.connect(self.reject)
#         button_layout.addWidget(self.cancel_button)
        
#         layout.addLayout(button_layout)
        
#     def search_product(self):
#         """Search for product by barcode"""
#         barcode = self.barcode_edit.text().strip()
#         if not barcode:
#             QMessageBox.warning(self, "Input Error", "Please enter a barcode")
#             return
        
#         product = self.db_manager.get_product_by_barcode(barcode)
#         if product:
#             self.selected_product = product
#             self.display_product_info(product)
#             self.unit_price_edit.setValue(product['selling_price'])
#             self.quantity_edit.setMaximum(product['quantity'])
#             self.save_button.setEnabled(True)
#         else:
#             QMessageBox.warning(self, "Product Not Found", f"No product found with barcode: {barcode}")
#             self.selected_product = None
#             self.product_info_label.setText("No product selected")
#             self.save_button.setEnabled(False)
    
#     def display_product_info(self, product):
#         """Display product information"""
#         info_text = f"""
#         <b>Product:</b> {product['name']}<br>
#         <b>Category:</b> {product['category'] or 'N/A'}<br>
#         <b>Available:</b> {product['quantity']} units<br>
#         <b>Cost Price:</b> {format_currency(product['cost_price'])}<br>
#         <b>Selling Price:</b> {format_currency(product['selling_price'])}
#         """
#         self.product_info_label.setText(info_text)
    
#     def calculate_total(self):
#         """Calculate total price"""
#         quantity = self.quantity_edit.value()
#         unit_price = self.unit_price_edit.value()
#         total = quantity * unit_price
#         self.total_price_label.setText(format_currency(total))
    
#     def get_sale_data(self):
#         """Get the sale data"""
#         return {
#             'product_id': self.selected_product['id'],
#             'quantity': self.quantity_edit.value(),
#             'unit_price': self.unit_price_edit.value(),
#             'notes': self.notes_edit.toPlainText().strip()
#         }

# class SalesTab(QWidget):
#     """Sales management tab"""
    
#     def __init__(self, db_manager):
#         super().__init__()
#         self.db_manager = db_manager
#         self.init_ui()
#         self.refresh_data()
        
#     def init_ui(self):
#         """Initialize the user interface"""
#         layout = QVBoxLayout(self)
        
#         # Quick sale section
#         quick_sale_group = QGroupBox("Quick Sale")
#         quick_sale_layout = QHBoxLayout()
        
#         self.new_sale_button = QPushButton("💰 New Sale")
#         self.new_sale_button.clicked.connect(self.new_sale)
#         quick_sale_layout.addWidget(self.new_sale_button)
        
#         quick_sale_layout.addStretch()
        
#         quick_sale_group.setLayout(quick_sale_layout)
#         layout.addWidget(quick_sale_group)
        
#         # Sales history section
#         history_group = QGroupBox("Sales History")
#         history_layout = QVBoxLayout()
        
#         # Filter controls
#         filter_layout = QHBoxLayout()
        
#         filter_layout.addWidget(QLabel("Date Range:"))
        
#         self.start_date_edit = QDateEdit()
#         self.start_date_edit.setDate(QDate.currentDate().addDays(-365))  # Show last year by default
#         self.start_date_edit.dateChanged.connect(self.refresh_data)
#         filter_layout.addWidget(self.start_date_edit)
        
#         filter_layout.addWidget(QLabel("to"))
        
#         self.end_date_edit = QDateEdit()
#         self.end_date_edit.setDate(QDate.currentDate().addDays(1))  # Include today
#         self.end_date_edit.dateChanged.connect(self.refresh_data)
#         filter_layout.addWidget(self.end_date_edit)
        
#         self.refresh_button = QPushButton("🔄 Refresh")
#         self.refresh_button.clicked.connect(self.refresh_data)
#         filter_layout.addWidget(self.refresh_button)
        
#         # Add "Show All" button
#         self.show_all_button = QPushButton("📊 Show All Sales")
#         self.show_all_button.clicked.connect(self.show_all_sales)
#         filter_layout.addWidget(self.show_all_button)
        
#         filter_layout.addStretch()
        
#         history_layout.addLayout(filter_layout)
        
#         # Sales table
#         self.sales_table = QTableWidget()
#         self.sales_table.setColumnCount(7)
#         self.sales_table.setHorizontalHeaderLabels([
#             "Date", "Product", "Quantity", "Unit Price", "Total Price", "Profit", "Notes"
#         ])
        
#         # Set table properties
#         header = self.sales_table.horizontalHeader()
#         header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Date
#         header.setSectionResizeMode(1, QHeaderView.Stretch)           # Product
#         header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Quantity
#         header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Unit Price
#         header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Total Price
#         header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Profit
#         header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Notes
        
#         self.sales_table.setAlternatingRowColors(True)
#         self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        
#         history_layout.addWidget(self.sales_table)
        
#         # Summary section
#         summary_layout = QHBoxLayout()
        
#         self.total_sales_label = QLabel(f"Total Sales: {get_currency_symbol()}0.00")
#         self.total_sales_label.setStyleSheet("font-weight: bold; font-size: 12px; color: blue;")
#         summary_layout.addWidget(self.total_sales_label)
        
#         self.total_profit_label = QLabel(f"Total Profit: {get_currency_symbol()}0.00")
#         self.total_profit_label.setStyleSheet("font-weight: bold; font-size: 12px; color: green;")
#         summary_layout.addWidget(self.total_profit_label)
        
#         self.total_items_label = QLabel("Total Items: 0")
#         self.total_items_label.setStyleSheet("font-weight: bold; font-size: 12px; color: orange;")
#         summary_layout.addWidget(self.total_items_label)
        
#         summary_layout.addStretch()
        
#         history_layout.addLayout(summary_layout)
        
#         history_group.setLayout(history_layout)
#         layout.addWidget(history_group)
        
#         # Status bar
#         self.status_label = QLabel("Ready")
#         layout.addWidget(self.status_label)
        
#     def refresh_data(self):
#         """Refresh the sales data"""
#         try:
#             start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
#             end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
            
#             print(f"🔍 Refreshing sales data: {start_date} to {end_date}")
#             sales_data = self.db_manager.get_sales_data(start_date, end_date)
#             print(f"📊 Retrieved {len(sales_data)} sales records")
            
#             self.populate_table(sales_data)
#             self.update_summary(sales_data)
#             self.status_label.setText(f"Loaded {len(sales_data)} sales records")
#         except Exception as e:
#             print(f"❌ Error in refresh_data: {e}")
#             self.status_label.setText(f"Error loading sales data: {str(e)}")
    
#     def show_all_sales(self):
#         """Show all sales without date filtering"""
#         try:
#             sales_data = self.db_manager.get_sales_data()  # No date filter
#             self.populate_table(sales_data)
#             self.update_summary(sales_data)
#             self.status_label.setText(f"Loaded {len(sales_data)} sales records (All Time)")
#         except Exception as e:
#             self.status_label.setText(f"Error loading all sales: {str(e)}")
    
#     def populate_table(self, sales_data):
#         """Populate the sales table"""
#         self.sales_table.setRowCount(len(sales_data))
        
#         for row, sale in enumerate(sales_data):
#             # Date
#             date_str = sale['sale_date'][:10] if sale['sale_date'] else 'N/A'
#             self.sales_table.setItem(row, 0, QTableWidgetItem(date_str))
            
#             # Product name
#             self.sales_table.setItem(row, 1, QTableWidgetItem(sale['product_name']))
            
#             # Quantity
#             quantity_item = QTableWidgetItem(str(sale['quantity']))
#             quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
#             self.sales_table.setItem(row, 2, quantity_item)
            
#             # Unit price
#             unit_price_item = QTableWidgetItem(format_currency(sale['unit_price']))
#             unit_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
#             self.sales_table.setItem(row, 3, unit_price_item)
            
#             # Total price
#             total_price_item = QTableWidgetItem(format_currency(sale['total_price']))
#             total_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
#             self.sales_table.setItem(row, 4, total_price_item)
            
#             # Profit
#             profit_item = QTableWidgetItem(format_currency(sale['profit']))
#             profit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
#             # Color code profit
#             if sale['profit'] > 0:
#                 profit_item.setBackground(Qt.green)
#             elif sale['profit'] < 0:
#                 profit_item.setBackground(Qt.red)
            
#             self.sales_table.setItem(row, 5, profit_item)
            
#             # Notes (placeholder for future enhancement)
#             self.sales_table.setItem(row, 6, QTableWidgetItem(""))
    
#     def update_summary(self, sales_data):
#         """Update summary information"""
#         total_sales = sum(sale['total_price'] for sale in sales_data)
#         total_profit = sum(sale['profit'] for sale in sales_data)
#         total_items = sum(sale['quantity'] for sale in sales_data)
        
#         self.total_sales_label.setText(f"Total Sales: {format_currency(total_sales)}")
#         self.total_profit_label.setText(f"Total Profit: {format_currency(total_profit)}")
#         self.total_items_label.setText(f"Total Items: {total_items}")
    
#     def new_sale(self):
#         """Open new sale dialog"""
#         dialog = SaleDialog(self, self.db_manager)
#         if dialog.exec_() == QDialog.Accepted:
#             sale_data = dialog.get_sale_data()
            
#             # Record the sale
#             if self.db_manager.add_sale(
#                 sale_data['product_id'],
#                 sale_data['quantity'],
#                 sale_data['unit_price']
#             ):
#                 # Force refresh to show new sale immediately
#                 self.show_all_sales()  # Show all sales including the new one
#                 QMessageBox.information(self, "Success", "Sale recorded successfully")
#             else:
#                 QMessageBox.warning(self, "Error", "Failed to record sale")



"""
Sales Tab
Handles sales transactions and sales history
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                              QHeaderView, QMessageBox, QDialog, QFormLayout,
                              QSpinBox, QDoubleSpinBox, QComboBox, QGroupBox,
                              QDateEdit, QTextEdit, QFrame, QSizePolicy, QGridLayout)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QIcon, QColor, QPalette
from datetime import datetime, timedelta
from .currency_utils import format_currency, get_currency_symbol

class SaleDialog(QDialog):
    """Dialog for recording a sale"""
    
    def __init__(self, parent=None, db_manager=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.selected_product = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the dialog UI"""
        self.setWindowTitle("Record Sale")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f7;
            }
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
            QPushButton:disabled {
                background-color: #aab7b8;
            }
            QPushButton#searchButton {
                background-color: #2ecc71;
            }
            QPushButton#searchButton:hover {
                background-color: #27ae60;
            }
            QPushButton#cancelButton {
                background-color: #95a5a6;
            }
            QPushButton#cancelButton:hover {
                background-color: #7f8c8d;
            }
            QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
                padding: 6px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
                border: 2px solid #3498db;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Product selection section
        product_group = QGroupBox("Product Selection")
        product_layout = QVBoxLayout()
        product_layout.setSpacing(10)
        
        # Barcode input
        barcode_layout = QHBoxLayout()
        barcode_label = QLabel("Barcode:")
        self.barcode_edit = QLineEdit()
        self.barcode_edit.setPlaceholderText("Enter barcode or scan...")
        self.barcode_edit.returnPressed.connect(self.search_product)
        barcode_layout.addWidget(barcode_label)
        barcode_layout.addWidget(self.barcode_edit)
        
        self.search_button = QPushButton(" Search")
        self.search_button.setObjectName("searchButton")
        self.search_button.setIcon(QIcon.fromTheme("system-search"))
        self.search_button.clicked.connect(self.search_product)
        barcode_layout.addWidget(self.search_button)
        product_layout.addLayout(barcode_layout)
        
        # Product info display
        self.product_info_label = QLabel("No product selected")
        self.product_info_label.setStyleSheet("""
            QLabel {
                padding: 12px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ecf0f1;
                color: #2c3e50;
            }
        """)
        self.product_info_label.setWordWrap(True)
        self.product_info_label.setMinimumHeight(80)
        product_layout.addWidget(self.product_info_label)
        
        product_group.setLayout(product_layout)
        layout.addWidget(product_group)
        
        # Sale details section
        sale_group = QGroupBox("Sale Details")
        sale_layout = QFormLayout()
        sale_layout.setSpacing(12)
        
        # Quantity
        self.quantity_edit = QSpinBox()
        self.quantity_edit.setMinimum(1)
        self.quantity_edit.setMaximum(999999)
        self.quantity_edit.valueChanged.connect(self.calculate_total)
        sale_layout.addRow("Quantity:", self.quantity_edit)
        
        # Unit price
        self.unit_price_edit = QDoubleSpinBox()
        self.unit_price_edit.setMaximum(999999.99)
        self.unit_price_edit.setDecimals(2)
        self.unit_price_edit.setPrefix(get_currency_symbol())
        self.unit_price_edit.valueChanged.connect(self.calculate_total)
        sale_layout.addRow("Unit Price:", self.unit_price_edit)
        
        # Total price
        total_layout = QHBoxLayout()
        total_label = QLabel("Total Price:")
        self.total_price_label = QLabel(f"{get_currency_symbol()}0.00")
        self.total_price_label.setStyleSheet("""
            QLabel {
                font-weight: bold; 
                font-size: 16px; 
                color: #27ae60;
                padding: 5px;
                background-color: #eafaf1;
                border-radius: 4px;
            }
        """)
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_price_label)
        total_layout.addStretch()
        sale_layout.addRow(total_layout)
        
        # Notes
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        self.notes_edit.setPlaceholderText("Add any notes about this sale...")
        sale_layout.addRow("Notes:", self.notes_edit)
        
        sale_group.setLayout(sale_layout)
        layout.addWidget(sale_group)
        
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
        
        self.save_button = QPushButton(" Record Sale")
        self.save_button.setIcon(QIcon.fromTheme("dialog-ok-apply"))
        self.save_button.clicked.connect(self.accept)
        self.save_button.setEnabled(False)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        
    def search_product(self):
        """Search for product by barcode"""
        barcode = self.barcode_edit.text().strip()
        if not barcode:
            QMessageBox.warning(self, "Input Error", "Please enter a barcode")
            return
        
        product = self.db_manager.get_product_by_barcode(barcode)
        if product:
            self.selected_product = product
            self.display_product_info(product)
            self.unit_price_edit.setValue(product['selling_price'])
            self.quantity_edit.setMaximum(product['quantity'])
            self.save_button.setEnabled(True)
            
            # Auto-focus on quantity field for faster input
            self.quantity_edit.selectAll()
            self.quantity_edit.setFocus()
        else:
            QMessageBox.warning(self, "Product Not Found", f"No product found with barcode: {barcode}")
            self.selected_product = None
            self.product_info_label.setText("No product selected")
            self.save_button.setEnabled(False)
    
    def display_product_info(self, product):
        """Display product information"""
        stock_status = "In Stock"
        stock_style = "color: #27ae60;"
        if product['quantity'] == 0:
            stock_status = "Out of Stock"
            stock_style = "color: #e74c3c;"
        elif product.get('min_quantity', 0) > 0 and product['quantity'] <= product['min_quantity']:
            stock_status = f"Low Stock ({product['quantity']})"
            stock_style = "color: #f39c12;"
        
        info_text = f"""
        <div style="line-height: 1.4;">
            <b style="font-size: 14px;">{product['name']}</b><br>
            <span style="color: #7f8c8d;">{product['category'] or 'Uncategorized'}</span><br>
            <span style="{stock_style}"><b>{stock_status}</b></span> | 
            <span>Cost: {format_currency(product['cost_price'])}</span> | 
            <span>Price: {format_currency(product['selling_price'])}</span>
        </div>
        """
        self.product_info_label.setText(info_text)
    
    def calculate_total(self):
        """Calculate total price"""
        quantity = self.quantity_edit.value()
        unit_price = self.unit_price_edit.value()
        total = quantity * unit_price
        self.total_price_label.setText(format_currency(total))
    
    def get_sale_data(self):
        """Get the sale data"""
        return {
            'product_id': self.selected_product['id'],
            'quantity': self.quantity_edit.value(),
            'unit_price': self.unit_price_edit.value(),
            'notes': self.notes_edit.toPlainText().strip()
        }

class SalesTab(QWidget):
    """Sales management tab"""
    
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
        
        title = QLabel("Sales Management")
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
        
        # Quick sale section
        quick_sale_group = QGroupBox("Quick Actions")
        quick_sale_group.setStyleSheet("""
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
        quick_sale_layout = QHBoxLayout()
        
        self.new_sale_button = QPushButton(" New Sale")
        self.new_sale_button.setIcon(QIcon.fromTheme("list-add"))
        self.new_sale_button.clicked.connect(self.new_sale)
        self.new_sale_button.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #219653;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        quick_sale_layout.addWidget(self.new_sale_button)
        
        quick_sale_layout.addStretch()
        
        quick_sale_group.setLayout(quick_sale_layout)
        main_layout.addWidget(quick_sale_group)
        
        # Sales history section
        history_group = QGroupBox("Sales History")
        history_group.setStyleSheet(quick_sale_group.styleSheet())
        history_layout = QVBoxLayout()
        history_layout.setSpacing(10)
        
        # Filter controls
        filter_group = QGroupBox("Filter Options")
        filter_group.setStyleSheet("""
            QGroupBox {
                font-weight: normal;
                border: 1px solid #d0d0d0;
                border-radius: 4px;
                margin-top: 0px;
                padding-top: 10px;
                background-color: #f8f9f9;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #7f8c8d;
            }
        """)
        filter_layout = QGridLayout()
        filter_layout.setVerticalSpacing(8)
        filter_layout.setHorizontalSpacing(15)
        
        # Date range filter
        filter_layout.addWidget(QLabel("Date Range:"), 0, 0)
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-30))  # Show last month by default
        self.start_date_edit.setCalendarPopup(True)
        self.start_date_edit.dateChanged.connect(self.refresh_data)
        filter_layout.addWidget(self.start_date_edit, 0, 1)
        
        filter_layout.addWidget(QLabel("to"), 0, 2)
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate())
        self.end_date_edit.setCalendarPopup(True)
        self.end_date_edit.dateChanged.connect(self.refresh_data)
        filter_layout.addWidget(self.end_date_edit, 0, 3)
        
        # Quick date range buttons
        quick_dates_layout = QHBoxLayout()
        
        today_btn = QPushButton("Today")
        today_btn.clicked.connect(lambda: self.set_date_range(0, 0))
        quick_dates_layout.addWidget(today_btn)
        
        week_btn = QPushButton("This Week")
        week_btn.clicked.connect(lambda: self.set_date_range(-7, 0))
        quick_dates_layout.addWidget(week_btn)
        
        month_btn = QPushButton("This Month")
        month_btn.clicked.connect(lambda: self.set_date_range(-30, 0))
        quick_dates_layout.addWidget(month_btn)
        
        quick_dates_layout.addStretch()
        filter_layout.addLayout(quick_dates_layout, 1, 0, 1, 4)
        
        filter_group.setLayout(filter_layout)
        history_layout.addWidget(filter_group)
        
        # Sales table
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(7)
        self.sales_table.setHorizontalHeaderLabels([
            "Date", "Product", "Quantity", "Unit Price", "Total Price", "Profit", "Notes"
        ])
        
        # Set table properties
        self.sales_table.setStyleSheet("""
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
        
        header = self.sales_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(1, QHeaderView.Stretch)           # Product
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Quantity
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Unit Price
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Total Price
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Profit
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)  # Notes
        
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.sales_table.setSortingEnabled(True)
        self.sales_table.setEditTriggers(QTableWidget.NoEditTriggers)
        
        history_layout.addWidget(self.sales_table)
        
        # Summary section
        summary_frame = QFrame()
        summary_frame.setStyleSheet("""
            QFrame {
                background-color: #ecf0f1;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                padding: 5px;
            }
        """)
        summary_layout = QHBoxLayout(summary_frame)
        
        self.total_sales_label = QLabel(f"Total Sales: {get_currency_symbol()}0.00")
        self.total_sales_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #2980b9;")
        summary_layout.addWidget(self.total_sales_label)
        
        self.total_profit_label = QLabel(f"Total Profit: {get_currency_symbol()}0.00")
        self.total_profit_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #27ae60;")
        summary_layout.addWidget(self.total_profit_label)
        
        self.total_items_label = QLabel("Total Items: 0")
        self.total_items_label.setStyleSheet("font-weight: bold; font-size: 12px; color: #f39c12;")
        summary_layout.addWidget(self.total_items_label)
        
        summary_layout.addStretch()
        
        # Add "Show All" button
        self.show_all_button = QPushButton(" Show All Sales")
        self.show_all_button.setIcon(QIcon.fromTheme("view-list"))
        self.show_all_button.clicked.connect(self.show_all_sales)
        summary_layout.addWidget(self.show_all_button)
        
        history_layout.addWidget(summary_frame)
        
        history_group.setLayout(history_layout)
        main_layout.addWidget(history_group)
        
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
        
        main_layout.addWidget(status_frame)
        
    def set_date_range(self, days_from, days_to):
        """Set date range with quick buttons"""
        self.start_date_edit.setDate(QDate.currentDate().addDays(days_from))
        self.end_date_edit.setDate(QDate.currentDate().addDays(days_to))
        
    def refresh_data(self):
        """Refresh the sales data"""
        try:
            start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
            end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
            
            sales_data = self.db_manager.get_sales_data(start_date, end_date)
            self.populate_table(sales_data)
            self.update_summary(sales_data)
            self.status_label.setText(f"Loaded {len(sales_data)} sales records from {start_date} to {end_date}")
        except Exception as e:
            self.status_label.setText(f"Error loading sales data: {str(e)}")
    
    def show_all_sales(self):
        """Show all sales without date filtering"""
        try:
            sales_data = self.db_manager.get_sales_data()  # No date filter
            self.populate_table(sales_data)
            self.update_summary(sales_data)
            self.status_label.setText(f"Loaded {len(sales_data)} sales records (All Time)")
        except Exception as e:
            self.status_label.setText(f"Error loading all sales: {str(e)}")
    
    def populate_table(self, sales_data):
        """Populate the sales table"""
        self.sales_table.setRowCount(len(sales_data))
        
        for row, sale in enumerate(sales_data):
            # Date
            date_str = sale['sale_date'][:10] if sale['sale_date'] else 'N/A'
            date_item = QTableWidgetItem(date_str)
            date_item.setTextAlignment(Qt.AlignCenter)
            self.sales_table.setItem(row, 0, date_item)
            
            # Product name
            self.sales_table.setItem(row, 1, QTableWidgetItem(sale['product_name']))
            
            # Quantity
            quantity_item = QTableWidgetItem(str(sale['quantity']))
            quantity_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.sales_table.setItem(row, 2, quantity_item)
            
            # Unit price
            unit_price_item = QTableWidgetItem(format_currency(sale['unit_price']))
            unit_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.sales_table.setItem(row, 3, unit_price_item)
            
            # Total price
            total_price_item = QTableWidgetItem(format_currency(sale['total_price']))
            total_price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.sales_table.setItem(row, 4, total_price_item)
            
            # Profit
            profit_item = QTableWidgetItem(format_currency(sale['profit']))
            profit_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Color code profit
            if sale['profit'] > 0:
                profit_item.setBackground(QColor(230, 245, 230))  # Light green
                profit_item.setForeground(QColor(39, 174, 96))    # Dark green text
            elif sale['profit'] < 0:
                profit_item.setBackground(QColor(255, 230, 230))  # Light red
                profit_item.setForeground(QColor(231, 76, 60))    # Dark red text
            
            self.sales_table.setItem(row, 5, profit_item)
            
            # Notes
            notes_item = QTableWidgetItem(sale.get('notes', ''))
            self.sales_table.setItem(row, 6, notes_item)
    
    def update_summary(self, sales_data):
        """Update summary information"""
        total_sales = sum(sale['total_price'] for sale in sales_data)
        total_profit = sum(sale['profit'] for sale in sales_data)
        total_items = sum(sale['quantity'] for sale in sales_data)
        
        self.total_sales_label.setText(f"Total Sales: {format_currency(total_sales)}")
        self.total_profit_label.setText(f"Total Profit: {format_currency(total_profit)}")
        self.total_items_label.setText(f"Total Items: {total_items}")
    
    def new_sale(self):
        """Open new sale dialog"""
        dialog = SaleDialog(self, self.db_manager)
        if dialog.exec_() == QDialog.Accepted:
            sale_data = dialog.get_sale_data()
            
            # Record the sale
            if self.db_manager.add_sale(
                sale_data['product_id'],
                sale_data['quantity'],
                sale_data['unit_price'],
                sale_data['notes']
            ):
                # Force refresh to show new sale immediately
                self.refresh_data()
                QMessageBox.information(self, "Success", "Sale recorded successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to record sale")