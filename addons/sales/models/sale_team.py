# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleTeam(models.Model):
    _name = 'sale.team'
    _description = 'Sales Team'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(
        string='Team Name',
        required=True,
        help="Name of the sales team"
    )
    
    code = fields.Char(
        string='Team Code',
        required=True,
        help="Code for the sales team"
    )
    
    # Team Information
    description = fields.Text(
        string='Description',
        help="Description of the sales team"
    )
    
    # Team Members
    member_ids = fields.One2many(
        'sale.team.member',
        'team_id',
        string='Team Members',
        help="Members of this sales team"
    )
    
    # Team Leader
    leader_id = fields.Many2one(
        'res.users',
        string='Team Leader',
        help="Leader of this sales team"
    )
    
    # Kids Clothing Specific Fields
    age_group_focus = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (Middle School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group Focus', default='all',
       help="Primary age group focus for this team")
    
    gender_focus = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender Focus', default='all',
       help="Primary gender focus for this team")
    
    season_focus = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Seasons'),
    ], string='Season Focus', default='all_season',
       help="Primary season focus for this team")
    
    # Team Performance
    target_amount = fields.Monetary(
        string='Target Amount',
        help="Target amount for this team"
    )
    
    achieved_amount = fields.Monetary(
        string='Achieved Amount',
        compute='_compute_achieved_amount',
        help="Amount achieved by this team"
    )
    
    target_orders = fields.Integer(
        string='Target Orders',
        help="Target number of orders for this team"
    )
    
    achieved_orders = fields.Integer(
        string='Achieved Orders',
        compute='_compute_achieved_orders',
        help="Number of orders achieved by this team"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help="Currency for this team"
    )
    
    # Team Analytics
    performance_percentage = fields.Float(
        string='Performance %',
        compute='_compute_performance_percentage',
        help="Performance percentage of this team"
    )
    
    # Territory
    territory_ids = fields.One2many(
        'sale.territory',
        'team_id',
        string='Territories',
        help="Territories assigned to this team"
    )
    
    # Commission
    commission_rule_ids = fields.One2many(
        'sale.commission.rule',
        'team_id',
        string='Commission Rules',
        help="Commission rules for this team"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_sales = fields.Monetary(
        string='Total Kids Sales',
        compute='_compute_kids_sales',
        help="Total sales of kids items by this team"
    )
    
    age_group_sales = fields.Text(
        string='Age Group Sales',
        compute='_compute_age_group_sales',
        help="Sales by age group for this team"
    )
    
    gender_sales = fields.Text(
        string='Gender Sales',
        compute='_compute_gender_sales',
        help="Sales by gender for this team"
    )
    
    season_sales = fields.Text(
        string='Season Sales',
        compute='_compute_season_sales',
        help="Sales by season for this team"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help="Company this team belongs to"
    )
    
    # Active
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this team is active"
    )
    
    @api.depends('member_ids', 'member_ids.sale_amount')
    def _compute_achieved_amount(self):
        for team in self:
            team.achieved_amount = sum(member.sale_amount for member in team.member_ids)
    
    @api.depends('member_ids', 'member_ids.sale_orders')
    def _compute_achieved_orders(self):
        for team in self:
            team.achieved_orders = sum(member.sale_orders for member in team.member_ids)
    
    @api.depends('achieved_amount', 'target_amount')
    def _compute_performance_percentage(self):
        for team in self:
            if team.target_amount > 0:
                team.performance_percentage = (team.achieved_amount / team.target_amount) * 100
            else:
                team.performance_percentage = 0.0
    
    @api.depends('member_ids', 'member_ids.kids_sales')
    def _compute_kids_sales(self):
        for team in self:
            team.total_kids_sales = sum(member.kids_sales for member in team.member_ids)
    
    @api.depends('member_ids', 'member_ids.age_group_sales')
    def _compute_age_group_sales(self):
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
    
    @api.depends('member_ids', 'member_ids.gender_sales')
    def _compute_gender_sales(self):
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
    
    @api.depends('member_ids', 'member_ids.season_sales')
    def _compute_season_sales(self):
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
        action = self.env.ref('sales.action_sale_team_member').read()[0]
        action['domain'] = [('team_id', '=', self.id)]
        return action
    
    def action_view_territories(self):
        """View team territories"""
        action = self.env.ref('sales.action_sale_territory').read()[0]
        action['domain'] = [('team_id', '=', self.id)]
        return action
    
    def action_view_commission_rules(self):
        """View team commission rules"""
        action = self.env.ref('sales.action_sale_commission_rule').read()[0]
        action['domain'] = [('team_id', '=', self.id)]
        return action
    
    def action_view_analytics(self):
        """View team analytics"""
        action = self.env.ref('sales.action_sale_analytics').read()[0]
        action['domain'] = [('team_id', '=', self.id)]
        return action


