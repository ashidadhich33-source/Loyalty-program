# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Journal Model
=================================

Journal management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class AccountJournal(BaseModel, KidsClothingMixin):
    """Account Journal Model for Ocean ERP"""
    
    _name = 'account.journal'
    _description = 'Account Journal'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Journal Name',
        required=True,
        help='Name of the journal'
    )
    
    code = CharField(
        string='Journal Code',
        required=True,
        help='Code for the journal'
    )
    
    type = SelectionField(
        selection=[
            ('sale', 'Sales'),
            ('purchase', 'Purchase'),
            ('cash', 'Cash'),
            ('bank', 'Bank'),
            ('general', 'General'),
            ('situation', 'Opening/Closing Situation'),
        ],
        string='Journal Type',
        required=True,
        help='Type of journal'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
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
        help='Age group for the journal'
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
        help='Size for the journal'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for the journal'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for the journal'
    )
    
    color = CharField(
        string='Color',
        help='Color for the journal'
    )
    
    # Journal Configuration
    currency_id = Many2OneField(
        'res.currency',
        string='Currency',
        help='Currency for this journal'
    )
    
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this journal belongs to'
    )
    
    # Journal Properties
    show_on_dashboard = BooleanField(
        string='Show on Dashboard',
        default=True,
        help='Show this journal on the dashboard'
    )
    
    restrict_mode_hash_table = BooleanField(
        string='Restrict Mode Hash Table',
        default=False,
        help='Restrict mode hash table'
    )
    
    # Sequence Configuration
    sequence_id = Many2OneField(
        'ir.sequence',
        string='Entry Sequence',
        help='Sequence for journal entries'
    )
    
    refund_sequence_id = Many2OneField(
        'ir.sequence',
        string='Refund Entry Sequence',
        help='Sequence for refund entries'
    )
    
    # Default Accounts
    default_account_id = Many2OneField(
        'account.account',
        string='Default Account',
        help='Default account for this journal'
    )
    
    # Bank Configuration
    bank_id = Many2OneField(
        'res.bank',
        string='Bank',
        help='Bank for this journal'
    )
    
    bank_account_id = Many2OneField(
        'res.partner.bank',
        string='Bank Account',
        help='Bank account for this journal'
    )
    
    # Payment Configuration
    payment_debit_account_id = Many2OneField(
        'account.account',
        string='Payment Debit Account',
        help='Account for payment debits'
    )
    
    payment_credit_account_id = Many2OneField(
        'account.account',
        string='Payment Credit Account',
        help='Account for payment credits'
    )
    
    # Invoice Configuration
    invoice_reference_type = SelectionField(
        selection=[
            ('none', 'Free Reference'),
            ('invoice', 'Based on Invoice'),
        ],
        string='Invoice Reference Type',
        default='none',
        help='Type of invoice reference'
    )
    
    # Alias Configuration
    alias_id = Many2OneField(
        'mail.alias',
        string='Alias',
        help='Email alias for this journal'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('code'):
            # Generate code based on journal type
            journal_type = vals.get('type', '')
            if journal_type == 'sale':
                prefix = 'SALE'
            elif journal_type == 'purchase':
                prefix = 'PURCH'
            elif journal_type == 'cash':
                prefix = 'CASH'
            elif journal_type == 'bank':
                prefix = 'BANK'
            elif journal_type == 'general':
                prefix = 'GEN'
            else:
                prefix = 'JOUR'
            
            # Find next available code
            existing_codes = self.search([('code', 'like', prefix)]).mapped('code')
            next_num = 1
            while f"{prefix}{next_num:03d}" in existing_codes:
                next_num += 1
            vals['code'] = f"{prefix}{next_num:03d}"
        
        return super(AccountJournal, self).create(vals)
    
    def action_create_journal_entry(self):
        """Create a new journal entry"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Create Journal Entry',
            'res_model': 'account.move',
            'view_mode': 'form',
            'context': {'default_journal_id': self.id},
            'target': 'new',
        }
    
    def action_view_journal_entries(self):
        """View journal entries"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Journal Entries',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('journal_id', '=', self.id)],
            'context': {'default_journal_id': self.id},
        }
    
    def get_kids_clothing_journals(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get journals filtered by kids clothing criteria"""
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


class AccountJournalTemplate(BaseModel, KidsClothingMixin):
    """Account Journal Template Model for Ocean ERP"""
    
    _name = 'account.journal.template'
    _description = 'Account Journal Template'
    _order = 'sequence, name'

    name = CharField(
        string='Template Name',
        required=True,
        help='Name of the journal template'
    )
    
    type = SelectionField(
        selection=[
            ('sale', 'Sales'),
            ('purchase', 'Purchase'),
            ('cash', 'Cash'),
            ('bank', 'Bank'),
            ('general', 'General'),
        ],
        string='Journal Type',
        required=True,
        help='Type of journal template'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
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
        help='Age group for the template'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for the template'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for the template'
    )
    
    color = CharField(
        string='Color',
        help='Color for the template'
    )
    
    # Template Configuration
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this template belongs to'
    )
    
    # Template Lines
    line_ids = One2ManyField(
        'account.journal.template.line',
        'template_id',
        string='Template Lines',
        help='Lines for this template'
    )
    
    def create_journal_from_template(self):
        """Create a journal from this template"""
        journal_vals = {
            'name': self.name,
            'type': self.type,
            'sequence': self.sequence,
            'age_group': self.age_group,
            'season': self.season,
            'brand': self.brand,
            'color': self.color,
            'company_id': self.company_id.id,
        }
        
        journal = self.env['account.journal'].create(journal_vals)
        
        # Create journal lines from template lines
        for line in self.line_ids:
            self.env['account.journal.line'].create({
                'journal_id': journal.id,
                'account_id': line.account_id.id,
                'name': line.name,
                'debit': line.debit,
                'credit': line.credit,
                'age_group': line.age_group,
                'size': line.size,
                'season': line.season,
                'brand': line.brand,
                'color': line.color,
            })
        
        return journal


class AccountJournalTemplateLine(BaseModel, KidsClothingMixin):
    """Account Journal Template Line Model for Ocean ERP"""
    
    _name = 'account.journal.template.line'
    _description = 'Account Journal Template Line'
    _order = 'sequence'

    template_id = Many2OneField(
        'account.journal.template',
        string='Template',
        required=True,
        help='Template this line belongs to'
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