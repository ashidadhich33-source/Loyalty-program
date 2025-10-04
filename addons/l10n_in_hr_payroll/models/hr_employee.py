# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Employee Model
====================================

HR employee management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class HrEmployee(BaseModel, KidsClothingMixin):
    """Indian HR Employee Model for Ocean ERP"""
    
    _name = 'hr.employee'
    _description = 'HR Employee'
    _order = 'name'
    _rec_name = 'name'

    name = CharField(
        string='Employee Name',
        required=True,
        help='Name of the employee'
    )
    
    # Employee Basic Information
    employee_id = CharField(
        string='Employee ID',
        required=True,
        help='Unique employee identifier'
    )
    
    gender = SelectionField(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        string='Gender',
        help='Gender of the employee'
    )
    
    marital_status = SelectionField(
        selection=[
            ('single', 'Single'),
            ('married', 'Married'),
            ('divorced', 'Divorced'),
            ('widowed', 'Widowed'),
        ],
        string='Marital Status',
        help='Marital status of the employee'
    )
    
    birth_date = DateTimeField(
        string='Birth Date',
        help='Date of birth of the employee'
    )
    
    # Indian Specific Fields
    pan = CharField(
        string='PAN',
        help='Permanent Account Number'
    )
    
    aadhar = CharField(
        string='Aadhar',
        help='Aadhar Number'
    )
    
    pf_number = CharField(
        string='PF Number',
        help='Provident Fund Number'
    )
    
    esi_number = CharField(
        string='ESI Number',
        help='Employee State Insurance Number'
    )
    
    uan = CharField(
        string='UAN',
        help='Universal Account Number'
    )
    
    # Address Information
    street = CharField(
        string='Street',
        help='Street address'
    )
    
    street2 = CharField(
        string='Street 2',
        help='Additional street information'
    )
    
    city = CharField(
        string='City',
        help='City name'
    )
    
    state_id = Many2OneField(
        'res.country.state',
        string='State',
        help='State/Province'
    )
    
    zip = CharField(
        string='ZIP',
        help='ZIP/Postal code'
    )
    
    country_id = Many2OneField(
        'res.country',
        string='Country',
        default=lambda self: self.env.ref('base.in'),
        help='Country'
    )
    
    # Contact Information
    phone = CharField(
        string='Phone',
        help='Phone number'
    )
    
    mobile = CharField(
        string='Mobile',
        help='Mobile number'
    )
    
    email = CharField(
        string='Email',
        help='Email address'
    )
    
    # Employment Information
    job_id = Many2OneField(
        'hr.job',
        string='Job Position',
        help='Job position of the employee'
    )
    
    department_id = Many2OneField(
        'hr.department',
        string='Department',
        help='Department of the employee'
    )
    
    manager_id = Many2OneField(
        'hr.employee',
        string='Manager',
        help='Manager of the employee'
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
        help='Age group for this employee'
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
        help='Size for this employee'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this employee'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this employee'
    )
    
    color = CharField(
        string='Color',
        help='Color for this employee'
    )
    
    # Employment Dates
    join_date = DateTimeField(
        string='Join Date',
        help='Date when employee joined'
    )
    
    resignation_date = DateTimeField(
        string='Resignation Date',
        help='Date when employee resigned'
    )
    
    # Status
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the employee is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this employee belongs to'
    )
    
    # Contracts
    contract_ids = One2ManyField(
        'hr.contract',
        'employee_id',
        string='Contracts',
        help='Employment contracts for this employee'
    )
    
    # Payslips
    payslip_ids = One2ManyField(
        'hr.payslip',
        'employee_id',
        string='Payslips',
        help='Payslips for this employee'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the employee'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('country_id'):
            vals['country_id'] = self.env.ref('base.in').id
        
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrEmployee, self).create(vals)
    
    def validate_pan(self, pan):
        """Validate PAN number format"""
        import re
        pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        return re.match(pan_pattern, pan) is not None
    
    def validate_aadhar(self, aadhar):
        """Validate Aadhar number format"""
        import re
        aadhar_pattern = r'^[0-9]{12}$'
        return re.match(aadhar_pattern, aadhar) is not None
    
    def validate_pf_number(self, pf_number):
        """Validate PF number format"""
        import re
        pf_pattern = r'^[A-Z]{2}[0-9]{7}[0-9]{3}$'
        return re.match(pf_pattern, pf_number) is not None
    
    def validate_esi_number(self, esi_number):
        """Validate ESI number format"""
        import re
        esi_pattern = r'^[0-9]{10}$'
        return re.match(esi_pattern, esi_number) is not None
    
    def validate_uan(self, uan):
        """Validate UAN format"""
        import re
        uan_pattern = r'^[0-9]{12}$'
        return re.match(uan_pattern, uan) is not None
    
    def get_kids_clothing_employees(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get employees filtered by kids clothing criteria"""
        domain = [('active', '=', True)]
        
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
    
    def get_current_contract(self):
        """Get current active contract"""
        return self.contract_ids.filtered(lambda c: c.state == 'open')
    
    def get_current_salary(self):
        """Get current salary from active contract"""
        contract = self.get_current_contract()
        if contract:
            return contract.wage
        return 0.0
    
    def calculate_age(self):
        """Calculate employee age"""
        if self.birth_date:
            from datetime import date
            today = date.today()
            birth_date = self.birth_date.date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        return 0