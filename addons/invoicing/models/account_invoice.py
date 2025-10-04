# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _description = 'Customer Invoice'
    _order = 'date_invoice desc, number desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # Basic Information
    name = fields.Char(
        string='Invoice Number',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New')
    )
    number = fields.Char(
        string='Invoice Number',
        copy=False,
        readonly=True
    )
    date_invoice = fields.Date(
        string='Invoice Date',
        required=True,
        default=fields.Date.context_today
    )
    date_due = fields.Date(
        string='Due Date',
        required=True
    )
    reference = fields.Char(
        string='Reference',
        help='Customer reference for this invoice'
    )
    
    # Partner Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        domain=[('is_company', '=', True)]
    )
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string='Shipping Address',
        help='Shipping address for this invoice'
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
    
    # Invoice Lines
    invoice_line_ids = fields.One2many(
        'account.invoice.line',
        'invoice_id',
        string='Invoice Lines',
        copy=True
    )
    
    # Tax Information
    tax_line_ids = fields.One2many(
        'account.invoice.tax',
        'invoice_id',
        string='Tax Lines',
        readonly=True
    )
    
    # Amounts
    amount_untaxed = fields.Monetary(
        string='Untaxed Amount',
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_tax = fields.Monetary(
        string='Tax Amount',
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_total = fields.Monetary(
        string='Total Amount',
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    amount_residual = fields.Monetary(
        string='Amount Due',
        store=True,
        readonly=True,
        compute='_compute_residual'
    )
    
    # Payment Information
    payment_ids = fields.One2many(
        'account.payment',
        'invoice_id',
        string='Payments'
    )
    payment_state = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('reversed', 'Reversed'),
        ('invoicing_legacy', 'Invoicing App Legacy'),
    ], string='Payment Status', readonly=True, copy=False, tracking=True)
    
    # State Management
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', readonly=True, default='draft', copy=False, tracking=True)
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
    ], string='Age Group', help='Primary age group for this invoice')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this invoice')
    
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
    
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position',
        string='Fiscal Position'
    )
    
    # EDI Fields
    edi_document_id = fields.Many2one(
        'edi.document',
        string='EDI Document',
        readonly=True
    )
    edi_status = fields.Selection([
        ('not_sent', 'Not Sent'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('rejected', 'Rejected'),
    ], string='EDI Status', default='not_sent', readonly=True)
    
    # Additional Fields
    note = fields.Text(
        string='Terms & Conditions',
        help='Terms and conditions for this invoice'
    )
    comment = fields.Text(
        string='Additional Information',
        help='Additional information or comments'
    )
    
    # Computed Fields
    invoice_count = fields.Integer(
        string='Invoice Count',
        compute='_compute_invoice_count'
    )
    
    @api.depends('invoice_line_ids.price_subtotal', 'tax_line_ids.amount')
    def _compute_amount(self):
        for invoice in self:
            invoice.amount_untaxed = sum(line.price_subtotal for line in invoice.invoice_line_ids)
            invoice.amount_tax = sum(line.amount for line in invoice.tax_line_ids)
            invoice.amount_total = invoice.amount_untaxed + invoice.amount_tax
    
    @api.depends('amount_total', 'payment_ids.amount')
    def _compute_residual(self):
        for invoice in self:
            total_paid = sum(payment.amount for payment in invoice.payment_ids if payment.state == 'posted')
            invoice.amount_residual = invoice.amount_total - total_paid
    
    @api.depends('partner_id')
    def _compute_invoice_count(self):
        for invoice in self:
            if invoice.partner_id:
                invoice.invoice_count = self.env['account.invoice'].search_count([
                    ('partner_id', '=', invoice.partner_id.id)
                ])
            else:
                invoice.invoice_count = 0
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('account.invoice') or _('New')
        return super(AccountInvoice, self).create(vals)
    
    def action_post(self):
        """Post the invoice"""
        for invoice in self:
            if invoice.state != 'draft':
                raise UserError(_('Only draft invoices can be posted.'))
            
            # Set due date if not set
            if not invoice.date_due:
                invoice.date_due = invoice.date_invoice
            
            # Compute taxes
            invoice._compute_tax_line_ids()
            
            # Change state
            invoice.state = 'open'
            invoice.payment_state = 'not_paid'
            
            # Create EDI document if required
            if invoice.company_id.country_id.code == 'IN':
                invoice._create_edi_document()
        
        return True
    
    def action_cancel(self):
        """Cancel the invoice"""
        for invoice in self:
            if invoice.state in ['paid']:
                raise UserError(_('Cannot cancel a paid invoice.'))
            invoice.state = 'cancelled'
        return True
    
    def action_draft(self):
        """Set invoice to draft"""
        for invoice in self:
            invoice.state = 'draft'
        return True
    
    def _compute_tax_line_ids(self):
        """Compute tax lines for the invoice"""
        for invoice in self:
            tax_lines = self.env['account.invoice.tax']
            for line in invoice.invoice_line_ids:
                for tax in line.tax_ids:
                    tax_line = tax_lines.filtered(lambda t: t.tax_id == tax)
                    if tax_line:
                        tax_line.amount += line.price_subtotal * tax.amount / 100
                    else:
                        tax_lines |= self.env['account.invoice.tax'].create({
                            'invoice_id': invoice.id,
                            'tax_id': tax.id,
                            'amount': line.price_subtotal * tax.amount / 100,
                            'base': line.price_subtotal,
                        })
            invoice.tax_line_ids = tax_lines
    
    def _create_edi_document(self):
        """Create EDI document for Indian compliance"""
        if not self.company_id.country_id.code == 'IN':
            return
        
        edi_document = self.env['edi.document'].create({
            'name': f'Invoice {self.name}',
            'document_type': 'invoice',
            'partner_id': self.partner_id.id,
            'amount': self.amount_total,
            'date': self.date_invoice,
            'state': 'draft',
        })
        self.edi_document_id = edi_document.id
    
    def action_view_payments(self):
        """View payments for this invoice"""
        action = self.env.ref('invoicing.action_account_payment').read()[0]
        action['domain'] = [('invoice_id', '=', self.id)]
        action['context'] = {'default_invoice_id': self.id}
        return action
    
    def action_send_invoice(self):
        """Send invoice by email"""
        template = self.env.ref('invoicing.email_template_invoice')
        template.send_mail(self.id, force_send=True)
        return True
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            self.partner_shipping_id = self.partner_id
            self.fiscal_position_id = self.partner_id.property_account_position_id
    
    @api.onchange('date_invoice')
    def _onchange_date_invoice(self):
        if self.date_invoice and not self.date_due:
            self.date_due = self.date_invoice