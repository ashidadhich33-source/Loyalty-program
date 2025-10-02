# -*- coding: utf-8 -*-

from odoo import models, fields

class ContactAddress(models.Model):
    _name = 'contact.address'
    _description = 'Contact Address'
    
    name = fields.Char(string='Address Name', required=True)
    contact_id = fields.Many2one('res.partner', string='Contact', required=True)
    address_type = fields.Selection([
        ('billing', 'Billing'),
        ('shipping', 'Shipping'),
        ('both', 'Billing & Shipping'),
        ('other', 'Other'),
    ], string='Address Type', required=True, default='both')
    street = fields.Char(string='Street')
    street2 = fields.Char(string='Street2')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    zip = fields.Char(string='ZIP')
    country_id = fields.Many2one('res.country', string='Country')
    is_primary = fields.Boolean(string='Primary Address')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
