# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Payroll Period Model
==========================================

HR payroll period management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class HrPayrollPeriod(BaseModel, KidsClothingMixin):
    """Indian HR Payroll Period Model for Ocean ERP"""
    
    _name = 'hr.payroll.period'
    _description = 'HR Payroll Period'
    _order = 'date_start desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Period Name',
        required=True,
        help='Name of the payroll period'
    )
    
    # Period Information
    date_start = DateTimeField(
        string='Start Date',
        required=True,
        help='Start date of the payroll period'
    )
    
    date_end = DateTimeField(
        string='End Date',
        required=True,
        help='End date of the payroll period'
    )
    
    # Period Configuration
    period_type = SelectionField(
        selection=[
            ('monthly', 'Monthly'),
            ('weekly', 'Weekly'),
            ('bi_weekly', 'Bi-Weekly'),
            ('quarterly', 'Quarterly'),
            ('yearly', 'Yearly'),
        ],
        string='Period Type',
        required=True,
        help='Type of payroll period'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('closed', 'Closed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the payroll period'
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
        help='Age group for this period'
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
        help='Size for this period'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this period'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this period'
    )
    
    color = CharField(
        string='Color',
        help='Color for this period'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this period belongs to'
    )
    
    # Payslips
    payslip_ids = One2ManyField(
        'hr.payslip',
        'period_id',
        string='Payslips',
        help='Payslips for this period'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the period'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrPayrollPeriod, self).create(vals)
    
    def action_open(self):
        """Open the payroll period"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft periods can be opened.')
            
            record.write({
                'state': 'open',
            })
    
    def action_close(self):
        """Close the payroll period"""
        for record in self:
            if record.state != 'open':
                raise UserError('Only open periods can be closed.')
            
            record.write({
                'state': 'closed',
            })
    
    def action_cancel(self):
        """Cancel the payroll period"""
        for record in self:
            if record.state not in ['draft', 'open']:
                raise UserError('Only draft or open periods can be cancelled.')
            
            record.write({
                'state': 'cancelled',
            })
    
    def get_kids_clothing_periods(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get periods filtered by kids clothing criteria"""
        domain = [('state', '=', 'closed')]
        
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