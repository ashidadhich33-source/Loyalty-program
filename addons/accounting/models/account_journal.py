# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountJournal(models.Model):
    _name = 'account.journal'
    _description = 'Journal'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = fields.Char(
        string='Journal Name',
        required=True,
        help='Name of the journal'
    )
    
    code = fields.Char(
        string='Journal Code',
        required=True,
        help='Short code for the journal'
    )
    
    type = fields.Selection([
        ('sale', 'Sales'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'General'),
        ('situation', 'Situation'),
        ('opening', 'Opening'),
        ('closing', 'Closing'),
    ], string='Journal Type', required=True, help='Type of journal')
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the journal is active'
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
    ], string='Age Group', help='Age group for this journal')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this journal')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this journal'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this journal'
    )
    
    # Journal Configuration
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this journal belongs to'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Currency for this journal'
    )
    
    # Default Accounts
    default_account_id = fields.Many2one(
        'account.account',
        string='Default Account',
        help='Default account for this journal'
    )
    
    default_credit_account_id = fields.Many2one(
        'account.account',
        string='Default Credit Account',
        help='Default credit account for this journal'
    )
    
    default_debit_account_id = fields.Many2one(
        'account.account',
        string='Default Debit Account',
        help='Default debit account for this journal'
    )
    
    # Journal Properties
    show_on_dashboard = fields.Boolean(
        string='Show on Dashboard',
        default=True,
        help='Show this journal on the dashboard'
    )
    
    show_on_invoice = fields.Boolean(
        string='Show on Invoice',
        default=False,
        help='Show this journal on invoices'
    )
    
    # Journal Entries
    move_ids = fields.One2many(
        'account.move',
        'journal_id',
        string='Journal Entries',
        help='Journal entries in this journal'
    )
    
    # Journal Statistics
    total_entries = fields.Integer(
        string='Total Entries',
        compute='_compute_statistics',
        help='Total number of entries'
    )
    
    total_debit = fields.Float(
        string='Total Debit',
        compute='_compute_statistics',
        help='Total debit amount'
    )
    
    total_credit = fields.Float(
        string='Total Credit',
        compute='_compute_statistics',
        help='Total credit amount'
    )
    
    last_entry_date = fields.Date(
        string='Last Entry Date',
        compute='_compute_statistics',
        help='Date of last entry'
    )
    
    @api.depends('move_ids')
    def _compute_statistics(self):
        for record in self:
            moves = record.move_ids.filtered(lambda m: m.state == 'posted')
            record.total_entries = len(moves)
            record.total_debit = sum(moves.mapped('line_ids.debit'))
            record.total_credit = sum(moves.mapped('line_ids.credit'))
            
            if moves:
                record.last_entry_date = max(moves.mapped('date'))
            else:
                record.last_entry_date = False
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('code'):
            # Generate code based on journal type
            journal_type = vals.get('type', 'general')
            if journal_type == 'sale':
                prefix = 'SAL'
            elif journal_type == 'purchase':
                prefix = 'PUR'
            elif journal_type == 'cash':
                prefix = 'CSH'
            elif journal_type == 'bank':
                prefix = 'BNK'
            elif journal_type == 'general':
                prefix = 'GEN'
            else:
                prefix = 'JRN'
            
            # Find next available code
            existing_codes = self.search([('code', 'like', prefix)]).mapped('code')
            next_num = 1
            while f"{prefix}{next_num:03d}" in existing_codes:
                next_num += 1
            vals['code'] = f"{prefix}{next_num:03d}"
        
        return super(AccountJournal, self).create(vals)
    
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
                    raise ValidationError(_('Journal code must be unique within the company.'))
    
    def action_create_entry(self):
        """Create a new journal entry"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Journal Entry'),
            'res_model': 'account.move',
            'view_mode': 'form',
            'context': {'default_journal_id': self.id},
            'target': 'current',
        }
    
    def action_view_entries(self):
        """View journal entries"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Journal Entries'),
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('journal_id', '=', self.id)],
            'context': {'default_journal_id': self.id},
        }
    
    def action_generate_report(self):
        """Generate journal report"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Journal Report'),
            'res_model': 'account.report',
            'view_mode': 'form',
            'context': {'default_journal_id': self.id},
            'target': 'new',
        }
    
    @api.model
    def get_kids_clothing_journals(self, age_group=None, season=None, brand=None, color=None):
        """Get journals filtered by kids clothing criteria"""
        domain = [('active', '=', True)]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)
    
    @api.model
    def create_kids_clothing_journals(self):
        """Create kids clothing specific journals"""
        # This method would create journals tailored for kids clothing retail
        pass


class AccountJournalTemplate(models.Model):
    _name = 'account.journal.template'
    _description = 'Journal Template'
    _order = 'sequence, name'

    name = fields.Char(
        string='Template Name',
        required=True,
        help='Name of the journal template'
    )
    
    journal_type = fields.Selection([
        ('sale', 'Sales'),
        ('purchase', 'Purchase'),
        ('cash', 'Cash'),
        ('bank', 'Bank'),
        ('general', 'General'),
    ], string='Journal Type', required=True, help='Type of journal')
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the template is active'
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
    ], string='Age Group', help='Age group for this template')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this template')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this template'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this template'
    )
    
    # Template Lines
    template_line_ids = fields.One2many(
        'account.journal.template.line',
        'template_id',
        string='Template Lines',
        help='Lines of the journal template'
    )
    
    # Template Properties
    description = fields.Text(
        string='Description',
        help='Description of the template'
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this template belongs to'
    )
    
    def action_create_journal_entry(self):
        """Create journal entry from template"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Journal Entry'),
            'res_model': 'account.move',
            'view_mode': 'form',
            'context': {
                'default_journal_template_id': self.id,
                'default_template_lines': [(0, 0, {
                    'account_id': line.account_id.id,
                    'debit': line.debit,
                    'credit': line.credit,
                    'name': line.name,
                }) for line in self.template_line_ids]
            },
            'target': 'current',
        }


class AccountJournalTemplateLine(models.Model):
    _name = 'account.journal.template.line'
    _description = 'Journal Template Line'
    _order = 'sequence'

    template_id = fields.Many2one(
        'account.journal.template',
        string='Template',
        required=True,
        ondelete='cascade',
        help='Journal template this line belongs to'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    account_id = fields.Many2one(
        'account.account',
        string='Account',
        required=True,
        help='Account for this line'
    )
    
    name = fields.Char(
        string='Description',
        help='Description of this line'
    )
    
    debit = fields.Float(
        string='Debit',
        digits='Account',
        help='Debit amount'
    )
    
    credit = fields.Float(
        string='Credit',
        digits='Account',
        help='Credit amount'
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
    ], string='Age Group', help='Age group for this line')
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('all', 'All Sizes'),
    ], string='Size', help='Size for this line')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this line')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this line'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this line'
    )
    
    @api.constrains('debit', 'credit')
    def _check_amounts(self):
        for record in self:
            if record.debit and record.credit:
                raise ValidationError(_('A line cannot have both debit and credit amounts.'))
            
            if not record.debit and not record.credit:
                raise ValidationError(_('A line must have either debit or credit amount.'))