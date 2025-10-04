# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class HrDepartment(models.Model):
    _name = 'hr.department'
    _description = 'Department'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char(
        string='Department Name',
        required=True,
        tracking=True
    )
    code = fields.Char(
        string='Department Code',
        required=True,
        help='Unique code for this department'
    )
    description = fields.Text(
        string='Description',
        help='Description of this department'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    
    # Hierarchy
    parent_id = fields.Many2one(
        'hr.department',
        string='Parent Department'
    )
    child_ids = fields.One2many(
        'hr.department',
        'parent_id',
        string='Sub Departments'
    )
    
    # Manager Information
    manager_id = fields.Many2one(
        'hr.employee',
        string='Department Manager'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group focus for this department')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season Specialization', help='Season specialization for this department')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Primary brands this department focuses on'
    )
    
    # Department Status
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Additional Fields
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this department'
    )
    
    # Computed Fields
    employee_count = fields.Integer(
        string='Employee Count',
        compute='_compute_employee_count'
    )
    
    @api.depends('name')
    def _compute_employee_count(self):
        for department in self:
            department.employee_count = self.env['hr.employee'].search_count([
                ('department_id', '=', department.id),
                ('active', '=', True)
            ])
    
    @api.constrains('code')
    def _check_code(self):
        for department in self:
            if self.search([('code', '=', department.code), ('id', '!=', department.id)]):
                raise ValidationError(_('Department code must be unique.'))
    
    @api.constrains('parent_id')
    def _check_parent_id(self):
        for department in self:
            if department.parent_id == department:
                raise ValidationError(_('A department cannot be its own parent.'))
    
    @api.model
    def get_department(self, age_group=None, season=None):
        """Get appropriate department based on criteria"""
        domain = [
            ('active', '=', True),
            ('company_id', '=', self.env.company.id)
        ]
        
        if age_group:
            domain.append('|')
            domain.append(('age_group_focus', '=', age_group))
            domain.append(('age_group_focus', '=', 'all'))
        
        if season:
            domain.append('|')
            domain.append(('season_specialization', '=', season))
            domain.append(('season_specialization', '=', 'all_season'))
        
        department = self.search(domain, limit=1)
        if not department:
            # Fallback to default department
            department = self.search([
                ('active', '=', True),
                ('company_id', '=', self.env.company.id)
            ], limit=1)
        
        return department