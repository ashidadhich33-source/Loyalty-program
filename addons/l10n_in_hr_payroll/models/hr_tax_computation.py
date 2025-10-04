# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Tax Computation Model
===========================================

HR tax computation management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class HrTaxComputation(BaseModel, KidsClothingMixin):
    """Indian HR Tax Computation Model for Ocean ERP"""
    
    _name = 'hr.tax.computation'
    _description = 'HR Tax Computation'
    _order = 'computation_date desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Computation Name',
        required=True,
        help='Name of the tax computation'
    )
    
    # Tax Computation Information
    employee_id = Many2OneField(
        'hr.employee',
        string='Employee',
        required=True,
        help='Employee this computation belongs to'
    )
    
    contract_id = Many2OneField(
        'hr.contract',
        string='Contract',
        required=True,
        help='Contract this computation belongs to'
    )
    
    # Tax Information
    tax_type = SelectionField(
        selection=[
            ('income_tax', 'Income Tax'),
            ('professional_tax', 'Professional Tax'),
            ('pf', 'Provident Fund'),
            ('esi', 'Employee State Insurance'),
            ('gratuity', 'Gratuity'),
            ('other', 'Other'),
        ],
        string='Tax Type',
        required=True,
        help='Type of tax computation'
    )
    
    computation_period = CharField(
        string='Computation Period',
        required=True,
        help='Period for the computation (YYYYMM)'
    )
    
    # Tax Calculation
    gross_salary = FloatField(
        string='Gross Salary',
        help='Gross salary for the period'
    )
    
    taxable_income = FloatField(
        string='Taxable Income',
        help='Taxable income for the period'
    )
    
    tax_amount = FloatField(
        string='Tax Amount',
        help='Tax amount for the period'
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
        help='Age group for this computation'
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
        help='Size for this computation'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this computation'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this computation'
    )
    
    color = CharField(
        string='Color',
        help='Color for this computation'
    )
    
    # Computation Status
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('computed', 'Computed'),
            ('verified', 'Verified'),
            ('filed', 'Filed'),
        ],
        string='Status',
        default='draft',
        help='Status of the tax computation'
    )
    
    # Dates
    computation_date = DateTimeField(
        string='Computation Date',
        help='Date of the computation'
    )
    
    verified_date = DateTimeField(
        string='Verified Date',
        help='Date when computation was verified'
    )
    
    filed_date = DateTimeField(
        string='Filed Date',
        help='Date when computation was filed'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this computation belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the computation'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrTaxComputation, self).create(vals)
    
    def action_compute(self):
        """Compute the tax"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft computations can be computed.')
            
            # Compute tax based on type
            tax_data = self._compute_tax(record)
            
            record.write({
                'state': 'computed',
                'gross_salary': tax_data['gross_salary'],
                'taxable_income': tax_data['taxable_income'],
                'tax_amount': tax_data['tax_amount'],
                'computation_date': self.env.context.get('computation_date'),
            })
    
    def action_verify(self):
        """Verify the tax computation"""
        for record in self:
            if record.state != 'computed':
                raise UserError('Only computed taxes can be verified.')
            
            record.write({
                'state': 'verified',
                'verified_date': self.env.context.get('verified_date'),
            })
    
    def action_file(self):
        """File the tax computation"""
        for record in self:
            if record.state != 'verified':
                raise UserError('Only verified computations can be filed.')
            
            record.write({
                'state': 'filed',
                'filed_date': self.env.context.get('filed_date'),
            })
    
    def _compute_tax(self, record):
        """Compute tax based on type"""
        contract = record.contract_id
        gross_salary = contract.wage
        
        if record.tax_type == 'income_tax':
            # Income tax computation
            annual_salary = gross_salary * 12
            if annual_salary > 250000:  # Above tax exemption limit
                taxable_income = annual_salary - 250000
                tax_amount = min(taxable_income * 0.05, 12500) / 12  # 5% tax rate
            else:
                taxable_income = 0
                tax_amount = 0
        elif record.tax_type == 'professional_tax':
            # Professional tax computation
            taxable_income = gross_salary
            tax_amount = min(200, gross_salary * 0.01)  # Max 200 or 1% of wage
        elif record.tax_type == 'pf':
            # PF computation
            taxable_income = gross_salary
            tax_amount = min(gross_salary * 0.12, 1800)  # 12% of basic wage, max 1800
        elif record.tax_type == 'esi':
            # ESI computation
            taxable_income = gross_salary
            if gross_salary <= 21000:
                tax_amount = gross_salary * 0.0075  # 0.75% of gross salary
            else:
                tax_amount = 0
        else:
            taxable_income = gross_salary
            tax_amount = 0
        
        return {
            'gross_salary': gross_salary,
            'taxable_income': taxable_income,
            'tax_amount': tax_amount,
        }
    
    def get_kids_clothing_computations(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get computations filtered by kids clothing criteria"""
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