# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales - Sales Territory
==========================================

Standalone version of the sales territory model for kids clothing retail.
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

class SaleTerritory(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Territory for Kids Clothing Retail"""
    
    _name = 'sale.territory'
    _description = 'Sales Territory'
    _table = 'sale_territory'
    
    # Territory Information
    name = CharField(
        string='Territory Name',
        size=128,
        required=True,
        help="Name of the sales territory"
    )
    
    code = CharField(
        string='Territory Code',
        size=32,
        required=True,
        help="Code for the sales territory"
    )
    
    description = TextField(
        string='Description',
        help="Description of the sales territory"
    )
    
    # Territory Type
    territory_type = SelectionField(
        selection=[
            ('region', 'Region'),
            ('state', 'State'),
            ('city', 'City'),
            ('area', 'Area'),
            ('zone', 'Zone'),
        ],
        string='Territory Type',
        default='area',
        help="Type of sales territory"
    )
    
    # Geographic Information
    country_id = Many2OneField(
        comodel_name='res.country',
        string='Country',
        help="Country of this territory"
    )
    
    state_id = Many2OneField(
        comodel_name='res.state',
        string='State',
        help="State of this territory"
    )
    
    city = CharField(
        string='City',
        size=64,
        help="City of this territory"
    )
    
    zip_code = CharField(
        string='ZIP Code',
        size=16,
        help="ZIP code of this territory"
    )
    
    # Territory Hierarchy
    parent_id = Many2OneField(
        comodel_name='sale.territory',
        string='Parent Territory',
        help="Parent territory of this territory"
    )
    
    child_ids = One2ManyField(
        comodel_name='sale.territory',
        inverse_name='parent_id',
        string='Child Territories',
        help="Child territories of this territory"
    )
    
    # Team Assignment
    team_id = Many2OneField(
        comodel_name='sale.team',
        string='Sales Team',
        help="Sales team assigned to this territory"
    )
    
    # Territory Manager
    manager_id = Many2OneField(
        comodel_name='res.users',
        string='Territory Manager',
        help="Manager of this territory"
    )
    
    # Territory Performance
    target_amount = FloatField(
        string='Target Amount',
        help="Target amount for this territory"
    )
    
    achieved_amount = FloatField(
        string='Achieved Amount',
        help="Amount achieved in this territory"
    )
    
    target_orders = IntegerField(
        string='Target Orders',
        help="Target number of orders for this territory"
    )
    
    achieved_orders = IntegerField(
        string='Achieved Orders',
        help="Number of orders achieved in this territory"
    )
    
    # Territory Analytics
    performance_percentage = FloatField(
        string='Performance %',
        help="Performance percentage of this territory"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_sales = FloatField(
        string='Total Kids Sales',
        help="Total sales of kids items in this territory"
    )
    
    age_group_sales = TextField(
        string='Age Group Sales',
        help="Sales by age group for this territory"
    )
    
    gender_sales = TextField(
        string='Gender Sales',
        help="Sales by gender for this territory"
    )
    
    season_sales = TextField(
        string='Season Sales',
        help="Sales by season for this territory"
    )
    
    # Territory Coverage
    coverage_percentage = FloatField(
        string='Coverage %',
        help="Percentage of territory covered"
    )
    
    # Territory Status
    status = SelectionField(
        selection=[
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('suspended', 'Suspended'),
        ],
        string='Status',
        default='active',
        help="Status of this territory"
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        comodel_name='res.company',
        string='Company',
        required=True,
        help="Company this territory belongs to"
    )
    
    # Active
    active = BooleanField(
        string='Active',
        default=True,
        help="Whether this territory is active"
    )
    
    def _compute_achieved_amount(self):
        """Compute achieved amount"""
        for territory in self:
            territory.achieved_amount = sum(member.sale_amount for member in territory.team_id.member_ids)
    
    def _compute_achieved_orders(self):
        """Compute achieved orders"""
        for territory in self:
            territory.achieved_orders = sum(member.sale_orders for member in territory.team_id.member_ids)
    
    def _compute_performance_percentage(self):
        """Compute performance percentage"""
        for territory in self:
            if territory.target_amount > 0:
                territory.performance_percentage = (territory.achieved_amount / territory.target_amount) * 100
            else:
                territory.performance_percentage = 0.0
    
    def _compute_kids_sales(self):
        """Compute kids sales"""
        for territory in self:
            territory.total_kids_sales = sum(member.kids_sales for member in territory.team_id.member_ids)
    
    def _compute_age_group_sales(self):
        """Compute age group sales"""
        for territory in self:
            age_group_sales = {}
            for member in territory.team_id.member_ids:
                if member.age_group_sales:
                    try:
                        member_sales = eval(member.age_group_sales)
                        for age_group, amount in member_sales.items():
                            if age_group not in age_group_sales:
                                age_group_sales[age_group] = 0
                            age_group_sales[age_group] += amount
                    except:
                        pass
            territory.age_group_sales = str(age_group_sales)
    
    def _compute_gender_sales(self):
        """Compute gender sales"""
        for territory in self:
            gender_sales = {}
            for member in territory.team_id.member_ids:
                if member.gender_sales:
                    try:
                        member_sales = eval(member.gender_sales)
                        for gender, amount in member_sales.items():
                            if gender not in gender_sales:
                                gender_sales[gender] = 0
                            gender_sales[gender] += amount
                    except:
                        pass
            territory.gender_sales = str(gender_sales)
    
    def _compute_season_sales(self):
        """Compute season sales"""
        for territory in self:
            season_sales = {}
            for member in territory.team_id.member_ids:
                if member.season_sales:
                    try:
                        member_sales = eval(member.season_sales)
                        for season, amount in member_sales.items():
                            if season not in season_sales:
                                season_sales[season] = 0
                            season_sales[season] += amount
                    except:
                        pass
            territory.season_sales = str(season_sales)
    
    def action_view_team(self):
        """View territory team"""
        # This would return an action to view team
        return True
    
    def action_view_analytics(self):
        """View territory analytics"""
        # This would return an action to view analytics
        return True
    
    def action_view_child_territories(self):
        """View child territories"""
        # This would return an action to view child territories
        return True