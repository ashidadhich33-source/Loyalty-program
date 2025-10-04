# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class HrJob(models.Model):
    _name = 'hr.job'
    _description = 'Job Position'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char(
        string='Job Position',
        required=True,
        tracking=True
    )
    code = fields.Char(
        string='Job Code',
        required=True,
        help='Unique code for this job position'
    )
    description = fields.Text(
        string='Job Description',
        help='Detailed description of this job position'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    
    # Department Information
    department_id = fields.Many2one(
        'hr.department',
        string='Department'
    )
    
    # Job Requirements
    required_skills = fields.Text(
        string='Required Skills',
        help='Skills required for this position'
    )
    experience_required = fields.Selection([
        ('fresher', 'Fresher (0-1 years)'),
        ('junior', 'Junior (1-3 years)'),
        ('mid', 'Mid-level (3-5 years)'),
        ('senior', 'Senior (5-10 years)'),
        ('expert', 'Expert (10+ years)'),
    ], string='Experience Required', default='fresher')
    
    # Salary Information
    min_salary = fields.Monetary(
        string='Minimum Salary',
        currency_field='currency_id'
    )
    max_salary = fields.Monetary(
        string='Maximum Salary',
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    # Kids Clothing Specific Fields
    age_group_expertise = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Expertise', help='Age group expertise required for this position')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season Specialization', help='Season specialization for this position')
    
    brand_knowledge = fields.Char(
        string='Brand Knowledge',
        help='Brand knowledge required for this position'
    )
    
    size_expertise = fields.Char(
        string='Size Expertise',
        help='Size expertise required for this position'
    )
    
    # Job Status
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    
    # Additional Fields
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this job position'
    )
    
    # Computed Fields
    employee_count = fields.Integer(
        string='Employee Count',
        compute='_compute_employee_count'
    )
    
    @api.depends('name')
    def _compute_employee_count(self):
        for job in self:
            job.employee_count = self.env['hr.employee'].search_count([
                ('job_id', '=', job.id),
                ('active', '=', True)
            ])
    
    @api.constrains('code')
    def _check_code(self):
        for job in self:
            if self.search([('code', '=', job.code), ('id', '!=', job.id)]):
                raise ValidationError(_('Job code must be unique.'))
    
    @api.constrains('min_salary', 'max_salary')
    def _check_salary_range(self):
        for job in self:
            if job.min_salary and job.max_salary and job.min_salary > job.max_salary:
                raise ValidationError(_('Minimum salary cannot be greater than maximum salary.'))
    
    def action_open(self):
        """Open the job position"""
        for job in self:
            if job.state != 'draft':
                raise UserError(_('Only draft job positions can be opened.'))
            job.state = 'open'
        return True
    
    def action_close(self):
        """Close the job position"""
        for job in self:
            if job.state not in ['open']:
                raise UserError(_('Only open job positions can be closed.'))
            job.state = 'closed'
        return True
    
    def action_draft(self):
        """Set job position to draft"""
        for job in self:
            job.state = 'draft'
        return True
    
    @api.model
    def get_job_position(self, age_group=None, season=None, experience=None):
        """Get appropriate job position based on criteria"""
        domain = [
            ('active', '=', True),
            ('state', '=', 'open'),
            ('company_id', '=', self.env.company.id)
        ]
        
        if age_group:
            domain.append('|')
            domain.append(('age_group_expertise', '=', age_group))
            domain.append(('age_group_expertise', '=', 'all'))
        
        if season:
            domain.append('|')
            domain.append(('season_specialization', '=', season))
            domain.append(('season_specialization', '=', 'all_season'))
        
        if experience:
            domain.append(('experience_required', '=', experience))
        
        job = self.search(domain, limit=1)
        if not job:
            # Fallback to default job
            job = self.search([
                ('active', '=', True),
                ('state', '=', 'open'),
                ('company_id', '=', self.env.company.id)
            ], limit=1)
        
        return job