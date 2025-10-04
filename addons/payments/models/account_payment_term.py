# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountPaymentTerm(models.Model):
    _name = 'account.payment.term'
    _description = 'Payment Terms'
    _order = 'name'

    # Basic Information
    name = fields.Char(
        string='Payment Terms',
        required=True
    )
    note = fields.Text(
        string='Notes',
        help='Additional notes about these payment terms'
    )
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    
    # Payment Term Lines
    line_ids = fields.One2many(
        'account.payment.term.line',
        'payment_id',
        string='Payment Term Lines',
        copy=True
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for these payment terms')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for these payment terms')
    
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
    
    @api.model
    def get_payment_term(self, age_group=None, season=None):
        """Get appropriate payment term based on criteria"""
        domain = [
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
        
        term = self.search(domain, limit=1)
        if not term:
            # Fallback to default term
            term = self.search([
                ('active', '=', True),
                ('company_id', '=', self.env.company.id)
            ], limit=1)
        
        return term


class AccountPaymentTermLine(models.Model):
    _name = 'account.payment.term.line'
    _description = 'Payment Term Line'
    _order = 'sequence, id'

    # Basic Information
    name = fields.Char(
        string='Description',
        help='Description of this payment term line'
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    
    # Payment Term Reference
    payment_id = fields.Many2one(
        'account.payment.term',
        string='Payment Terms',
        required=True,
        ondelete='cascade'
    )
    
    # Payment Details
    value = fields.Selection([
        ('balance', 'Balance'),
        ('percent', 'Percent'),
        ('fixed', 'Fixed Amount'),
    ], string='Type', required=True, default='balance')
    
    value_amount = fields.Float(
        string='Value',
        digits='Payment Terms',
        help='Value for this payment term line'
    )
    
    days = fields.Integer(
        string='Days',
        required=True,
        default=0,
        help='Number of days to add to the invoice date'
    )
    
    day_of_the_month = fields.Integer(
        string='Day of the Month',
        help='Day of the month to pay (1-31)'
    )
    
    # Additional Fields
    note = fields.Text(
        string='Notes',
        help='Additional notes about this payment term line'
    )
    
    @api.constrains('value_amount')
    def _check_value_amount(self):
        for line in self:
            if line.value in ['percent', 'fixed'] and line.value_amount <= 0:
                raise ValidationError(_('Value amount must be greater than 0 for percent and fixed amount types.'))
    
    @api.constrains('days')
    def _check_days(self):
        for line in self:
            if line.days < 0:
                raise ValidationError(_('Days cannot be negative.'))
    
    @api.constrains('day_of_the_month')
    def _check_day_of_the_month(self):
        for line in self:
            if line.day_of_the_month and (line.day_of_the_month < 1 or line.day_of_the_month > 31):
                raise ValidationError(_('Day of the month must be between 1 and 31.'))