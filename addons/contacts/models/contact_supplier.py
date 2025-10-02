# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContactSupplier(models.Model):
    _name = 'contact.supplier'
    _description = 'Supplier Contact'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True)
    supplier_code = fields.Char(string='Supplier Code', readonly=True, copy=False)
    supplier_type = fields.Selection([
        ('manufacturer', 'Manufacturer'),
        ('wholesaler', 'Wholesaler'),
        ('distributor', 'Distributor'),
        ('agent', 'Agent'),
    ], string='Supplier Type', default='manufacturer')
    
    supplier_rating = fields.Selection([
        ('1', '1 Star'),
        ('2', '2 Stars'),
        ('3', '3 Stars'),
        ('4', '4 Stars'),
        ('5', '5 Stars'),
    ], string='Supplier Rating')
    
    payment_terms = fields.Many2one('account.payment.term', string='Payment Terms')
    delivery_lead_time = fields.Integer(string='Delivery Lead Time (Days)')
    minimum_order_quantity = fields.Integer(string='Minimum Order Quantity')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    ], string='Status', default='active')
    
    @api.model
    def create(self, vals):
        if not vals.get('supplier_code'):
            vals['supplier_code'] = self.env['ir.sequence'].next_by_code('contact.supplier') or '/'
        return super().create(vals)
