# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Return Model
===================================

GST return management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class GstReturn(BaseModel, KidsClothingMixin):
    """Indian GST Return Model for Ocean ERP"""
    
    _name = 'gst.return'
    _description = 'GST Return'
    _order = 'return_period desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Return Name',
        required=True,
        help='Name of the GST return'
    )
    
    # GST Return Specific Fields
    return_type = SelectionField(
        selection=[
            ('gstr1', 'GSTR-1'),
            ('gstr2', 'GSTR-2'),
            ('gstr3', 'GSTR-3'),
            ('gstr4', 'GSTR-4'),
            ('gstr5', 'GSTR-5'),
            ('gstr6', 'GSTR-6'),
            ('gstr7', 'GSTR-7'),
            ('gstr8', 'GSTR-8'),
            ('gstr9', 'GSTR-9'),
            ('gstr10', 'GSTR-10'),
        ],
        string='Return Type',
        required=True,
        help='Type of GST return'
    )
    
    return_period = CharField(
        string='Return Period',
        required=True,
        help='Period for the return (YYYYMM)'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('ready', 'Ready'),
            ('filed', 'Filed'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        string='Status',
        default='draft',
        help='Status of the return'
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
        help='Age group for this return'
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
        help='Size for this return'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this return'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this return'
    )
    
    color = CharField(
        string='Color',
        help='Color for this return'
    )
    
    # Return Data
    return_data = TextField(
        string='Return Data',
        help='JSON data for the return'
    )
    
    # Filing Information
    filing_date = DateTimeField(
        string='Filing Date',
        help='Date when the return was filed'
    )
    
    ack_number = CharField(
        string='Acknowledgment Number',
        help='Acknowledgment number from GST portal'
    )
    
    ack_date = DateTimeField(
        string='Acknowledgment Date',
        help='Date of acknowledgment'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this return belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the return'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            return_type = vals.get('return_type', '')
            return_period = vals.get('return_period', '')
            vals['name'] = f"{return_type} - {return_period}"
        
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(GstReturn, self).create(vals)
    
    def action_prepare(self):
        """Prepare the GST return"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft returns can be prepared.')
            
            # Generate return data based on type
            return_data = self._generate_return_data(record)
            
            record.write({
                'state': 'ready',
                'return_data': return_data,
            })
    
    def action_file(self):
        """File the GST return"""
        for record in self:
            if record.state != 'ready':
                raise UserError('Only ready returns can be filed.')
            
            # File the return with GST portal
            ack_number = self._file_with_gst_portal(record)
            
            record.write({
                'state': 'filed',
                'filing_date': self.env.context.get('filing_date'),
                'ack_number': ack_number,
                'ack_date': self.env.context.get('ack_date'),
            })
    
    def _generate_return_data(self, record):
        """Generate return data based on type"""
        # This would generate the actual return data
        return '{}'
    
    def _file_with_gst_portal(self, record):
        """File return with GST portal"""
        # This would integrate with GST portal API
        return 'ACK123456789'
    
    def get_kids_clothing_returns(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get returns filtered by kids clothing criteria"""
        domain = [('state', '=', 'filed')]
        
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


class GstReport(BaseModel, KidsClothingMixin):
    """Indian GST Report Model for Ocean ERP"""
    
    _name = 'gst.report'
    _description = 'GST Report'
    _order = 'date_from desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Report Name',
        required=True,
        help='Name of the GST report'
    )
    
    # GST Report Specific Fields
    report_type = SelectionField(
        selection=[
            ('gst_summary', 'GST Summary'),
            ('gst_liability', 'GST Liability'),
            ('gst_input_tax', 'GST Input Tax'),
            ('gst_output_tax', 'GST Output Tax'),
            ('gst_reconciliation', 'GST Reconciliation'),
            ('gst_audit', 'GST Audit'),
            ('gst_compliance', 'GST Compliance'),
        ],
        string='Report Type',
        required=True,
        help='Type of GST report'
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
        help='Age group for this report'
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
        help='Size for this report'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this report'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this report'
    )
    
    color = CharField(
        string='Color',
        help='Color for this report'
    )
    
    # Report Data
    report_data = TextField(
        string='Report Data',
        help='Generated report data'
    )
    
    # Generated Information
    generated_date = DateTimeField(
        string='Generated Date',
        help='Date when the report was generated'
    )
    
    generated_by = Many2OneField(
        'res.users',
        string='Generated By',
        help='User who generated the report'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this report belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the report'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            report_type = vals.get('report_type', '')
            date_from = vals.get('date_from', '')
            vals['name'] = f"{report_type.replace('_', ' ').title()} - {date_from}"
        
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(GstReport, self).create(vals)
    
    def action_generate(self):
        """Generate the GST report"""
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
        # This would generate the actual report data
        return '{}'
    
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