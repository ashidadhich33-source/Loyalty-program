# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Core Base - Configuration Settings
====================================================

Standalone version of the configuration settings model.
"""

from core_framework.orm import BaseModel, CharField, BooleanField, Many2OneField, IntegerField, FloatField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class ResConfigSettings(BaseModel):
    """System configuration settings for Kids Clothing ERP"""
    
    _name = 'res.config.settings'
    _description = 'System Configuration Settings'
    _table = 'res_config_settings'
    
    # Company Information
    company_name = CharField(
        string='Company Name',
        size=255,
        help='Name of the company'
    )
    
    company_currency_id = IntegerField(
        string='Company Currency ID',
        help='Default currency for the company'
    )
    
    # Kids Clothing Specific Settings
    enable_child_profiles = BooleanField(
        string='Enable Child Profiles',
        default=True,
        help='Enable child profile management for customers'
    )
    
    enable_age_based_discounts = BooleanField(
        string='Enable Age-based Discounts',
        default=True,
        help='Enable automatic discounts based on child age'
    )
    
    enable_loyalty_program = BooleanField(
        string='Enable Loyalty Program',
        default=True,
        help='Enable customer loyalty points and rewards'
    )
    
    enable_exchange_system = BooleanField(
        string='Enable Exchange System',
        default=True,
        help='Enable product exchange functionality'
    )
    
    # Inventory Settings
    enable_multi_location = BooleanField(
        string='Enable Multi-location Inventory',
        default=True,
        help='Enable multiple warehouse locations'
    )
    
    enable_stock_aging = BooleanField(
        string='Enable Stock Aging',
        default=True,
        help='Enable stock aging and expiry tracking'
    )
    
    # POS Settings
    enable_touchscreen_mode = BooleanField(
        string='Enable Touchscreen Mode',
        default=True,
        help='Enable touchscreen-friendly POS interface'
    )
    
    enable_barcode_scanning = BooleanField(
        string='Enable Barcode Scanning',
        default=True,
        help='Enable barcode scanning in POS'
    )
    
    # Indian Localization Settings
    enable_gst = BooleanField(
        string='Enable GST',
        default=True,
        help='Enable GST compliance features'
    )
    
    enable_e_invoice = BooleanField(
        string='Enable E-invoice',
        default=True,
        help='Enable E-invoice generation'
    )
    
    enable_e_way_bill = BooleanField(
        string='Enable E-way Bill',
        default=True,
        help='Enable E-way bill generation'
    )
    
    # Notification Settings
    enable_sms_notifications = BooleanField(
        string='Enable SMS Notifications',
        default=True,
        help='Enable SMS notifications for customers'
    )
    
    enable_email_notifications = BooleanField(
        string='Enable Email Notifications',
        default=True,
        help='Enable email notifications'
    )
    
    enable_whatsapp_notifications = BooleanField(
        string='Enable WhatsApp Notifications',
        default=True,
        help='Enable WhatsApp notifications'
    )
    
    def get_values(self):
        """Get configuration values"""
        # In standalone version, we'll get values from database
        # This is a simplified version - in real implementation,
        # we'd have a proper configuration system
        return {
            'enable_child_profiles': True,
            'enable_age_based_discounts': True,
            'enable_loyalty_program': True,
            'enable_exchange_system': True,
            'enable_multi_location': True,
            'enable_stock_aging': True,
            'enable_touchscreen_mode': True,
            'enable_barcode_scanning': True,
            'enable_gst': True,
            'enable_e_invoice': True,
            'enable_e_way_bill': True,
            'enable_sms_notifications': True,
            'enable_email_notifications': True,
            'enable_whatsapp_notifications': True,
        }
    
    def set_values(self, values: Dict[str, Any]):
        """Set configuration values"""
        # In standalone version, we'll save values to database
        # This is a simplified version - in real implementation,
        # we'd have a proper configuration system
        logger.info(f"Setting configuration values: {values}")
        return True
    
    def get_system_info(self):
        """Get system information"""
        return {
            'version': '1.0.0',
            'modules_installed': 0,  # Will be updated when addon system is ready
            'users_count': 0,        # Will be updated when user system is ready
            'companies_count': 0,   # Will be updated when company system is ready
        }