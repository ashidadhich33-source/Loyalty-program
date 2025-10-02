# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ContactHistory(models.Model):
    _name = 'contact.history'
    _description = 'Contact History'
    _order = 'date desc'
    
    name = fields.Char(string='Subject', required=True)
    contact_id = fields.Many2one('res.partner', string='Contact', required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    history_type = fields.Selection([
        ('call', 'Phone Call'),
        ('email', 'Email'),
        ('meeting', 'Meeting'),
        ('note', 'Note'),
        ('order', 'Order'),
        ('payment', 'Payment'),
        ('other', 'Other'),
    ], string='Type', required=True)
    description = fields.Text(string='Description')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
