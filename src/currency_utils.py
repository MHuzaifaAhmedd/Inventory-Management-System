"""
Currency Utilities Module
Handles currency formatting and conversion for different regions
"""

from PyQt5.QtCore import QSettings

class CurrencyManager:
    """Manages currency settings and formatting"""
    
    def __init__(self):
        self.settings = QSettings('InventoryCorp', 'InventoryManagementSystem')
        self.currencies = {
            0: {"code": "USD", "symbol": "$", "name": "US Dollar", "locale": "en_US"},
            1: {"code": "EUR", "symbol": "€", "name": "Euro", "locale": "en_EU"},
            2: {"code": "GBP", "symbol": "£", "name": "British Pound", "locale": "en_GB"},
            3: {"code": "CAD", "symbol": "C$", "name": "Canadian Dollar", "locale": "en_CA"},
            4: {"code": "AUD", "symbol": "A$", "name": "Australian Dollar", "locale": "en_AU"},
            5: {"code": "PKR", "symbol": "₨", "name": "Pakistani Rupee", "locale": "en_PK"}
        }
    
    def get_current_currency(self):
        """Get the currently selected currency"""
        currency_index = self.settings.value('currency/type', 0, type=int)
        return self.currencies.get(currency_index, self.currencies[0])
    
    def get_currency_symbol(self):
        """Get the current currency symbol"""
        return self.get_current_currency()["symbol"]
    
    def get_currency_code(self):
        """Get the current currency code"""
        return self.get_current_currency()["code"]
    
    def get_currency_name(self):
        """Get the current currency name"""
        return self.get_current_currency()["name"]
    
    def get_decimal_places(self):
        """Get the number of decimal places for the current currency"""
        return self.settings.value('currency/decimal_places', 2, type=int)
    
    def format_currency(self, amount, show_symbol=True, show_code=False):
        """
        Format a monetary amount according to current currency settings
        
        Args:
            amount (float): The amount to format
            show_symbol (bool): Whether to show the currency symbol
            show_code (bool): Whether to show the currency code
            
        Returns:
            str: Formatted currency string
        """
        try:
            amount = float(amount)
            decimal_places = self.get_decimal_places()
            
            # Format the number
            if decimal_places == 0:
                formatted_amount = f"{int(amount):,}"
            else:
                formatted_amount = f"{amount:,.{decimal_places}f}"
            
            # Add currency symbol/code
            if show_symbol and show_code:
                return f"{self.get_currency_symbol()} {formatted_amount} ({self.get_currency_code()})"
            elif show_symbol:
                return f"{self.get_currency_symbol()}{formatted_amount}"
            elif show_code:
                return f"{formatted_amount} {self.get_currency_code()}"
            else:
                return formatted_amount
                
        except (ValueError, TypeError):
            return "0"
    
    def get_currency_options(self):
        """Get list of currency options for the combo box"""
        return [f"{currency['code']} ({currency['symbol']})" for currency in self.currencies.values()]
    
    def get_currency_by_index(self, index):
        """Get currency info by index"""
        return self.currencies.get(index, self.currencies[0])

# Global instance
currency_manager = CurrencyManager()

# Convenience functions
def format_currency(amount, show_symbol=True, show_code=False):
    """Format currency using the global currency manager"""
    return currency_manager.format_currency(amount, show_symbol, show_code)

def get_currency_symbol():
    """Get current currency symbol"""
    return currency_manager.get_currency_symbol()

def get_currency_code():
    """Get current currency code"""
    return currency_manager.get_currency_code()
