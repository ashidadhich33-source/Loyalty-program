# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _name = 'account.move'
    _description = 'Journal Entry'
    _order = 'date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Entry Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        help='Journal entry number'
    )
    
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
        help='Date of the journal entry'
    )
    
    journal_id = fields.Many2one(
        'account.journal',
        string='Journal',
        required=True,
        help='Journal for this entry'
    )
    
    ref = fields.Char(
        string='Reference',
        help='Reference for this entry'
    )
    
    narration = fields.Text(
        string='Narration',
        help='Narration for this entry'
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True, help='State of the entry')
    
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
    ], string='Age Group', help='Age group for this entry')
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
        ('all', 'All Sizes'),
    ], string='Size', help='Size for this entry')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this entry')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for this entry'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for this entry'
    )
    
    # Entry Lines
    line_ids = fields.One2many(
        'account.move.line',
        'move_id',
        string='Entry Lines',
        help='Lines of the journal entry'
    )
    
    # Financial Information
    total_debit = fields.Float(
        string='Total Debit',
        compute='_compute_totals',
        help='Total debit amount'
    )
    
    total_credit = fields.Float(
        string='Total Credit',
        compute='_compute_totals',
        help='Total credit amount'
    )
    
    balance = fields.Float(
        string='Balance',
        compute='_compute_totals',
        help='Balance of the entry'
    )
    
    is_balanced = fields.Boolean(
        string='Is Balanced',
        compute='_compute_totals',
        help='Whether the entry is balanced'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this entry belongs to'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Currency for this entry'
    )
    
    # Timestamps
    create_date = fields.Datetime(
        string='Created On',
        readonly=True,
        help='Date when the entry was created'
    )
    
    posted_date = fields.Datetime(
        string='Posted On',
        readonly=True,
        help='Date when the entry was posted'
    )
    
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        help='User who created the entry'
    )
    
    posted_by = fields.Many2one(
        'res.users',
        string='Posted By',
        readonly=True,
        help='User who posted the entry'
    )
    
    @api.depends('line_ids')
    def _compute_totals(self):
        for record in self:
            lines = record.line_ids
            record.total_debit = sum(lines.mapped('debit'))
            record.total_credit = sum(lines.mapped('credit'))
            record.balance = record.total_debit - record.total_credit
            record.is_balanced = abs(record.balance) < 0.01  # Allow for small rounding differences
    
    @api.model
    def create(self, vals):
        """Override create to generate sequence"""
        if vals.get('name', _('New')) == _('New'):
            journal = self.env['account.journal'].browse(vals.get('journal_id'))
            vals['name'] = self.env['ir.sequence'].with_context(
                journal_id=journal.id
            ).next_by_code('account.move') or _('New')
        return super(AccountMove, self).create(vals)
    
    def action_post(self):
        """Post the journal entry"""
        for record in self:
            if record.state == 'draft':
                if not record.is_balanced:
                    raise UserError(_('Journal entry must be balanced before posting.'))
                
                record.write({
                    'state': 'posted',
                    'posted_date': fields.Datetime.now(),
                    'posted_by': self.env.user.id,
                })
    
    def action_cancel(self):
        """Cancel the journal entry"""
        for record in self:
            if record.state == 'posted':
                # Check if entry can be cancelled
                if record.line_ids.filtered('reconciled'):
                    raise UserError(_('Cannot cancel a journal entry with reconciled lines.'))
                
                record.write({'state': 'cancelled'})
            elif record.state == 'draft':
                record.write({'state': 'cancelled'})
    
    def action_reset_to_draft(self):
        """Reset to draft state"""
        for record in self:
            if record.state == 'cancelled':
                record.write({'state': 'draft'})
    
    @api.constrains('line_ids')
    def _check_lines(self):
        for record in self:
            if not record.line_ids:
                raise ValidationError(_('Journal entry must have at least one line.'))
    
    def action_add_line(self):
        """Add a new line to the entry"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Add Line'),
            'res_model': 'account.move.line',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_move_id': self.id},
        }
    
    def action_reconcile_lines(self):
        """Reconcile lines in this entry"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reconcile Lines'),
            'res_model': 'account.reconciliation',
            'view_mode': 'form',
            'context': {'default_move_id': self.id},
            'target': 'new',
        }
    
    @api.model
    def get_kids_clothing_entries(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get journal entries filtered by kids clothing criteria"""
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
    
    @api.model
    def create_kids_clothing_entry(self, entry_type, amount, age_group=None, size=None, season=None, brand=None, color=None):
        """Create a journal entry for kids clothing transaction"""
        # This method would create entries tailored for kids clothing transactions
        pass


class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _description = 'Journal Entry Line'
    _order = 'move_id, sequence, id'

    move_id = fields.Many2one(
        'account.move',
        string='Journal Entry',
        required=True,
        ondelete='cascade',
        help='Journal entry this line belongs to'
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
    
    balance = fields.Float(
        string='Balance',
        compute='_compute_balance',
        help='Balance of this line'
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
    
    # Partner Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Partner for this line'
    )
    
    # Product Information
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        help='Product for this line'
    )
    
    # Reconciliation
    reconciled = fields.Boolean(
        string='Reconciled',
        default=False,
        help='Whether this line is reconciled'
    )
    
    reconciled_date = fields.Date(
        string='Reconciled Date',
        help='Date when this line was reconciled'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help='Company this line belongs to'
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Currency for this line'
    )
    
    @api.depends('debit', 'credit')
    def _compute_balance(self):
        for record in self:
            record.balance = record.debit - record.credit
    
    @api.constrains('debit', 'credit')
    def _check_amounts(self):
        for record in self:
            if record.debit and record.credit:
                raise ValidationError(_('A line cannot have both debit and credit amounts.'))
            
            if not record.debit and not record.credit:
                raise ValidationError(_('A line must have either debit or credit amount.'))
    
    @api.onchange('account_id')
    def _onchange_account_id(self):
        if self.account_id:
            self.age_group = self.account_id.age_group
            self.size = self.account_id.size
            self.season = self.account_id.season
            self.brand = self.account_id.brand
            self.color = self.account_id.color
    
    def action_reconcile(self):
        """Reconcile this line"""
        if not self.account_id.reconcile:
            raise UserError(_('This account does not allow reconciliation.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': _('Reconcile Line'),
            'res_model': 'account.reconciliation',
            'view_mode': 'form',
            'context': {'default_line_id': self.id},
            'target': 'new',
        }
    
    @api.model
    def get_kids_clothing_lines(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get journal entry lines filtered by kids clothing criteria"""
        domain = [('move_id.state', '=', 'posted')]
        
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