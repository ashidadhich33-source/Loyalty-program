# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class BankStatementLine(models.Model):
    _name = 'bank.statement.line'
    _description = 'Bank Statement Line'
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
    
    # Statement Reference
    statement_id = fields.Many2one(
        'bank.statement',
        string='Bank Statement',
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
        related='statement_id.currency_id',
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
    
    # Reconciliation
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
    
    @api.onchange('statement_id')
    def _onchange_statement_id(self):
        if self.statement_id:
            self.currency_id = self.statement_id.currency_id
            self.age_group = self.statement_id.age_group
            self.season = self.statement_id.season
            self.gst_treatment = self.statement_id.gst_treatment