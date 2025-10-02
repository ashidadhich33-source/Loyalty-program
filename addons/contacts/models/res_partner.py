# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    # Contact Type
    contact_type = fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('vendor', 'Vendor'),
        ('both', 'Customer & Supplier'),
        ('other', 'Other'),
    ], string='Contact Type', default='customer')
    
    # Kids Clothing Specific
    preferred_age_group = fields.Selection([
        ('newborn', 'Newborn (0-3 months)'),
        ('infant', 'Infant (3-12 months)'),
        ('toddler', 'Toddler (1-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (13-18 years)'),
    ], string='Preferred Age Group')
    
    preferred_gender = fields.Selection([
        ('boy', 'Boy'),
        ('girl', 'Girl'),
        ('unisex', 'Unisex'),
    ], string='Preferred Gender')
    
    preferred_brands = fields.Many2many('product.brand', string='Preferred Brands')
    preferred_colors = fields.Char(string='Preferred Colors')
    preferred_styles = fields.Char(string='Preferred Styles')
    
    # Contact Details
    alternate_mobile = fields.Char(string='Alternate Mobile')
    whatsapp_number = fields.Char(string='WhatsApp Number')
    skype_id = fields.Char(string='Skype ID')
    linkedin_url = fields.Char(string='LinkedIn URL')
    facebook_url = fields.Char(string='Facebook URL')
    instagram_url = fields.Char(string='Instagram URL')
    
    # Indian Localization
    gstin = fields.Char(string='GSTIN', size=15)
    pan_number = fields.Char(string='PAN Number', size=10)
    gst_registered = fields.Boolean(string='GST Registered')
    
    # Contact Categories and Tags
    category_ids = fields.Many2many('contact.category', string='Categories')
    tag_ids = fields.Many2many('contact.tag', string='Tags')
    
    # Contact Status
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('prospect', 'Prospect'),
        ('blacklisted', 'Blacklisted'),
    ], string='Status', default='active')
    
    # Contact Rating
    rating = fields.Selection([
        ('1', '1 Star'),
        ('2', '2 Stars'),
        ('3', '3 Stars'),
        ('4', '4 Stars'),
        ('5', '5 Stars'),
    ], string='Rating')
    
    # Contact Analytics
    total_orders = fields.Integer(string='Total Orders', compute='_compute_analytics')
    total_purchases = fields.Float(string='Total Purchases', compute='_compute_analytics')
    last_order_date = fields.Date(string='Last Order Date', compute='_compute_analytics')
    average_order_value = fields.Float(string='Average Order Value', compute='_compute_analytics')
    
    # Relations
    child_profile_ids = fields.One2many('child.profile', 'parent_id', string='Child Profiles')
    history_ids = fields.One2many('contact.history', 'contact_id', string='History')
    communication_ids = fields.One2many('contact.communication', 'contact_id', string='Communications')
    address_ids = fields.One2many('contact.address', 'contact_id', string='Addresses')
    
    # Multi-Company
    company_ids = fields.Many2many('res.company', string='Companies')
    
    @api.depends('sale_order_ids', 'purchase_order_ids')
    def _compute_analytics(self):
        for record in self:
            orders = record.sale_order_ids.filtered(lambda o: o.state in ['sale', 'done'])
            record.total_orders = len(orders)
            record.total_purchases = sum(orders.mapped('amount_total'))
            record.last_order_date = max(orders.mapped('date_order')) if orders else False
            record.average_order_value = record.total_purchases / record.total_orders if record.total_orders else 0
    
    @api.constrains('gstin')
    def _check_gstin(self):
        for record in self:
            if record.gstin and record.gst_registered:
                # Basic GSTIN validation (15 characters)
                if len(record.gstin) != 15:
                    raise ValidationError('GSTIN must be 15 characters long')
    
    @api.constrains('pan_number')
    def _check_pan(self):
        for record in self:
            if record.pan_number:
                # Basic PAN validation (10 characters, format: AAAAA9999A)
                if len(record.pan_number) != 10:
                    raise ValidationError('PAN must be 10 characters long')
