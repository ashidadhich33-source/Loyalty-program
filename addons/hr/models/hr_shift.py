# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class HrShift(models.Model):
    _name = 'hr.shift'
    _description = 'Work Shift'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char(
        string='Shift Name',
        required=True,
        tracking=True
    )
    code = fields.Char(
        string='Shift Code',
        required=True,
        help='Unique code for this shift'
    )
    description = fields.Text(
        string='Description',
        help='Description of this shift'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    
    # Shift Timing
    start_time = fields.Float(
        string='Start Time',
        required=True,
        help='Shift start time (in hours, e.g., 9.5 for 9:30 AM)'
    )
    end_time = fields.Float(
        string='End Time',
        required=True,
        help='Shift end time (in hours, e.g., 18.5 for 6:30 PM)'
    )
    duration = fields.Float(
        string='Duration (Hours)',
        compute='_compute_duration',
        store=True
    )
    
    # Break Information
    break_duration = fields.Float(
        string='Break Duration (Minutes)',
        default=30.0,
        help='Break duration in minutes'
    )
    break_start_time = fields.Float(
        string='Break Start Time',
        help='Break start time (in hours)'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Age group focus for this shift')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season Specialization', help='Season specialization for this shift')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Primary brands this shift focuses on'
    )
    
    # Shift Requirements
    min_employees = fields.Integer(
        string='Minimum Employees',
        default=1,
        help='Minimum number of employees required for this shift'
    )
    max_employees = fields.Integer(
        string='Maximum Employees',
        default=10,
        help='Maximum number of employees allowed for this shift'
    )
    
    # Shift Status
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='draft', tracking=True)
    
    # Additional Fields
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this shift'
    )
    
    # Computed Fields
    employee_count = fields.Integer(
        string='Current Employees',
        compute='_compute_employee_count'
    )
    
    @api.depends('start_time', 'end_time')
    def _compute_duration(self):
        for shift in self:
            if shift.start_time and shift.end_time:
                if shift.end_time > shift.start_time:
                    shift.duration = shift.end_time - shift.start_time
                else:
                    # Handle overnight shifts
                    shift.duration = (24 - shift.start_time) + shift.end_time
            else:
                shift.duration = 0.0
    
    @api.depends('name')
    def _compute_employee_count(self):
        for shift in self:
            shift.employee_count = self.env['hr.employee'].search_count([
                ('active', '=', True),
                ('company_id', '=', shift.company_id.id)
            ])
    
    @api.constrains('code')
    def _check_code(self):
        for shift in self:
            if self.search([('code', '=', shift.code), ('id', '!=', shift.id)]):
                raise ValidationError(_('Shift code must be unique.'))
    
    @api.constrains('start_time', 'end_time')
    def _check_timing(self):
        for shift in self:
            if shift.start_time < 0 or shift.start_time >= 24:
                raise ValidationError(_('Start time must be between 0 and 24 hours.'))
            if shift.end_time < 0 or shift.end_time >= 24:
                raise ValidationError(_('End time must be between 0 and 24 hours.'))
    
    @api.constrains('min_employees', 'max_employees')
    def _check_employee_limits(self):
        for shift in self:
            if shift.min_employees < 0:
                raise ValidationError(_('Minimum employees cannot be negative.'))
            if shift.max_employees < shift.min_employees:
                raise ValidationError(_('Maximum employees cannot be less than minimum employees.'))
    
    def action_activate(self):
        """Activate the shift"""
        for shift in self:
            if shift.state != 'draft':
                raise UserError(_('Only draft shifts can be activated.'))
            shift.state = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate the shift"""
        for shift in self:
            if shift.state not in ['active']:
                raise UserError(_('Only active shifts can be deactivated.'))
            shift.state = 'inactive'
        return True
    
    def action_draft(self):
        """Set shift to draft"""
        for shift in self:
            shift.state = 'draft'
        return True
    
    @api.model
    def get_shift(self, age_group=None, season=None):
        """Get appropriate shift based on criteria"""
        domain = [
            ('active', '=', True),
            ('state', '=', 'active'),
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
        
        shift = self.search(domain, limit=1)
        if not shift:
            # Fallback to default shift
            shift = self.search([
                ('active', '=', True),
                ('state', '=', 'active'),
                ('company_id', '=', self.env.company.id)
            ], limit=1)
        
        return shift