"""
Simple Scanner Tab
Provides manual barcode entry and QR code generation without camera dependencies
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QLabel, QLineEdit, QTextEdit, QGroupBox, QMessageBox,
                             QFileDialog, QSpinBox, QFormLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap
import qrcode
import os

class SimpleScannerTab(QWidget):
    """Simple scanner tab with manual entry and QR generation"""
    
    barcode_detected = pyqtSignal(str)  # Signal for barcode detection
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout(self)
        
        # Manual Barcode Entry Section
        barcode_group = QGroupBox("📱 Manual Barcode Entry")
        barcode_layout = QVBoxLayout()
        
        # Barcode input
        input_layout = QHBoxLayout()
        self.barcode_edit = QLineEdit()
        self.barcode_edit.setPlaceholderText("Enter barcode manually...")
        self.barcode_edit.returnPressed.connect(self.emit_barcode)
        input_layout.addWidget(self.barcode_edit)
        
        self.enter_button = QPushButton("Enter Barcode")
        self.enter_button.clicked.connect(self.emit_barcode)
        input_layout.addWidget(self.enter_button)
        
        barcode_layout.addLayout(input_layout)
        
        # Instructions
        instructions = QLabel(
            "💡 <b>How to use:</b><br>"
            "1. Type or paste a barcode number above<br>"
            "2. Press Enter or click 'Enter Barcode'<br>"
            "3. The barcode will be sent to the inventory system"
        )
        instructions.setWordWrap(True)
        instructions.setStyleSheet("padding: 10px; background-color: #f0f8ff; border: 1px solid #ccc;")
        barcode_layout.addWidget(instructions)
        
        barcode_group.setLayout(barcode_layout)
        layout.addWidget(barcode_group)
        
        # QR Code Generation Section
        qr_group = QGroupBox("🔄 QR Code Generator")
        qr_layout = QVBoxLayout()
        
        # QR input form
        form_layout = QFormLayout()
        
        self.qr_text_edit = QTextEdit()
        self.qr_text_edit.setMaximumHeight(80)
        self.qr_text_edit.setPlaceholderText("Enter text or URL to generate QR code...")
        form_layout.addRow("Text/URL:", self.qr_text_edit)
        
        self.qr_size_spin = QSpinBox()
        self.qr_size_spin.setRange(100, 400)
        self.qr_size_spin.setValue(200)
        self.qr_size_spin.setSuffix(" px")
        form_layout.addRow("Size:", self.qr_size_spin)
        
        qr_layout.addLayout(form_layout)
        
        # Generate button
        self.generate_qr_button = QPushButton("🔄 Generate QR Code")
        self.generate_qr_button.clicked.connect(self.generate_qr_code)
        qr_layout.addWidget(self.generate_qr_button)
        
        # QR code display
        self.qr_display_label = QLabel("QR Code will appear here")
        self.qr_display_label.setAlignment(Qt.AlignCenter)
        self.qr_display_label.setStyleSheet("border: 2px dashed #ccc; padding: 20px;")
        self.qr_display_label.setMinimumSize(250, 250)
        qr_layout.addWidget(self.qr_display_label)
        
        # Save button
        self.save_qr_button = QPushButton("💾 Save QR Code")
        self.save_qr_button.clicked.connect(self.save_qr_code)
        self.save_qr_button.setEnabled(False)
        qr_layout.addWidget(self.save_qr_button)
        
        qr_group.setLayout(qr_layout)
        layout.addWidget(qr_group)
        
        # Status
        self.status_label = QLabel("Ready - Enter a barcode or generate a QR code")
        self.status_label.setStyleSheet("padding: 5px; background-color: #f0f0f0; border: 1px solid #ccc;")
        layout.addWidget(self.status_label)
        
        # Store generated QR code
        self.current_qr_pixmap = None
        
    def emit_barcode(self):
        """Emit the barcode signal"""
        barcode = self.barcode_edit.text().strip()
        if barcode:
            self.barcode_detected.emit(barcode)
            self.status_label.setText(f"Barcode sent: {barcode}")
            self.barcode_edit.clear()
            self.barcode_edit.setFocus()
        else:
            QMessageBox.warning(self, "Input Error", "Please enter a barcode")
    
    def generate_qr_code(self):
        """Generate a QR code from the input text"""
        text = self.qr_text_edit.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Input Error", "Please enter text to generate QR code")
            return
        
        try:
            # Generate QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(text)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to QPixmap
            size = self.qr_size_spin.value()
            img = img.resize((size, size))
            
            # Save temporarily and load as QPixmap
            temp_path = "temp_qr.png"
            img.save(temp_path)
            
            self.current_qr_pixmap = QPixmap(temp_path)
            self.qr_display_label.setPixmap(self.current_qr_pixmap)
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            self.save_qr_button.setEnabled(True)
            self.status_label.setText(f"QR Code generated for: {text[:30]}...")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate QR code: {str(e)}")
            self.status_label.setText("Error generating QR code")
    
    def save_qr_code(self):
        """Save the generated QR code to a file"""
        if not self.current_qr_pixmap:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save QR Code", "qr_code.png", "PNG Files (*.png);;All Files (*)"
        )
        
        if file_path:
            try:
                self.current_qr_pixmap.save(file_path)
                QMessageBox.information(self, "Success", f"QR Code saved to: {file_path}")
                self.status_label.setText(f"QR Code saved to: {os.path.basename(file_path)}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save QR code: {str(e)}")
                self.status_label.setText("Error saving QR code")
