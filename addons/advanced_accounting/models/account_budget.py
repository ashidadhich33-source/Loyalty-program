# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Advanced Accounting - Budget Management
==========================================================

Budget management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountBudget(models.Model):
    """Budget"""
    
    _name = 'account.budget'
    _description = 'Budget'
    _order = 'name'
    
    # Basic Information
    name = fields.Char(
        string='Budget Name',
        required=True,
        help='Budget name'
    )
    
    # Budget Period
    fiscal_year_id = fields.Many2one(
        'account.fiscal.year',
        string='Fiscal Year',
        required=True,
        help='Fiscal year for this budget'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        help='Company this budget belongs to'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Budget currency'
    )
    
    # Budget Lines
    line_ids = fields.One2many(
        'account.budget.line',
        'budget_id',
        string='Budget Lines',
        help='Budget lines'
    )
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', help='Budget status')
    
    # Amounts
    total_budget = fields.Float(
        string='Total Budget',
        compute='_compute_amounts',
        store=True,
        help='Total budget amount'
    )
    
    total_actual = fields.Float(
        string='Total Actual',
        compute='_compute_amounts',
        store=True,
        help='Total actual amount'
    )
    
    variance = fields.Float(
        string='Variance',
        compute='_compute_amounts',
        store=True,
        help='Budget variance'
    )
    
    variance_percentage = fields.Float(
        string='Variance %',
        compute='_compute_amounts',
        store=True,
        help='Budget variance percentage'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this budget')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this budget')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this budget relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this budget')
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Budget notes'
    )
    
    @api.depends('line_ids.budget_amount', 'line_ids.actual_amount')
    def _compute_amounts(self):
        """Compute amounts"""
        for budget in self:
            budget.total_budget = sum(budget.line_ids.mapped('budget_amount'))
            budget.total_actual = sum(budget.line_ids.mapped('actual_amount'))
            budget.variance = budget.total_budget - budget.total_actual
            budget.variance_percentage = (budget.variance / budget.total_budget * 100) if budget.total_budget > 0 else 0.0
    
    def action_approve(self):
        """Approve budget"""
        for budget in self:
            if budget.state != 'draft':
                raise UserError(_('Only draft budgets can be approved.'))
            
            budget.state = 'approved'
    
    def action_cancel(self):
        """Cancel budget"""
        for budget in self:
            if budget.state == 'approved':
                raise UserError(_('Approved budgets cannot be cancelled.'))
            
            budget.state = 'cancelled'
    
    def action_draft(self):
        """Set to draft"""
        for budget in self:
            if budget.state == 'cancelled':
                budget.state = 'draft'
    
    def get_budget_analytics(self):
        """Get budget analytics"""
        self.ensure_one()
        return {
            'total_budget': self.total_budget,
            'total_actual': self.total_actual,
            'variance': self.variance,
            'variance_percentage': self.variance_percentage,
        }


class AccountBudgetLine(models.Model):
    """Budget Line"""
    
    _name = 'account.budget.line'
    _description = 'Budget Line'
    _order = 'budget_id, sequence'
    
    # Basic Information
    name = fields.Char(
        string='Description',
        required=True,
        help='Line description'
    )
    
    # Budget Information
    budget_id = fields.Many2one(
        'account.budget',
        string='Budget',
        required=True,
        ondelete='cascade',
        help='Budget this line belongs to'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Line sequence'
    )
    
    # Account Information
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        required=True,
        help='Account for this line'
    )
    
    # Amounts
    budget_amount = fields.Float(
        string='Budget Amount',
        digits=(12, 2),
        default=0.0,
        help='Budget amount'
    )
    
    actual_amount = fields.Float(
        string='Actual Amount',
        digits=(12, 2),
        default=0.0,
        help='Actual amount'
    )
    
    variance = fields.Float(
        string='Variance',
        compute='_compute_variance',
        store=True,
        help='Budget variance'
    )
    
    variance_percentage = fields.Float(
        string='Variance %',
        compute='_compute_variance',
        store=True,
        help='Budget variance percentage'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='budget_id.currency_id',
        help='Line currency'
    )
    
    # Company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='budget_id.company_id',
        help='Company this line belongs to'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this line')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this line')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this line relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this line')
    
    @api.depends('budget_amount', 'actual_amount')
    def _compute_variance(self):
        """Compute variance"""
        for line in self:
            line.variance = line.budget_amount - line.actual_amount
            line.variance_percentage = (line.variance / line.budget_amount * 100) if line.budget_amount > 0 else 0.0
    
    @api.constrains('budget_amount', 'actual_amount')
    def _check_amounts(self):
        """Check line amounts"""
        for line in self:
            if line.budget_amount < 0 or line.actual_amount < 0:
                raise ValidationError(_('Budget and actual amounts cannot be negative.'))