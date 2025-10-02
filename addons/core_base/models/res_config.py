# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ResConfigSettings(models.TransientModel):
    """System configuration settings for Kids Clothing ERP"""
    
    _name = 'res.config.settings'
    _inherit = 'res.config.settings'
    _description = 'System Configuration Settings'
    
    # Company Information
    company_name = fields.Char(
        string='Company Name',
        related='company_id.name',
        readonly=False,
        help='Name of the company'
    )
    
    company_currency = fields.Many2one(
        'res.currency',
        string='Company Currency',
        related='company_id.currency_id',
        readonly=False,
        help='Default currency for the company'
    )
    
    # Kids Clothing Specific Settings
    enable_child_profiles = fields.Boolean(
        string='Enable Child Profiles',
        default=True,
        help='Enable child profile management for customers'
    )
    
    enable_age_based_discounts = fields.Boolean(
        string='Enable Age-based Discounts',
        default=True,
        help='Enable automatic discounts based on child age'
    )
    
    enable_loyalty_program = fields.Boolean(
        string='Enable Loyalty Program',
        default=True,
        help='Enable customer loyalty points and rewards'
    )
    
    enable_exchange_system = fields.Boolean(
        string='Enable Exchange System',
        default=True,
        help='Enable product exchange functionality'
    )
    
    # Inventory Settings
    enable_multi_location = fields.Boolean(
        string='Enable Multi-location Inventory',
        default=True,
        help='Enable multiple warehouse locations'
    )
    
    enable_stock_aging = fields.Boolean(
        string='Enable Stock Aging',
        default=True,
        help='Enable stock aging and expiry tracking'
    )
    
    # POS Settings
    enable_touchscreen_mode = fields.Boolean(
        string='Enable Touchscreen Mode',
        default=True,
        help='Enable touchscreen-friendly POS interface'
    )
    
    enable_barcode_scanning = fields.Boolean(
        string='Enable Barcode Scanning',
        default=True,
        help='Enable barcode scanning in POS'
    )
    
    # Indian Localization Settings
    enable_gst = fields.Boolean(
        string='Enable GST',
        default=True,
        help='Enable GST compliance features'
    )
    
    enable_e_invoice = fields.Boolean(
        string='Enable E-invoice',
        default=True,
        help='Enable E-invoice generation'
    )
    
    enable_e_way_bill = fields.Boolean(
        string='Enable E-way Bill',
        default=True,
        help='Enable E-way bill generation'
    )
    
    # Notification Settings
    enable_sms_notifications = fields.Boolean(
        string='Enable SMS Notifications',
        default=True,
        help='Enable SMS notifications for customers'
    )
    
    enable_email_notifications = fields.Boolean(
        string='Enable Email Notifications',
        default=True,
        help='Enable email notifications'
    )
    
    enable_whatsapp_notifications = fields.Boolean(
        string='Enable WhatsApp Notifications',
        default=True,
        help='Enable WhatsApp notifications'
    )
    
    @api.model
    def get_values(self):
        """Get configuration values"""
        res = super(ResConfigSettings, self).get_values()
        
        # Get system parameters
        params = self.env['ir.config_parameter'].sudo()
        
        res.update(
            enable_child_profiles=params.get_param('core_base.enable_child_profiles', 'True') == 'True',
            enable_age_based_discounts=params.get_param('core_base.enable_age_based_discounts', 'True') == 'True',
            enable_loyalty_program=params.get_param('core_base.enable_loyalty_program', 'True') == 'True',
            enable_exchange_system=params.get_param('core_base.enable_exchange_system', 'True') == 'True',
            enable_multi_location=params.get_param('core_base.enable_multi_location', 'True') == 'True',
            enable_stock_aging=params.get_param('core_base.enable_stock_aging', 'True') == 'True',
            enable_touchscreen_mode=params.get_param('core_base.enable_touchscreen_mode', 'True') == 'True',
            enable_barcode_scanning=params.get_param('core_base.enable_barcode_scanning', 'True') == 'True',
            enable_gst=params.get_param('core_base.enable_gst', 'True') == 'True',
            enable_e_invoice=params.get_param('core_base.enable_e_invoice', 'True') == 'True',
            enable_e_way_bill=params.get_param('core_base.enable_e_way_bill', 'True') == 'True',
            enable_sms_notifications=params.get_param('core_base.enable_sms_notifications', 'True') == 'True',
            enable_email_notifications=params.get_param('core_base.enable_email_notifications', 'True') == 'True',
            enable_whatsapp_notifications=params.get_param('core_base.enable_whatsapp_notifications', 'True') == 'True',
        )
        
        return res
    
    def set_values(self):
        """Set configuration values"""
        super(ResConfigSettings, self).set_values()
        
        # Set system parameters
        params = self.env['ir.config_parameter'].sudo()
        
        params.set_param('core_base.enable_child_profiles', str(self.enable_child_profiles))
        params.set_param('core_base.enable_age_based_discounts', str(self.enable_age_based_discounts))
        params.set_param('core_base.enable_loyalty_program', str(self.enable_loyalty_program))
        params.set_param('core_base.enable_exchange_system', str(self.enable_exchange_system))
        params.set_param('core_base.enable_multi_location', str(self.enable_multi_location))
        params.set_param('core_base.enable_stock_aging', str(self.enable_stock_aging))
        params.set_param('core_base.enable_touchscreen_mode', str(self.enable_touchscreen_mode))
        params.set_param('core_base.enable_barcode_scanning', str(self.enable_barcode_scanning))
        params.set_param('core_base.enable_gst', str(self.enable_gst))
        params.set_param('core_base.enable_e_invoice', str(self.enable_e_invoice))
        params.set_param('core_base.enable_e_way_bill', str(self.enable_e_way_bill))
        params.set_param('core_base.enable_sms_notifications', str(self.enable_sms_notifications))
        params.set_param('core_base.enable_email_notifications', str(self.enable_email_notifications))
        params.set_param('core_base.enable_whatsapp_notifications', str(self.enable_whatsapp_notifications))
    
    @api.model
    def get_system_info(self):
        """Get system information"""
        return {
            'version': '1.0.0',
            'modules_installed': len(self.env['ir.module.module'].search([('state', '=', 'installed')])),
            'users_count': self.env['res.users'].search_count([]),
            'companies_count': self.env['res.company'].search_count([]),
        }