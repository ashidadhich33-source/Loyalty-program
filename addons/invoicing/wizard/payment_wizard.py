# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class PaymentWizard(models.TransientModel):
    _name = 'account.payment.wizard'
    _description = 'Payment Wizard'

    # Basic Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        domain=[('is_company', '=', True)]
    )
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice',
        domain="[('state', '=', 'open'), ('partner_id', '=', partner_id)]"
    )
    date = fields.Date(
        string='Payment Date',
        required=True,
        default=fields.Date.context_today
    )
    amount = fields.Monetary(
        string='Payment Amount',
        required=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id
    )
    
    # Payment Details
    payment_method_id = fields.Many2one(
        'account.payment.method',
        string='Payment Method',
        required=True
    )
    payment_reference = fields.Char(
        string='Payment Reference',
        help='Reference of the payment (e.g., cheque number, UPI reference)'
    )
    communication = fields.Char(
        string='Memo',
        help='Additional information about the payment'
    )
    
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
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.invoice_id = False
            return {
                'domain': {
                    'invoice_id': [('state', '=', 'open'), ('partner_id', '=', self.partner_id.id)]
                }
            }
    
    @api.onchange('invoice_id')
    def _onchange_invoice_id(self):
        if self.invoice_id:
            self.amount = self.invoice_id.amount_residual
            self.currency_id = self.invoice_id.currency_id
            self.age_group = self.invoice_id.age_group
            self.season = self.invoice_id.season
    
    def action_create_payment(self):
        """Create payment from wizard"""
        if not self.partner_id:
            raise ValidationError(_('Please select a customer.'))
        
        if not self.amount or self.amount <= 0:
            raise ValidationError(_('Payment amount must be greater than 0.'))
        
        # Create payment
        payment_vals = {
            'partner_id': self.partner_id.id,
            'invoice_id': self.invoice_id.id if self.invoice_id else False,
            'date': self.date,
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'payment_method_id': self.payment_method_id.id,
            'payment_type': 'inbound',
            'payment_reference': self.payment_reference,
            'communication': self.communication,
            'age_group': self.age_group,
            'season': self.season,
        }
        
        payment = self.env['account.payment'].create(payment_vals)
        
        # Return action to open the created payment
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'res_id': payment.id,
            'view_mode': 'form',
            'target': 'current',
        }