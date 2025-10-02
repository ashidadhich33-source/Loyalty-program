# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import json
import datetime
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)


class SystemUtils(models.AbstractModel):
    """System utilities for Kids Clothing ERP"""
    
    _name = 'system.utils'
    _description = 'System Utilities'
    
    @api.model
    def get_age_group_from_months(self, months):
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
    
    @api.model
    def get_age_group_from_birth_date(self, birth_date):
        """Get age group from birth date"""
        if not birth_date:
            return 'newborn'
        
        today = fields.Date.today()
        age_months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
        
        return self.get_age_group_from_months(age_months)
    
    @api.model
    def calculate_age_in_months(self, birth_date):
        """Calculate age in months from birth date"""
        if not birth_date:
            return 0
        
        today = fields.Date.today()
        age_months = (today.year - birth_date.year) * 12 + (today.month - birth_date.month)
        
        return age_months
    
    @api.model
    def get_season_from_date(self, date=None):
        """Get season from date (defaults to today)"""
        if not date:
            date = fields.Date.today()
        
        month = date.month
        
        if month in [3, 4, 5]:  # March, April, May
            return 'summer'
        elif month in [6, 7, 8, 9]:  # June, July, August, September
            return 'monsoon'
        elif month in [10, 11, 12, 1, 2]:  # October, November, December, January, February
            return 'winter'
        else:
            return 'all_season'
    
    @api.model
    def get_size_recommendation(self, age_months, gender='unisex'):
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
    
    @api.model
    def generate_barcode(self, prefix='KC', length=10):
        """Generate unique barcode for products"""
        import random
        import string
        
        # Generate random string
        random_part = ''.join(random.choices(string.digits, k=length-len(prefix)))
        barcode = prefix + random_part
        
        # Check if barcode already exists
        existing = self.env['product.template'].search([('barcode', '=', barcode)], limit=1)
        if existing:
            return self.generate_barcode(prefix, length)
        
        return barcode
    
    @api.model
    def validate_gst_number(self, gst_number):
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
    
    @api.model
    def validate_pan_number(self, pan_number):
        """Validate Indian PAN number format"""
        if not pan_number:
            return False
        
        # PAN format: 5 letters + 4 digits + 1 letter
        if len(pan_number) != 10:
            return False
        
        if not (pan_number[:5].isalpha() and pan_number[5:9].isdigit() and pan_number[9:10].isalpha()):
            return False
        
        return True
    
    @api.model
    def validate_mobile_number(self, mobile_number):
        """Validate Indian mobile number format"""
        if not mobile_number:
            return False
        
        # Remove any non-digit characters
        mobile_clean = ''.join(filter(str.isdigit, mobile_number))
        
        # Indian mobile numbers are 10 digits starting with 6, 7, 8, or 9
        if len(mobile_clean) == 10 and mobile_clean[0] in '6789':
            return True
        
        return False
    
    @api.model
    def format_mobile_number(self, mobile_number):
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
    
    @api.model
    def get_currency_symbol(self, currency_code):
        """Get currency symbol from currency code"""
        currency_symbols = {
            'INR': '₹',
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'JPY': '¥',
        }
        
        return currency_symbols.get(currency_code, currency_code)
    
    @api.model
    def format_currency(self, amount, currency_code='INR'):
        """Format currency amount with symbol"""
        symbol = self.get_currency_symbol(currency_code)
        return f"{symbol} {amount:,.2f}"
    
    @api.model
    def calculate_discount(self, list_price, discount_percent):
        """Calculate discount amount and final price"""
        discount_amount = (list_price * discount_percent) / 100
        final_price = list_price - discount_amount
        
        return {
            'original_price': list_price,
            'discount_percent': discount_percent,
            'discount_amount': discount_amount,
            'final_price': final_price,
        }
    
    @api.model
    def calculate_age_based_discount(self, age_months, base_discount=0):
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
    
    @api.model
    def generate_loyalty_points(self, order_amount, points_per_rupee=1):
        """Generate loyalty points based on order amount"""
        return int(order_amount * points_per_rupee)
    
    @api.model
    def calculate_loyalty_discount(self, loyalty_points, points_per_rupee=1):
        """Calculate discount from loyalty points"""
        return loyalty_points / points_per_rupee
    
    @api.model
    def get_stock_status(self, quantity, min_quantity=0):
        """Get stock status based on quantity"""
        if quantity <= 0:
            return 'out_of_stock'
        elif quantity <= min_quantity:
            return 'low_stock'
        else:
            return 'in_stock'
    
    @api.model
    def send_notification(self, message, notification_type='info', user_ids=None):
        """Send notification to users"""
        if not user_ids:
            user_ids = [self.env.user.id]
        
        notification_vals = {
            'message': message,
            'type': notification_type,
            'user_ids': [(6, 0, user_ids)],
        }
        
        self.env['mail.notification'].create(notification_vals)
    
    @api.model
    def log_activity(self, model_name, record_id, activity_type, description):
        """Log activity for audit trail"""
        activity_vals = {
            'model_name': model_name,
            'record_id': record_id,
            'activity_type': activity_type,
            'description': description,
            'user_id': self.env.user.id,
            'date': fields.Datetime.now(),
        }
        
        self.env['activity.log'].create(activity_vals)