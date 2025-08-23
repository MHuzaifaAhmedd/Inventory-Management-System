# Inventory Management System

A comprehensive desktop application built with Python and PyQt5 for managing inventory, sales tracking, and business analytics.

## 🚀 Features

### 📦 Inventory Management
- **Product Management**: Add, edit, delete, and search products
- **Barcode/QR Support**: Scan barcodes and QR codes using camera
- **Category Organization**: Organize products by categories
- **Stock Tracking**: Monitor quantities and set minimum stock levels
- **Status Indicators**: Visual indicators for stock levels (In Stock, Low Stock, Out of Stock)

### 📷 Barcode & QR Scanner
- **Camera Integration**: Use built-in or external cameras
- **Real-time Scanning**: Live camera feed with barcode detection
- **Multiple Formats**: Support for various barcode and QR code types
- **Auto-detection**: Automatic product lookup when scanning

### 💰 Sales Management
- **Sales Recording**: Record sales transactions with product details
- **Quick Sales**: Fast product lookup by barcode
- **Sales History**: Complete transaction history with filtering
- **Profit Calculation**: Automatic profit calculation per sale

### 📊 Advanced Reporting
- **Sales Overview**: Daily sales trends and patterns
- **Profit Analysis**: Product profitability analysis
- **Product Performance**: Sales volume and performance metrics
- **Category Analysis**: Sales breakdown by product categories
- **Low Stock Alerts**: Products requiring reorder
- **Interactive Charts**: Beautiful matplotlib-based visualizations
- **Data Export**: Export reports to Excel with multiple sheets

### ⚙️ Settings & Configuration
- **Company Information**: Store business details
- **Application Settings**: Customize refresh intervals and auto-backup
- **Currency Settings**: Support for multiple currencies
- **Scanner Configuration**: Camera and scanning preferences
- **Export Settings**: Default paths and email export options

### 🗄️ Database Management
- **SQLite Database**: Lightweight, reliable data storage
- **Backup & Restore**: Database backup and restoration
- **Maintenance Tools**: Database optimization and cleanup
- **Data Import/Export**: CSV and Excel data exchange

## 🛠️ Technology Stack

- **Frontend**: PyQt5 (Modern Python GUI framework)
- **Backend**: Python 3.8+
- **Database**: SQLite3
- **Computer Vision**: OpenCV for camera integration
- **Barcode Processing**: pyzbar for barcode/QR detection
- **Data Analysis**: Pandas for data manipulation
- **Charts**: Matplotlib for data visualization
- **Excel Export**: openpyxl for professional reports

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB available space
- **Camera**: Built-in or USB camera for scanning

