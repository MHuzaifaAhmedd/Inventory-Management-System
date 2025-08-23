"""
Settings Tab
Handles application settings and configuration
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QSpinBox, QComboBox, QGroupBox,
                             QMessageBox, QFileDialog, QCheckBox, QFormLayout,
                             QTabWidget, QTextEdit, QProgressBar)
from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtGui import QFont
import os
import shutil
import sqlite3
from datetime import datetime

class SettingsTab(QWidget):
    """Settings and configuration tab"""
    
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.settings = QSettings('InventoryCorp', 'InventoryManagementSystem')
        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Create tab widget for different settings categories
        self.settings_tabs = QTabWidget()
        
        # General Settings Tab
        self.create_general_tab()
        
        # Database Settings Tab
        self.create_database_tab()
        
        # Scanner Settings Tab
        self.create_scanner_tab()
        
        # Export Settings Tab
        self.create_export_tab()
        
        layout.addWidget(self.settings_tabs)
        
        # Save/Cancel buttons
        button_layout = QHBoxLayout()
        
        self.save_button = QPushButton("💾 Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_button)
        
        self.reset_button = QPushButton("🔄 Reset to Defaults")
        self.reset_button.clicked.connect(self.reset_settings)
        button_layout.addWidget(self.reset_button)
        
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
    def create_general_tab(self):
        """Create general settings tab"""
        general_widget = QWidget()
        layout = QVBoxLayout(general_widget)
        
        # Company Information
        company_group = QGroupBox("Company Information")
        company_layout = QFormLayout()
        
        self.company_name_edit = QLineEdit()
        self.company_name_edit.setPlaceholderText("Enter company name")
        company_layout.addRow("Company Name:", self.company_name_edit)
        
        self.company_address_edit = QTextEdit()
        self.company_address_edit.setMaximumHeight(80)
        self.company_address_edit.setPlaceholderText("Enter company address")
        company_layout.addRow("Company Address:", self.company_address_edit)
        
        self.company_phone_edit = QLineEdit()
        self.company_phone_edit.setPlaceholderText("Enter phone number")
        company_layout.addRow("Phone Number:", self.company_phone_edit)
        
        self.company_email_edit = QLineEdit()
        self.company_email_edit.setPlaceholderText("Enter email address")
        company_layout.addRow("Email Address:", self.company_email_edit)
        
        company_group.setLayout(company_layout)
        layout.addWidget(company_group)
        
        # Application Settings
        app_group = QGroupBox("Application Settings")
        app_layout = QFormLayout()
        
        self.auto_refresh_checkbox = QCheckBox("Enable auto-refresh")
        app_layout.addRow("Auto Refresh:", self.auto_refresh_checkbox)
        
        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setRange(10, 300)
        self.refresh_interval_spin.setSuffix(" seconds")
        self.refresh_interval_spin.setValue(30)
        app_layout.addRow("Refresh Interval:", self.refresh_interval_spin)
        
        self.startup_checkbox = QCheckBox("Check for updates on startup")
        app_layout.addRow("Startup Updates:", self.startup_checkbox)
        
        self.backup_checkbox = QCheckBox("Auto-backup database")
        app_layout.addRow("Auto Backup:", self.backup_checkbox)
        
        app_group.setLayout(app_layout)
        layout.addWidget(app_group)
        
        # Currency Settings
        currency_group = QGroupBox("Currency Settings")
        currency_layout = QFormLayout()
        
        self.currency_combo = QComboBox()
        self.currency_combo.addItems(["USD ($)", "EUR (€)", "GBP (£)", "CAD (C$)", "AUD (A$)", "PKR (₨)"])
        currency_layout.addRow("Currency:", self.currency_combo)
        
        self.decimal_places_spin = QSpinBox()
        self.decimal_places_spin.setRange(0, 4)
        self.decimal_places_spin.setValue(2)
        currency_layout.addRow("Decimal Places:", self.decimal_places_spin)
        
        currency_group.setLayout(currency_layout)
        layout.addWidget(currency_group)
        
        layout.addStretch()
        general_widget.setLayout(layout)
        self.settings_tabs.addTab(general_widget, "General")
        
    def create_database_tab(self):
        """Create database settings tab"""
        db_widget = QWidget()
        layout = QVBoxLayout(db_widget)
        
        # Database Information
        db_info_group = QGroupBox("Database Information")
        db_info_layout = QFormLayout()
        
        self.db_path_label = QLabel("inventory.db")
        self.db_path_label.setStyleSheet("padding: 5px; border: 1px solid gray; background-color: #f0f0f0;")
        db_info_layout.addRow("Database Path:", self.db_path_label)
        
        self.db_size_label = QLabel("Calculating...")
        db_info_layout.addRow("Database Size:", self.db_size_label)
        
        self.db_tables_label = QLabel("Calculating...")
        db_info_layout.addRow("Tables:", self.db_tables_label)
        
        self.db_records_label = QLabel("Calculating...")
        db_info_layout.addRow("Total Records:", self.db_records_label)
        
        db_info_group.setLayout(db_info_layout)
        layout.addWidget(db_info_group)
        
        # Database Operations
        db_ops_group = QGroupBox("Database Operations")
        db_ops_layout = QVBoxLayout()
        
        # Backup section
        backup_layout = QHBoxLayout()
        backup_layout.addWidget(QLabel("Backup Database:"))
        
        self.backup_button = QPushButton("📦 Create Backup")
        self.backup_button.clicked.connect(self.create_backup)
        backup_layout.addWidget(self.backup_button)
        
        self.backup_path_edit = QLineEdit()
        self.backup_path_edit.setPlaceholderText("Backup location (optional)")
        backup_layout.addWidget(self.backup_path_edit)
        
        db_ops_layout.addLayout(backup_layout)
        
        # Restore section
        restore_layout = QHBoxLayout()
        restore_layout.addWidget(QLabel("Restore Database:"))
        
        self.restore_button = QPushButton("📥 Restore from Backup")
        self.restore_button.clicked.connect(self.restore_backup)
        restore_layout.addWidget(self.restore_button)
        
        db_ops_layout.addLayout(restore_layout)
        
        # Maintenance section
        maintenance_layout = QHBoxLayout()
        maintenance_layout.addWidget(QLabel("Database Maintenance:"))
        
        self.optimize_button = QPushButton("🔧 Optimize Database")
        self.optimize_button.clicked.connect(self.optimize_database)
        maintenance_layout.addWidget(self.optimize_button)
        
        self.vacuum_button = QPushButton("🧹 Vacuum Database")
        self.vacuum_button.clicked.connect(self.vacuum_database)
        maintenance_layout.addWidget(self.vacuum_button)
        
        db_ops_layout.addLayout(maintenance_layout)
        
        db_ops_group.setLayout(db_ops_layout)
        layout.addWidget(db_ops_group)
        
        # Progress bar for operations
        self.db_progress = QProgressBar()
        self.db_progress.setVisible(False)
        layout.addWidget(self.db_progress)
        
        layout.addStretch()
        db_widget.setLayout(layout)
        self.settings_tabs.addTab(db_widget, "Database")
        
        # Update database info
        self.update_database_info()
        
    def create_scanner_tab(self):
        """Create scanner settings tab"""
        scanner_widget = QWidget()
        layout = QVBoxLayout(scanner_widget)
        
        # Camera Settings
        camera_group = QGroupBox("Camera Settings")
        camera_layout = QFormLayout()
        
        self.camera_device_combo = QComboBox()
        self.camera_device_combo.addItems(["Default Camera (0)", "Camera 1", "Camera 2"])
        camera_layout.addRow("Camera Device:", self.camera_device_combo)
        
        self.camera_resolution_combo = QComboBox()
        self.camera_resolution_combo.addItems(["640x480", "1280x720", "1920x1080"])
        camera_layout.addRow("Resolution:", self.camera_resolution_combo)
        
        self.camera_fps_spin = QSpinBox()
        self.camera_fps_spin.setRange(15, 60)
        self.camera_fps_spin.setValue(30)
        self.camera_fps_spin.setSuffix(" FPS")
        camera_layout.addRow("Frame Rate:", self.camera_fps_spin)
        
        camera_group.setLayout(camera_layout)
        layout.addWidget(camera_group)
        
        # Scanner Settings
        scanner_group = QGroupBox("Scanner Settings")
        scanner_layout = QFormLayout()
        
        self.auto_scan_checkbox = QCheckBox("Enable auto-scanning")
        scanner_layout.addRow("Auto Scan:", self.auto_scan_checkbox)
        
        self.scan_delay_spin = QSpinBox()
        self.scan_delay_spin.setRange(1, 10)
        self.scan_delay_spin.setValue(2)
        self.scan_delay_spin.setSuffix(" seconds")
        scanner_layout.addRow("Scan Delay:", self.scan_delay_spin)
        
        self.sound_feedback_checkbox = QCheckBox("Enable sound feedback")
        scanner_layout.addRow("Sound Feedback:", self.sound_feedback_checkbox)
        
        self.vibrate_feedback_checkbox = QCheckBox("Enable vibration feedback")
        scanner_layout.addRow("Vibration Feedback:", self.vibrate_feedback_checkbox)
        
        scanner_group.setLayout(scanner_layout)
        layout.addWidget(scanner_group)
        
        # Barcode Settings
        barcode_group = QGroupBox("Barcode Settings")
        barcode_layout = QFormLayout()
        
        self.barcode_types_combo = QComboBox()
        self.barcode_types_combo.addItems(["All Types", "QR Code Only", "Barcode Only"])
        barcode_layout.addRow("Barcode Types:", self.barcode_types_combo)
        
        self.barcode_validation_checkbox = QCheckBox("Enable barcode validation")
        barcode_layout.addRow("Validation:", self.barcode_validation_checkbox)
        
        barcode_group.setLayout(barcode_layout)
        layout.addWidget(barcode_group)
        
        layout.addStretch()
        scanner_widget.setLayout(layout)
        self.settings_tabs.addTab(scanner_widget, "Scanner")
        
    def create_export_tab(self):
        """Create export settings tab"""
        export_widget = QWidget()
        layout = QVBoxLayout(export_widget)
        
        # Export Settings
        export_group = QGroupBox("Export Settings")
        export_layout = QFormLayout()
        
        self.default_export_path_edit = QLineEdit()
        self.default_export_path_edit.setPlaceholderText("Select default export directory")
        export_layout.addRow("Default Export Path:", self.default_export_path_edit)
        
        self.browse_export_button = QPushButton("Browse")
        self.browse_export_button.clicked.connect(self.browse_export_path)
        export_layout.addRow("", self.browse_export_button)
        
        self.export_format_combo = QComboBox()
        self.export_format_combo.addItems(["Excel (.xlsx)", "CSV (.csv)", "PDF (.pdf)"])
        export_layout.addRow("Default Format:", self.export_format_combo)
        
        self.include_charts_checkbox = QCheckBox("Include charts in exports")
        export_layout.addRow("Include Charts:", self.include_charts_checkbox)
        
        self.auto_export_checkbox = QCheckBox("Auto-export reports")
        export_layout.addRow("Auto Export:", self.auto_export_checkbox)
        
        export_group.setLayout(export_layout)
        layout.addWidget(export_group)
        
        # Email Export Settings
        email_group = QGroupBox("Email Export Settings")
        email_layout = QFormLayout()
        
        self.email_export_checkbox = QCheckBox("Enable email export")
        email_layout.addRow("Email Export:", self.email_export_checkbox)
        
        self.smtp_server_edit = QLineEdit()
        self.smtp_server_edit.setPlaceholderText("smtp.gmail.com")
        email_layout.addRow("SMTP Server:", self.smtp_server_edit)
        
        self.smtp_port_spin = QSpinBox()
        self.smtp_port_spin.setRange(1, 65535)
        self.smtp_port_spin.setValue(587)
        email_layout.addRow("SMTP Port:", self.smtp_port_spin)
        
        self.email_username_edit = QLineEdit()
        self.email_username_edit.setPlaceholderText("your-email@gmail.com")
        email_layout.addRow("Email Username:", self.email_username_edit)
        
        self.email_password_edit = QLineEdit()
        self.email_password_edit.setEchoMode(QLineEdit.Password)
        self.email_password_edit.setPlaceholderText("Enter email password")
        email_layout.addRow("Email Password:", self.email_password_edit)
        
        email_group.setLayout(email_layout)
        layout.addWidget(email_group)
        
        layout.addStretch()
        export_widget.setLayout(layout)
        self.settings_tabs.addTab(export_widget, "Export")
        
    def load_settings(self):
        """Load saved settings"""
        # General settings
        self.company_name_edit.setText(self.settings.value('company/name', ''))
        self.company_address_edit.setPlainText(self.settings.value('company/address', ''))
        self.company_phone_edit.setText(self.settings.value('company/phone', ''))
        self.company_email_edit.setText(self.settings.value('company/email', ''))
        
        self.auto_refresh_checkbox.setChecked(self.settings.value('app/auto_refresh', True, type=bool))
        self.refresh_interval_spin.setValue(self.settings.value('app/refresh_interval', 30, type=int))
        self.startup_checkbox.setChecked(self.settings.value('app/startup_updates', False, type=bool))
        self.backup_checkbox.setChecked(self.settings.value('app/auto_backup', True, type=bool))
        
        currency_index = self.settings.value('currency/type', 0, type=int)
        self.currency_combo.setCurrentIndex(currency_index)
        self.decimal_places_spin.setValue(self.settings.value('currency/decimal_places', 2, type=int))
        
        # Scanner settings
        self.camera_device_combo.setCurrentIndex(self.settings.value('scanner/camera_device', 0, type=int))
        self.camera_resolution_combo.setCurrentIndex(self.settings.value('scanner/resolution', 0, type=int))
        self.camera_fps_spin.setValue(self.settings.value('scanner/fps', 30, type=int))
        
        self.auto_scan_checkbox.setChecked(self.settings.value('scanner/auto_scan', False, type=bool))
        self.scan_delay_spin.setValue(self.settings.value('scanner/scan_delay', 2, type=int))
        self.sound_feedback_checkbox.setChecked(self.settings.value('scanner/sound_feedback', True, type=bool))
        self.vibrate_feedback_checkbox.setChecked(self.settings.value('scanner/vibrate_feedback', False, type=bool))
        
        self.barcode_types_combo.setCurrentIndex(self.settings.value('scanner/barcode_types', 0, type=int))
        self.barcode_validation_checkbox.setChecked(self.settings.value('scanner/validation', True, type=bool))
        
        # Export settings
        self.default_export_path_edit.setText(self.settings.value('export/default_path', ''))
        self.export_format_combo.setCurrentIndex(self.settings.value('export/format', 0, type=int))
        self.include_charts_checkbox.setChecked(self.settings.value('export/include_charts', True, type=bool))
        self.auto_export_checkbox.setChecked(self.settings.value('export/auto_export', False, type=bool))
        
        self.email_export_checkbox.setChecked(self.settings.value('export/email_enabled', False, type=bool))
        self.smtp_server_edit.setText(self.settings.value('export/smtp_server', ''))
        self.smtp_port_spin.setValue(self.settings.value('export/smtp_port', 587, type=int))
        self.email_username_edit.setText(self.settings.value('export/email_username', ''))
        self.email_password_edit.setText(self.settings.value('export/email_password', ''))
        
    def save_settings(self):
        """Save current settings"""
        try:
            # General settings
            self.settings.setValue('company/name', self.company_name_edit.text())
            self.settings.setValue('company/address', self.company_address_edit.toPlainText())
            self.settings.setValue('company/phone', self.company_phone_edit.text())
            self.settings.setValue('company/email', self.company_email_edit.text())
            
            self.settings.setValue('app/auto_refresh', self.auto_refresh_checkbox.isChecked())
            self.settings.setValue('app/refresh_interval', self.refresh_interval_spin.value())
            self.settings.setValue('app/startup_updates', self.startup_checkbox.isChecked())
            self.settings.setValue('app/auto_backup', self.backup_checkbox.isChecked())
            
            self.settings.setValue('currency/type', self.currency_combo.currentIndex())
            self.settings.setValue('currency/decimal_places', self.decimal_places_spin.value())
            
            # Scanner settings
            self.settings.setValue('scanner/camera_device', self.camera_device_combo.currentIndex())
            self.settings.setValue('scanner/resolution', self.camera_resolution_combo.currentIndex())
            self.settings.setValue('scanner/fps', self.camera_fps_spin.value())
            
            self.settings.setValue('scanner/auto_scan', self.auto_scan_checkbox.isChecked())
            self.settings.setValue('scanner/scan_delay', self.scan_delay_spin.value())
            self.settings.setValue('scanner/sound_feedback', self.sound_feedback_checkbox.isChecked())
            self.settings.setValue('scanner/vibrate_feedback', self.vibrate_feedback_checkbox.isChecked())
            
            self.settings.setValue('scanner/barcode_types', self.barcode_types_combo.currentIndex())
            self.settings.setValue('scanner/validation', self.barcode_validation_checkbox.isChecked())
            
            # Export settings
            self.settings.setValue('export/default_path', self.default_export_path_edit.text())
            self.settings.setValue('export/format', self.export_format_combo.currentIndex())
            self.settings.setValue('export/include_charts', self.include_charts_checkbox.isChecked())
            self.settings.setValue('export/auto_export', self.auto_export_checkbox.isChecked())
            
            self.settings.setValue('export/email_enabled', self.email_export_checkbox.isChecked())
            self.settings.setValue('export/smtp_server', self.smtp_server_edit.text())
            self.settings.setValue('export/smtp_port', self.smtp_port_spin.value())
            self.settings.setValue('export/email_username', self.email_username_edit.text())
            self.settings.setValue('export/email_password', self.email_password_edit.text())
            
            self.settings.sync()
            self.status_label.setText("Settings saved successfully")
            
        except Exception as e:
            self.status_label.setText(f"Error saving settings: {str(e)}")
    
    def reset_settings(self):
        """Reset settings to defaults"""
        reply = QMessageBox.question(
            self, "Reset Settings", 
            "Are you sure you want to reset all settings to defaults?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.settings.clear()
            self.load_settings()
            self.status_label.setText("Settings reset to defaults")
    
    def update_database_info(self):
        """Update database information display"""
        try:
            db_path = "inventory.db"
            self.db_path_label.setText(db_path)
            
            # Get database size
            if os.path.exists(db_path):
                size_bytes = os.path.getsize(db_path)
                size_mb = size_bytes / (1024 * 1024)
                self.db_size_label.setText(f"{size_mb:.2f} MB")
            else:
                self.db_size_label.setText("Database not found")
            
            # Get table count and record count
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Count tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            self.db_tables_label.setText(str(len(tables)))
            
            # Count total records
            total_records = 0
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
                count = cursor.fetchone()[0]
                total_records += count
            
            self.db_records_label.setText(str(total_records))
            
            conn.close()
            
        except Exception as e:
            self.db_size_label.setText("Error")
            self.db_tables_label.setText("Error")
            self.db_records_label.setText("Error")
    
    def create_backup(self):
        """Create database backup"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"backup_inventory_{timestamp}.db"
            
            if self.backup_path_edit.text():
                backup_dir = self.backup_path_edit.text()
                backup_path = os.path.join(backup_dir, default_filename)
            else:
                backup_path, _ = QFileDialog.getSaveFileName(
                    self, "Save Backup", default_filename, "Database Files (*.db)"
                )
            
            if backup_path:
                shutil.copy2("inventory.db", backup_path)
                QMessageBox.information(self, "Backup Successful", f"Database backed up to:\n{backup_path}")
                self.status_label.setText("Backup created successfully")
                
        except Exception as e:
            QMessageBox.warning(self, "Backup Error", f"Failed to create backup: {str(e)}")
    
    def restore_backup(self):
        """Restore database from backup"""
        try:
            backup_path, _ = QFileDialog.getOpenFileName(
                self, "Select Backup File", "", "Database Files (*.db)"
            )
            
            if backup_path:
                reply = QMessageBox.question(
                    self, "Confirm Restore", 
                    "This will replace the current database. Are you sure?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    # Create backup of current database first
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    current_backup = f"pre_restore_backup_{timestamp}.db"
                    shutil.copy2("inventory.db", current_backup)
                    
                    # Restore from backup
                    shutil.copy2(backup_path, "inventory.db")
                    
                    QMessageBox.information(self, "Restore Successful", 
                                          f"Database restored from backup.\nCurrent database backed up as: {current_backup}")
                    self.status_label.setText("Database restored successfully")
                    
                    # Update database info
                    self.update_database_info()
                    
        except Exception as e:
            QMessageBox.warning(self, "Restore Error", f"Failed to restore database: {str(e)}")
    
    def optimize_database(self):
        """Optimize database"""
        try:
            self.db_progress.setVisible(True)
            self.db_progress.setValue(0)
            
            conn = sqlite3.connect("inventory.db")
            cursor = conn.cursor()
            
            # Analyze tables
            self.db_progress.setValue(25)
            cursor.execute("ANALYZE")
            
            # Update statistics
            self.db_progress.setValue(50)
            cursor.execute("UPDATE sqlite_stat1 SET stat = (SELECT COUNT(*) FROM sqlite_master WHERE type='table')")
            
            # Commit changes
            self.db_progress.setValue(75)
            conn.commit()
            conn.close()
            
            self.db_progress.setValue(100)
            QMessageBox.information(self, "Optimization Complete", "Database optimization completed successfully")
            self.status_label.setText("Database optimized successfully")
            
            # Hide progress bar after delay
            QTimer.singleShot(2000, lambda: self.db_progress.setVisible(False))
            
        except Exception as e:
            QMessageBox.warning(self, "Optimization Error", f"Failed to optimize database: {str(e)}")
            self.db_progress.setVisible(False)
    
    def vacuum_database(self):
        """Vacuum database to reclaim space"""
        try:
            reply = QMessageBox.question(
                self, "Confirm Vacuum", 
                "This operation will reclaim unused space but may take some time. Continue?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.db_progress.setVisible(True)
                self.db_progress.setValue(0)
                
                conn = sqlite3.connect("inventory.db")
                cursor = conn.cursor()
                
                # Vacuum database
                self.db_progress.setValue(50)
                cursor.execute("VACUUM")
                
                conn.close()
                
                self.db_progress.setValue(100)
                QMessageBox.information(self, "Vacuum Complete", "Database vacuum completed successfully")
                self.status_label.setText("Database vacuum completed")
                
                # Update database info
                self.update_database_info()
                
                # Hide progress bar after delay
                QTimer.singleShot(2000, lambda: self.db_progress.setVisible(False))
                
        except Exception as e:
            QMessageBox.warning(self, "Vacuum Error", f"Failed to vacuum database: {str(e)}")
            self.db_progress.setVisible(False)
    
    def browse_export_path(self):
        """Browse for export directory"""
        directory = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if directory:
            self.default_export_path_edit.setText(directory)
