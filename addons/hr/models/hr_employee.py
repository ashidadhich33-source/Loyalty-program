# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _name = 'hr.employee'
    _description = 'Employee'
    _order = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char(
        string='Employee Name',
        required=True,
        tracking=True
    )
    employee_id = fields.Char(
        string='Employee ID',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    first_name = fields.Char(
        string='First Name',
        required=True
    )
    last_name = fields.Char(
        string='Last Name',
        required=True
    )
    
    # Personal Information
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string='Gender', default='male')
    
    birth_date = fields.Date(
        string='Date of Birth'
    )
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True
    )
    
    # Contact Information
    work_email = fields.Char(
        string='Work Email'
    )
    work_phone = fields.Char(
        string='Work Phone'
    )
    mobile_phone = fields.Char(
        string='Mobile Phone'
    )
    
    # Address Information
    work_address_id = fields.Many2one(
        'res.partner',
        string='Work Address'
    )
    home_address_id = fields.Many2one(
        'res.partner',
        string='Home Address'
    )
    
    # Employment Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    department_id = fields.Many2one(
        'hr.department',
        string='Department'
    )
    job_id = fields.Many2one(
        'hr.job',
        string='Job Position'
    )
    manager_id = fields.Many2one(
        'hr.employee',
        string='Manager'
    )
    
    # Employment Status
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('terminated', 'Terminated'),
    ], string='Status', default='draft', tracking=True)
    
    # Employment Dates
    hire_date = fields.Date(
        string='Hire Date',
        default=fields.Date.context_today
    )
    termination_date = fields.Date(
        string='Termination Date'
    )
    
    # Kids Clothing Specific Fields
    age_group_specialization = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Specialization', help='Age group this employee specializes in')
    
    season_preference = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season Preference', help='Preferred season for work')
    
    brand_expertise = fields.Char(
        string='Brand Expertise',
        help='Brands this employee has expertise in'
    )
    
    size_specialization = fields.Char(
        string='Size Specialization',
        help='Size ranges this employee specializes in'
    )
    
    # Indian Compliance Fields
    pan_number = fields.Char(
        string='PAN Number',
        help='Permanent Account Number'
    )
    aadhar_number = fields.Char(
        string='Aadhar Number',
        help='Aadhar Card Number'
    )
    pf_number = fields.Char(
        string='PF Number',
        help='Provident Fund Number'
    )
    esi_number = fields.Char(
        string='ESI Number',
        help='Employee State Insurance Number'
    )
    
    # Salary Information
    basic_salary = fields.Monetary(
        string='Basic Salary',
        currency_field='currency_id'
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    
    # Sales Performance Fields
    commission_rate = fields.Float(
        string='Commission Rate %',
        digits=(5, 2),
        default=0.0,
        help='Commission rate for sales (percentage)'
    )
    
    monthly_sales_target = fields.Monetary(
        string='Monthly Sales Target',
        currency_field='currency_id',
        help='Monthly sales target for this employee'
    )
    
    weekly_sales_target = fields.Monetary(
        string='Weekly Sales Target',
        currency_field='currency_id',
        help='Weekly sales target for this employee'
    )
    
    daily_sales_target = fields.Monetary(
        string='Daily Sales Target',
        currency_field='currency_id',
        help='Daily sales target for this employee'
    )
    
    # Additional Fields
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this employee'
    )
    
    # Computed Fields
    attendance_count = fields.Integer(
        string='Attendance Count',
        compute='_compute_attendance_count'
    )
    leave_count = fields.Integer(
        string='Leave Count',
        compute='_compute_leave_count'
    )
    
    # Sales Performance Computed Fields
    current_month_sales = fields.Monetary(
        string='Current Month Sales',
        currency_field='currency_id',
        compute='_compute_current_month_sales'
    )
    
    current_week_sales = fields.Monetary(
        string='Current Week Sales',
        currency_field='currency_id',
        compute='_compute_current_week_sales'
    )
    
    current_day_sales = fields.Monetary(
        string='Current Day Sales',
        currency_field='currency_id',
        compute='_compute_current_day_sales'
    )
    
    monthly_target_achievement = fields.Float(
        string='Monthly Target Achievement %',
        compute='_compute_monthly_target_achievement'
    )
    
    weekly_target_achievement = fields.Float(
        string='Weekly Target Achievement %',
        compute='_compute_weekly_target_achievement'
    )
    
    daily_target_achievement = fields.Float(
        string='Daily Target Achievement %',
        compute='_compute_daily_target_achievement'
    )
    
    total_commission_earned = fields.Monetary(
        string='Total Commission Earned',
        currency_field='currency_id',
        compute='_compute_total_commission_earned'
    )
    
    @api.depends('birth_date')
    def _compute_age(self):
        for employee in self:
            if employee.birth_date:
                today = fields.Date.today()
                employee.age = today.year - employee.birth_date.year - (
                    (today.month, today.day) < (employee.birth_date.month, employee.birth_date.day)
                )
            else:
                employee.age = 0
    
    @api.depends('name')
    def _compute_attendance_count(self):
        for employee in self:
            employee.attendance_count = self.env['hr.attendance'].search_count([
                ('employee_id', '=', employee.id)
            ])
    
    @api.depends('name')
    def _compute_leave_count(self):
        for employee in self:
            employee.leave_count = self.env['hr.leave'].search_count([
                ('employee_id', '=', employee.id)
            ])
    
    @api.depends('name')
    def _compute_current_month_sales(self):
        for employee in self:
            from datetime import datetime, date
            today = date.today()
            month_start = date(today.year, today.month, 1)
            
            orders = self.env['pos.order'].search([
                ('employee_id', '=', employee.id),
                ('date_order', '>=', month_start),
                ('state', 'in', ['paid', 'done'])
            ])
            
            employee.current_month_sales = sum(order.amount_total for order in orders)
    
    @api.depends('name')
    def _compute_current_week_sales(self):
        for employee in self:
            from datetime import datetime, date, timedelta
            today = date.today()
            week_start = today - timedelta(days=today.weekday())
            
            orders = self.env['pos.order'].search([
                ('employee_id', '=', employee.id),
                ('date_order', '>=', week_start),
                ('state', 'in', ['paid', 'done'])
            ])
            
            employee.current_week_sales = sum(order.amount_total for order in orders)
    
    @api.depends('name')
    def _compute_current_day_sales(self):
        for employee in self:
            from datetime import datetime, date
            today = date.today()
            
            orders = self.env['pos.order'].search([
                ('employee_id', '=', employee.id),
                ('date_order', '>=', today),
                ('state', 'in', ['paid', 'done'])
            ])
            
            employee.current_day_sales = sum(order.amount_total for order in orders)
    
    @api.depends('current_month_sales', 'monthly_sales_target')
    def _compute_monthly_target_achievement(self):
        for employee in self:
            if employee.monthly_sales_target > 0:
                employee.monthly_target_achievement = (employee.current_month_sales / employee.monthly_sales_target) * 100
            else:
                employee.monthly_target_achievement = 0.0
    
    @api.depends('current_week_sales', 'weekly_sales_target')
    def _compute_weekly_target_achievement(self):
        for employee in self:
            if employee.weekly_sales_target > 0:
                employee.weekly_target_achievement = (employee.current_week_sales / employee.weekly_sales_target) * 100
            else:
                employee.weekly_target_achievement = 0.0
    
    @api.depends('current_day_sales', 'daily_sales_target')
    def _compute_daily_target_achievement(self):
        for employee in self:
            if employee.daily_sales_target > 0:
                employee.daily_target_achievement = (employee.current_day_sales / employee.daily_sales_target) * 100
            else:
                employee.daily_target_achievement = 0.0
    
    @api.depends('name')
    def _compute_total_commission_earned(self):
        for employee in self:
            orders = self.env['pos.order'].search([
                ('employee_id', '=', employee.id),
                ('state', 'in', ['paid', 'done'])
            ])
            
            employee.total_commission_earned = sum(order.sales_commission for order in orders)
    
    @api.model
    def create(self, vals):
        if vals.get('employee_id', _('New')) == _('New'):
            vals['employee_id'] = self.env['ir.sequence'].next_by_code('hr.employee') or _('New')
        
        # Set name from first_name and last_name
        if 'first_name' in vals and 'last_name' in vals:
            vals['name'] = f"{vals['first_name']} {vals['last_name']}"
        
        return super(HrEmployee, self).create(vals)
    
    def action_activate(self):
        """Activate employee"""
        for employee in self:
            if employee.state != 'draft':
                raise UserError(_('Only draft employees can be activated.'))
            employee.state = 'active'
        return True
    
    def action_deactivate(self):
        """Deactivate employee"""
        for employee in self:
            if employee.state not in ['active']:
                raise UserError(_('Only active employees can be deactivated.'))
            employee.state = 'inactive'
        return True
    
    def action_terminate(self):
        """Terminate employee"""
        for employee in self:
            if employee.state not in ['active', 'inactive']:
                raise UserError(_('Only active or inactive employees can be terminated.'))
            employee.state = 'terminated'
            employee.termination_date = fields.Date.today()
        return True
    
    def action_view_attendance(self):
        """View attendance records for this employee"""
        action = self.env.ref('hr.action_hr_attendance').read()[0]
        action['domain'] = [('employee_id', '=', self.id)]
        action['context'] = {'default_employee_id': self.id}
        return action
    
    def action_view_leaves(self):
        """View leave records for this employee"""
        action = self.env.ref('hr.action_hr_leave').read()[0]
        action['domain'] = [('employee_id', '=', self.id)]
        action['context'] = {'default_employee_id': self.id}
        return action
    
    def action_view_sales_performance(self):
        """View sales performance for this employee"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Sales Performance - {self.name}',
            'res_model': 'pos.order',
            'view_mode': 'tree,form',
            'domain': [('employee_id', '=', self.id), ('state', 'in', ['paid', 'done'])],
            'context': {'default_employee_id': self.id}
        }
    
    def get_performance_summary(self):
        """Get comprehensive performance summary"""
        return {
            'employee_name': self.name,
            'department': self.department_id.name if self.department_id else 'N/A',
            'job_position': self.job_id.name if self.job_id else 'N/A',
            'current_month_sales': self.current_month_sales,
            'monthly_target': self.monthly_sales_target,
            'monthly_achievement': self.monthly_target_achievement,
            'current_week_sales': self.current_week_sales,
            'weekly_target': self.weekly_sales_target,
            'weekly_achievement': self.weekly_target_achievement,
            'current_day_sales': self.current_day_sales,
            'daily_target': self.daily_sales_target,
            'daily_achievement': self.daily_target_achievement,
            'total_commission': self.total_commission_earned,
            'commission_rate': self.commission_rate,
            'age_group_specialization': self.age_group_specialization,
            'season_preference': self.season_preference,
            'brand_expertise': self.brand_expertise
        }
    
    def get_age_group_performance(self, age_group=None):
        """Get performance by age group"""
        domain = [
            ('employee_id', '=', self.id),
            ('state', 'in', ['paid', 'done'])
        ]
        
        if age_group:
            # This would need to be enhanced to filter by product age group
            pass
        
        orders = self.env['pos.order'].search(domain)
        
        age_group_sales = {}
        for order in orders:
            age_group_focus = order._get_age_group_focus()
            if age_group_focus not in age_group_sales:
                age_group_sales[age_group_focus] = 0
            age_group_sales[age_group_focus] += order.amount_total
        
        return age_group_sales
    
    def get_season_performance(self, season=None):
        """Get performance by season"""
        domain = [
            ('employee_id', '=', self.id),
            ('state', 'in', ['paid', 'done'])
        ]
        
        if season:
            # This would need to be enhanced to filter by product season
            pass
        
        orders = self.env['pos.order'].search(domain)
        
        season_sales = {}
        for order in orders:
            season_focus = order._get_season_focus()
            if season_focus not in season_sales:
                season_sales[season_focus] = 0
            season_sales[season_focus] += order.amount_total
        
        return season_sales
    
    def get_brand_performance(self, brand=None):
        """Get performance by brand"""
        domain = [
            ('employee_id', '=', self.id),
            ('state', 'in', ['paid', 'done'])
        ]
        
        if brand:
            # This would need to be enhanced to filter by product brand
            pass
        
        orders = self.env['pos.order'].search(domain)
        
        brand_sales = {}
        for order in orders:
            brand_focus = order._get_brand_focus()
            if brand_focus not in brand_sales:
                brand_sales[brand_focus] = 0
            brand_sales[brand_focus] += order.amount_total
        
        return brand_sales
    
    @api.constrains('pan_number')
    def _check_pan_number(self):
        for employee in self:
            if employee.pan_number and len(employee.pan_number) != 10:
                raise ValidationError(_('PAN number must be 10 characters long.'))
    
    @api.constrains('aadhar_number')
    def _check_aadhar_number(self):
        for employee in self:
            if employee.aadhar_number and len(employee.aadhar_number) != 12:
                raise ValidationError(_('Aadhar number must be 12 digits long.'))
    
    @api.constrains('basic_salary')
    def _check_basic_salary(self):
        for employee in self:
            if employee.basic_salary and employee.basic_salary < 0:
                raise ValidationError(_('Basic salary cannot be negative.'))