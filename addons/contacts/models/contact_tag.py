# -*- coding: utf-8 -*-

from odoo import models, fields

class ContactTag(models.Model):
    _name = 'contact.tag'
    _description = 'Contact Tag'
    
    name = fields.Char(string='Tag Name', required=True)
    color = fields.Integer(string='Color Index')
    partner_ids = fields.Many2many('res.partner', string='Contacts')
    active = fields.Boolean(string='Active', default=True)
