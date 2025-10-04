# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _name = 'hr.attendance'
    _description = 'Attendance'
    _order = 'check_in desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char(
        string='Attendance Reference',
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
    
    # Attendance Timing
    check_in = fields.Datetime(
        string='Check In',
        required=True,
        default=fields.Datetime.now
    )
    check_out = fields.Datetime(
        string='Check Out'
    )
    
    # Shift Information
    shift_id = fields.Many2one(
        'hr.shift',
        string='Work Shift'
    )
    
    # Attendance Details
    worked_hours = fields.Float(
        string='Worked Hours',
        compute='_compute_worked_hours',
        store=True
    )
    overtime_hours = fields.Float(
        string='Overtime Hours',
        compute='_compute_overtime_hours',
        store=True
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Age group focus for this attendance')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season Specialization', help='Season specialization for this attendance')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Primary brands this attendance focuses on'
    )
    
    # Attendance Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='checked_in', tracking=True)
    
    # Additional Fields
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this attendance'
    )
    
    @api.depends('check_in', 'check_out')
    def _compute_worked_hours(self):
        for attendance in self:
            if attendance.check_in and attendance.check_out:
                delta = attendance.check_out - attendance.check_in
                attendance.worked_hours = delta.total_seconds() / 3600.0
            else:
                attendance.worked_hours = 0.0
    
    @api.depends('worked_hours', 'shift_id')
    def _compute_overtime_hours(self):
        for attendance in self:
            if attendance.shift_id and attendance.worked_hours > attendance.shift_id.duration:
                attendance.overtime_hours = attendance.worked_hours - attendance.shift_id.duration
            else:
                attendance.overtime_hours = 0.0
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.attendance') or _('New')
        return super(HrAttendance, self).create(vals)
    
    def action_check_out(self):
        """Check out employee"""
        for attendance in self:
            if attendance.state != 'checked_in':
                raise UserError(_('Only checked-in attendance can be checked out.'))
            attendance.check_out = fields.Datetime.now()
            attendance.state = 'checked_out'
        return True
    
    def action_approve(self):
        """Approve attendance"""
        for attendance in self:
            if attendance.state not in ['checked_out']:
                raise UserError(_('Only checked-out attendance can be approved.'))
            attendance.state = 'approved'
        return True
    
    def action_reject(self):
        """Reject attendance"""
        for attendance in self:
            if attendance.state not in ['checked_out']:
                raise UserError(_('Only checked-out attendance can be rejected.'))
            attendance.state = 'rejected'
        return True
    
    def action_draft(self):
        """Set attendance to draft"""
        for attendance in self:
            attendance.state = 'draft'
        return True
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.age_group_focus = self.employee_id.age_group_specialization
            self.season_specialization = self.employee_id.season_preference
            self.brand_focus = self.employee_id.brand_expertise
    
    @api.constrains('check_in', 'check_out')
    def _check_timing(self):
        for attendance in self:
            if attendance.check_out and attendance.check_out <= attendance.check_in:
                raise ValidationError(_('Check out time must be after check in time.'))
    
    @api.constrains('employee_id', 'check_in')
    def _check_duplicate_check_in(self):
        for attendance in self:
            if attendance.check_in:
                # Check for duplicate check-in on the same day
                same_day = self.search([
                    ('employee_id', '=', attendance.employee_id.id),
                    ('check_in', '>=', attendance.check_in.date()),
                    ('check_in', '<', attendance.check_in.date() + timedelta(days=1)),
                    ('id', '!=', attendance.id)
                ])
                if same_day:
                    raise ValidationError(_('Employee already has attendance record for this day.'))