class SaleTeamMember(models.Model):
    _name = 'sale.team.member'
    _description = 'Sales Team Member'
    _order = 'team_id, sequence, id'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this team member"
    )
    
    # Team Reference
    team_id = fields.Many2one(
        'sale.team',
        string='Sales Team',
        required=True,
        ondelete='cascade',
        help="Sales team this member belongs to"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of members in the team"
    )
    
    # Member Information
    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        help="User for this team member"
    )
    
    role = fields.Selection([
        ('leader', 'Team Leader'),
        ('member', 'Team Member'),
        ('assistant', 'Assistant'),
    ], string='Role', default='member',
       help="Role of this team member"
    )
    
    # Kids Clothing Specific Fields
    age_group_expertise = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (Middle School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group Expertise', default='all',
       help="Age group expertise of this member")
    
    gender_expertise = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender Expertise', default='all',
       help="Gender expertise of this member")
    
    season_expertise = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Seasons'),
    ], string='Season Expertise', default='all_season',
       help="Season expertise of this member")
    
    # Performance
    sale_amount = fields.Monetary(
        string='Sale Amount',
        compute='_compute_sale_amount',
        help="Total sale amount by this member"
    )
    
    sale_orders = fields.Integer(
        string='Sale Orders',
        compute='_compute_sale_orders',
        help="Total number of sale orders by this member"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='team_id.currency_id',
        store=True,
        help="Currency for this member"
    )
    
    # Kids Clothing Specific Analytics
    kids_sales = fields.Monetary(
        string='Kids Sales',
        compute='_compute_kids_sales',
        help="Total sales of kids items by this member"
    )
    
    age_group_sales = fields.Text(
        string='Age Group Sales',
        compute='_compute_age_group_sales',
        help="Sales by age group for this member"
    )
    
    gender_sales = fields.Text(
        string='Gender Sales',
        compute='_compute_gender_sales',
        help="Sales by gender for this member"
    )
    
    season_sales = fields.Text(
        string='Season Sales',
        compute='_compute_season_sales',
        help="Sales by season for this member"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='team_id.company_id',
        store=True,
        help="Company this member belongs to"
    )
    
    # Active
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this member is active"
    )
    
    @api.depends('user_id', 'user_id.name')
    def _compute_display_name(self):
        for member in self:
            if member.user_id:
                member.display_name = f"{member.user_id.name} - {member.team_id.name}"
            else:
                member.display_name = "New Member"
    
    @api.depends('user_id')
    def _compute_sale_amount(self):
        for member in self:
            if member.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', member.user_id.id),
                    ('state', 'in', ['sale', 'done']),
                ])
                member.sale_amount = sum(order.amount_total for order in orders)
            else:
                member.sale_amount = 0.0
    
    @api.depends('user_id')
    def _compute_sale_orders(self):
        for member in self:
            if member.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', member.user_id.id),
                    ('state', 'in', ['sale', 'done']),
                ])
                member.sale_orders = len(orders)
            else:
                member.sale_orders = 0
    
    @api.depends('user_id')
    def _compute_kids_sales(self):
        for member in self:
            if member.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', member.user_id.id),
                    ('state', 'in', ['sale', 'done']),
                ])
                kids_sales = 0
                for order in orders:
                    for line in order.order_line:
                        if line.product_id and line.product_id.age_group != 'all':
                            kids_sales += line.price_total
                member.kids_sales = kids_sales
            else:
                member.kids_sales = 0.0
    
    @api.depends('user_id')
    def _compute_age_group_sales(self):
        for member in self:
            if member.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', member.user_id.id),
                    ('state', 'in', ['sale', 'done']),
                ])
                age_group_sales = {}
                for order in orders:
                    for line in order.order_line:
                        if line.product_id and line.product_id.age_group:
                            age_group = line.product_id.age_group
                            if age_group not in age_group_sales:
                                age_group_sales[age_group] = 0
                            age_group_sales[age_group] += line.price_total
                member.age_group_sales = str(age_group_sales)
            else:
                member.age_group_sales = str({})
    
    @api.depends('user_id')
    def _compute_gender_sales(self):
        for member in self:
            if member.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', member.user_id.id),
                    ('state', 'in', ['sale', 'done']),
                ])
                gender_sales = {}
                for order in orders:
                    for line in order.order_line:
                        if line.product_id and line.product_id.gender:
                            gender = line.product_id.gender
                            if gender not in gender_sales:
                                gender_sales[gender] = 0
                            gender_sales[gender] += line.price_total
                member.gender_sales = str(gender_sales)
            else:
                member.gender_sales = str({})
    
    @api.depends('user_id')
    def _compute_season_sales(self):
        for member in self:
            if member.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', member.user_id.id),
                    ('state', 'in', ['sale', 'done']),
                ])
                season_sales = {}
                for order in orders:
                    for line in order.order_line:
                        if line.product_id and line.product_id.season:
                            season = line.product_id.season
                            if season not in season_sales:
                                season_sales[season] = 0
                            season_sales[season] += line.price_total
                member.season_sales = str(season_sales)
            else:
                member.season_sales = str({})