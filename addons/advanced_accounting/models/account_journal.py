# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Advanced Accounting - Journal Management
===========================================================

Journal management for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    """Journal"""
    
    _name = 'account.journal'
    _description = 'Journal'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Journal Name',
        required=True,
        help='Journal name'
    )
    
    code = fields.Char(
        string='Journal Code',
        required=True,
        help='Journal code (e.g., SAL, PUR, etc.)'
    )
    
    # Journal Type
    journal_type = fields.Selection([
        ('sale', 'Sales'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'General'),
        ('opening', 'Opening'),
        ('closing', 'Closing'),
        ('miscellaneous', 'Miscellaneous'),
    ], string='Journal Type', required=True, help='Type of journal')
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        help='Company this journal belongs to'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Journal currency'
    )
    
    # Sequence
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering journals'
    )
    
    # Default Accounts
    default_debit_account_id = fields.Many2one(
        'account.account',
        string='Default Debit Account',
        help='Default debit account for this journal'
    )
    
    default_credit_account_id = fields.Many2one(
        'account.account',
        string='Default Credit Account',
        help='Default credit account for this journal'
    )
    
    # Bank Information (for bank journals)
    bank_id = fields.Many2one(
        'res.bank',
        string='Bank',
        help='Bank for bank journals'
    )
    
    bank_account_id = fields.Many2one(
        'res.partner.bank',
        string='Bank Account',
        help='Bank account for bank journals'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this journal')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this journal')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this journal relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this journal')
    
    # Indian Compliance Fields
    gst_applicable = fields.Boolean(
        string='GST Applicable',
        default=True,
        help='Whether GST is applicable to this journal'
    )
    
    tds_applicable = fields.Boolean(
        string='TDS Applicable',
        default=False,
        help='Whether TDS is applicable to this journal'
    )
    
    # Status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this journal is active'
    )
    
    # Analytics
    total_entries = fields.Integer(
        string='Total Entries',
        compute='_compute_analytics',
        store=True,
        help='Total number of entries'
    )
    
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
        help='Additional notes about this journal'
    )
    
    @api.depends('name')
    def _compute_analytics(self):
        """Compute analytics"""
        for journal in self:
            # This would be computed from journal entries
            # For now, setting to 0
            journal.total_entries = 0
            journal.total_debit = 0.0
            journal.total_credit = 0.0
    
    @api.constrains('code')
    def _check_code(self):
        """Validate journal code"""
        for journal in self:
            if not journal.code:
                raise ValidationError(_('Journal code is required.'))
            
            # Check for duplicate codes
            duplicate = self.search([
                ('code', '=', journal.code),
                ('company_id', '=', journal.company_id.id),
                ('id', '!=', journal.id)
            ])
            if duplicate:
                raise ValidationError(_('Journal code must be unique within the company.'))
    
    @api.constrains('journal_type', 'bank_id')
    def _check_bank_journal(self):
        """Validate bank journal"""
        for journal in self:
            if journal.journal_type == 'bank' and not journal.bank_id:
                raise ValidationError(_('Bank journals must have a bank specified.'))
    
    def name_get(self):
        """Return display name"""
        result = []
        for journal in self:
            result.append((journal.id, f"{journal.code} - {journal.name}"))
        return result
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """Search by name or code"""
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('code', operator, name)]
        journals = self.search(domain + args, limit=limit)
        return journals.name_get()
    
    def action_view_entries(self):
        """View journal entries"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Journal Entries'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('journal_id', '=', self.id)],
            'context': {'default_journal_id': self.id},
        }
    
    def action_create_entry(self):
        """Create new journal entry"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Journal Entry'),
            'res_model': 'account.move',
            'view_mode': 'form',
            'context': {
                'default_journal_id': self.id,
                'default_move_type': 'entry',
            },
        }
    
    def get_journal_analytics(self, date_from=None, date_to=None):
        """Get journal analytics for date range"""
        self.ensure_one()
        # This would query journal entries
        # For now, returning basic info
        return {
            'total_entries': self.total_entries,
            'total_debit': self.total_debit,
            'total_credit': self.total_credit,
        }