# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class BankAccount(models.Model):
    _name = 'bank.account'
    _description = 'Bank Account'
    _order = 'name'

    # Basic Information
    name = fields.Char(
        string='Account Name',
        required=True
    )
    account_number = fields.Char(
        string='Account Number',
        required=True
    )
    bank_id = fields.Many2one(
        'res.bank',
        string='Bank',
        required=True
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    
    # Account Details
    account_type = fields.Selection([
        ('current', 'Current Account'),
        ('savings', 'Savings Account'),
        ('fixed_deposit', 'Fixed Deposit'),
        ('recurring_deposit', 'Recurring Deposit'),
        ('credit_card', 'Credit Card'),
        ('loan', 'Loan Account'),
    ], string='Account Type', required=True, default='current')
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this bank account')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this bank account')
    
    # Indian Compliance Fields
    gst_treatment = fields.Selection([
        ('regular', 'Regular'),
        ('composition', 'Composition'),
        ('unregistered', 'Unregistered'),
        ('consumer', 'Consumer'),
        ('overseas', 'Overseas'),
        ('special_economic_zone', 'Special Economic Zone'),
        ('deemed_export', 'Deemed Export'),
    ], string='GST Treatment', default='regular')
    
    # Account Status
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Additional Fields
    description = fields.Text(
        string='Description',
        help='Description of this bank account'
    )
    
    # Computed Fields
    balance = fields.Monetary(
        string='Balance',
        compute='_compute_balance',
        store=True
    )
    
    @api.depends('account_number', 'bank_id')
    def _compute_balance(self):
        for account in self:
            # This would be computed from bank statements
            account.balance = 0.0
    
    @api.constrains('account_number')
    def _check_account_number(self):
        for account in self:
            if self.search([('account_number', '=', account.account_number), ('id', '!=', account.id)]):
                raise ValidationError(_('Account number must be unique.'))
    
    @api.model
    def get_bank_account(self, account_type='current', age_group=None, season=None):
        """Get appropriate bank account based on criteria"""
        domain = [
            ('account_type', '=', account_type),
            ('active', '=', True),
            ('company_id', '=', self.env.company.id)
        ]
        
        if age_group:
            domain.append('|')
            domain.append(('age_group', '=', age_group))
            domain.append(('age_group', '=', 'all'))
        
        if season:
            domain.append('|')
            domain.append(('season', '=', season))
            domain.append(('season', '=', 'all_season'))
        
        account = self.search(domain, limit=1)
        if not account:
            # Fallback to default account
            account = self.search([
                ('account_type', '=', account_type),
                ('active', '=', True),
                ('company_id', '=', self.env.company.id)
            ], limit=1)
        
        return account