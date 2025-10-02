# -*- coding: utf-8 -*-

from odoo import models, fields

class ContactCommunication(models.Model):
    _name = 'contact.communication'
    _description = 'Contact Communication'
    _order = 'date desc'
    
    name = fields.Char(string='Subject', required=True)
    contact_id = fields.Many2one('res.partner', string='Contact', required=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now, required=True)
    communication_type = fields.Selection([
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('whatsapp', 'WhatsApp'),
        ('call', 'Phone Call'),
        ('letter', 'Letter'),
    ], string='Type', required=True)
    direction = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ], string='Direction', required=True)
    message = fields.Text(string='Message')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read'),
        ('failed', 'Failed'),
    ], string='Status', default='draft')
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
