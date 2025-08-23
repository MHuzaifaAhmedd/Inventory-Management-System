#!/usr/bin/env python3
"""
Test Scanner Functionality
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal

class TestScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Barcode input
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Enter barcode manually...")
        self.barcode_input.returnPressed.connect(self.on_barcode_entered)
        layout.addWidget(self.barcode_input)
        
        # Scan button
        self.scan_btn = QPushButton("Scan Barcode")
        self.scan_btn.clicked.connect(self.on_barcode_entered)
        layout.addWidget(self.scan_btn)
        
        # Status
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
    def on_barcode_entered(self):
        """Handle barcode entry"""
        barcode = self.barcode_input.text().strip()
        if not barcode:
            QMessageBox.warning(self, "Input Error", "Please enter a barcode")
            return
            
        self.status_label.setText(f"Barcode entered: {barcode}")
        QMessageBox.information(self, "Success", f"Barcode: {barcode}")

def main():
    app = QApplication(sys.argv)
    window = TestScanner()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
