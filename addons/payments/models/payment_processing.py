# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class PaymentProcessing(models.Model):
    _name = 'payment.processing'
    _description = 'Payment Processing'
    _order = 'date desc, name desc'

    # Basic Information
    name = fields.Char(
        string='Processing Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    date = fields.Date(
        string='Processing Date',
        required=True,
        default=fields.Date.context_today
    )
    
    # Payment Reference
    payment_id = fields.Many2one(
        'account.payment',
        string='Payment',
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
        related='payment_id.currency_id',
        store=True
    )
    
    # Processing Details
    amount = fields.Monetary(
        string='Amount',
        related='payment_id.amount',
        store=True
    )
    payment_method_id = fields.Many2one(
        'account.payment.method',
        string='Payment Method',
        related='payment_id.payment_method_id',
        store=True
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this payment processing')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this payment processing')
    
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
    
    # Processing Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('processing', 'Processing'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', readonly=True, default='draft', copy=False, tracking=True)
    
    # Processing Details
    processing_reference = fields.Char(
        string='Processing Reference',
        help='Reference from payment processor'
    )
    processing_response = fields.Text(
        string='Processing Response',
        help='Response from payment processor'
    )
    error_message = fields.Text(
        string='Error Message',
        help='Error message if processing failed'
    )
    
    # Additional Fields
    note = fields.Text(
        string='Notes',
        help='Additional notes about this payment processing'
    )
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('payment.processing') or _('New')
        return super(PaymentProcessing, self).create(vals)
    
    def action_process(self):
        """Process the payment"""
        for processing in self:
            if processing.state != 'draft':
                raise UserError(_('Only draft payments can be processed.'))
            
            processing.state = 'processing'
            
            # Simulate payment processing
            try:
                # Here you would integrate with actual payment processors
                # For now, we'll simulate success
                processing.state = 'success'
                processing.processing_reference = f'PROC_{processing.id:06d}'
                processing.processing_response = 'Payment processed successfully'
                
                # Update payment state
                if processing.payment_id:
                    processing.payment_id.state = 'posted'
                
            except Exception as e:
                processing.state = 'failed'
                processing.error_message = str(e)
        
        return True
    
    def action_cancel(self):
        """Cancel the payment processing"""
        for processing in self:
            if processing.state in ['success']:
                raise UserError(_('Cannot cancel a successful payment processing.'))
            processing.state = 'cancelled'
        return True
    
    def action_draft(self):
        """Set processing to draft"""
        for processing in self:
            processing.state = 'draft'
        return True
    
    @api.onchange('payment_id')
    def _onchange_payment_id(self):
        if self.payment_id:
            self.currency_id = self.payment_id.currency_id
            self.age_group = self.payment_id.age_group
            self.season = self.payment_id.season
            self.gst_treatment = self.payment_id.gst_treatment