# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class BankStatement(models.Model):
    _name = 'bank.statement'
    _description = 'Bank Statement'
    _order = 'date desc, name desc'

    # Basic Information
    name = fields.Char(
        string='Statement Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    date = fields.Date(
        string='Statement Date',
        required=True,
        default=fields.Date.context_today
    )
    
    # Bank Account Reference
    bank_account_id = fields.Many2one(
        'bank.account',
        string='Bank Account',
        required=True
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='bank_account_id.currency_id',
        store=True
    )
    
    # Statement Details
    balance_start = fields.Monetary(
        string='Starting Balance',
        required=True,
        default=0.0
    )
    balance_end = fields.Monetary(
        string='Ending Balance',
        required=True,
        default=0.0
    )
    total_credit = fields.Monetary(
        string='Total Credit',
        compute='_compute_totals',
        store=True
    )
    total_debit = fields.Monetary(
        string='Total Debit',
        compute='_compute_totals',
        store=True
    )
    
    # Statement Lines
    line_ids = fields.One2many(
        'bank.statement.line',
        'statement_id',
        string='Statement Lines',
        copy=True
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this bank statement')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this bank statement')
    
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
    
    # State Management
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft', copy=False, tracking=True)
    
    # Additional Fields
    note = fields.Text(
        string='Notes',
        help='Additional notes about this bank statement'
    )
    
    @api.depends('line_ids.amount')
    def _compute_totals(self):
        for statement in self:
            statement.total_credit = sum(line.amount for line in statement.line_ids if line.amount > 0)
            statement.total_debit = sum(abs(line.amount) for line in statement.line_ids if line.amount < 0)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('bank.statement') or _('New')
        return super(BankStatement, self).create(vals)
    
    def action_open(self):
        """Open the bank statement"""
        for statement in self:
            if statement.state != 'draft':
                raise UserError(_('Only draft statements can be opened.'))
            statement.state = 'open'
        return True
    
    def action_confirm(self):
        """Confirm the bank statement"""
        for statement in self:
            if statement.state != 'open':
                raise UserError(_('Only open statements can be confirmed.'))
            statement.state = 'confirm'
        return True
    
    def action_cancel(self):
        """Cancel the bank statement"""
        for statement in self:
            if statement.state in ['confirm']:
                raise UserError(_('Cannot cancel a confirmed statement.'))
            statement.state = 'cancel'
        return True
    
    def action_draft(self):
        """Set statement to draft"""
        for statement in self:
            statement.state = 'draft'
        return True
    
    @api.onchange('bank_account_id')
    def _onchange_bank_account_id(self):
        if self.bank_account_id:
            self.currency_id = self.bank_account_id.currency_id
            self.age_group = self.bank_account_id.age_group
            self.season = self.bank_account_id.season
            self.gst_treatment = self.bank_account_id.gst_treatment
    
    @api.constrains('balance_start', 'balance_end')
    def _check_balances(self):
        for statement in self:
            if statement.balance_start < 0:
                raise ValidationError(_('Starting balance cannot be negative.'))
            if statement.balance_end < 0:
                raise ValidationError(_('Ending balance cannot be negative.'))