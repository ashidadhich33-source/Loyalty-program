# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Reconciliation Model
========================================

Account reconciliation management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class AccountReconciliation(BaseModel, KidsClothingMixin):
    """Account Reconciliation Model for Ocean ERP"""
    
    _name = 'account.reconciliation'
    _description = 'Account Reconciliation'
    _order = 'date desc, name desc'
    _rec_name = 'name'

    name = CharField(
        string='Reconciliation Name',
        required=True,
        help='Name of the reconciliation'
    )
    
    date = DateTimeField(
        string='Date',
        required=True,
        help='Date of the reconciliation'
    )
    
    account_id = Many2OneField(
        'account.account',
        string='Account',
        required=True,
        help='Account to reconcile'
    )
    
    reconciliation_type = SelectionField(
        selection=[
            ('bank', 'Bank Reconciliation'),
            ('customer', 'Customer Reconciliation'),
            ('supplier', 'Supplier Reconciliation'),
            ('inventory', 'Inventory Reconciliation'),
        ],
        string='Reconciliation Type',
        required=True,
        help='Type of reconciliation'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the reconciliation'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        selection=[
            ('0-2', 'Baby (0-2 years)'),
            ('2-4', 'Toddler (2-4 years)'),
            ('4-6', 'Pre-school (4-6 years)'),
            ('6-8', 'Early School (6-8 years)'),
            ('8-10', 'Middle School (8-10 years)'),
            ('10-12', 'Late School (10-12 years)'),
            ('12-14', 'Teen (12-14 years)'),
            ('14-16', 'Young Adult (14-16 years)'),
            ('all', 'All Age Groups'),
        ],
        string='Age Group',
        help='Age group for the reconciliation'
    )
    
    size = SelectionField(
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('xxxl', 'XXXL'),
            ('all', 'All Sizes'),
        ],
        string='Size',
        help='Size for the reconciliation'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for the reconciliation'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for the reconciliation'
    )
    
    color = CharField(
        string='Color',
        help='Color for the reconciliation'
    )
    
    # Reconciliation Lines
    line_ids = One2ManyField(
        'account.reconciliation.line',
        'reconciliation_id',
        string='Reconciliation Lines',
        help='Lines for this reconciliation'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this reconciliation belongs to'
    )
    
    # Currency
    currency_id = Many2OneField(
        'res.currency',
        string='Currency',
        help='Currency for this reconciliation'
    )
    
    # Amounts
    total_amount = FloatField(
        string='Total Amount',
        compute='_compute_amounts',
        help='Total amount of the reconciliation'
    )
    
    reconciled_amount = FloatField(
        string='Reconciled Amount',
        compute='_compute_amounts',
        help='Reconciled amount'
    )
    
    unreconciled_amount = FloatField(
        string='Unreconciled Amount',
        compute='_compute_amounts',
        help='Unreconciled amount'
    )
    
    # Partner
    partner_id = Many2OneField(
        'res.partner',
        string='Partner',
        help='Partner for this reconciliation'
    )
    
    # Bank
    bank_id = Many2OneField(
        'res.bank',
        string='Bank',
        help='Bank for this reconciliation'
    )
    
    # Bank Account
    bank_account_id = Many2OneField(
        'res.partner.bank',
        string='Bank Account',
        help='Bank account for this reconciliation'
    )
    
    # Notes
    notes = TextField(
        string='Notes',
        help='Notes for this reconciliation'
    )
    
    def _compute_amounts(self):
        """Compute amounts from reconciliation lines"""
        for record in self:
            total_amount = sum(record.line_ids.mapped('amount'))
            reconciled_amount = sum(record.line_ids.filtered('reconciled').mapped('amount'))
            record.total_amount = total_amount
            record.reconciled_amount = reconciled_amount
            record.unreconciled_amount = total_amount - reconciled_amount
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            # Generate name from account and date
            account = self.env['account.account'].browse(vals.get('account_id'))
            date = vals.get('date', '')
            vals['name'] = f"REC-{account.code}-{date}"
        
        return super(AccountReconciliation, self).create(vals)
    
    def action_start(self):
        """Start the reconciliation"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft reconciliations can be started.')
            
            record.write({'state': 'in_progress'})
    
    def action_complete(self):
        """Complete the reconciliation"""
        for record in self:
            if record.state != 'in_progress':
                raise UserError('Only in-progress reconciliations can be completed.')
            
            # Check if all lines are reconciled
            unreconciled_lines = record.line_ids.filtered(lambda l: not l.reconciled)
            if unreconciled_lines:
                raise UserError('Cannot complete reconciliation with unreconciled lines.')
            
            record.write({'state': 'completed'})
    
    def action_cancel(self):
        """Cancel the reconciliation"""
        for record in self:
            if record.state == 'completed':
                raise UserError('Completed reconciliations cannot be cancelled.')
            
            record.write({'state': 'cancelled'})
    
    def action_reopen(self):
        """Reopen the reconciliation"""
        for record in self:
            if record.state != 'completed':
                raise UserError('Only completed reconciliations can be reopened.')
            
            record.write({'state': 'in_progress'})
    
    def action_view_lines(self):
        """View reconciliation lines"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Reconciliation Lines',
            'res_model': 'account.reconciliation.line',
            'view_mode': 'tree,form',
            'domain': [('reconciliation_id', '=', self.id)],
            'context': {'default_reconciliation_id': self.id},
        }
    
    def get_kids_clothing_reconciliations(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get reconciliations filtered by kids clothing criteria"""
        domain = [('state', '=', 'completed')]
        
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


class AccountReconciliationLine(BaseModel, KidsClothingMixin):
    """Account Reconciliation Line Model for Ocean ERP"""
    
    _name = 'account.reconciliation.line'
    _description = 'Account Reconciliation Line'
    _order = 'reconciliation_id, sequence, id'

    reconciliation_id = Many2OneField(
        'account.reconciliation',
        string='Reconciliation',
        required=True,
        help='Reconciliation this line belongs to'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    move_line_id = Many2OneField(
        'account.move.line',
        string='Move Line',
        help='Move line for this reconciliation'
    )
    
    name = CharField(
        string='Description',
        help='Description for this line'
    )
    
    date = DateTimeField(
        string='Date',
        help='Date for this line'
    )
    
    amount = FloatField(
        string='Amount',
        help='Amount for this line'
    )
    
    reconciled = BooleanField(
        string='Reconciled',
        default=False,
        help='Whether this line is reconciled'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        selection=[
            ('0-2', 'Baby (0-2 years)'),
            ('2-4', 'Toddler (2-4 years)'),
            ('4-6', 'Pre-school (4-6 years)'),
            ('6-8', 'Early School (6-8 years)'),
            ('8-10', 'Middle School (8-10 years)'),
            ('10-12', 'Late School (10-12 years)'),
            ('12-14', 'Teen (12-14 years)'),
            ('14-16', 'Young Adult (14-16 years)'),
            ('all', 'All Age Groups'),
        ],
        string='Age Group',
        help='Age group for this line'
    )
    
    size = SelectionField(
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('xxxl', 'XXXL'),
            ('all', 'All Sizes'),
        ],
        string='Size',
        help='Size for this line'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this line'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this line'
    )
    
    color = CharField(
        string='Color',
        help='Color for this line'
    )
    
    # Partner
    partner_id = Many2OneField(
        'res.partner',
        string='Partner',
        help='Partner for this line'
    )
    
    # Reference
    ref = CharField(
        string='Reference',
        help='Reference for this line'
    )
    
    # Currency
    currency_id = Many2OneField(
        'res.currency',
        string='Currency',
        help='Currency for this line'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this line belongs to'
    )
    
    def action_reconcile(self):
        """Reconcile this line"""
        for record in self:
            if record.reconciled:
                raise UserError('Line is already reconciled.')
            
            record.write({'reconciled': True})
    
    def action_unreconcile(self):
        """Unreconcile this line"""
        for record in self:
            if not record.reconciled:
                raise UserError('Line is not reconciled.')
            
            record.write({'reconciled': False})
    
    def get_kids_clothing_lines(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get lines filtered by kids clothing criteria"""
        domain = []
        
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