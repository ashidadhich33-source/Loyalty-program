# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Contract Model
====================================

HR contract management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class HrContract(BaseModel, KidsClothingMixin):
    """Indian HR Contract Model for Ocean ERP"""
    
    _name = 'hr.contract'
    _description = 'HR Contract'
    _order = 'date_start desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Contract Reference',
        required=True,
        help='Reference of the contract'
    )
    
    employee_id = Many2OneField(
        'hr.employee',
        string='Employee',
        required=True,
        help='Employee this contract belongs to'
    )
    
    # Contract Information
    contract_type = SelectionField(
        selection=[
            ('permanent', 'Permanent'),
            ('temporary', 'Temporary'),
            ('contract', 'Contract'),
            ('intern', 'Intern'),
            ('consultant', 'Consultant'),
        ],
        string='Contract Type',
        required=True,
        help='Type of contract'
    )
    
    job_id = Many2OneField(
        'hr.job',
        string='Job Position',
        help='Job position for this contract'
    )
    
    department_id = Many2OneField(
        'hr.department',
        string='Department',
        help='Department for this contract'
    )
    
    # Salary Information
    wage = FloatField(
        string='Wage',
        required=True,
        help='Basic wage/salary'
    )
    
    wage_type = SelectionField(
        selection=[
            ('monthly', 'Monthly'),
            ('weekly', 'Weekly'),
            ('daily', 'Daily'),
            ('hourly', 'Hourly'),
        ],
        string='Wage Type',
        required=True,
        help='Type of wage calculation'
    )
    
    # Indian Specific Fields
    pf_applicable = BooleanField(
        string='PF Applicable',
        default=True,
        help='Whether PF is applicable'
    )
    
    esi_applicable = BooleanField(
        string='ESI Applicable',
        default=True,
        help='Whether ESI is applicable'
    )
    
    professional_tax_applicable = BooleanField(
        string='Professional Tax Applicable',
        default=True,
        help='Whether Professional Tax is applicable'
    )
    
    income_tax_applicable = BooleanField(
        string='Income Tax Applicable',
        default=True,
        help='Whether Income Tax is applicable'
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
        help='Age group for this contract'
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
        help='Size for this contract'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this contract'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this contract'
    )
    
    color = CharField(
        string='Color',
        help='Color for this contract'
    )
    
    # Contract Dates
    date_start = DateTimeField(
        string='Start Date',
        required=True,
        help='Start date of the contract'
    )
    
    date_end = DateTimeField(
        string='End Date',
        help='End date of the contract'
    )
    
    # Contract Status
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('open', 'Running'),
            ('close', 'Expired'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the contract'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this contract belongs to'
    )
    
    # Salary Structure
    struct_id = Many2OneField(
        'hr.payroll.structure',
        string='Salary Structure',
        help='Salary structure for this contract'
    )
    
    # Payslips
    payslip_ids = One2ManyField(
        'hr.payslip',
        'contract_id',
        string='Payslips',
        help='Payslips for this contract'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the contract'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrContract, self).create(vals)
    
    def action_confirm(self):
        """Confirm the contract"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft contracts can be confirmed.')
            
            record.write({
                'state': 'open',
            })
    
    def action_close(self):
        """Close the contract"""
        for record in self:
            if record.state != 'open':
                raise UserError('Only running contracts can be closed.')
            
            record.write({
                'state': 'close',
            })
    
    def action_cancel(self):
        """Cancel the contract"""
        for record in self:
            if record.state not in ['draft', 'open']:
                raise UserError('Only draft or running contracts can be cancelled.')
            
            record.write({
                'state': 'cancel',
            })
    
    def get_kids_clothing_contracts(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get contracts filtered by kids clothing criteria"""
        domain = [('state', '=', 'open')]
        
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
    
    def calculate_gross_salary(self):
        """Calculate gross salary including all allowances"""
        gross = self.wage
        
        # Add allowances from salary structure
        if self.struct_id:
            for rule in self.struct_id.rule_ids:
                if rule.category_id.code == 'ALW':
                    gross += rule.amount
        
        return gross
    
    def calculate_deductions(self):
        """Calculate total deductions"""
        deductions = 0
        
        # PF deduction
        if self.pf_applicable:
            pf_amount = min(self.wage * 0.12, 1800)  # 12% of basic wage, max 1800
            deductions += pf_amount
        
        # ESI deduction
        if self.esi_applicable and self.wage <= 21000:
            esi_amount = self.wage * 0.0075  # 0.75% of gross salary
            deductions += esi_amount
        
        # Professional Tax
        if self.professional_tax_applicable:
            # Professional tax varies by state, using average
            pt_amount = min(200, self.wage * 0.01)  # Max 200 or 1% of wage
            deductions += pt_amount
        
        # Income Tax (TDS)
        if self.income_tax_applicable:
            # Simplified tax calculation
            annual_salary = self.wage * 12
            if annual_salary > 250000:  # Above tax exemption limit
                taxable_income = annual_salary - 250000
                tax_amount = min(taxable_income * 0.05, 12500) / 12  # 5% tax rate
                deductions += tax_amount
        
        return deductions
    
    def calculate_net_salary(self):
        """Calculate net salary after deductions"""
        gross = self.calculate_gross_salary()
        deductions = self.calculate_deductions()
        return gross - deductions