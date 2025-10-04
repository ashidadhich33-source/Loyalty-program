# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class InvoiceWizard(models.TransientModel):
    _name = 'account.invoice.wizard'
    _description = 'Invoice Wizard'

    # Basic Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        domain=[('is_company', '=', True)]
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
    
    # Template Selection
    template_id = fields.Many2one(
        'account.invoice.template',
        string='Invoice Template',
        domain="[('template_type', '=', 'customer')]"
    )
    
    # Additional Fields
    note = fields.Text(
        string='Notes',
        help='Additional notes for the invoice'
    )
    
    @api.onchange('date_invoice')
    def _onchange_date_invoice(self):
        if self.date_invoice and not self.date_due:
            self.date_due = self.date_invoice
    
    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            # Auto-select appropriate template based on partner
            template = self.env['account.invoice.template'].get_template(
                template_type='customer',
                age_group=self.age_group,
                season=self.season
            )
            if template:
                self.template_id = template
    
    def action_create_invoice(self):
        """Create invoice from wizard"""
        if not self.partner_id:
            raise ValidationError(_('Please select a customer.'))
        
        # Create invoice
        invoice_vals = {
            'partner_id': self.partner_id.id,
            'date_invoice': self.date_invoice,
            'date_due': self.date_due,
            'age_group': self.age_group,
            'season': self.season,
            'note': self.note,
        }
        
        invoice = self.env['account.invoice'].create(invoice_vals)
        
        # Apply template if selected
        if self.template_id:
            self.template_id.apply_template(invoice)
        
        # Return action to open the created invoice
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice',
            'res_id': invoice.id,
            'view_mode': 'form',
            'target': 'current',
        }