### Python Requirements
- **Python**: 3.8 or higher
- **Dependencies**: See requirements.txt

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd inventory-management-system
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python main.py
```

## 📖 Usage Guide

### Getting Started
1. **Launch Application**: Run `python main.py`
2. **First Run**: The application will create a new database automatically
3. **Add Products**: Use the Inventory tab to add your first products
4. **Scan Barcodes**: Use the Scanner tab to scan product barcodes
5. **Record Sales**: Use the Sales tab to record transactions
6. **View Reports**: Use the Reports tab for business analytics

### Adding Products
1. Go to **Inventory** tab
2. Click **"➕ Add Product"**
3. Enter product details:
   - Barcode (optional, can be scanned)
   - Name (required)
   - Description
   - Category
   - Cost Price
   - Selling Price
   - Initial Quantity
   - Minimum Stock Level
4. Click **"Save"**

### Recording Sales
1. Go to **Sales** tab
2. Click **"💰 New Sale"**
3. Enter barcode or scan product
4. Set quantity and verify price
5. Add notes if needed
6. Click **"Record Sale"**

### Generating Reports
1. Go to **Reports** tab
2. Select report type:
   - Sales Overview
   - Profit Analysis
   - Product Performance
   - Category Analysis
   - Low Stock Alert
3. Set date range
4. Click **"🔄 Refresh"** to generate
5. Click **"📊 Export"** to save to Excel

## 🔧 Configuration

### Scanner Settings
- **Camera Device**: Select camera (0 for default)
- **Resolution**: Choose camera resolution
- **Frame Rate**: Set FPS for smooth scanning
- **Auto-scan**: Enable automatic barcode detection
- **Feedback**: Sound and vibration options

### Export Settings
- **Default Path**: Set default export directory
- **Format**: Choose Excel, CSV, or PDF
- **Charts**: Include charts in exports
- **Email**: Configure email export settings

### Database Settings
- **Auto-backup**: Enable automatic database backups
- **Backup Location**: Set backup directory
- **Maintenance**: Schedule database optimization

## 📁 Project Structure

```
inventory-management-system/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── src/                   # Source code
│   ├── __init__.py        # Package initialization
│   ├── main_window.py     # Main application window
│   ├── database.py        # Database management
│   ├── barcode_scanner.py # Barcode scanning functionality
│   ├── inventory_tab.py   # Inventory management tab
│   ├── sales_tab.py       # Sales management tab
│   ├── reports_tab.py     # Reporting and analytics tab
│   └── settings_tab.py    # Settings and configuration tab
└── inventory.db           # SQLite database (created automatically)
```

## 🎯 Key Features Explained

### Barcode Scanning
The application uses OpenCV for camera capture and pyzbar for barcode detection. It supports:
- **1D Barcodes**: UPC, EAN, Code 128, Code 39, etc.
- **2D Codes**: QR codes, Data Matrix, PDF417
- **Real-time Detection**: Live camera feed with instant recognition
- **Auto-lookup**: Automatic product search when barcodes are detected

### Profit Analysis
Advanced profit calculation includes:
- **Per-sale Profit**: (Selling Price - Cost Price) × Quantity
- **Product Profitability**: Total profit per product
- **Category Analysis**: Profit breakdown by product categories
- **Trend Analysis**: Profit trends over time

### Data Export
Professional Excel exports with:
- **Multiple Sheets**: Separate sheets for different data views
- **Formatted Data**: Proper currency formatting and alignment
- **Summary Statistics**: Key metrics and totals
- **Chart Integration**: Include charts in exports (future feature)

## 🔒 Security Features

- **Input Validation**: All user inputs are validated
- **SQL Injection Protection**: Parameterized queries
- **Error Handling**: Comprehensive error handling and user feedback
- **Data Integrity**: Foreign key constraints and data validation

## 🚧 Troubleshooting

### Common Issues

#### Camera Not Working
- **Check Permissions**: Ensure camera access is allowed
- **Driver Issues**: Update camera drivers
- **Alternative Camera**: Try different camera device in settings

#### Database Errors
- **File Permissions**: Check write permissions in application directory
- **Corrupted Database**: Use backup/restore functionality
- **Disk Space**: Ensure sufficient disk space

#### Import Errors
- **Dependencies**: Ensure all requirements are installed
- **Python Version**: Use Python 3.8 or higher
- **Virtual Environment**: Activate virtual environment before running

### Performance Tips
- **Regular Backups**: Schedule automatic database backups
- **Database Maintenance**: Run optimization tools periodically
- **Image Resolution**: Use appropriate camera resolution for scanning
- **Memory Management**: Close unused tabs to free memory

## 🔄 Updates and Maintenance

### Regular Maintenance
- **Database Optimization**: Run monthly database optimization
- **Backup Verification**: Test backup restoration periodically
- **Log Review**: Check application logs for errors
- **Performance Monitoring**: Monitor application performance

### Future Enhancements
- **Cloud Sync**: Synchronize data across multiple devices
- **Mobile App**: Companion mobile application
- **Advanced Analytics**: Machine learning insights
- **Multi-language**: Internationalization support
- **API Integration**: Connect with external systems

## 📞 Support

### Getting Help
1. **Documentation**: Check this README first
2. **Error Messages**: Note exact error messages
3. **System Info**: Include OS and Python version
4. **Steps to Reproduce**: Document steps leading to issue

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PyQt5**: Modern Python GUI framework
- **OpenCV**: Computer vision library
- **pyzbar**: Barcode processing library
- **Matplotlib**: Data visualization library
- **Pandas**: Data manipulation library

---

**Built with ❤️ using Python and PyQt5**

*For business use, please ensure compliance with local regulations and data protection laws.*
