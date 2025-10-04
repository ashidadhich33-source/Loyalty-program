# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Report Model
================================

Financial report management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class AccountReport(BaseModel, KidsClothingMixin):
    """Account Report Model for Ocean ERP"""
    
    _name = 'account.report'
    _description = 'Account Report'
    _order = 'date_from desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Report Name',
        required=True,
        help='Name of the report'
    )
    
    report_type = SelectionField(
        selection=[
            ('profit_loss', 'Profit & Loss'),
            ('balance_sheet', 'Balance Sheet'),
            ('cash_flow', 'Cash Flow'),
            ('trial_balance', 'Trial Balance'),
            ('aged_receivables', 'Aged Receivables'),
            ('aged_payables', 'Aged Payables'),
            ('inventory_valuation', 'Inventory Valuation'),
            ('sales_by_age', 'Sales by Age Group'),
            ('sales_by_size', 'Sales by Size'),
            ('sales_by_brand', 'Sales by Brand'),
            ('sales_by_color', 'Sales by Color'),
            ('sales_by_season', 'Sales by Season'),
            ('cost_analysis', 'Cost Analysis'),
            ('profitability_analysis', 'Profitability Analysis'),
            ('seasonal_analysis', 'Seasonal Analysis'),
        ],
        string='Report Type',
        required=True,
        help='Type of report'
    )
    
    date_from = DateTimeField(
        string='From Date',
        required=True,
        help='Start date for the report'
    )
    
    date_to = DateTimeField(
        string='To Date',
        required=True,
        help='End date for the report'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('generated', 'Generated'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the report'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        selection=[
            ('0-2', 'Baby (0-2 years)'),
            ('2-4', 'Toddler (2-4 years)'),
            ('4-6', 'Pre-school (4-6 years)'),
            ('6-8', 'Early School (6-8 years)'),
            ('8-10', 'Middle School (8-10 years)'),
            ('10-12', 'Late School (10-12 years)'),
            ('12-14', 'Teen (12-14 years)'),
            ('14-16', 'Young Adult (14-16 years)'),
            ('all', 'All Age Groups'),
        ],
        string='Age Group',
        help='Age group for the report'
    )
    
    size = SelectionField(
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('xxxl', 'XXXL'),
            ('all', 'All Sizes'),
        ],
        string='Size',
        help='Size for the report'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for the report'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for the report'
    )
    
    color = CharField(
        string='Color',
        help='Color for the report'
    )
    
    # Report Lines
    line_ids = One2ManyField(
        'account.report.line',
        'report_id',
        string='Report Lines',
        help='Lines for this report'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this report belongs to'
    )
    
    # Currency
    currency_id = Many2OneField(
        'res.currency',
        string='Currency',
        help='Currency for this report'
    )
    
    # Report Configuration
    target_move = SelectionField(
        selection=[
            ('posted', 'All Posted Entries'),
            ('all', 'All Entries'),
        ],
        string='Target Moves',
        default='posted',
        help='Target moves for the report'
    )
    
    display_detail = SelectionField(
        selection=[
            ('no_detail', 'No Detail'),
            ('detail_flat', 'Detail (Flat)'),
            ('detail_with_hierarchy', 'Detail with Hierarchy'),
        ],
        string='Display Detail',
        default='no_detail',
        help='Display detail for the report'
    )
    
    # Report Data
    report_data = TextField(
        string='Report Data',
        help='Generated report data'
    )
    
    # Generated Date
    generated_date = DateTimeField(
        string='Generated Date',
        help='Date when the report was generated'
    )
    
    # Generated By
    generated_by = Many2OneField(
        'res.users',
        string='Generated By',
        help='User who generated the report'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            # Generate name from report type and date
            report_type = vals.get('report_type', '')
            date_from = vals.get('date_from', '')
            vals['name'] = f"{report_type.replace('_', ' ').title()} - {date_from}"
        
        return super(AccountReport, self).create(vals)
    
    def action_generate(self):
        """Generate the report"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft reports can be generated.')
            
            # Generate report data based on type
            report_data = self._generate_report_data(record)
            
            record.write({
                'state': 'generated',
                'report_data': report_data,
                'generated_date': self.env.context.get('generated_date'),
                'generated_by': self.env.context.get('generated_by'),
            })
    
    def _generate_report_data(self, record):
        """Generate report data based on type"""
        if record.report_type == 'profit_loss':
            return self._generate_profit_loss_data(record)
        elif record.report_type == 'balance_sheet':
            return self._generate_balance_sheet_data(record)
        elif record.report_type == 'cash_flow':
            return self._generate_cash_flow_data(record)
        elif record.report_type == 'trial_balance':
            return self._generate_trial_balance_data(record)
        elif record.report_type == 'aged_receivables':
            return self._generate_aged_receivables_data(record)
        elif record.report_type == 'aged_payables':
            return self._generate_aged_payables_data(record)
        elif record.report_type == 'inventory_valuation':
            return self._generate_inventory_valuation_data(record)
        elif record.report_type == 'sales_by_age':
            return self._generate_sales_by_age_data(record)
        elif record.report_type == 'sales_by_size':
            return self._generate_sales_by_size_data(record)
        elif record.report_type == 'sales_by_brand':
            return self._generate_sales_by_brand_data(record)
        elif record.report_type == 'sales_by_color':
            return self._generate_sales_by_color_data(record)
        elif record.report_type == 'sales_by_season':
            return self._generate_sales_by_season_data(record)
        elif record.report_type == 'cost_analysis':
            return self._generate_cost_analysis_data(record)
        elif record.report_type == 'profitability_analysis':
            return self._generate_profitability_analysis_data(record)
        elif record.report_type == 'seasonal_analysis':
            return self._generate_seasonal_analysis_data(record)
        else:
            return {}
    
    def _generate_profit_loss_data(self, record):
        """Generate profit and loss data"""
        # This would generate P&L data based on the date range and kids clothing criteria
        return {
            'revenue': 0.0,
            'cost_of_goods_sold': 0.0,
            'gross_profit': 0.0,
            'operating_expenses': 0.0,
            'net_profit': 0.0,
        }
    
    def _generate_balance_sheet_data(self, record):
        """Generate balance sheet data"""
        # This would generate balance sheet data based on the date range and kids clothing criteria
        return {
            'total_assets': 0.0,
            'total_liabilities': 0.0,
            'total_equity': 0.0,
        }
    
    def _generate_cash_flow_data(self, record):
        """Generate cash flow data"""
        # This would generate cash flow data based on the date range and kids clothing criteria
        return {
            'operating_cash_flow': 0.0,
            'investing_cash_flow': 0.0,
            'financing_cash_flow': 0.0,
            'net_cash_flow': 0.0,
        }
    
    def _generate_trial_balance_data(self, record):
        """Generate trial balance data"""
        # This would generate trial balance data based on the date range and kids clothing criteria
        return {}
    
    def _generate_aged_receivables_data(self, record):
        """Generate aged receivables data"""
        # This would generate aged receivables data based on the date range and kids clothing criteria
        return {}
    
    def _generate_aged_payables_data(self, record):
        """Generate aged payables data"""
        # This would generate aged payables data based on the date range and kids clothing criteria
        return {}
    
    def _generate_inventory_valuation_data(self, record):
        """Generate inventory valuation data"""
        # This would generate inventory valuation data based on the date range and kids clothing criteria
        return {}
    
    def _generate_sales_by_age_data(self, record):
        """Generate sales by age group data"""
        # This would generate sales by age group data based on the date range and kids clothing criteria
        return {}
    
    def _generate_sales_by_size_data(self, record):
        """Generate sales by size data"""
        # This would generate sales by size data based on the date range and kids clothing criteria
        return {}
    
    def _generate_sales_by_brand_data(self, record):
        """Generate sales by brand data"""
        # This would generate sales by brand data based on the date range and kids clothing criteria
        return {}
    
    def _generate_sales_by_color_data(self, record):
        """Generate sales by color data"""
        # This would generate sales by color data based on the date range and kids clothing criteria
        return {}
    
    def _generate_sales_by_season_data(self, record):
        """Generate sales by season data"""
        # This would generate sales by season data based on the date range and kids clothing criteria
        return {}
    
    def _generate_cost_analysis_data(self, record):
        """Generate cost analysis data"""
        # This would generate cost analysis data based on the date range and kids clothing criteria
        return {}
    
    def _generate_profitability_analysis_data(self, record):
        """Generate profitability analysis data"""
        # This would generate profitability analysis data based on the date range and kids clothing criteria
        return {}
    
    def _generate_seasonal_analysis_data(self, record):
        """Generate seasonal analysis data"""
        # This would generate seasonal analysis data based on the date range and kids clothing criteria
        return {}
    
    def action_cancel(self):
        """Cancel the report"""
        for record in self:
            if record.state == 'generated':
                raise UserError('Generated reports cannot be cancelled.')
            
            record.write({'state': 'cancelled'})
    
    def action_view_lines(self):
        """View report lines"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Report Lines',
            'res_model': 'account.report.line',
            'view_mode': 'tree,form',
            'domain': [('report_id', '=', self.id)],
            'context': {'default_report_id': self.id},
        }
    
    def get_kids_clothing_reports(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get reports filtered by kids clothing criteria"""
        domain = [('state', '=', 'generated')]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if size:
            domain.append(('size', 'in', [size, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)


class AccountReportLine(BaseModel, KidsClothingMixin):
    """Account Report Line Model for Ocean ERP"""
    
    _name = 'account.report.line'
    _description = 'Account Report Line'
    _order = 'report_id, sequence, id'

    report_id = Many2OneField(
        'account.report',
        string='Report',
        required=True,
        help='Report this line belongs to'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    name = CharField(
        string='Line Name',
        required=True,
        help='Name of this line'
    )
    
    code = CharField(
        string='Code',
        help='Code for this line'
    )
    
    level = IntegerField(
        string='Level',
        default=0,
        help='Level in hierarchy'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        selection=[
            ('0-2', 'Baby (0-2 years)'),
            ('2-4', 'Toddler (2-4 years)'),
            ('4-6', 'Pre-school (4-6 years)'),
            ('6-8', 'Early School (6-8 years)'),
            ('8-10', 'Middle School (8-10 years)'),
            ('10-12', 'Late School (10-12 years)'),
            ('12-14', 'Teen (12-14 years)'),
            ('14-16', 'Young Adult (14-16 years)'),
            ('all', 'All Age Groups'),
        ],
        string='Age Group',
        help='Age group for this line'
    )
    
    size = SelectionField(
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('xxxl', 'XXXL'),
            ('all', 'All Sizes'),
        ],
        string='Size',
        help='Size for this line'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this line'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this line'
    )
    
    color = CharField(
        string='Color',
        help='Color for this line'
    )
    
    # Amounts
    amount = FloatField(
        string='Amount',
        help='Amount for this line'
    )
    
    currency_id = Many2OneField(
        'res.currency',
        string='Currency',
        help='Currency for this line'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this line belongs to'
    )
    
    def get_kids_clothing_lines(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get lines filtered by kids clothing criteria"""
        domain = []
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if size:
            domain.append(('size', 'in', [size, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)