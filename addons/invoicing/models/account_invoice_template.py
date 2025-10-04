# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class AccountInvoiceTemplate(models.Model):
    _name = 'account.invoice.template'
    _description = 'Invoice Template'
    _order = 'name'

    # Basic Information
    name = fields.Char(
        string='Template Name',
        required=True
    )
    description = fields.Text(
        string='Description',
        help='Description of this invoice template'
    )
    
    # Template Type
    template_type = fields.Selection([
        ('customer', 'Customer Invoice'),
        ('supplier', 'Supplier Invoice'),
        ('credit_note', 'Credit Note'),
        ('debit_note', 'Debit Note'),
    ], string='Template Type', required=True, default='customer')
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company
    )
    
    # Template Content
    header_html = fields.Html(
        string='Header HTML',
        help='HTML content for invoice header'
    )
    footer_html = fields.Html(
        string='Footer HTML',
        help='HTML content for invoice footer'
    )
    
    # Default Values
    default_payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Default Payment Terms'
    )
    default_fiscal_position_id = fields.Many2one(
        'account.fiscal.position',
        string='Default Fiscal Position'
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group', help='Age group for this template')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this template')
    
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
    note = fields.Text(
        string='Notes',
        help='Additional notes about this template'
    )
    
    @api.model
    def get_template(self, template_type='customer', age_group=None, season=None):
        """Get appropriate template based on criteria"""
        domain = [
            ('template_type', '=', template_type),
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
        
        template = self.search(domain, limit=1)
        if not template:
            # Fallback to default template
            template = self.search([
                ('template_type', '=', template_type),
                ('active', '=', True),
                ('company_id', '=', self.env.company.id)
            ], limit=1)
        
        return template
    
    def apply_template(self, invoice):
        """Apply template to invoice"""
        if self.default_payment_term_id:
            invoice.payment_term_id = self.default_payment_term_id
        if self.default_fiscal_position_id:
            invoice.fiscal_position_id = self.default_fiscal_position_id
        
        return True