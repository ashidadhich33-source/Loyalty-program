# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class HrLeave(models.Model):
    _name = 'hr.leave'
    _description = 'Leave Request'
    _order = 'date_from desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char(
        string='Leave Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    
    # Employee Information
    employee_id = fields.Many2one(
        'hr.employee',
        string='Employee',
        required=True,
        index=True
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='employee_id.company_id',
        store=True
    )
    
    # Leave Details
    leave_type = fields.Selection([
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('earned', 'Earned Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('compensatory', 'Compensatory Leave'),
        ('unpaid', 'Unpaid Leave'),
        ('other', 'Other'),
    ], string='Leave Type', required=True, default='casual')
    
    date_from = fields.Date(
        string='From Date',
        required=True,
        default=fields.Date.context_today
    )
    date_to = fields.Date(
        string='To Date',
        required=True
    )
    days = fields.Float(
        string='Number of Days',
        compute='_compute_days',
        store=True
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Age group focus for this leave')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season Specialization', help='Season specialization for this leave')
    
    # Leave Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    
    # Approval Information
    approved_by = fields.Many2one(
        'hr.employee',
        string='Approved By',
        readonly=True
    )
    approved_date = fields.Date(
        string='Approved Date',
        readonly=True
    )
    rejection_reason = fields.Text(
        string='Rejection Reason',
        readonly=True
    )
    
    # Additional Fields
    reason = fields.Text(
        string='Reason',
        help='Reason for leave request'
    )
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this leave'
    )
    
    @api.depends('date_from', 'date_to')
    def _compute_days(self):
        for leave in self:
            if leave.date_from and leave.date_to:
                delta = leave.date_to - leave.date_from
                leave.days = delta.days + 1  # Include both start and end dates
            else:
                leave.days = 0.0
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.leave') or _('New')
        return super(HrLeave, self).create(vals)
    
    def action_submit(self):
        """Submit leave request"""
        for leave in self:
            if leave.state != 'draft':
                raise UserError(_('Only draft leave requests can be submitted.'))
            leave.state = 'submitted'
        return True
    
    def action_approve(self):
        """Approve leave request"""
        for leave in self:
            if leave.state != 'submitted':
                raise UserError(_('Only submitted leave requests can be approved.'))
            leave.state = 'approved'
            leave.approved_by = self.env.user.employee_id
            leave.approved_date = fields.Date.today()
        return True
    
    def action_reject(self):
        """Reject leave request"""
        for leave in self:
            if leave.state != 'submitted':
                raise UserError(_('Only submitted leave requests can be rejected.'))
            leave.state = 'rejected'
        return True
    
    def action_cancel(self):
        """Cancel leave request"""
        for leave in self:
            if leave.state in ['approved']:
                raise UserError(_('Cannot cancel an approved leave request.'))
            leave.state = 'cancelled'
        return True
    
    def action_draft(self):
        """Set leave to draft"""
        for leave in self:
            leave.state = 'draft'
        return True
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.age_group_focus = self.employee_id.age_group_specialization
            self.season_specialization = self.employee_id.season_preference
    
    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for leave in self:
            if leave.date_to and leave.date_to < leave.date_from:
                raise ValidationError(_('To date cannot be before from date.'))
    
    @api.constrains('employee_id', 'date_from', 'date_to')
    def _check_overlapping_leaves(self):
        for leave in self:
            if leave.date_from and leave.date_to:
                overlapping = self.search([
                    ('employee_id', '=', leave.employee_id.id),
                    ('state', 'in', ['submitted', 'approved']),
                    ('id', '!=', leave.id),
                    ('date_from', '<=', leave.date_to),
                    ('date_to', '>=', leave.date_from)
                ])
                if overlapping:
                    raise ValidationError(_('Employee already has overlapping leave request.'))