# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Move Model
==============================

Journal entry management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class AccountMove(BaseModel, KidsClothingMixin):
    """Account Move Model for Ocean ERP"""
    
    _name = 'account.move'
    _description = 'Account Move'
    _order = 'date desc, name desc'
    _rec_name = 'name'

    name = CharField(
        string='Entry Number',
        help='Entry number'
    )
    
    date = DateTimeField(
        string='Date',
        required=True,
        help='Date of the entry'
    )
    
    ref = CharField(
        string='Reference',
        help='Reference for the entry'
    )
    
    journal_id = Many2OneField(
        'account.journal',
        string='Journal',
        required=True,
        help='Journal for this entry'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('posted', 'Posted'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the entry'
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
        help='Age group for the entry'
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
        help='Size for the entry'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for the entry'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for the entry'
    )
    
    color = CharField(
        string='Color',
        help='Color for the entry'
    )
    
    # Move Lines
    line_ids = One2ManyField(
        'account.move.line',
        'move_id',
        string='Move Lines',
        help='Lines for this entry'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this entry belongs to'
    )
    
    # Currency
    currency_id = Many2OneField(
        'res.currency',
        string='Currency',
        help='Currency for this entry'
    )
    
    # Amounts
    amount_total = FloatField(
        string='Total Amount',
        compute='_compute_amounts',
        help='Total amount of the entry'
    )
    
    amount_untaxed = FloatField(
        string='Untaxed Amount',
        compute='_compute_amounts',
        help='Untaxed amount of the entry'
    )
    
    amount_tax = FloatField(
        string='Tax Amount',
        compute='_compute_amounts',
        help='Tax amount of the entry'
    )
    
    # Narration
    narration = TextField(
        string='Narration',
        help='Narration for the entry'
    )
    
    # Partner
    partner_id = Many2OneField(
        'res.partner',
        string='Partner',
        help='Partner for this entry'
    )
    
    # Invoice
    invoice_id = Many2OneField(
        'account.invoice',
        string='Invoice',
        help='Invoice for this entry'
    )
    
    # Payment
    payment_id = Many2OneField(
        'account.payment',
        string='Payment',
        help='Payment for this entry'
    )
    
    def _compute_amounts(self):
        """Compute amounts from move lines"""
        for record in self:
            total_debit = sum(record.line_ids.mapped('debit'))
            total_credit = sum(record.line_ids.mapped('credit'))
            record.amount_total = max(total_debit, total_credit)
            record.amount_untaxed = record.amount_total
            record.amount_tax = 0.0
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            # Generate name from journal sequence
            journal = self.env['account.journal'].browse(vals.get('journal_id'))
            if journal.sequence_id:
                vals['name'] = journal.sequence_id.next_by_id()
            else:
                vals['name'] = f"ENTRY/{self.env.context.get('default_date', '')}"
        
        return super(AccountMove, self).create(vals)
    
    def action_post(self):
        """Post the journal entry"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft entries can be posted.')
            
            # Check if entry is balanced
            total_debit = sum(record.line_ids.mapped('debit'))
            total_credit = sum(record.line_ids.mapped('credit'))
            
            if abs(total_debit - total_credit) > 0.01:
                raise UserError('Journal entry is not balanced.')
            
            record.write({'state': 'posted'})
    
    def action_cancel(self):
        """Cancel the journal entry"""
        for record in self:
            if record.state == 'posted':
                raise UserError('Posted entries cannot be cancelled.')
            
            record.write({'state': 'cancel'})
    
    def action_draft(self):
        """Set entry to draft"""
        for record in self:
            record.write({'state': 'draft'})
    
    def action_reverse(self):
        """Reverse the journal entry"""
        for record in self:
            if record.state != 'posted':
                raise UserError('Only posted entries can be reversed.')
            
            # Create reversal entry
            reversal_vals = {
                'name': f"REV-{record.name}",
                'date': record.date,
                'journal_id': record.journal_id.id,
                'ref': f"Reversal of {record.name}",
                'narration': f"Reversal of {record.narration or ''}",
                'partner_id': record.partner_id.id,
                'company_id': record.company_id.id,
                'currency_id': record.currency_id.id,
                'age_group': record.age_group,
                'size': record.size,
                'season': record.season,
                'brand': record.brand,
                'color': record.color,
            }
            
            reversal_entry = self.create(reversal_vals)
            
            # Create reversal lines
            for line in record.line_ids:
                self.env['account.move.line'].create({
                    'move_id': reversal_entry.id,
                    'account_id': line.account_id.id,
                    'name': line.name,
                    'debit': line.credit,  # Reverse debit/credit
                    'credit': line.debit,
                    'partner_id': line.partner_id.id,
                    'age_group': line.age_group,
                    'size': line.size,
                    'season': line.season,
                    'brand': line.brand,
                    'color': line.color,
                })
            
            return reversal_entry
    
    def get_kids_clothing_entries(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get entries filtered by kids clothing criteria"""
        domain = [('state', '=', 'posted')]
        
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


class AccountMoveLine(BaseModel, KidsClothingMixin):
    """Account Move Line Model for Ocean ERP"""
    
    _name = 'account.move.line'
    _description = 'Account Move Line'
    _order = 'move_id, sequence, id'

    move_id = Many2OneField(
        'account.move',
        string='Journal Entry',
        required=True,
        help='Journal entry this line belongs to'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    account_id = Many2OneField(
        'account.account',
        string='Account',
        required=True,
        help='Account for this line'
    )
    
    name = CharField(
        string='Label',
        help='Label for this line'
    )
    
    debit = FloatField(
        string='Debit',
        help='Debit amount'
    )
    
    credit = FloatField(
        string='Credit',
        help='Credit amount'
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
    
    # Product
    product_id = Many2OneField(
        'product.product',
        string='Product',
        help='Product for this line'
    )
    
    # Quantity
    quantity = FloatField(
        string='Quantity',
        help='Quantity for this line'
    )
    
    # Unit Price
    price_unit = FloatField(
        string='Unit Price',
        help='Unit price for this line'
    )
    
    # Amount
    amount_currency = FloatField(
        string='Amount Currency',
        help='Amount in currency'
    )
    
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
    
    # Date
    date = DateTimeField(
        string='Date',
        help='Date for this line'
    )
    
    # Reference
    ref = CharField(
        string='Reference',
        help='Reference for this line'
    )
    
    # Tax
    tax_ids = Many2ManyField(
        'account.tax',
        string='Taxes',
        help='Taxes for this line'
    )
    
    # Analytic
    analytic_account_id = Many2OneField(
        'account.analytic.account',
        string='Analytic Account',
        help='Analytic account for this line'
    )
    
    def _check_balance(self):
        """Check if move lines are balanced"""
        for record in self:
            if record.move_id.state == 'posted':
                total_debit = sum(record.move_id.line_ids.mapped('debit'))
                total_credit = sum(record.move_id.line_ids.mapped('credit'))
                
                if abs(total_debit - total_credit) > 0.01:
                    raise ValidationError('Journal entry is not balanced.')
    
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