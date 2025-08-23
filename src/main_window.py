"""
Main Window Module
Main application window with tabbed interface
"""

import sys
from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QWidget, QVBoxLayout, 
                             QHBoxLayout, QMessageBox, QStatusBar, QMenuBar, QMenu, QAction)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QFont

from .database import DatabaseManager
from .inventory_tab import InventoryTab
from .sales_tab import SalesTab
from .settings_tab import SettingsTab

class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        try:
            print("🔨 Initializing MainWindow...")
            super().__init__()
            print("✅ MainWindow super() initialized")
            
            self.db_manager = DatabaseManager()
            print("✅ Database manager created")
            
            self.init_ui()
            print("✅ UI initialized")
            
            self.setup_menu()
            print("✅ Menu setup complete")
            
            self.setup_status_bar()
            print("✅ Status bar setup complete")
            
            # Ensure window is visible
            self.show()
            self.raise_()
            self.activateWindow()
            print("✅ Window visibility set")
            
            # Auto-refresh timer
            self.refresh_timer = QTimer()
            self.refresh_timer.timeout.connect(self.refresh_data)
            self.refresh_timer.start(30000)  # Refresh every 30 seconds
            print("✅ Timer started")
            
            print("🎉 MainWindow initialization complete!")
            
        except Exception as e:
            print(f"❌ ERROR in MainWindow.__init__: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Inventory Management System")
        self.setGeometry(100, 100, 1200, 800)
        self.setMinimumSize(1000, 600)
        
        # Set application icon (if available)
        # self.setWindowIcon(QIcon("icons/app_icon.png"))
        
        # Force window to front and focus
        self.raise_()
        self.activateWindow()
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setFont(QFont("Segoe UI", 10))
        
        # Create tabs
        self.create_tabs()
        
        main_layout.addWidget(self.tab_widget)
        
        # Set tab widget as central widget
        self.setCentralWidget(central_widget)
        
        # Ensure window is visible and focused
        self.show()
        self.raise_()
        self.activateWindow()
        
    def create_tabs(self):
        """Create all application tabs"""
        try:
            print("🔨 Creating Inventory Tab...")
            # Inventory Management Tab
            self.inventory_tab = InventoryTab(self.db_manager)
            self.tab_widget.addTab(self.inventory_tab, "📦 Inventory")
            print("✅ Inventory Tab created")
            
            print("🔨 Creating Scanner Tab...")
            # Barcode Scanner Tab (Professional with camera support)
            try:
                from .scanner_tab_full import ProfessionalScannerTab
                self.scanner_tab = ProfessionalScannerTab()
                self.scanner_tab.barcode_detected.connect(self.on_barcode_detected)
                self.scanner_tab.qr_code_detected.connect(self.on_barcode_detected)
                self.tab_widget.addTab(self.scanner_tab, "📷 Scanner")
                print("✅ Professional scanner loaded with camera support")
            except Exception as e:
                print(f"❌ Scanner failed: {e}")
                QMessageBox.critical(self, "Scanner Error", 
                                   "Camera scanner failed to load. Please check OpenCV installation.")
                # Create a basic placeholder
                self.scanner_tab = QWidget()
                self.scanner_tab.barcode_detected = pyqtSignal(str)
                self.scanner_tab.qr_code_detected = pyqtSignal(str)
                self.tab_widget.addTab(self.scanner_tab, "📷 Scanner (Error)")
            
            print("🔨 Creating Sales Tab...")
            # Sales Tab
            self.sales_tab = SalesTab(self.db_manager)
            self.tab_widget.addTab(self.sales_tab, "💰 Sales")
            print("✅ Sales Tab created")
            
            print("🔨 Creating Reports Tab...")
            # Reports Tab (Basic reporting functionality)
            try:
                from .reports_tab import ReportsTab
                self.reports_tab = ReportsTab(self.db_manager)
                self.tab_widget.addTab(self.reports_tab, "📊 Reports")
                print("✅ Basic reports loaded successfully")
            except Exception as e:
                print(f"❌ Reports failed: {e}")
                QMessageBox.critical(self, "Reports Error", 
                                   "Reports failed to load. Please check the installation.")
                # Create a basic placeholder
                self.reports_tab = QWidget()
                self.tab_widget.addTab(self.reports_tab, "📊 Reports (Error)")
            
            print("🔨 Creating Settings Tab...")
            # Settings Tab
            self.settings_tab = SettingsTab(self.db_manager)
            self.tab_widget.addTab(self.settings_tab, "⚙️ Settings")
            print("✅ Settings Tab created")
            
            print("🎉 All tabs created successfully!")
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR in create_tabs: {e}")
            import traceback
            traceback.print_exc()
            raise
        
    def setup_menu(self):
        """Setup application menu bar"""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu('&File')
        
        # Export action
        export_action = QAction('&Export Data', self)
        export_action.setShortcut('Ctrl+E')
        export_action.triggered.connect(self.export_data)
        file_menu.addAction(export_action)
        
        # Import action
        import_action = QAction('&Import Data', self)
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.import_data)
        file_menu.addAction(import_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('E&xit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools Menu
        tools_menu = menubar.addMenu('&Tools')
        
        # Refresh action
        refresh_action = QAction('&Refresh Data', self)
        refresh_action.setShortcut('F5')
        refresh_action.triggered.connect(self.refresh_data)
        tools_menu.addAction(refresh_action)
        
        # Backup action
        backup_action = QAction('&Backup Database', self)
        backup_action.triggered.connect(self.backup_database)
        tools_menu.addAction(backup_action)
        
        # Help Menu
        help_menu = menubar.addMenu('&Help')
        
        # About action
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def on_barcode_detected(self, barcode_data):
        """Handle barcode detection from scanner tab"""
        # Switch to inventory tab
        self.tab_widget.setCurrentIndex(0)
        
        # Search for product with this barcode
        product = self.db_manager.get_product_by_barcode(barcode_data)
        
        if product:
            # Show product details
            self.inventory_tab.show_product_details(product)
            self.status_bar.showMessage(f"Product found: {product['name']}")
        else:
            # Show add product dialog
            self.inventory_tab.add_new_product(barcode_data)
            self.status_bar.showMessage(f"New barcode detected: {barcode_data}")
    
    def refresh_data(self):
        """Refresh all data across tabs"""
        try:
            # Refresh inventory tab
            if hasattr(self.inventory_tab, 'refresh_data'):
                self.inventory_tab.refresh_data()
            
            # Refresh sales tab
            if hasattr(self.sales_tab, 'refresh_data'):
                self.sales_tab.refresh_data()
            
            # Refresh reports tab
            if hasattr(self.reports_tab, 'refresh_data'):
                self.reports_tab.refresh_data()
            
            self.status_bar.showMessage("Data refreshed successfully")
            
        except Exception as e:
            self.status_bar.showMessage(f"Error refreshing data: {str(e)}")
    
    def export_data(self):
        """Export data to file"""
        try:
            # This will be implemented in the reports tab
            self.tab_widget.setCurrentIndex(3)  # Switch to reports tab
            self.reports_tab.export_data()
            self.status_bar.showMessage("Data export initiated")
        except Exception as e:
            QMessageBox.warning(self, "Export Error", f"Failed to export data: {str(e)}")
    
    def import_data(self):
        """Import data from file"""
        try:
            # This will be implemented in the inventory tab
            self.tab_widget.setCurrentIndex(0)  # Switch to inventory tab
            self.inventory_tab.import_data()
            self.status_bar.showMessage("Data import initiated")
        except Exception as e:
            QMessageBox.warning(self, "Import Error", f"Failed to import data: {str(e)}")
    
    def backup_database(self):
        """Backup the database"""
        try:
            # Simple backup - copy database file
            import shutil
            import datetime
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = f"backup_inventory_{timestamp}.db"
            
            shutil.copy2("inventory.db", backup_path)
            
            QMessageBox.information(self, "Backup Successful", 
                                  f"Database backed up to: {backup_path}")
            self.status_bar.showMessage("Database backup completed")
            
        except Exception as e:
            QMessageBox.warning(self, "Backup Error", f"Failed to backup database: {str(e)}")
    
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(self, "About Inventory Management System",
                         """<h3>Inventory Management System</h3>
                         <p><b>Version:</b> 1.0.0</p>
                         <p><b>Features:</b></p>
                         <ul>
                             <li>Barcode/QR Code Scanning</li>
                             <li>Inventory Management</li>
                             <li>Sales Tracking</li>
                             <li>Profit Reporting</li>
                             <li>Database Management</li>
                         </ul>
                         <p><b>Built with:</b> Python + PyQt5</p>""")
    
    def closeEvent(self, event):
        """Handle application close event"""
        # Stop camera if running
        if hasattr(self.scanner_tab, 'stop_camera'):
            self.scanner_tab.stop_camera()
        
        # Close database connections
        if hasattr(self.db_manager, 'close'):
            self.db_manager.close()
        
        event.accept()
