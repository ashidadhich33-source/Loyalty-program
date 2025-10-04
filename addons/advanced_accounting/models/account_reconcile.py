# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Advanced Accounting - Account Reconciliation
==============================================================

Account reconciliation for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountReconcile(models.Model):
    """Account Reconciliation"""
    
    _name = 'account.reconcile'
    _description = 'Account Reconciliation'
    _order = 'date desc, name desc'
    
    # Basic Information
    name = fields.Char(
        string='Reconciliation Name',
        required=True,
        help='Reconciliation name'
    )
    
    # Account Information
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        required=True,
        help='Account to reconcile'
    )
    
    # Dates
    date = fields.Date(
        string='Reconciliation Date',
        required=True,
        default=fields.Date.context_today,
        help='Reconciliation date'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        help='Company this reconciliation belongs to'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Reconciliation currency'
    )
    
    # Reconciliation Lines
    line_ids = fields.One2many(
        'account.reconcile.line',
        'reconcile_id',
        string='Reconciliation Lines',
        help='Reconciliation lines'
    )
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('reconciled', 'Reconciled'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', help='Reconciliation status')
    
    # Amounts
    total_debit = fields.Float(
        string='Total Debit',
        compute='_compute_amounts',
        store=True,
        help='Total debit amount'
    )
    
    total_credit = fields.Float(
        string='Total Credit',
        compute='_compute_amounts',
        store=True,
        help='Total credit amount'
    )
    
    difference = fields.Float(
        string='Difference',
        compute='_compute_amounts',
        store=True,
        help='Difference between debit and credit'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Reconciliation notes'
    )
    
    @api.depends('line_ids.debit', 'line_ids.credit')
    def _compute_amounts(self):
        """Compute amounts"""
        for reconcile in self:
            reconcile.total_debit = sum(reconcile.line_ids.mapped('debit'))
            reconcile.total_credit = sum(reconcile.line_ids.mapped('credit'))
            reconcile.difference = reconcile.total_debit - reconcile.total_credit
    
    @api.constrains('line_ids')
    def _check_balanced(self):
        """Check if reconciliation is balanced"""
        for reconcile in self:
            if reconcile.line_ids:
                if abs(reconcile.difference) > 0.01:
                    raise ValidationError(_('Reconciliation must be balanced. Difference: %s') % reconcile.difference)
    
    def action_reconcile(self):
        """Reconcile account"""
        for reconcile in self:
            if reconcile.state != 'draft':
                raise UserError(_('Only draft reconciliations can be reconciled.'))
            
            # Validate reconciliation
            reconcile._check_balanced()
            
            # Reconcile
            reconcile.state = 'reconciled'
            
            # Update account balances
            for line in reconcile.line_ids:
                line._update_account_balance()
    
    def action_cancel(self):
        """Cancel reconciliation"""
        for reconcile in self:
            if reconcile.state == 'reconciled':
                # Reverse account balances
                for line in reconcile.line_ids:
                    line._reverse_account_balance()
            
            reconcile.state = 'cancelled'
    
    def action_draft(self):
        """Set to draft"""
        for reconcile in self:
            if reconcile.state == 'cancelled':
                reconcile.state = 'draft'


class AccountReconcileLine(models.Model):
    """Account Reconciliation Line"""
    
    _name = 'account.reconcile.line'
    _description = 'Account Reconciliation Line'
    _order = 'reconcile_id, sequence'
    
    # Basic Information
    name = fields.Char(
        string='Description',
        required=True,
        help='Line description'
    )
    
    # Reconciliation Information
    reconcile_id = fields.Many2one(
        'account.reconcile',
        string='Reconciliation',
        required=True,
        ondelete='cascade',
        help='Reconciliation this line belongs to'
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
    
    # Partner Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Partner for this line'
    )
    
    # Amounts
    debit = fields.Float(
        string='Debit',
        digits=(12, 2),
        default=0.0,
        help='Debit amount'
    )
    
    credit = fields.Float(
        string='Credit',
        digits=(12, 2),
        default=0.0,
        help='Credit amount'
    )
    
    balance = fields.Float(
        string='Balance',
        compute='_compute_balance',
        store=True,
        help='Line balance'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='reconcile_id.currency_id',
        help='Line currency'
    )
    
    # Company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='reconcile_id.company_id',
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
    
    @api.depends('debit', 'credit')
    def _compute_balance(self):
        """Compute line balance"""
        for line in self:
            line.balance = line.debit - line.credit
    
    @api.constrains('debit', 'credit')
    def _check_amounts(self):
        """Check line amounts"""
        for line in self:
            if line.debit < 0 or line.credit < 0:
                raise ValidationError(_('Debit and credit amounts cannot be negative.'))
    
    def _update_account_balance(self):
        """Update account balance"""
        self.ensure_one()
        # This would update the account balance
        # For now, just logging
        _logger.info(f"Updating account balance for {self.account_id.name}")
    
    def _reverse_account_balance(self):
        """Reverse account balance"""
        self.ensure_one()
        # This would reverse the account balance
        # For now, just logging
        _logger.info(f"Reversing account balance for {self.account_id.name}")