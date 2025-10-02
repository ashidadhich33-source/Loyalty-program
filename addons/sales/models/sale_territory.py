# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleTerritory(models.Model):
    _name = 'sale.territory'
    _description = 'Sales Territory'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(
        string='Territory Name',
        required=True,
        help="Name of the sales territory"
    )
    
    code = fields.Char(
        string='Territory Code',
        required=True,
        help="Code for the sales territory"
    )
    
    # Territory Information
    description = fields.Text(
        string='Description',
        help="Description of the sales territory"
    )
    
    # Territory Assignment
    team_id = fields.Many2one(
        'sale.team',
        string='Sales Team',
        help="Sales team assigned to this territory"
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        help="Salesperson assigned to this territory"
    )
    
    # Geographic Information
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        help="Country for this territory"
    )
    
    state_id = fields.Many2one(
        'res.country.state',
        string='State',
        help="State for this territory"
    )
    
    city_ids = fields.Many2many(
        'res.city',
        string='Cities',
        help="Cities in this territory"
    )
    
    zip_codes = fields.Text(
        string='ZIP Codes',
        help="ZIP codes in this territory"
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
       help="Primary age group focus for this territory")
    
    gender_focus = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
        ('all', 'All Genders'),
    ], string='Gender Focus', default='all',
       help="Primary gender focus for this territory")
    
    season_focus = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Seasons'),
    ], string='Season Focus', default='all_season',
       help="Primary season focus for this territory")
    
    # Territory Performance
    target_amount = fields.Monetary(
        string='Target Amount',
        help="Target amount for this territory"
    )
    
    achieved_amount = fields.Monetary(
        string='Achieved Amount',
        compute='_compute_achieved_amount',
        help="Amount achieved in this territory"
    )
    
    target_orders = fields.Integer(
        string='Target Orders',
        help="Target number of orders for this territory"
    )
    
    achieved_orders = fields.Integer(
        string='Achieved Orders',
        compute='_compute_achieved_orders',
        help="Number of orders achieved in this territory"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help="Currency for this territory"
    )
    
    # Territory Analytics
    performance_percentage = fields.Float(
        string='Performance %',
        compute='_compute_performance_percentage',
        help="Performance percentage of this territory"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_sales = fields.Monetary(
        string='Total Kids Sales',
        compute='_compute_kids_sales',
        help="Total sales of kids items in this territory"
    )
    
    age_group_sales = fields.Text(
        string='Age Group Sales',
        compute='_compute_age_group_sales',
        help="Sales by age group in this territory"
    )
    
    gender_sales = fields.Text(
        string='Gender Sales',
        compute='_compute_gender_sales',
        help="Sales by gender in this territory"
    )
    
    season_sales = fields.Text(
        string='Season Sales',
        compute='_compute_season_sales',
        help="Sales by season in this territory"
    )
    
    # Territory Statistics
    total_customers = fields.Integer(
        string='Total Customers',
        compute='_compute_total_customers',
        help="Total number of customers in this territory"
    )
    
    active_customers = fields.Integer(
        string='Active Customers',
        compute='_compute_active_customers',
        help="Number of active customers in this territory"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help="Company this territory belongs to"
    )
    
    # Active
    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this territory is active"
    )
    
    @api.depends('user_id')
    def _compute_achieved_amount(self):
        for territory in self:
            if territory.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', territory.user_id.id),
                    ('state', 'in', ['sale', 'done']),
                ])
                territory.achieved_amount = sum(order.amount_total for order in orders)
            else:
                territory.achieved_amount = 0.0
    
    @api.depends('user_id')
    def _compute_achieved_orders(self):
        for territory in self:
            if territory.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', territory.user_id.id),
                    ('state', 'in', ['sale', 'done']),
                ])
                territory.achieved_orders = len(orders)
            else:
                territory.achieved_orders = 0
    
    @api.depends('achieved_amount', 'target_amount')
    def _compute_performance_percentage(self):
        for territory in self:
            if territory.target_amount > 0:
                territory.performance_percentage = (territory.achieved_amount / territory.target_amount) * 100
            else:
                territory.performance_percentage = 0.0
    
    @api.depends('user_id')
    def _compute_kids_sales(self):
        for territory in self:
            if territory.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', territory.user_id.id),
                    ('state', 'in', ['sale', 'done']),
                ])
                kids_sales = 0
                for order in orders:
                    for line in order.order_line:
                        if line.product_id and line.product_id.age_group != 'all':
                            kids_sales += line.price_total
                territory.total_kids_sales = kids_sales
            else:
                territory.total_kids_sales = 0.0
    
    @api.depends('user_id')
    def _compute_age_group_sales(self):
        for territory in self:
            if territory.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', territory.user_id.id),
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
                territory.age_group_sales = str(age_group_sales)
            else:
                territory.age_group_sales = str({})
    
    @api.depends('user_id')
    def _compute_gender_sales(self):
        for territory in self:
            if territory.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', territory.user_id.id),
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
                territory.gender_sales = str(gender_sales)
            else:
                territory.gender_sales = str({})
    
    @api.depends('user_id')
    def _compute_season_sales(self):
        for territory in self:
            if territory.user_id:
                orders = self.env['sale.order'].search([
                    ('user_id', '=', territory.user_id.id),
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
                territory.season_sales = str(season_sales)
            else:
                territory.season_sales = str({})
    
    @api.depends('user_id')
    def _compute_total_customers(self):
        for territory in self:
            if territory.user_id:
                customers = self.env['res.partner'].search([
                    ('user_id', '=', territory.user_id.id),
                    ('is_company', '=', False),
                ])
                territory.total_customers = len(customers)
            else:
                territory.total_customers = 0
    
    @api.depends('user_id')
    def _compute_active_customers(self):
        for territory in self:
            if territory.user_id:
                # Get customers with recent orders
                recent_date = fields.Datetime.now() - fields.timedelta(days=90)
                orders = self.env['sale.order'].search([
                    ('user_id', '=', territory.user_id.id),
                    ('date_order', '>=', recent_date),
                ])
                active_customers = set(order.partner_id.id for order in orders)
                territory.active_customers = len(active_customers)
            else:
                territory.active_customers = 0
    
    def action_view_orders(self):
        """View orders for this territory"""
        action = self.env.ref('sales.action_sale_order').read()[0]
        action['domain'] = [('territory_id', '=', self.id)]
        return action
    
    def action_view_customers(self):
        """View customers for this territory"""
        action = self.env.ref('contacts.action_res_partner').read()[0]
        action['domain'] = [('user_id', '=', self.user_id.id)]
        return action
    
    def action_view_analytics(self):
        """View analytics for this territory"""
        action = self.env.ref('sales.action_sale_analytics').read()[0]
        action['domain'] = [('territory_id', '=', self.id)]
        return action