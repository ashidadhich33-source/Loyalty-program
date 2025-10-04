# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Salary Rule Model
=======================================

HR salary rule management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class HrSalaryRule(BaseModel, KidsClothingMixin):
    """Indian HR Salary Rule Model for Ocean ERP"""
    
    _name = 'hr.salary.rule'
    _description = 'HR Salary Rule'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Salary Rule Name',
        required=True,
        help='Name of the salary rule'
    )
    
    # Salary Rule Information
    code = CharField(
        string='Code',
        required=True,
        help='Code of the salary rule'
    )
    
    category_id = Many2OneField(
        'hr.salary.rule.category',
        string='Category',
        required=True,
        help='Category of the salary rule'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    # Rule Configuration
    amount_select = SelectionField(
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount'),
            ('code', 'Python Code'),
        ],
        string='Amount Type',
        required=True,
        help='Type of amount calculation'
    )
    
    amount_percentage = FloatField(
        string='Percentage',
        help='Percentage for calculation'
    )
    
    amount_fixed = FloatField(
        string='Fixed Amount',
        help='Fixed amount for calculation'
    )
    
    amount_python_compute = TextField(
        string='Python Code',
        help='Python code for calculation'
    )
    
    # Indian Specific Fields
    pf_applicable = BooleanField(
        string='PF Applicable',
        default=False,
        help='Whether PF is applicable for this rule'
    )
    
    esi_applicable = BooleanField(
        string='ESI Applicable',
        default=False,
        help='Whether ESI is applicable for this rule'
    )
    
    professional_tax_applicable = BooleanField(
        string='Professional Tax Applicable',
        default=False,
        help='Whether Professional Tax is applicable for this rule'
    )
    
    income_tax_applicable = BooleanField(
        string='Income Tax Applicable',
        default=False,
        help='Whether Income Tax is applicable for this rule'
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
        help='Age group for this salary rule'
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
        help='Size for this salary rule'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this salary rule'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this salary rule'
    )
    
    color = CharField(
        string='Color',
        help='Color for this salary rule'
    )
    
    # Rule Status
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the salary rule is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this salary rule belongs to'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the salary rule'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrSalaryRule, self).create(vals)
    
    def compute_amount(self, payslip, contract, basic_wage):
        """Compute amount for this salary rule"""
        if self.amount_select == 'percentage':
            return basic_wage * (self.amount_percentage / 100)
        elif self.amount_select == 'fixed':
            return self.amount_fixed
        elif self.amount_select == 'code':
            # Execute Python code for calculation
            return self._execute_python_code(payslip, contract, basic_wage)
        return 0.0
    
    def _execute_python_code(self, payslip, contract, basic_wage):
        """Execute Python code for calculation"""
        # This would execute the Python code safely
        # For now, return 0
        return 0.0
    
    def get_kids_clothing_salary_rules(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get salary rules filtered by kids clothing criteria"""
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


class HrSalaryRuleCategory(BaseModel, KidsClothingMixin):
    """Indian HR Salary Rule Category Model for Ocean ERP"""
    
    _name = 'hr.salary.rule.category'
    _description = 'HR Salary Rule Category'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Category Name',
        required=True,
        help='Name of the salary rule category'
    )
    
    code = CharField(
        string='Code',
        required=True,
        help='Code of the salary rule category'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    # Category Type
    category_type = SelectionField(
        selection=[
            ('basic', 'Basic'),
            ('allowance', 'Allowance'),
            ('deduction', 'Deduction'),
            ('benefit', 'Benefit'),
            ('other', 'Other'),
        ],
        string='Category Type',
        required=True,
        help='Type of salary rule category'
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
        help='Age group for this category'
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
        help='Size for this category'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this category'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this category'
    )
    
    color = CharField(
        string='Color',
        help='Color for this category'
    )
    
    # Category Status
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the category is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this category belongs to'
    )
    
    # Additional Information
    description = TextField(
        string='Description',
        help='Description of the category'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrSalaryRuleCategory, self).create(vals)
    
    def get_kids_clothing_categories(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get categories filtered by kids clothing criteria"""
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