# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class HrPerformance(models.Model):
    _name = 'hr.performance'
    _description = 'Employee Performance'
    _order = 'review_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char(
        string='Performance Review Reference',
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
    
    # Review Information
    review_date = fields.Date(
        string='Review Date',
        required=True,
        default=fields.Date.context_today
    )
    review_period_from = fields.Date(
        string='Review Period From',
        required=True
    )
    review_period_to = fields.Date(
        string='Review Period To',
        required=True
    )
    
    # Reviewer Information
    reviewer_id = fields.Many2one(
        'hr.employee',
        string='Reviewer',
        required=True
    )
    
    # Performance Ratings
    overall_rating = fields.Selection([
        ('excellent', 'Excellent (5)'),
        ('good', 'Good (4)'),
        ('satisfactory', 'Satisfactory (3)'),
        ('needs_improvement', 'Needs Improvement (2)'),
        ('unsatisfactory', 'Unsatisfactory (1)'),
    ], string='Overall Rating', required=True)
    
    # Kids Clothing Specific Ratings
    age_group_knowledge = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('needs_improvement', 'Needs Improvement'),
        ('unsatisfactory', 'Unsatisfactory'),
    ], string='Age Group Knowledge')
    
    season_expertise = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('needs_improvement', 'Needs Improvement'),
        ('unsatisfactory', 'Unsatisfactory'),
    ], string='Season Expertise')
    
    brand_knowledge = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('needs_improvement', 'Needs Improvement'),
        ('unsatisfactory', 'Unsatisfactory'),
    ], string='Brand Knowledge')
    
    customer_service = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('needs_improvement', 'Needs Improvement'),
        ('unsatisfactory', 'Unsatisfactory'),
    ], string='Customer Service')
    
    # Performance Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_review', 'In Review'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    
    # Additional Fields
    strengths = fields.Text(
        string='Strengths',
        help='Employee strengths identified during review'
    )
    areas_for_improvement = fields.Text(
        string='Areas for Improvement',
        help='Areas where employee can improve'
    )
    goals = fields.Text(
        string='Goals',
        help='Goals set for the next review period'
    )
    comments = fields.Text(
        string='Comments',
        help='Additional comments from reviewer'
    )
    employee_comments = fields.Text(
        string='Employee Comments',
        help='Comments from employee'
    )
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.performance') or _('New')
        return super(HrPerformance, self).create(vals)
    
    def action_start_review(self):
        """Start performance review"""
        for performance in self:
            if performance.state != 'draft':
                raise UserError(_('Only draft performance reviews can be started.'))
            performance.state = 'in_review'
        return True
    
    def action_complete_review(self):
        """Complete performance review"""
        for performance in self:
            if performance.state != 'in_review':
                raise UserError(_('Only in-review performance reviews can be completed.'))
            performance.state = 'completed'
        return True
    
    def action_cancel(self):
        """Cancel performance review"""
        for performance in self:
            if performance.state in ['completed']:
                raise UserError(_('Cannot cancel a completed performance review.'))
            performance.state = 'cancelled'
        return True
    
    def action_draft(self):
        """Set performance review to draft"""
        for performance in self:
            performance.state = 'draft'
        return True
    
    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.reviewer_id = self.employee_id.manager_id
    
    @api.constrains('review_period_from', 'review_period_to')
    def _check_review_period(self):
        for performance in self:
            if performance.review_period_to and performance.review_period_to < performance.review_period_from:
                raise ValidationError(_('Review period end date cannot be before start date.'))
    
    @api.constrains('employee_id', 'review_period_from', 'review_period_to')
    def _check_overlapping_reviews(self):
        for performance in self:
            if performance.review_period_from and performance.review_period_to:
                overlapping = self.search([
                    ('employee_id', '=', performance.employee_id.id),
                    ('state', 'in', ['in_review', 'completed']),
                    ('id', '!=', performance.id),
                    ('review_period_from', '<=', performance.review_period_to),
                    ('review_period_to', '>=', performance.review_period_from)
                ])
                if overlapping:
                    raise ValidationError(_('Employee already has overlapping performance review.'))