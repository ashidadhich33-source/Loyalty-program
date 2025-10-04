# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceTax(models.Model):
    _name = 'account.invoice.tax'
    _description = 'Invoice Tax'
    _order = 'invoice_id, sequence'

    # Basic Information
    name = fields.Char(
        string='Tax Description',
        required=True
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    
    # Invoice Reference
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    # Tax Information
    tax_id = fields.Many2one(
        'account.tax',
        string='Tax',
        required=True
    )
    
    # Amounts
    base = fields.Monetary(
        string='Base Amount',
        required=True,
        default=0.0
    )
    amount = fields.Monetary(
        string='Tax Amount',
        required=True,
        default=0.0
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='invoice_id.currency_id',
        store=True
    )
    
    # Indian GST Specific Fields
    cgst_amount = fields.Monetary(
        string='CGST Amount',
        compute='_compute_gst_amounts',
        store=True
    )
    sgst_amount = fields.Monetary(
        string='SGST Amount',
        compute='_compute_gst_amounts',
        store=True
    )
    igst_amount = fields.Monetary(
        string='IGST Amount',
        compute='_compute_gst_amounts',
        store=True
    )
    utgst_amount = fields.Monetary(
        string='UTGST Amount',
        compute='_compute_gst_amounts',
        store=True
    )
    cess_amount = fields.Monetary(
        string='CESS Amount',
        compute='_compute_gst_amounts',
        store=True
    )
    
    @api.depends('tax_id', 'amount')
    def _compute_gst_amounts(self):
        for tax_line in self:
            if tax_line.tax_id and tax_line.tax_id.tax_group_id:
                group_name = tax_line.tax_id.tax_group_id.name.lower()
                if 'cgst' in group_name:
                    tax_line.cgst_amount = tax_line.amount
                elif 'sgst' in group_name:
                    tax_line.sgst_amount = tax_line.amount
                elif 'igst' in group_name:
                    tax_line.igst_amount = tax_line.amount
                elif 'utgst' in group_name:
                    tax_line.utgst_amount = tax_line.amount
                elif 'cess' in group_name:
                    tax_line.cess_amount = tax_line.amount