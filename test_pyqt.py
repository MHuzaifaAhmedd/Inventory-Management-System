#!/usr/bin/env python3
"""
Simple PyQt Test
Tests if PyQt is working correctly
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt Test Window")
        self.setGeometry(200, 200, 400, 300)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Add test label
        label = QLabel("🎉 PyQt is working!")
        label.setFont(QFont("Arial", 16))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        # Add test button
        button = QPushButton("Click Me!")
        button.clicked.connect(self.button_clicked)
        layout.addWidget(button)
        
        # Force window to front
        self.raise_()
        self.activateWindow()
        
    def button_clicked(self):
        print("✅ Button clicked! PyQt is working correctly!")
        
    def showEvent(self, event):
        """Ensure window is visible when shown"""
        super().showEvent(event)
        self.raise_()
        self.activateWindow()
        print("✅ Window show event triggered")

def main():
    """Test PyQt functionality"""
    print("🚀 Starting PyQt test...")
    
    # Create application
    app = QApplication(sys.argv)
    print("✅ QApplication created")
    
    # Create and show window
    window = TestWindow()
    window.show()
    print("✅ Window.show() called")
    
    # Force window to front
    window.raise_()
    window.activateWindow()
    print("✅ Window forced to front")
    
    print("🔄 Starting event loop...")
    # Start event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
