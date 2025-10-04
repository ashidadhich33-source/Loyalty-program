# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentMethod(models.Model):
    _name = 'account.payment.method'
    _description = 'Payment Method'
    _order = 'sequence, name'

    # Basic Information
    name = fields.Char(
        string='Payment Method',
        required=True
    )
    code = fields.Char(
        string='Code',
        required=True,
        help='Unique code for this payment method'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    
    # Payment Type
    payment_type = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ('both', 'Both'),
    ], string='Payment Type', required=True, default='both')
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this payment method')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this payment method')
    
    # Payment Processing
    requires_reference = fields.Boolean(
        string='Requires Reference',
        help='Whether this payment method requires a reference number'
    )
    requires_approval = fields.Boolean(
        string='Requires Approval',
        help='Whether this payment method requires approval'
    )
    auto_reconcile = fields.Boolean(
        string='Auto Reconcile',
        help='Whether payments using this method should be auto-reconciled'
    )
    
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
    
    # Status
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    # Additional Fields
    description = fields.Text(
        string='Description',
        help='Description of this payment method'
    )
    
    @api.constrains('code')
    def _check_code(self):
        for method in self:
            if self.search([('code', '=', method.code), ('id', '!=', method.id)]):
                raise ValidationError(_('Payment method code must be unique.'))
    
    @api.model
    def get_payment_method(self, payment_type='inbound', age_group=None, season=None):
        """Get appropriate payment method based on criteria"""
        domain = [
            ('payment_type', 'in', [payment_type, 'both']),
            ('active', '=', True),
            ('company_id', '=', self.env.company.id)
        ]
        
        if age_group:
            domain.append('|')
            domain.append(('age_group', '=', age_group))
            domain.append(('age_group', '=', 'all'))
        
        if season:
            domain.append('|')
            domain.append(('season', '=', season))
            domain.append(('season', '=', 'all_season'))
        
        method = self.search(domain, limit=1)
        if not method:
            # Fallback to default method
            method = self.search([
                ('payment_type', 'in', [payment_type, 'both']),
                ('active', '=', True),
                ('company_id', '=', self.env.company.id)
            ], limit=1)
        
        return method