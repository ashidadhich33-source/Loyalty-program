# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountAccount(models.Model):
    _name = 'account.account'
    _description = 'Account'
    _order = 'code'
    _rec_name = 'name'

    name = fields.Char(
        string='Account Name',
        required=True,
        help='Name of the account'
    )
    
    code = fields.Char(
        string='Account Code',
        required=True,
        help='Account code for identification'
    )
    
    account_type = fields.Selection([
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('income', 'Income'),
        ('expense', 'Expense'),
    ], string='Account Type', required=True, help='Type of account')
    
    account_subtype = fields.Selection([
        # Asset subtypes
        ('current_asset', 'Current Asset'),
        ('fixed_asset', 'Fixed Asset'),
        ('intangible_asset', 'Intangible Asset'),
        ('other_asset', 'Other Asset'),
        # Liability subtypes
        ('current_liability', 'Current Liability'),
        ('long_term_liability', 'Long Term Liability'),
        ('other_liability', 'Other Liability'),
        # Equity subtypes
        ('share_capital', 'Share Capital'),
        ('retained_earnings', 'Retained Earnings'),
        ('other_equity', 'Other Equity'),
        # Income subtypes
        ('sales', 'Sales'),
        ('other_income', 'Other Income'),
        # Expense subtypes
        ('cost_of_goods_sold', 'Cost of Goods Sold'),
        ('operating_expense', 'Operating Expense'),
        ('administrative_expense', 'Administrative Expense'),
        ('selling_expense', 'Selling Expense'),
        ('other_expense', 'Other Expense'),
    ], string='Account Subtype', help='Subtype of account')
    
    parent_id = fields.Many2one(
        'account.account',
        string='Parent Account',
        help='Parent account in hierarchy'
    )
    
    child_ids = fields.One2many(
        'account.account',
        'parent_id',
        string='Child Accounts',
        help='Child accounts'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Currency for this account'
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-16', 'Young Adult (14-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this account')
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('all', 'All Sizes'),
    ], string='Size', help='Size for this account')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this account')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this account'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this account'
    )
    
    # Account Configuration
    reconcile = fields.Boolean(
        string='Allow Reconciliation',
        default=False,
        help='Allow reconciliation of this account'
    )
    
    deprecated = fields.Boolean(
        string='Deprecated',
        default=False,
        help='Mark account as deprecated'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the account is active'
    )
    
    # Account Properties
    user_type_id = fields.Many2one(
        'account.account.type',
        string='Account Type',
        help='Account type for this account'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this account belongs to'
    )
    
    # Financial Information
    balance = fields.Float(
        string='Balance',
        compute='_compute_balance',
        help='Current balance of the account'
    )
    
    debit = fields.Float(
        string='Debit',
        compute='_compute_balance',
        help='Total debit amount'
    )
    
    credit = fields.Float(
        string='Credit',
        compute='_compute_balance',
        help='Total credit amount'
    )
    
    # Account Hierarchy
    level = fields.Integer(
        string='Level',
        compute='_compute_level',
        help='Level in account hierarchy'
    )
    
    full_code = fields.Char(
        string='Full Code',
        compute='_compute_full_code',
        help='Full account code including parent codes'
    )
    
    @api.depends('move_line_ids')
    def _compute_balance(self):
        for record in self:
            move_lines = record.move_line_ids
            record.debit = sum(move_lines.mapped('debit'))
            record.credit = sum(move_lines.mapped('credit'))
            record.balance = record.debit - record.credit
    
    @api.depends('parent_id')
    def _compute_level(self):
        for record in self:
            level = 0
            parent = record.parent_id
            while parent:
                level += 1
                parent = parent.parent_id
            record.level = level
    
    @api.depends('code', 'parent_id')
    def _compute_full_code(self):
        for record in self:
            if record.parent_id:
                record.full_code = f"{record.parent_id.full_code}.{record.code}"
            else:
                record.full_code = record.code
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('code'):
            # Generate code based on account type
            account_type = vals.get('account_type', '')
            if account_type == 'asset':
                prefix = '1'
            elif account_type == 'liability':
                prefix = '2'
            elif account_type == 'equity':
                prefix = '3'
            elif account_type == 'income':
                prefix = '4'
            elif account_type == 'expense':
                prefix = '5'
            else:
                prefix = '9'
            
            # Find next available code
            existing_codes = self.search([('code', 'like', prefix)]).mapped('code')
            next_num = 1
            while f"{prefix}{next_num:03d}" in existing_codes:
                next_num += 1
            vals['code'] = f"{prefix}{next_num:03d}"
        
        return super(AccountAccount, self).create(vals)
    
    @api.constrains('code')
    def _check_code(self):
        for record in self:
            if record.code:
                # Check for duplicate codes
                duplicate = self.search([
                    ('code', '=', record.code),
                    ('id', '!=', record.id),
                    ('company_id', '=', record.company_id.id)
                ])
                if duplicate:
                    raise ValidationError(_('Account code must be unique within the company.'))
    
    @api.constrains('parent_id')
    def _check_parent(self):
        for record in self:
            if record.parent_id:
                # Check for circular reference
                if record.parent_id.id == record.id:
                    raise ValidationError(_('Account cannot be its own parent.'))
                
                # Check parent hierarchy
                parent = record.parent_id
                while parent:
                    if parent.id == record.id:
                        raise ValidationError(_('Circular reference detected in account hierarchy.'))
                    parent = parent.parent_id
    
    def action_view_move_lines(self):
        """View account move lines"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Account Move Lines'),
            'res_model': 'account.move.line',
            'view_mode': 'tree,form',
            'domain': [('account_id', '=', self.id)],
            'context': {'default_account_id': self.id},
        }
    
    def action_reconcile(self):
        """Reconcile account"""
        if not self.reconcile:
            raise UserError(_('This account does not allow reconciliation.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reconcile Account'),
            'res_model': 'account.reconciliation',
            'view_mode': 'form',
            'context': {'default_account_id': self.id},
            'target': 'new',
        }
    
    def action_generate_report(self):
        """Generate account report"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Account Report'),
            'res_model': 'account.report',
            'view_mode': 'form',
            'context': {'default_account_id': self.id},
            'target': 'new',
        }
    
    @api.model
    def get_kids_clothing_accounts(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get accounts filtered by kids clothing criteria"""
        domain = [('active', '=', True)]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if size:
            domain.append(('size', 'in', [size, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)
    
    @api.model
    def create_kids_clothing_chart(self):
        """Create kids clothing specific chart of accounts"""
        # This method would create a complete chart of accounts
        # tailored for kids clothing retail business
        pass


class AccountAccountType(models.Model):
    _name = 'account.account.type'
    _description = 'Account Type'
    _order = 'sequence, name'

    name = fields.Char(
        string='Name',
        required=True,
        help='Name of the account type'
    )
    
    type = fields.Selection([
        ('asset', 'Asset'),
        ('liability', 'Liability'),
        ('equity', 'Equity'),
        ('income', 'Income'),
        ('expense', 'Expense'),
    ], string='Type', required=True, help='Type of account')
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the account type is active'
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-16', 'Young Adult (14-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this account type')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this account type')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this account type'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this account type'
    )
    
    # Account Type Properties
    include_initial_balance = fields.Boolean(
        string='Include Initial Balance',
        default=False,
        help='Include initial balance in reports'
    )
    
    reconcile = fields.Boolean(
        string='Allow Reconciliation',
        default=False,
        help='Allow reconciliation for this account type'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this account type belongs to'
    )