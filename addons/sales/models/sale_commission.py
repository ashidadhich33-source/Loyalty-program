# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales - Sales Commission
============================================

Standalone version of the sales commission model for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField
from core_framework.orm import DateField, DateTimeField, Many2OneField, One2ManyField, SelectionField
from addons.core_base.models.base_mixins import KidsClothingMixin, PriceMixin
from addons.company.models.res_company import ResCompany
from addons.users.models.res_users import ResUsers
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

class SaleCommission(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Commission for Kids Clothing Retail"""
    
    _name = 'sale.commission'
    _description = 'Sales Commission'
    _table = 'sale_commission'
    
    # Commission Information
    name = CharField(
        string='Commission Reference',
        size=128,
        required=True,
        help="Reference for this commission"
    )
    
    # Commission Type
    commission_type = SelectionField(
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount'),
            ('tiered', 'Tiered'),
        ],
        string='Commission Type',
        default='percentage',
        help="Type of commission calculation"
    )
    
    # Commission Rate
    commission_rate = FloatField(
        string='Commission Rate (%)',
        help="Commission rate percentage"
    )
    
    commission_amount = FloatField(
        string='Commission Amount',
        help="Fixed commission amount"
    )
    
    # Commission Calculation
    base_amount = FloatField(
        string='Base Amount',
        help="Base amount for commission calculation"
    )
    
    calculated_amount = FloatField(
        string='Calculated Amount',
        help="Calculated commission amount"
    )
    
    # Commission Status
    status = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('calculated', 'Calculated'),
            ('approved', 'Approved'),
            ('paid', 'Paid'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help="Status of this commission"
    )
    
    # Commission Period
    period_start = DateField(
        string='Period Start',
        help="Start date of commission period"
    )
    
    period_end = DateField(
        string='Period End',
        help="End date of commission period"
    )
    
    # Commission Date
    commission_date = DateField(
        string='Commission Date',
        help="Date when commission was calculated"
    )
    
    # Salesperson
    salesperson_id = Many2OneField(
        comodel_name='res.users',
        string='Salesperson',
        required=True,
        help="Salesperson earning this commission"
    )
    
    # Sales Team
    team_id = Many2OneField(
        comodel_name='sale.team',
        string='Sales Team',
        help="Sales team of the salesperson"
    )
    
    # Territory
    territory_id = Many2OneField(
        comodel_name='sale.territory',
        string='Territory',
        help="Territory of the salesperson"
    )
    
    # Related Sales
    sale_order_id = Many2OneField(
        comodel_name='sale.order',
        string='Sales Order',
        help="Related sales order"
    )
    
    # Commission Rules
    rule_id = Many2OneField(
        comodel_name='sale.commission.rule',
        string='Commission Rule',
        help="Commission rule applied"
    )
    
    # Kids Clothing Specific Fields
    kids_commission_rate = FloatField(
        string='Kids Commission Rate (%)',
        help="Special commission rate for kids items"
    )
    
    age_group_commission = TextField(
        string='Age Group Commission',
        help="Commission by age group"
    )
    
    gender_commission = TextField(
        string='Gender Commission',
        help="Commission by gender"
    )
    
    season_commission = TextField(
        string='Season Commission',
        help="Commission by season"
    )
    
    # Commission Notes
    notes = TextField(
        string='Notes',
        help="Notes about this commission"
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        comodel_name='res.company',
        string='Company',
        required=True,
        help="Company this commission belongs to"
    )
    
    # Active
    active = BooleanField(
        string='Active',
        default=True,
        help="Whether this commission is active"
    )
    
    def _compute_calculated_amount(self):
        """Compute calculated commission amount"""
        for commission in self:
            if commission.commission_type == 'percentage':
                commission.calculated_amount = (commission.base_amount * commission.commission_rate) / 100
            elif commission.commission_type == 'fixed':
                commission.calculated_amount = commission.commission_amount
            else:
                commission.calculated_amount = 0.0
    
    def _compute_kids_commission(self):
        """Compute kids commission"""
        for commission in self:
            if commission.kids_commission_rate > 0:
                commission.calculated_amount += (commission.base_amount * commission.kids_commission_rate) / 100
    
    def _compute_age_group_commission(self):
        """Compute age group commission"""
        for commission in self:
            if commission.age_group_commission:
                try:
                    age_group_commission = eval(commission.age_group_commission)
                    for age_group, rate in age_group_commission.items():
                        commission.calculated_amount += (commission.base_amount * rate) / 100
                except:
                    pass
    
    def _compute_gender_commission(self):
        """Compute gender commission"""
        for commission in self:
            if commission.gender_commission:
                try:
                    gender_commission = eval(commission.gender_commission)
                    for gender, rate in gender_commission.items():
                        commission.calculated_amount += (commission.base_amount * rate) / 100
                except:
                    pass
    
    def _compute_season_commission(self):
        """Compute season commission"""
        for commission in self:
            if commission.season_commission:
                try:
                    season_commission = eval(commission.season_commission)
                    for season, rate in season_commission.items():
                        commission.calculated_amount += (commission.base_amount * rate) / 100
                except:
                    pass
    
    def action_calculate_commission(self):
        """Calculate commission"""
        for commission in self:
            commission._compute_calculated_amount()
            commission._compute_kids_commission()
            commission._compute_age_group_commission()
            commission._compute_gender_commission()
            commission._compute_season_commission()
            commission.status = 'calculated'
    
    def action_approve_commission(self):
        """Approve commission"""
        for commission in self:
            commission.status = 'approved'
    
    def action_pay_commission(self):
        """Pay commission"""
        for commission in self:
            commission.status = 'paid'
    
    def action_cancel_commission(self):
        """Cancel commission"""
        for commission in self:
            commission.status = 'cancelled'


class SaleCommissionRule(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Commission Rule for Kids Clothing Retail"""
    
    _name = 'sale.commission.rule'
    _description = 'Sales Commission Rule'
    _table = 'sale_commission_rule'
    
    # Rule Information
    name = CharField(
        string='Rule Name',
        size=128,
        required=True,
        help="Name of this commission rule"
    )
    
    code = CharField(
        string='Rule Code',
        size=32,
        required=True,
        help="Code for this commission rule"
    )
    
    description = TextField(
        string='Description',
        help="Description of this commission rule"
    )
    
    # Rule Type
    rule_type = SelectionField(
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount'),
            ('tiered', 'Tiered'),
        ],
        string='Rule Type',
        default='percentage',
        help="Type of commission rule"
    )
    
    # Commission Rate
    commission_rate = FloatField(
        string='Commission Rate (%)',
        help="Commission rate percentage"
    )
    
    commission_amount = FloatField(
        string='Commission Amount',
        help="Fixed commission amount"
    )
    
    # Rule Conditions
    min_amount = FloatField(
        string='Minimum Amount',
        help="Minimum amount for this rule to apply"
    )
    
    max_amount = FloatField(
        string='Maximum Amount',
        help="Maximum amount for this rule to apply"
    )
    
    # Rule Priority
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help="Priority of this rule"
    )
    
    # Rule Status
    active = BooleanField(
        string='Active',
        default=True,
        help="Whether this rule is active"
    )
    
    # Kids Clothing Specific Fields
    kids_commission_rate = FloatField(
        string='Kids Commission Rate (%)',
        help="Special commission rate for kids items"
    )
    
    age_group_commission = TextField(
        string='Age Group Commission',
        help="Commission by age group"
    )
    
    gender_commission = TextField(
        string='Gender Commission',
        help="Commission by gender"
    )
    
    season_commission = TextField(
        string='Season Commission',
        help="Commission by season"
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        comodel_name='res.company',
        string='Company',
        required=True,
        help="Company this rule belongs to"
    )
    
    def _compute_commission_amount(self, base_amount):
        """Compute commission amount based on rule"""
        if self.rule_type == 'percentage':
            return (base_amount * self.commission_rate) / 100
        elif self.rule_type == 'fixed':
            return self.commission_amount
        else:
            return 0.0
    
    def _compute_kids_commission(self, base_amount):
        """Compute kids commission"""
        if self.kids_commission_rate > 0:
            return (base_amount * self.kids_commission_rate) / 100
        return 0.0
    
    def _compute_age_group_commission(self, base_amount, age_group):
        """Compute age group commission"""
        if self.age_group_commission:
            try:
                age_group_commission = eval(self.age_group_commission)
                if age_group in age_group_commission:
                    return (base_amount * age_group_commission[age_group]) / 100
            except:
                pass
        return 0.0
    
    def _compute_gender_commission(self, base_amount, gender):
        """Compute gender commission"""
        if self.gender_commission:
            try:
                gender_commission = eval(self.gender_commission)
                if gender in gender_commission:
                    return (base_amount * gender_commission[gender]) / 100
            except:
                pass
        return 0.0
    
    def _compute_season_commission(self, base_amount, season):
        """Compute season commission"""
        if self.season_commission:
            try:
                season_commission = eval(self.season_commission)
                if season in season_commission:
                    return (base_amount * season_commission[season]) / 100
            except:
                pass
        return 0.0