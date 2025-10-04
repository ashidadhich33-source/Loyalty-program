# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Payslip Model
====================================

HR payslip management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class HrPayslip(BaseModel, KidsClothingMixin):
    """Indian HR Payslip Model for Ocean ERP"""
    
    _name = 'hr.payslip'
    _description = 'HR Payslip'
    _order = 'date_from desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Payslip Name',
        required=True,
        help='Name of the payslip'
    )
    
    employee_id = Many2OneField(
        'hr.employee',
        string='Employee',
        required=True,
        help='Employee this payslip belongs to'
    )
    
    contract_id = Many2OneField(
        'hr.contract',
        string='Contract',
        required=True,
        help='Contract this payslip belongs to'
    )
    
    # Payslip Information
    date_from = DateTimeField(
        string='Date From',
        required=True,
        help='Start date of the payslip period'
    )
    
    date_to = DateTimeField(
        string='Date To',
        required=True,
        help='End date of the payslip period'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('verify', 'Waiting'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the payslip'
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
        help='Age group for this payslip'
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
        help='Size for this payslip'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this payslip'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this payslip'
    )
    
    color = CharField(
        string='Color',
        help='Color for this payslip'
    )
    
    # Salary Information
    basic_wage = FloatField(
        string='Basic Wage',
        help='Basic wage for the period'
    )
    
    gross_wage = FloatField(
        string='Gross Wage',
        help='Gross wage for the period'
    )
    
    net_wage = FloatField(
        string='Net Wage',
        help='Net wage for the period'
    )
    
    # Payslip Lines
    line_ids = One2ManyField(
        'hr.payslip.line',
        'payslip_id',
        string='Payslip Lines',
        help='Payslip lines for this payslip'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this payslip belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the payslip'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrPayslip, self).create(vals)
    
    def action_compute_sheet(self):
        """Compute payslip sheet"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft payslips can be computed.')
            
            # Clear existing lines
            record.line_ids.unlink()
            
            # Compute payslip lines
            self._compute_payslip_lines(record)
            
            # Update totals
            self._update_totals(record)
    
    def action_verify_sheet(self):
        """Verify payslip sheet"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft payslips can be verified.')
            
            record.write({
                'state': 'verify',
            })
    
    def action_done(self):
        """Mark payslip as done"""
        for record in self:
            if record.state != 'verify':
                raise UserError('Only verified payslips can be marked as done.')
            
            record.write({
                'state': 'done',
            })
    
    def action_cancel(self):
        """Cancel payslip"""
        for record in self:
            if record.state not in ['draft', 'verify']:
                raise UserError('Only draft or verified payslips can be cancelled.')
            
            record.write({
                'state': 'cancel',
            })
    
    def _compute_payslip_lines(self, record):
        """Compute payslip lines based on contract and salary structure"""
        contract = record.contract_id
        
        # Basic wage line
        self.env['hr.payslip.line'].create({
            'payslip_id': record.id,
            'name': 'Basic Wage',
            'code': 'BASIC',
            'category_id': self.env.ref('hr_payroll.BASIC').id,
            'amount': contract.wage,
            'quantity': 1.0,
            'rate': contract.wage,
        })
        
        # PF Employee Contribution
        if contract.pf_applicable:
            pf_amount = min(contract.wage * 0.12, 1800)
            self.env['hr.payslip.line'].create({
                'payslip_id': record.id,
                'name': 'PF Employee Contribution',
                'code': 'PF_EMP',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'amount': -pf_amount,
                'quantity': 1.0,
                'rate': -pf_amount,
            })
        
        # ESI Employee Contribution
        if contract.esi_applicable and contract.wage <= 21000:
            esi_amount = contract.wage * 0.0075
            self.env['hr.payslip.line'].create({
                'payslip_id': record.id,
                'name': 'ESI Employee Contribution',
                'code': 'ESI_EMP',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'amount': -esi_amount,
                'quantity': 1.0,
                'rate': -esi_amount,
            })
        
        # Professional Tax
        if contract.professional_tax_applicable:
            pt_amount = min(200, contract.wage * 0.01)
            self.env['hr.payslip.line'].create({
                'payslip_id': record.id,
                'name': 'Professional Tax',
                'code': 'PT',
                'category_id': self.env.ref('hr_payroll.DED').id,
                'amount': -pt_amount,
                'quantity': 1.0,
                'rate': -pt_amount,
            })
        
        # Income Tax (TDS)
        if contract.income_tax_applicable:
            annual_salary = contract.wage * 12
            if annual_salary > 250000:
                taxable_income = annual_salary - 250000
                tax_amount = min(taxable_income * 0.05, 12500) / 12
                self.env['hr.payslip.line'].create({
                    'payslip_id': record.id,
                    'name': 'Income Tax (TDS)',
                    'code': 'TDS',
                    'category_id': self.env.ref('hr_payroll.DED').id,
                    'amount': -tax_amount,
                    'quantity': 1.0,
                    'rate': -tax_amount,
                })
    
    def _update_totals(self, record):
        """Update payslip totals"""
        contract = record.contract_id
        
        # Calculate gross wage
        gross_wage = contract.wage
        
        # Calculate net wage
        net_wage = contract.calculate_net_salary()
        
        record.write({
            'basic_wage': contract.wage,
            'gross_wage': gross_wage,
            'net_wage': net_wage,
        })
    
    def get_kids_clothing_payslips(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get payslips filtered by kids clothing criteria"""
        domain = [('state', '=', 'done')]
        
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


class HrPayslipLine(BaseModel, KidsClothingMixin):
    """Indian HR Payslip Line Model for Ocean ERP"""
    
    _name = 'hr.payslip.line'
    _description = 'HR Payslip Line'
    _order = 'sequence, id'

    payslip_id = Many2OneField(
        'hr.payslip',
        string='Payslip',
        required=True,
        help='Payslip this line belongs to'
    )
    
    # Line Information
    name = CharField(
        string='Name',
        required=True,
        help='Name of the payslip line'
    )
    
    code = CharField(
        string='Code',
        required=True,
        help='Code of the payslip line'
    )
    
    category_id = Many2OneField(
        'hr.salary.rule.category',
        string='Category',
        help='Category of the payslip line'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    # Amount Information
    amount = FloatField(
        string='Amount',
        help='Amount of the payslip line'
    )
    
    quantity = FloatField(
        string='Quantity',
        default=1.0,
        help='Quantity for calculation'
    )
    
    rate = FloatField(
        string='Rate',
        help='Rate for calculation'
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
        help='Age group for this payslip line'
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
        help='Size for this payslip line'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this payslip line'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this payslip line'
    )
    
    color = CharField(
        string='Color',
        help='Color for this payslip line'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this payslip line belongs to'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrPayslipLine, self).create(vals)
    
    def get_kids_clothing_payslip_lines(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get payslip lines filtered by kids clothing criteria"""
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