# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceReport(models.Model):
    _name = 'account.invoice.report'
    _description = 'Invoice Report'
    _auto = False
    _order = 'date_invoice desc'

    # Basic Information
    name = fields.Char(
        string='Invoice Number',
        readonly=True
    )
    date_invoice = fields.Date(
        string='Invoice Date',
        readonly=True
    )
    date_due = fields.Date(
        string='Due Date',
        readonly=True
    )
    
    # Partner Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        readonly=True
    )
    partner_name = fields.Char(
        string='Customer Name',
        readonly=True
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        readonly=True
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        readonly=True
    )
    
    # Amounts
    amount_untaxed = fields.Monetary(
        string='Untaxed Amount',
        readonly=True
    )
    amount_tax = fields.Monetary(
        string='Tax Amount',
        readonly=True
    )
    amount_total = fields.Monetary(
        string='Total Amount',
        readonly=True
    )
    amount_residual = fields.Monetary(
        string='Amount Due',
        readonly=True
    )
    
    # State Information
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', readonly=True)
    
    payment_state = fields.Selection([
        ('not_paid', 'Not Paid'),
        ('in_payment', 'In Payment'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('reversed', 'Reversed'),
        ('invoicing_legacy', 'Invoicing App Legacy'),
    ], string='Payment Status', readonly=True)
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
    ], string='Age Group', readonly=True)
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', readonly=True)
    
    # Indian Compliance Fields
    gst_treatment = fields.Selection([
        ('regular', 'Regular'),
        ('composition', 'Composition'),
        ('unregistered', 'Unregistered'),
        ('consumer', 'Consumer'),
        ('overseas', 'Overseas'),
        ('special_economic_zone', 'Special Economic Zone'),
        ('deemed_export', 'Deemed Export'),
    ], string='GST Treatment', readonly=True)
    
    # EDI Fields
    edi_status = fields.Selection([
        ('not_sent', 'Not Sent'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
        ('rejected', 'Rejected'),
    ], string='EDI Status', readonly=True)
    
    def init(self):
        """Initialize the report view"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT 
                    ai.id,
                    ai.name,
                    ai.date_invoice,
                    ai.date_due,
                    ai.partner_id,
                    rp.name as partner_name,
                    ai.company_id,
                    ai.currency_id,
                    ai.amount_untaxed,
                    ai.amount_tax,
                    ai.amount_total,
                    ai.amount_residual,
                    ai.state,
                    ai.payment_state,
                    ai.age_group,
                    ai.season,
                    ai.gst_treatment,
                    ai.edi_status
                FROM account_invoice ai
                LEFT JOIN res_partner rp ON ai.partner_id = rp.id
                WHERE ai.state != 'cancelled'
            )
        """ % self._table)