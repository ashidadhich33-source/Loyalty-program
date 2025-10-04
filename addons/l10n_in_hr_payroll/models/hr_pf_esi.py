# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR PF ESI Model
==================================

HR PF ESI management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class HrPfEsi(BaseModel, KidsClothingMixin):
    """Indian HR PF ESI Model for Ocean ERP"""
    
    _name = 'hr.pf.esi'
    _description = 'HR PF ESI'
    _order = 'period desc, name'
    _rec_name = 'name'

    name = CharField(
        string='PF ESI Name',
        required=True,
        help='Name of the PF ESI record'
    )
    
    # PF ESI Information
    employee_id = Many2OneField(
        'hr.employee',
        string='Employee',
        required=True,
        help='Employee this record belongs to'
    )
    
    contract_id = Many2OneField(
        'hr.contract',
        string='Contract',
        required=True,
        help='Contract this record belongs to'
    )
    
    # PF Information
    pf_number = CharField(
        string='PF Number',
        help='Provident Fund Number'
    )
    
    pf_employee_contribution = FloatField(
        string='PF Employee Contribution',
        help='PF employee contribution amount'
    )
    
    pf_employer_contribution = FloatField(
        string='PF Employer Contribution',
        help='PF employer contribution amount'
    )
    
    pf_total_contribution = FloatField(
        string='PF Total Contribution',
        help='PF total contribution amount'
    )
    
    # ESI Information
    esi_number = CharField(
        string='ESI Number',
        help='Employee State Insurance Number'
    )
    
    esi_employee_contribution = FloatField(
        string='ESI Employee Contribution',
        help='ESI employee contribution amount'
    )
    
    esi_employer_contribution = FloatField(
        string='ESI Employer Contribution',
        help='ESI employer contribution amount'
    )
    
    esi_total_contribution = FloatField(
        string='ESI Total Contribution',
        help='ESI total contribution amount'
    )
    
    # Period Information
    period = CharField(
        string='Period',
        required=True,
        help='Period for the contribution (YYYYMM)'
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
        help='Age group for this record'
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
        help='Size for this record'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this record'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this record'
    )
    
    color = CharField(
        string='Color',
        help='Color for this record'
    )
    
    # Status
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('computed', 'Computed'),
            ('submitted', 'Submitted'),
            ('acknowledged', 'Acknowledged'),
        ],
        string='Status',
        default='draft',
        help='Status of the PF ESI record'
    )
    
    # Dates
    computation_date = DateTimeField(
        string='Computation Date',
        help='Date when contribution was computed'
    )
    
    submission_date = DateTimeField(
        string='Submission Date',
        help='Date when contribution was submitted'
    )
    
    acknowledgment_date = DateTimeField(
        string='Acknowledgment Date',
        help='Date when contribution was acknowledged'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this record belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the record'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(HrPfEsi, self).create(vals)
    
    def action_compute(self):
        """Compute PF ESI contributions"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft records can be computed.')
            
            # Compute PF ESI contributions
            contributions = self._compute_contributions(record)
            
            record.write({
                'state': 'computed',
                'pf_employee_contribution': contributions['pf_employee'],
                'pf_employer_contribution': contributions['pf_employer'],
                'pf_total_contribution': contributions['pf_total'],
                'esi_employee_contribution': contributions['esi_employee'],
                'esi_employer_contribution': contributions['esi_employer'],
                'esi_total_contribution': contributions['esi_total'],
                'computation_date': self.env.context.get('computation_date'),
            })
    
    def action_submit(self):
        """Submit PF ESI contributions"""
        for record in self:
            if record.state != 'computed':
                raise UserError('Only computed records can be submitted.')
            
            record.write({
                'state': 'submitted',
                'submission_date': self.env.context.get('submission_date'),
            })
    
    def action_acknowledge(self):
        """Acknowledge PF ESI contributions"""
        for record in self:
            if record.state != 'submitted':
                raise UserError('Only submitted records can be acknowledged.')
            
            record.write({
                'state': 'acknowledged',
                'acknowledgment_date': self.env.context.get('acknowledgment_date'),
            })
    
    def _compute_contributions(self, record):
        """Compute PF ESI contributions"""
        contract = record.contract_id
        basic_wage = contract.wage
        
        # PF contributions
        if contract.pf_applicable:
            pf_employee = min(basic_wage * 0.12, 1800)  # 12% of basic wage, max 1800
            pf_employer = min(basic_wage * 0.12, 1800)  # 12% of basic wage, max 1800
            pf_total = pf_employee + pf_employer
        else:
            pf_employee = 0
            pf_employer = 0
            pf_total = 0
        
        # ESI contributions
        if contract.esi_applicable and basic_wage <= 21000:
            esi_employee = basic_wage * 0.0075  # 0.75% of gross salary
            esi_employer = basic_wage * 0.0325  # 3.25% of gross salary
            esi_total = esi_employee + esi_employer
        else:
            esi_employee = 0
            esi_employer = 0
            esi_total = 0
        
        return {
            'pf_employee': pf_employee,
            'pf_employer': pf_employer,
            'pf_total': pf_total,
            'esi_employee': esi_employee,
            'esi_employer': esi_employer,
            'esi_total': esi_total,
        }
    
    def get_kids_clothing_pf_esi(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get PF ESI records filtered by kids clothing criteria"""
        domain = [('state', '=', 'acknowledged')]
        
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