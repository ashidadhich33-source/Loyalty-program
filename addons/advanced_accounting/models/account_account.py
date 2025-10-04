# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Advanced Accounting - Chart of Accounts
==========================================================

Chart of accounts management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountAccount(models.Model):
    """Chart of Accounts"""
    
    _name = 'account.account'
    _description = 'Account'
    _order = 'code'
    _rec_name = 'display_name'
    
    # Basic Information
    name = fields.Char(
        string='Account Name',
        required=True,
        help='Account name'
    )
    
    code = fields.Char(
        string='Account Code',
        required=True,
        help='Account code (e.g., 1000, 2000, etc.)'
    )
    
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help='Account code and name combined'
    )
    
    # Account Classification
    account_type = fields.Selection([
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('cost_of_sales', 'Cost of Sales'),
        ('other_income', 'Other Income'),
        ('other_expense', 'Other Expense'),
    ], string='Account Type', required=True, help='Account classification')
    
    # Account Properties
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this account is active'
    )
    
    is_reconcilable = fields.Boolean(
        string='Reconcilable',
        default=False,
        help='Whether this account can be reconciled'
    )
    
    is_depreciated = fields.Boolean(
        string='Depreciated',
        default=False,
        help='Whether this account is depreciated'
    )
    
    # Hierarchy
    parent_id = fields.Many2one(
        'account.account',
        string='Parent Account',
        help='Parent account in the hierarchy'
    )
    
    child_ids = fields.One2many(
        'account.account',
        'parent_id',
        string='Child Accounts',
        help='Child accounts'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        help='Company this account belongs to'
    )
    
    # Currency and Multi-currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Account currency'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this account')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this account')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this account relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this account')
    
    # Indian Compliance Fields
    gst_applicable = fields.Boolean(
        string='GST Applicable',
        default=False,
        help='Whether GST is applicable to this account'
    )
    
    gst_rate = fields.Float(
        string='GST Rate (%)',
        digits=(5, 2),
        help='GST rate applicable to this account'
    )
    
    tds_applicable = fields.Boolean(
        string='TDS Applicable',
        default=False,
        help='Whether TDS is applicable to this account'
    )
    
    tds_rate = fields.Float(
        string='TDS Rate (%)',
        digits=(5, 2),
        help='TDS rate applicable to this account'
    )
    
    # Financial Information
    opening_balance = fields.Float(
        string='Opening Balance',
        digits=(12, 2),
        default=0.0,
        help='Opening balance for this account'
    )
    
    current_balance = fields.Float(
        string='Current Balance',
        compute='_compute_current_balance',
        store=True,
        help='Current balance of this account'
    )
    
    # Analytics
    total_debit = fields.Float(
        string='Total Debit',
        compute='_compute_analytics',
        store=True,
        help='Total debit amount'
    )
    
    total_credit = fields.Float(
        string='Total Credit',
        compute='_compute_analytics',
        store=True,
        help='Total credit amount'
    )
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this account'
    )
    
    @api.depends('code', 'name')
    def _compute_display_name(self):
        """Compute display name"""
        for account in self:
            account.display_name = f"{account.code} - {account.name}"
    
    @api.depends('opening_balance')
    def _compute_current_balance(self):
        """Compute current balance"""
        for account in self:
            # This would be computed from journal entries
            # For now, using opening balance
            account.current_balance = account.opening_balance
    
    @api.depends('opening_balance')
    def _compute_analytics(self):
        """Compute analytics"""
        for account in self:
            # This would be computed from journal entries
            # For now, setting to 0
            account.total_debit = 0.0
            account.total_credit = 0.0
    
    @api.constrains('code')
    def _check_code(self):
        """Validate account code"""
        for account in self:
            if not account.code:
                raise ValidationError(_('Account code is required.'))
            
            # Check for duplicate codes
            duplicate = self.search([
                ('code', '=', account.code),
                ('company_id', '=', account.company_id.id),
                ('id', '!=', account.id)
            ])
            if duplicate:
                raise ValidationError(_('Account code must be unique within the company.'))
    
    @api.constrains('parent_id')
    def _check_parent(self):
        """Validate parent account"""
        for account in self:
            if account.parent_id:
                if account.parent_id == account:
                    raise ValidationError(_('Account cannot be its own parent.'))
                
                if account.parent_id.parent_id == account:
                    raise ValidationError(_('Account cannot be parent of its parent.'))
    
    def name_get(self):
        """Return display name"""
        result = []
        for account in self:
            result.append((account.id, f"{account.code} - {account.name}"))
        return result
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Search by name or code"""
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        accounts = self.search(domain + args, limit=limit)
        return accounts.name_get()
    
    def action_view_entries(self):
        """View journal entries for this account"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Journal Entries'),
            'res_model': 'account.move.line',
            'view_mode': 'tree,form',
            'domain': [('account_id', '=', self.id)],
            'context': {'default_account_id': self.id},
        }
    
    def action_view_balance(self):
        """View account balance"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Account Balance'),
            'res_model': 'account.account',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
    
    def get_account_balance(self, date_from=None, date_to=None):
        """Get account balance for date range"""
        self.ensure_one()
        # This would query journal entries
        # For now, returning opening balance
        return self.opening_balance
    
    def get_account_analytics(self, date_from=None, date_to=None):
        """Get account analytics for date range"""
        self.ensure_one()
        # This would query journal entries
        # For now, returning basic info
        return {
            'opening_balance': self.opening_balance,
            'current_balance': self.current_balance,
            'total_debit': self.total_debit,
            'total_credit': self.total_credit,
        }