# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales - Sales Team
=====================================

Standalone version of the sales team model for kids clothing retail.
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

class SaleTeam(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Team for Kids Clothing Retail"""
    
    _name = 'sale.team'
    _description = 'Sales Team'
    _table = 'sale_team'
    
    # Team Information
    name = CharField(
        string='Team Name',
        size=128,
        required=True,
        help="Name of the sales team"
    )
    
    code = CharField(
        string='Team Code',
        size=32,
        required=True,
        help="Code for the sales team"
    )
    
    description = TextField(
        string='Description',
        help="Description of the sales team"
    )
    
    # Team Members
    member_ids = One2ManyField(
        comodel_name='sale.team.member',
        inverse_name='team_id',
        string='Team Members',
        help="Members of this sales team"
    )
    
    # Team Leader
    leader_id = Many2OneField(
        comodel_name='res.users',
        string='Team Leader',
        help="Leader of this sales team"
    )
    
    # Team Performance
    target_amount = FloatField(
        string='Target Amount',
        help="Target amount for this team"
    )
    
    achieved_amount = FloatField(
        string='Achieved Amount',
        help="Amount achieved by this team"
    )
    
    target_orders = IntegerField(
        string='Target Orders',
        help="Target number of orders for this team"
    )
    
    achieved_orders = IntegerField(
        string='Achieved Orders',
        help="Number of orders achieved by this team"
    )
    
    # Team Analytics
    performance_percentage = FloatField(
        string='Performance %',
        help="Performance percentage of this team"
    )
    
    # Territory
    territory_ids = One2ManyField(
        comodel_name='sale.territory',
        inverse_name='team_id',
        string='Territories',
        help="Territories assigned to this team"
    )
    
    # Commission
    commission_rule_ids = One2ManyField(
        comodel_name='sale.commission.rule',
        inverse_name='team_id',
        string='Commission Rules',
        help="Commission rules for this team"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_sales = FloatField(
        string='Total Kids Sales',
        help="Total sales of kids items by this team"
    )
    
    age_group_sales = TextField(
        string='Age Group Sales',
        help="Sales by age group for this team"
    )
    
    gender_sales = TextField(
        string='Gender Sales',
        help="Sales by gender for this team"
    )
    
    season_sales = TextField(
        string='Season Sales',
        help="Sales by season for this team"
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        comodel_name='res.company',
        string='Company',
        required=True,
        help="Company this team belongs to"
    )
    
    # Active
    active = BooleanField(
        string='Active',
        default=True,
        help="Whether this team is active"
    )
    
    def _compute_achieved_amount(self):
        """Compute achieved amount"""
        for team in self:
            team.achieved_amount = sum(member.sale_amount for member in team.member_ids)
    
    def _compute_achieved_orders(self):
        """Compute achieved orders"""
        for team in self:
            team.achieved_orders = sum(member.sale_orders for member in team.member_ids)
    
    def _compute_performance_percentage(self):
        """Compute performance percentage"""
        for team in self:
            if team.target_amount > 0:
                team.performance_percentage = (team.achieved_amount / team.target_amount) * 100
            else:
                team.performance_percentage = 0.0
    
    def _compute_kids_sales(self):
        """Compute kids sales"""
        for team in self:
            team.total_kids_sales = sum(member.kids_sales for member in team.member_ids)
    
    def _compute_age_group_sales(self):
        """Compute age group sales"""
        for team in self:
            age_group_sales = {}
            for member in team.member_ids:
                if member.age_group_sales:
                    try:
                        member_sales = eval(member.age_group_sales)
                        for age_group, amount in member_sales.items():
                            if age_group not in age_group_sales:
                                age_group_sales[age_group] = 0
                            age_group_sales[age_group] += amount
                    except:
                        pass
            team.age_group_sales = str(age_group_sales)
    
    def _compute_gender_sales(self):
        """Compute gender sales"""
        for team in self:
            gender_sales = {}
            for member in team.member_ids:
                if member.gender_sales:
                    try:
                        member_sales = eval(member.gender_sales)
                        for gender, amount in member_sales.items():
                            if gender not in gender_sales:
                                gender_sales[gender] = 0
                            gender_sales[gender] += amount
                    except:
                        pass
            team.gender_sales = str(gender_sales)
    
    def _compute_season_sales(self):
        """Compute season sales"""
        for team in self:
            season_sales = {}
            for member in team.member_ids:
                if member.season_sales:
                    try:
                        member_sales = eval(member.season_sales)
                        for season, amount in member_sales.items():
                            if season not in season_sales:
                                season_sales[season] = 0
                            season_sales[season] += amount
                    except:
                        pass
            team.season_sales = str(season_sales)
    
    def action_view_members(self):
        """View team members"""
        # This would return an action to view members
        return True
    
    def action_view_territories(self):
        """View team territories"""
        # This would return an action to view territories
        return True
    
    def action_view_commission_rules(self):
        """View team commission rules"""
        # This would return an action to view commission rules
        return True
    
    def action_view_analytics(self):
        """View team analytics"""
        # This would return an action to view analytics
        return True


class SaleTeamMember(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Team Member for Kids Clothing Retail"""
    
    _name = 'sale.team.member'
    _description = 'Sales Team Member'
    _table = 'sale_team_member'
    
    # Team Reference
    team_id = Many2OneField(
        comodel_name='sale.team',
        string='Sales Team',
        required=True,
        help="Sales team this member belongs to"
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help="Order of members in the team"
    )
    
    # Member Information
    user_id = Many2OneField(
        comodel_name='res.users',
        string='User',
        required=True,
        help="User for this team member"
    )
    
    role = SelectionField(
        selection=[
            ('leader', 'Team Leader'),
            ('member', 'Team Member'),
            ('assistant', 'Assistant'),
        ],
        string='Role',
        default='member',
        help="Role of this team member"
    )
    
    # Performance
    sale_amount = FloatField(
        string='Sale Amount',
        help="Total sale amount by this member"
    )
    
    sale_orders = IntegerField(
        string='Sale Orders',
        help="Total number of sale orders by this member"
    )
    
    # Kids Clothing Specific Analytics
    kids_sales = FloatField(
        string='Kids Sales',
        help="Total sales of kids items by this member"
    )
    
    age_group_sales = TextField(
        string='Age Group Sales',
        help="Sales by age group for this member"
    )
    
    gender_sales = TextField(
        string='Gender Sales',
        help="Sales by gender for this member"
    )
    
    season_sales = TextField(
        string='Season Sales',
        help="Sales by season for this member"
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        comodel_name='res.company',
        string='Company',
        required=True,
        help="Company this member belongs to"
    )
    
    # Active
    active = BooleanField(
        string='Active',
        default=True,
        help="Whether this member is active"
    )
    
    def _compute_sale_amount(self):
        """Compute sale amount"""
        for member in self:
            if member.user_id:
                # This would calculate actual sales in a real implementation
                member.sale_amount = 0.0
            else:
                member.sale_amount = 0.0
    
    def _compute_sale_orders(self):
        """Compute sale orders"""
        for member in self:
            if member.user_id:
                # This would calculate actual orders in a real implementation
                member.sale_orders = 0
            else:
                member.sale_orders = 0
    
    def _compute_kids_sales(self):
        """Compute kids sales"""
        for member in self:
            if member.user_id:
                # This would calculate actual kids sales in a real implementation
                member.kids_sales = 0.0
            else:
                member.kids_sales = 0.0
    
    def _compute_age_group_sales(self):
        """Compute age group sales"""
        for member in self:
            if member.user_id:
                # This would calculate actual age group sales in a real implementation
                member.age_group_sales = str({})
            else:
                member.age_group_sales = str({})
    
    def _compute_gender_sales(self):
        """Compute gender sales"""
        for member in self:
            if member.user_id:
                # This would calculate actual gender sales in a real implementation
                member.gender_sales = str({})
            else:
                member.gender_sales = str({})
    
    def _compute_season_sales(self):
        """Compute season sales"""
        for member in self:
            if member.user_id:
                # This would calculate actual season sales in a real implementation
                member.season_sales = str({})
            else:
                member.season_sales = str({})