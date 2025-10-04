# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Advanced Accounting - Financial Reports
===========================================================

Financial reports for kids clothing retail business.
"""

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class AccountFinancialReport(models.Model):
    """Financial Report"""
    
    _name = 'account.financial.report'
    _description = 'Financial Report'
    _order = 'sequence, name'
    
    # Basic Information
    name = fields.Char(
        string='Report Name',
        required=True,
        help='Report name'
    )
    
    # Report Type
    report_type = fields.Selection([
        ('balance_sheet', 'Balance Sheet'),
        ('profit_loss', 'Profit & Loss'),
        ('cash_flow', 'Cash Flow'),
        ('trial_balance', 'Trial Balance'),
        ('aged_receivable', 'Aged Receivable'),
        ('aged_payable', 'Aged Payable'),
        ('general_ledger', 'General Ledger'),
        ('custom', 'Custom Report'),
    ], string='Report Type', required=True, help='Type of financial report')
    
    # Company Information
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
        help='Company this report belongs to'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help='Report currency'
    )
    
    # Sequence
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Sequence for ordering reports'
    )
    
    # Report Lines
    line_ids = fields.One2many(
        'account.financial.report.line',
        'report_id',
        string='Report Lines',
        help='Report lines'
    )
    
    # Status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether this report is active'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this report')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this report')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this report relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this report')
    
    # Notes
    notes = fields.Text(
        string='Notes',
        help='Additional notes about this report'
    )
    
    def action_generate_report(self, date_from=None, date_to=None):
        """Generate financial report"""
        self.ensure_one()
        
        # This would generate the actual report
        # For now, returning basic info
        return {
            'type': 'ir.actions.act_window',
            'name': _('Financial Report'),
            'res_model': 'account.financial.report',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'new',
        }
    
    def get_report_data(self, date_from=None, date_to=None):
        """Get report data"""
        self.ensure_one()
        
        # This would query the actual data
        # For now, returning basic info
        return {
            'report_name': self.name,
            'report_type': self.report_type,
            'date_from': date_from,
            'date_to': date_to,
            'lines': [],
        }


class AccountFinancialReportLine(models.Model):
    """Financial Report Line"""
    
    _name = 'account.financial.report.line'
    _description = 'Financial Report Line'
    _order = 'report_id, sequence'
    
    # Basic Information
    name = fields.Char(
        string='Line Name',
        required=True,
        help='Line name'
    )
    
    # Report Information
    report_id = fields.Many2one(
        'account.financial.report',
        string='Report',
        required=True,
        ondelete='cascade',
        help='Report this line belongs to'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help='Line sequence'
    )
    
    # Account Information
    account_ids = fields.Many2many(
        'account.account',
        string='Accounts',
        help='Accounts for this line'
    )
    
    # Line Type
    line_type = fields.Selection([
        ('header', 'Header'),
        ('line', 'Line'),
        ('total', 'Total'),
        ('subtotal', 'Subtotal'),
    ], string='Line Type', required=True, default='line', help='Type of line')
    
    # Hierarchy
    parent_id = fields.Many2one(
        'account.financial.report.line',
        string='Parent Line',
        help='Parent line in the hierarchy'
    )
    
    child_ids = fields.One2many(
        'account.financial.report.line',
        'parent_id',
        string='Child Lines',
        help='Child lines'
    )
    
    # Amounts
    amount = fields.Float(
        string='Amount',
        compute='_compute_amount',
        store=True,
        help='Line amount'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='report_id.currency_id',
        help='Line currency'
    )
    
    # Company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='report_id.company_id',
        help='Company this line belongs to'
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('infant', 'Infant (0-2 years)'),
        ('toddler', 'Toddler (2-4 years)'),
        ('preschool', 'Preschool (4-6 years)'),
        ('school_age', 'School Age (6-12 years)'),
        ('teen', 'Teen (12+ years)'),
        ('all', 'All Age Groups'),
    ], string='Age Group Focus', help='Primary age group for this line')
    
    season_specialization = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('festival', 'Festival'),
        ('all_seasons', 'All Seasons'),
    ], string='Season Specialization', help='Season specialization for this line')
    
    brand_focus = fields.Char(
        string='Brand Focus',
        help='Specific brands this line relates to'
    )
    
    product_category = fields.Selection([
        ('clothing', 'Clothing'),
        ('accessories', 'Accessories'),
        ('shoes', 'Shoes'),
        ('toys', 'Toys'),
        ('books', 'Books'),
        ('general', 'General'),
    ], string='Product Category', help='Product category for this line')
    
    @api.depends('account_ids')
    def _compute_amount(self):
        """Compute line amount"""
        for line in self:
            # This would compute the actual amount from accounts
            # For now, setting to 0
            line.amount = 0.0
    
    @api.constrains('parent_id')
    def _check_parent(self):
        """Validate parent line"""
        for line in self:
            if line.parent_id:
                if line.parent_id == line:
                    raise ValidationError(_('Line cannot be its own parent.'))
                
                if line.parent_id.parent_id == line:
                    raise ValidationError(_('Line cannot be parent of its parent.'))