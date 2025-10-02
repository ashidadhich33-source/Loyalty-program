# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContactVendor(models.Model):
    _name = 'contact.vendor'
    _description = 'Vendor Contact'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name', required=True, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Related Partner', required=True)
    vendor_code = fields.Char(string='Vendor Code', readonly=True, copy=False)
    vendor_type = fields.Selection([
        ('logistics', 'Logistics'),
        ('packaging', 'Packaging'),
        ('printing', 'Printing'),
        ('marketing', 'Marketing'),
        ('service', 'Service'),
        ('other', 'Other'),
    ], string='Vendor Type', default='service')
    
    vendor_rating = fields.Selection([
        ('1', '1 Star'),
        ('2', '2 Stars'),
        ('3', '3 Stars'),
        ('4', '4 Stars'),
        ('5', '5 Stars'),
    ], string='Vendor Rating')
    
    payment_terms = fields.Many2one('account.payment.term', string='Payment Terms')
    service_areas = fields.Char(string='Service Areas')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('blacklisted', 'Blacklisted'),
    ], string='Status', default='active')
    
    @api.model
    def create(self, vals):
        if not vals.get('vendor_code'):
            vals['vendor_code'] = self.env['ir.sequence'].next_by_code('contact.vendor') or '/'
        return super().create(vals)
