# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContactAnalytics(models.Model):
    _name = 'contact.analytics'
    _description = 'Contact Analytics'
    _rec_name = 'contact_id'
    
    contact_id = fields.Many2one('res.partner', string='Contact', required=True)
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    
    # Sales Analytics
    total_orders = fields.Integer(string='Total Orders')
    total_sales = fields.Float(string='Total Sales')
    average_order_value = fields.Float(string='Average Order Value')
    last_order_date = fields.Date(string='Last Order Date')
    
    # Purchase Analytics
    total_purchases = fields.Integer(string='Total Purchases')
    total_purchase_value = fields.Float(string='Total Purchase Value')
    average_purchase_value = fields.Float(string='Average Purchase Value')
    last_purchase_date = fields.Date(string='Last Purchase Date')
    
    # Engagement Analytics
    total_interactions = fields.Integer(string='Total Interactions')
    last_interaction_date = fields.Date(string='Last Interaction Date')
    engagement_score = fields.Float(string='Engagement Score')
    
    # Customer Lifetime Value
    lifetime_value = fields.Float(string='Lifetime Value')
    predicted_ltv = fields.Float(string='Predicted LTV')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
