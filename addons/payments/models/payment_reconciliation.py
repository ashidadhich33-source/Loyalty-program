# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class PaymentReconciliation(models.Model):
    _name = 'payment.reconciliation'
    _description = 'Payment Reconciliation'
    _order = 'date desc, name desc'

    # Basic Information
    name = fields.Char(
        string='Reconciliation Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    date = fields.Date(
        string='Reconciliation Date',
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
    
    # Reconciliation Lines
    line_ids = fields.One2many(
        'payment.reconciliation.line',
        'reconciliation_id',
        string='Reconciliation Lines',
        copy=True
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this reconciliation')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this reconciliation')
    
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
        help='Additional notes about this reconciliation'
    )
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('payment.reconciliation') or _('New')
        return super(PaymentReconciliation, self).create(vals)
    
    def action_open(self):
        """Open the reconciliation"""
        for reconciliation in self:
            if reconciliation.state != 'draft':
                raise UserError(_('Only draft reconciliations can be opened.'))
            reconciliation.state = 'open'
        return True
    
    def action_confirm(self):
        """Confirm the reconciliation"""
        for reconciliation in self:
            if reconciliation.state != 'open':
                raise UserError(_('Only open reconciliations can be confirmed.'))
            reconciliation.state = 'confirm'
        return True
    
    def action_cancel(self):
        """Cancel the reconciliation"""
        for reconciliation in self:
            if reconciliation.state in ['confirm']:
                raise UserError(_('Cannot cancel a confirmed reconciliation.'))
            reconciliation.state = 'cancel'
        return True
    
    def action_draft(self):
        """Set reconciliation to draft"""
        for reconciliation in self:
            reconciliation.state = 'draft'
        return True
    
    @api.onchange('bank_account_id')
    def _onchange_bank_account_id(self):
        if self.bank_account_id:
            self.currency_id = self.bank_account_id.currency_id
            self.age_group = self.bank_account_id.age_group
            self.season = self.bank_account_id.season
            self.gst_treatment = self.bank_account_id.gst_treatment


class PaymentReconciliationLine(models.Model):
    _name = 'payment.reconciliation.line'
    _description = 'Payment Reconciliation Line'
    _order = 'date desc, id desc'

    # Basic Information
    name = fields.Char(
        string='Description',
        required=True
    )
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.context_today
    )
    
    # Reconciliation Reference
    reconciliation_id = fields.Many2one(
        'payment.reconciliation',
        string='Reconciliation',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    # Transaction Details
    amount = fields.Monetary(
        string='Amount',
        required=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='reconciliation_id.currency_id',
        store=True
    )
    
    # Transaction Reference
    ref = fields.Char(
        string='Reference',
        help='Transaction reference number'
    )
    
    # Partner Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        help='Partner associated with this transaction'
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this transaction')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this transaction')
    
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
    
    # Reconciliation Status
    is_reconciled = fields.Boolean(
        string='Reconciled',
        default=False,
        help='Whether this line has been reconciled'
    )
    
    # Additional Fields
    note = fields.Text(
        string='Notes',
        help='Additional notes about this transaction'
    )
    
    @api.constrains('amount')
    def _check_amount(self):
        for line in self:
            if line.amount == 0:
                raise ValidationError(_('Amount cannot be zero.'))
    
    @api.onchange('reconciliation_id')
    def _onchange_reconciliation_id(self):
        if self.reconciliation_id:
            self.currency_id = self.reconciliation_id.currency_id
            self.age_group = self.reconciliation_id.age_group
            self.season = self.reconciliation_id.season
            self.gst_treatment = self.reconciliation_id.gst_treatment