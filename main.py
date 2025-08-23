#!/usr/bin/env python3
"""
Inventory Management System
Main Application Entry Point
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from src.main_window import MainWindow

def main():
    """Main application entry point"""
    try:
        print("🚀 Starting Inventory Management System...")
        
        # Create the application
        app = QApplication(sys.argv)
        print("✅ QApplication created successfully")
        
        app.setApplicationName("Inventory Management System")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("Inventory Corp")
        
        # Set application style
        app.setStyle('Fusion')
        print("✅ Application style set")
        
        # Create main window
        print("🔨 Creating main window...")
        main_window = MainWindow()
        print("✅ Main window created successfully")
        
        # Show the window
        print("👁️ Showing main window...")
        main_window.show()
        main_window.raise_()
        main_window.activateWindow()
        print("✅ Window show() called successfully")
        
        print("🔄 Starting event loop...")
        # Start the event loop
        return app.exec_()
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    main()
