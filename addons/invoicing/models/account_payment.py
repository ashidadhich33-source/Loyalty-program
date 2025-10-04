# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _name = 'account.payment'
    _description = 'Account Payment'
    _order = 'date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char(
        string='Payment Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    date = fields.Date(
        string='Payment Date',
        required=True,
        default=fields.Date.context_today
    )
    
    # Partner Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True
    )
    
    # Invoice Reference
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice',
        domain=[('state', '=', 'open')]
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
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    
    # Payment Information
    amount = fields.Monetary(
        string='Payment Amount',
        required=True
    )
    payment_method_id = fields.Many2one(
        'account.payment.method',
        string='Payment Method',
        required=True
    )
    payment_type = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ], string='Payment Type', required=True, default='inbound')
    
    # Payment Details
    payment_reference = fields.Char(
        string='Payment Reference',
        help='Reference of the payment (e.g., cheque number, UPI reference)'
    )
    communication = fields.Char(
        string='Memo',
        help='Additional information about the payment'
    )
    
    # State Management
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('sent', 'Sent'),
        ('reconciled', 'Reconciled'),
        ('cancelled', 'Cancelled'),
    ], string='Status', readonly=True, default='draft', copy=False, tracking=True)
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
    ], string='Age Group', help='Primary age group for this payment')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this payment')
    
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
    
    # Additional Fields
    note = fields.Text(
        string='Notes',
        help='Additional notes about this payment'
    )
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('account.payment') or _('New')
        return super(AccountPayment, self).create(vals)
    
    def action_post(self):
        """Post the payment"""
        for payment in self:
            if payment.state != 'draft':
                raise UserError(_('Only draft payments can be posted.'))
            
            # Validate amount
            if payment.amount <= 0:
                raise ValidationError(_('Payment amount must be greater than 0.'))
            
            # Update invoice payment state if linked
            if payment.invoice_id:
                payment.invoice_id._compute_payment_state()
            
            # Change state
            payment.state = 'posted'
        
        return True
    
    def action_cancel(self):
        """Cancel the payment"""
        for payment in self:
            if payment.state in ['reconciled']:
                raise UserError(_('Cannot cancel a reconciled payment.'))
            payment.state = 'cancelled'
        return True
    
    def action_draft(self):
        """Set payment to draft"""
        for payment in self:
            payment.state = 'draft'
        return True
    
    def action_reconcile(self):
        """Reconcile the payment with invoice"""
        for payment in self:
            if payment.invoice_id and payment.state == 'posted':
                # Update invoice payment state
                payment.invoice_id._compute_payment_state()
                payment.state = 'reconciled'
        return True
    
    @api.onchange('invoice_id')
    def _onchange_invoice_id(self):
        if self.invoice_id:
            self.partner_id = self.invoice_id.partner_id
            self.amount = self.invoice_id.amount_residual
            self.currency_id = self.invoice_id.currency_id
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.gst_treatment = self.partner_id.l10n_in_gst_treatment
    
    @api.constrains('amount')
    def _check_amount(self):
        for payment in self:
            if payment.amount <= 0:
                raise ValidationError(_('Payment amount must be greater than 0.'))
    
    @api.constrains('invoice_id', 'amount')
    def _check_invoice_amount(self):
        for payment in self:
            if payment.invoice_id and payment.amount > payment.invoice_id.amount_residual:
                raise ValidationError(_('Payment amount cannot exceed invoice residual amount.'))