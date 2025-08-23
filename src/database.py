"""
Database Management Module
Handles all database operations for the inventory system
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class DatabaseManager:
    def __init__(self, db_path: str = "inventory.db"):
        """Initialize database connection"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create products table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                barcode TEXT UNIQUE,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                cost_price REAL NOT NULL,
                selling_price REAL NOT NULL,
                quantity INTEGER DEFAULT 0,
                min_quantity INTEGER DEFAULT 0,
                created_date TEXT,
                updated_date TEXT
            )
        ''')
        
        # Create sales table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_amount REAL NOT NULL,
                sale_date TEXT,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Create purchases table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                quantity INTEGER NOT NULL,
                unit_cost REAL NOT NULL,
                total_cost REAL NOT NULL,
                purchase_date TEXT,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_product(self, product_data: Dict) -> bool:
        """Add a new product to the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO products (barcode, name, description, category, 
                                   cost_price, selling_price, quantity, min_quantity, 
                                   created_date, updated_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                product_data.get('barcode'),
                product_data.get('name'),
                product_data.get('description', ''),
                product_data.get('category', ''),
                product_data.get('cost_price'),
                product_data.get('selling_price'),
                product_data.get('quantity', 0),
                product_data.get('min_quantity', 0),
                datetime.now().isoformat(),
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding product: {e}")
            return False
    
    def get_product_by_barcode(self, barcode: str) -> Optional[Dict]:
        """Get product by barcode"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM products WHERE barcode = ?', (barcode,))
            row = cursor.fetchone()
            
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'barcode': row[1],
                    'name': row[2],
                    'description': row[3],
                    'category': row[4],
                    'cost_price': row[5],
                    'selling_price': row[6],
                    'quantity': row[7],
                    'min_quantity': row[8],
                    'created_date': row[9],
                    'updated_date': row[10]
                }
            return None
        except Exception as e:
            print(f"Error getting product: {e}")
            return None
    
    def update_product_quantity(self, product_id: int, new_quantity: int) -> bool:
        """Update product quantity"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE products 
                SET quantity = ?, updated_date = ?
                WHERE id = ?
            ''', (new_quantity, datetime.now().isoformat(), product_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating quantity: {e}")
            return False
    
    def add_sale(self, product_id: int, quantity: int, unit_price: float) -> bool:
        """Record a sale transaction"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            total_amount = quantity * unit_price
            
            # Add sale record
            cursor.execute('''
                INSERT INTO sales (product_id, quantity, unit_price, total_amount, sale_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (product_id, quantity, unit_price, total_amount, datetime.now().isoformat()))
            
            # Update product quantity
            cursor.execute('SELECT quantity FROM products WHERE id = ?', (product_id,))
            current_quantity = cursor.fetchone()[0]
            new_quantity = current_quantity - quantity
            
            cursor.execute('''
                UPDATE products 
                SET quantity = ?, updated_date = ?
                WHERE id = ?
            ''', (new_quantity, datetime.now().isoformat(), product_id))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding sale: {e}")
            return False
    
    def get_all_products(self) -> List[Dict]:
        """Get all products"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM products ORDER BY name')
            rows = cursor.fetchall()
            
            conn.close()
            
            products = []
            for row in rows:
                products.append({
                    'id': row[0],
                    'barcode': row[1],
                    'name': row[2],
                    'description': row[3],
                    'category': row[4],
                    'cost_price': row[5],
                    'selling_price': row[6],
                    'quantity': row[7],
                    'min_quantity': row[8],
                    'created_date': row[9],
                    'updated_date': row[10]
                })
            
            return products
        except Exception as e:
            print(f"Error getting products: {e}")
            return []
    
    def get_sales_report(self, start_date: str = None, end_date: str = None) -> List[Tuple]:
        """Get sales report data as tuples for compatibility with reports"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if start_date and end_date:
                cursor.execute('''
                    SELECT s.id, s.product_id, s.quantity, s.unit_price, s.total_amount, 
                           s.sale_date, p.name, p.cost_price
                    FROM sales s
                    JOIN products p ON s.product_id = p.id
                    WHERE s.sale_date BETWEEN ? AND ?
                    ORDER BY s.sale_date DESC
                ''', (start_date, end_date))
            else:
                cursor.execute('''
                    SELECT s.id, s.product_id, s.quantity, s.unit_price, s.total_amount, 
                           s.sale_date, p.name, p.cost_price
                    FROM sales s
                    JOIN products p ON s.product_id = p.id
                    ORDER BY s.sale_date DESC
                ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            # Return raw rows as tuples for compatibility with reports
            return rows
        except Exception as e:
            print(f"Error getting sales report: {e}")
            return []
    
    def get_sales_data(self, start_date: str = None, end_date: str = None) -> List[Dict]:
        """Get sales data as dictionaries for sales tab compatibility"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if start_date and end_date:
                cursor.execute('''
                    SELECT s.id, s.product_id, s.quantity, s.unit_price, s.total_amount, 
                           s.sale_date, p.name, p.cost_price
                    FROM sales s
                    JOIN products p ON s.product_id = p.id
                    WHERE s.sale_date BETWEEN ? AND ?
                    ORDER BY s.sale_date DESC
                ''', (start_date, end_date))
            else:
                cursor.execute('''
                    SELECT s.id, s.product_id, s.quantity, s.unit_price, s.total_amount, 
                           s.sale_date, p.name, p.cost_price
                    FROM sales s
                    JOIN products p ON s.product_id = p.id
                    ORDER BY s.sale_date DESC
                ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            sales = []
            for row in rows:
                cost_price = row[7] or 0
                profit = (row[3] - cost_price) * row[2]  # (unit_price - cost_price) * quantity
                
                sales.append({
                    'id': row[0],
                    'product_id': row[1],
                    'quantity': row[2],
                    'unit_price': row[3],
                    'total_price': row[4],  # Using total_price key for compatibility
                    'sale_date': row[5],
                    'product_name': row[6],
                    'cost_price': cost_price,
                    'profit': profit
                })
            
            return sales
        except Exception as e:
            print(f"Error getting sales data: {e}")
            return []
    
    def get_low_stock_products(self) -> List[Dict]:
        """Get products with low stock"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM products 
                WHERE quantity <= min_quantity AND min_quantity > 0
                ORDER BY quantity ASC
            ''')
            
            rows = cursor.fetchall()
            conn.close()
            
            products = []
            for row in rows:
                products.append({
                    'id': row[0],
                    'barcode': row[1],
                    'name': row[2],
                    'description': row[3],
                    'category': row[4],
                    'cost_price': row[5],
                    'selling_price': row[6],
                    'quantity': row[7],
                    'min_quantity': row[8],
                    'created_date': row[9],
                    'updated_date': row[10]
                })
            
            return products
        except Exception as e:
            print(f"Error getting low stock products: {e}")
            return []
    
    def get_product_by_name(self, product_name: str) -> Dict:
        """Get product by name"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM products WHERE name = ?
            ''', (product_name,))
            
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return {
                    'id': row[0],
                    'barcode': row[1],
                    'name': row[2],
                    'description': row[3],
                    'category': row[4],
                    'cost_price': row[5],
                    'selling_price': row[6],
                    'quantity': row[7],
                    'min_quantity': row[8],
                    'created_date': row[9],
                    'updated_date': row[10]
                }
            return None
        except Exception as e:
            print(f"Error getting product by name: {e}")
            return None
    
    def update_product(self, product_data: Dict) -> bool:
        """Update an existing product"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE products 
                SET name = ?, description = ?, category = ?, cost_price = ?, 
                    selling_price = ?, quantity = ?, min_quantity = ?, updated_date = ?
                WHERE id = ?
            ''', (
                product_data.get('name'),
                product_data.get('description', ''),
                product_data.get('category', ''),
                product_data.get('cost_price'),
                product_data.get('selling_price'),
                product_data.get('quantity', 0),
                product_data.get('min_quantity', 0),
                datetime.now().isoformat(),
                product_data.get('id')
            ))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating product: {e}")
            return False
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error deleting product: {e}")
            return False
    
    def close(self):
        """Close database connections"""
        pass  # SQLite connections are closed after each operation
