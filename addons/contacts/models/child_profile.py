# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date

class ChildProfile(models.Model):
    _name = 'child.profile'
    _description = 'Child Profile'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Child Name', required=True, tracking=True)
    parent_id = fields.Many2one('res.partner', string='Parent', required=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Integer(string='Age', compute='_compute_age', store=True)
    gender = fields.Selection([
        ('boy', 'Boy'),
        ('girl', 'Girl'),
        ('other', 'Other'),
    ], string='Gender', required=True)
    
    age_group = fields.Selection([
        ('newborn', 'Newborn (0-3 months)'),
        ('infant', 'Infant (3-12 months)'),
        ('toddler', 'Toddler (1-3 years)'),
        ('preschool', 'Preschool (3-5 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (13-18 years)'),
    ], string='Age Group', compute='_compute_age_group', store=True)
    
    current_height = fields.Float(string='Current Height (cm)')
    current_weight = fields.Float(string='Current Weight (kg)')
    clothing_size = fields.Char(string='Clothing Size')
    shoe_size = fields.Char(string='Shoe Size')
    
    favorite_colors = fields.Char(string='Favorite Colors')
    favorite_brands = fields.Many2many('product.brand', string='Favorite Brands')
    preferred_styles = fields.Char(string='Preferred Styles')
    
    allergies = fields.Text(string='Allergies/Sensitivities')
    special_notes = fields.Text(string='Special Notes')
    
    photo = fields.Binary(string='Photo')
    
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='active')
    
    @api.depends('date_of_birth')
    def _compute_age(self):
        for record in self:
            if record.date_of_birth:
                today = date.today()
                dob = fields.Date.from_string(record.date_of_birth)
                record.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            else:
                record.age = 0
    
    @api.depends('age')
    def _compute_age_group(self):
        for record in self:
            age = record.age
            if age < 0.25:  # 0-3 months
                record.age_group = 'newborn'
            elif age < 1:  # 3-12 months
                record.age_group = 'infant'
            elif age < 3:  # 1-3 years
                record.age_group = 'toddler'
            elif age < 5:  # 3-5 years
                record.age_group = 'preschool'
            elif age < 13:  # 6-12 years
                record.age_group = 'school_age'
            else:  # 13+ years
                record.age_group = 'teen'
