# -*- coding: utf-8 -*-

from odoo import models, fields

class ContactCategory(models.Model):
    _name = 'contact.category'
    _description = 'Contact Category'
    
    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string='Color Index')
    parent_id = fields.Many2one('contact.category', string='Parent Category')
    child_ids = fields.One2many('contact.category', 'parent_id', string='Sub-Categories')
    partner_ids = fields.Many2many('res.partner', string='Contacts')
    active = fields.Boolean(string='Active', default=True)
