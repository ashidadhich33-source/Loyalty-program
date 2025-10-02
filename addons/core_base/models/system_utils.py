# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Core Base - System Utilities
===============================================

Standalone version of the system utilities for Kids Clothing ERP.
"""

from core_framework.orm import BaseModel, CharField, IntegerField, FloatField, BooleanField
from core_framework.orm import Field
from typing import Dict, Any, Optional, List, Tuple
import logging
import json
import datetime
from dateutil.relativedelta import relativedelta
import random
import string

logger = logging.getLogger(__name__)

class SystemUtils(BaseModel):
    """System utilities for Kids Clothing ERP"""
    
    _name = 'system.utils'
    _description = 'System Utilities'
    
    def get_age_group_from_months(self, months: int) -> str:
        """Get age group from age in months"""
        if months <= 6:
            return 'newborn'
        elif months <= 12:
            return 'infant'
        elif months <= 36:
            return 'toddler'
        elif months <= 60:
            return 'preschool'
        elif months <= 144:
            return 'school'
        else:
            return 'teen'
    
    def get_age_group_from_birth_date(self, birth_date: datetime.date) -> str:
        """Get age group from birth date"""
        if not birth_date:
            return 'newborn'
        
        today = datetime.date.today()
        age_months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
        
        return self.get_age_group_from_months(age_months)
    
    def calculate_age_in_months(self, birth_date: datetime.date) -> int:
        """Calculate age in months from birth date"""
        if not birth_date:
            return 0
        
        today = datetime.date.today()
        age_months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
        
        return age_months
    
    def get_season_from_date(self, date: datetime.date = None) -> str:
        """Get season from date (defaults to today)"""
        if not date:
            date = datetime.date.today()
        
        month = date.month
        
        if month in [3, 4, 5]:  # March, April, May
            return 'summer'
        elif month in [6, 7, 8, 9]:  # June, July, August, September
            return 'monsoon'
        elif month in [10, 11, 12, 1, 2]:  # October, November, December, January, February
            return 'winter'
        else:
            return 'all_season'
    
    def get_size_recommendation(self, age_months: int, gender: str = 'unisex') -> str:
        """Get size recommendation based on age and gender"""
        size_mapping = {
            'newborn': 'XS',
            'infant': 'S',
            'toddler': 'M',
            'preschool': 'L',
            'school': 'XL',
            'teen': 'XXL',
        }
        
        age_group = self.get_age_group_from_months(age_months)
        return size_mapping.get(age_group, 'M')
    
    def generate_barcode(self, prefix: str = 'KC', length: int = 10) -> str:
        """Generate unique barcode for products"""
        # Generate random string
        random_part = ''.join(random.choices(string.digits, k=length-len(prefix)))
        barcode = prefix + random_part
        
        # In real implementation, we'd check if barcode already exists
        # For now, we'll just return the generated barcode
        return barcode
    
    def validate_gst_number(self, gst_number: str) -> bool:
        """Validate Indian GST number format"""
        if not gst_number:
            return False
        
        # GST number format: 2 digits state code + 10 digits PAN + 1 digit entity number + 1 digit Z + 1 digit checksum
        if len(gst_number) != 15:
            return False
        
        if not gst_number.isdigit():
            return False
        
        # Basic format validation
        state_code = gst_number[:2]
        pan_number = gst_number[2:12]
        entity_number = gst_number[12:13]
        z_character = gst_number[13:14]
        checksum = gst_number[14:15]
        
        # Validate state code (01-37)
        if not (1 <= int(state_code) <= 37):
            return False
        
        # Validate PAN format (first 5 letters, next 4 digits, last 1 letter)
        if not (pan_number[:5].isalpha() and pan_number[5:9].isdigit() and pan_number[9:10].isalpha()):
            return False
        
        return True
    
    def validate_pan_number(self, pan_number: str) -> bool:
        """Validate Indian PAN number format"""
        if not pan_number:
            return False
        
        # PAN format: 5 letters + 4 digits + 1 letter
        if len(pan_number) != 10:
            return False
        
        if not (pan_number[:5].isalpha() and pan_number[5:9].isdigit() and pan_number[9:10].isalpha()):
            return False
        
        return True
    
    def validate_mobile_number(self, mobile_number: str) -> bool:
        """Validate Indian mobile number format"""
        if not mobile_number:
            return False
        
        # Remove any non-digit characters
        mobile_clean = ''.join(filter(str.isdigit, mobile_number))
        
        # Indian mobile numbers are 10 digits starting with 6, 7, 8, or 9
        if len(mobile_clean) == 10 and mobile_clean[0] in '6789':
            return True
        
        return False
    
    def format_mobile_number(self, mobile_number: str) -> str:
        """Format mobile number to standard Indian format"""
        if not mobile_number:
            return ''
        
        # Remove any non-digit characters
        mobile_clean = ''.join(filter(str.isdigit, mobile_number))
        
        # Add +91 prefix if not present
        if len(mobile_clean) == 10:
            return '+91' + mobile_clean
        elif len(mobile_clean) == 12 and mobile_clean.startswith('91'):
            return '+' + mobile_clean
        else:
            return mobile_number
    
    def get_currency_symbol(self, currency_code: str) -> str:
        """Get currency symbol from currency code"""
        currency_symbols = {
            'INR': '₹',
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
        }
        
        return currency_symbols.get(currency_code, currency_code)
    
    def format_currency(self, amount: float, currency_code: str = 'INR') -> str:
        """Format currency amount with symbol"""
        symbol = self.get_currency_symbol(currency_code)
        return f"{symbol} {amount:,.2f}"
    
    def calculate_discount(self, list_price: float, discount_percent: float) -> Dict[str, float]:
        """Calculate discount amount and final price"""
        discount_amount = (list_price * discount_percent) / 100
        final_price = list_price - discount_amount
        
        return {
            'original_price': list_price,
            'discount_percent': discount_percent,
            'discount_amount': discount_amount,
            'final_price': final_price,
        }
    
    def calculate_age_based_discount(self, age_months: int, base_discount: float = 0) -> float:
        """Calculate age-based discount for kids clothing"""
        age_group = self.get_age_group_from_months(age_months)
        
        # Age-based discount percentages
        age_discounts = {
            'newborn': 15,  # 15% discount for newborn items
            'infant': 10,   # 10% discount for infant items
            'toddler': 5,   # 5% discount for toddler items
            'preschool': 0, # No additional discount
            'school': 0,    # No additional discount
            'teen': 0,      # No additional discount
        }
        
        additional_discount = age_discounts.get(age_group, 0)
        total_discount = base_discount + additional_discount
        
        return min(total_discount, 50)  # Maximum 50% discount
    
    def generate_loyalty_points(self, order_amount: float, points_per_rupee: int = 1) -> int:
        """Generate loyalty points based on order amount"""
        return int(order_amount * points_per_rupee)
    
    def calculate_loyalty_discount(self, loyalty_points: int, points_per_rupee: int = 1) -> float:
        """Calculate discount from loyalty points"""
        return loyalty_points / points_per_rupee
    
    def get_stock_status(self, quantity: int, min_quantity: int = 0) -> str:
        """Get stock status based on quantity"""
        if quantity <= 0:
            return 'out_of_stock'
        elif quantity <= min_quantity:
            return 'low_stock'
        else:
            return 'in_stock'
    
    def send_notification(self, message: str, notification_type: str = 'info', user_ids: List[int] = None):
        """Send notification to users"""
        if not user_ids:
            user_ids = [1]  # Default to admin user
        
        logger.info(f"Sending notification to users {user_ids}: {message}")
        # In real implementation, we'd create notification records
    
    def log_activity(self, model_name: str, record_id: int, activity_type: str, description: str):
        """Log activity for audit trail"""
        logger.info(f"Activity logged: {model_name} {record_id} - {activity_type}: {description}")
        # In real implementation, we'd create activity log records