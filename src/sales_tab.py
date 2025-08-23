"""
Sales Tab
Handles sales transactions and sales history
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                              QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
                              QHeaderView, QMessageBox, QDialog, QFormLayout,
                              QSpinBox, QDoubleSpinBox, QComboBox, QGroupBox,
                              QDateEdit, QTextEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
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
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Product selection section
        product_group = QGroupBox("Product Selection")
        product_layout = QVBoxLayout()
        
        # Barcode input
        barcode_layout = QHBoxLayout()
        self.barcode_edit = QLineEdit()
        self.barcode_edit.setPlaceholderText("Enter barcode or scan...")
        self.barcode_edit.returnPressed.connect(self.search_product)
        barcode_layout.addWidget(QLabel("Barcode:"))
        barcode_layout.addWidget(self.barcode_edit)
        
        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self.search_product)
        barcode_layout.addWidget(self.search_button)
        product_layout.addLayout(barcode_layout)
        
        # Product info display
        self.product_info_label = QLabel("No product selected")
        self.product_info_label.setStyleSheet("padding: 10px; border: 1px solid gray; background-color: #f0f0f0;")
        product_layout.addWidget(self.product_info_label)
        
        product_group.setLayout(product_layout)
        layout.addWidget(product_group)
        
        # Sale details section
        sale_group = QGroupBox("Sale Details")
        sale_layout = QFormLayout()
        
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
        self.total_price_label = QLabel(f"{get_currency_symbol()}0.00")
        self.total_price_label.setStyleSheet("font-weight: bold; font-size: 14px; color: green;")
        sale_layout.addRow("Total Price:", self.total_price_label)
        
        # Notes
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(60)
        sale_layout.addRow("Notes:", self.notes_edit)
        
        sale_group.setLayout(sale_layout)
        layout.addWidget(sale_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("Record Sale")
        self.save_button.clicked.connect(self.accept)
        self.save_button.setEnabled(False)
        button_layout.addWidget(self.save_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        
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
        else:
            QMessageBox.warning(self, "Product Not Found", f"No product found with barcode: {barcode}")
            self.selected_product = None
            self.product_info_label.setText("No product selected")
            self.save_button.setEnabled(False)
    
    def display_product_info(self, product):
        """Display product information"""
        info_text = f"""
        <b>Product:</b> {product['name']}<br>
        <b>Category:</b> {product['category'] or 'N/A'}<br>
        <b>Available:</b> {product['quantity']} units<br>
        <b>Cost Price:</b> {format_currency(product['cost_price'])}<br>
        <b>Selling Price:</b> {format_currency(product['selling_price'])}
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
        layout = QVBoxLayout(self)
        
        # Quick sale section
        quick_sale_group = QGroupBox("Quick Sale")
        quick_sale_layout = QHBoxLayout()
        
        self.new_sale_button = QPushButton("💰 New Sale")
        self.new_sale_button.clicked.connect(self.new_sale)
        quick_sale_layout.addWidget(self.new_sale_button)
        
        quick_sale_layout.addStretch()
        
        quick_sale_group.setLayout(quick_sale_layout)
        layout.addWidget(quick_sale_group)
        
        # Sales history section
        history_group = QGroupBox("Sales History")
        history_layout = QVBoxLayout()
        
        # Filter controls
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Date Range:"))
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate().addDays(-365))  # Show last year by default
        self.start_date_edit.dateChanged.connect(self.refresh_data)
        filter_layout.addWidget(self.start_date_edit)
        
        filter_layout.addWidget(QLabel("to"))
        
        self.end_date_edit = QDateEdit()
        self.end_date_edit.setDate(QDate.currentDate().addDays(1))  # Include today
        self.end_date_edit.dateChanged.connect(self.refresh_data)
        filter_layout.addWidget(self.end_date_edit)
        
        self.refresh_button = QPushButton("🔄 Refresh")
        self.refresh_button.clicked.connect(self.refresh_data)
        filter_layout.addWidget(self.refresh_button)
        
        # Add "Show All" button
        self.show_all_button = QPushButton("📊 Show All Sales")
        self.show_all_button.clicked.connect(self.show_all_sales)
        filter_layout.addWidget(self.show_all_button)
        
        filter_layout.addStretch()
        
        history_layout.addLayout(filter_layout)
        
        # Sales table
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(7)
        self.sales_table.setHorizontalHeaderLabels([
            "Date", "Product", "Quantity", "Unit Price", "Total Price", "Profit", "Notes"
        ])
        
        # Set table properties
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
        
        history_layout.addWidget(self.sales_table)
        
        # Summary section
        summary_layout = QHBoxLayout()
        
        self.total_sales_label = QLabel(f"Total Sales: {get_currency_symbol()}0.00")
        self.total_sales_label.setStyleSheet("font-weight: bold; font-size: 12px; color: blue;")
        summary_layout.addWidget(self.total_sales_label)
        
        self.total_profit_label = QLabel(f"Total Profit: {get_currency_symbol()}0.00")
        self.total_profit_label.setStyleSheet("font-weight: bold; font-size: 12px; color: green;")
        summary_layout.addWidget(self.total_profit_label)
        
        self.total_items_label = QLabel("Total Items: 0")
        self.total_items_label.setStyleSheet("font-weight: bold; font-size: 12px; color: orange;")
        summary_layout.addWidget(self.total_items_label)
        
        summary_layout.addStretch()
        
        history_layout.addLayout(summary_layout)
        
        history_group.setLayout(history_layout)
        layout.addWidget(history_group)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
    def refresh_data(self):
        """Refresh the sales data"""
        try:
            start_date = self.start_date_edit.date().toString("yyyy-MM-dd")
            end_date = self.end_date_edit.date().toString("yyyy-MM-dd")
            
            print(f"🔍 Refreshing sales data: {start_date} to {end_date}")
            sales_data = self.db_manager.get_sales_data(start_date, end_date)
            print(f"📊 Retrieved {len(sales_data)} sales records")
            
            self.populate_table(sales_data)
            self.update_summary(sales_data)
            self.status_label.setText(f"Loaded {len(sales_data)} sales records")
        except Exception as e:
            print(f"❌ Error in refresh_data: {e}")
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
            self.sales_table.setItem(row, 0, QTableWidgetItem(date_str))
            
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
                profit_item.setBackground(Qt.green)
            elif sale['profit'] < 0:
                profit_item.setBackground(Qt.red)
            
            self.sales_table.setItem(row, 5, profit_item)
            
            # Notes (placeholder for future enhancement)
            self.sales_table.setItem(row, 6, QTableWidgetItem(""))
    
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
                sale_data['unit_price']
            ):
                # Force refresh to show new sale immediately
                self.show_all_sales()  # Show all sales including the new one
                QMessageBox.information(self, "Success", "Sale recorded successfully")
            else:
                QMessageBox.warning(self, "Error", "Failed to record sale")
