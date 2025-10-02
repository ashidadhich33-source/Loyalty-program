# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CategoryAnalytics(models.Model):
    _name = 'category.analytics'
    _description = 'Category Analytics'
    _order = 'date desc'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this analytics record"
    )
    
    category_id = fields.Many2one(
        'product.category',
        string='Category',
        required=True,
        ondelete='cascade',
        help="Category this analytics record belongs to"
    )
    
    date = fields.Date(
        string='Date',
        required=True,
        default=fields.Date.today,
        help="Date for this analytics record"
    )
    
    period = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ], string='Period', required=True, default='daily',
       help="Period for this analytics record")
    
    # Sales Analytics
    total_sales = fields.Float(
        string='Total Sales',
        digits='Product Price',
        help="Total sales amount for this period"
    )
    
    sales_count = fields.Integer(
        string='Sales Count',
        help="Number of sales transactions for this period"
    )
    
    avg_order_value = fields.Float(
        string='Average Order Value',
        digits='Product Price',
        compute='_compute_avg_order_value',
        help="Average order value for this period"
    )
    
    # Product Analytics
    product_count = fields.Integer(
        string='Product Count',
        help="Number of products in this category"
    )
    
    active_product_count = fields.Integer(
        string='Active Product Count',
        help="Number of active products in this category"
    )
    
    new_product_count = fields.Integer(
        string='New Product Count',
        help="Number of new products added in this period"
    )
    
    # Inventory Analytics
    total_stock = fields.Float(
        string='Total Stock',
        digits='Product Unit of Measure',
        help="Total stock quantity for this category"
    )
    
    stock_value = fields.Float(
        string='Stock Value',
        digits='Product Price',
        help="Total stock value for this category"
    )
    
    stock_turnover = fields.Float(
        string='Stock Turnover',
        digits='Product Unit of Measure',
        help="Stock turnover rate for this category"
    )
    
    # Customer Analytics
    customer_count = fields.Integer(
        string='Customer Count',
        help="Number of customers who purchased from this category"
    )
    
    repeat_customer_count = fields.Integer(
        string='Repeat Customer Count',
        help="Number of repeat customers for this category"
    )
    
    customer_retention_rate = fields.Float(
        string='Customer Retention Rate (%)',
        digits=(5, 2),
        compute='_compute_customer_retention_rate',
        help="Customer retention rate for this category"
    )
    
    # Performance Metrics
    conversion_rate = fields.Float(
        string='Conversion Rate (%)',
        digits=(5, 2),
        help="Conversion rate for this category"
    )
    
    bounce_rate = fields.Float(
        string='Bounce Rate (%)',
        digits=(5, 2),
        help="Bounce rate for this category"
    )
    
    avg_session_duration = fields.Float(
        string='Average Session Duration (minutes)',
        digits=(8, 2),
        help="Average session duration for this category"
    )
    
    # Financial Metrics
    revenue = fields.Float(
        string='Revenue',
        digits='Product Price',
        help="Total revenue for this category"
    )
    
    cost = fields.Float(
        string='Cost',
        digits='Product Price',
        help="Total cost for this category"
    )
    
    profit = fields.Float(
        string='Profit',
        digits='Product Price',
        compute='_compute_profit',
        help="Total profit for this category"
    )
    
    profit_margin = fields.Float(
        string='Profit Margin (%)',
        digits=(5, 2),
        compute='_compute_profit_margin',
        help="Profit margin percentage for this category"
    )
    
    # Market Share
    market_share = fields.Float(
        string='Market Share (%)',
        digits=(5, 2),
        help="Market share for this category"
    )
    
    growth_rate = fields.Float(
        string='Growth Rate (%)',
        digits=(5, 2),
        help="Growth rate for this category"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
        help="Company this analytics record belongs to"
    )
    
    @api.depends('category_id.name', 'date', 'period')
    def _compute_display_name(self):
        for analytics in self:
            analytics.display_name = f"{analytics.category_id.name} - {analytics.date} ({analytics.period})"
    
    @api.depends('total_sales', 'sales_count')
    def _compute_avg_order_value(self):
        for analytics in self:
            if analytics.sales_count > 0:
                analytics.avg_order_value = analytics.total_sales / analytics.sales_count
            else:
                analytics.avg_order_value = 0.0
    
    @api.depends('customer_count', 'repeat_customer_count')
    def _compute_customer_retention_rate(self):
        for analytics in self:
            if analytics.customer_count > 0:
                analytics.customer_retention_rate = (analytics.repeat_customer_count / analytics.customer_count) * 100
            else:
                analytics.customer_retention_rate = 0.0
    
    @api.depends('revenue', 'cost')
    def _compute_profit(self):
        for analytics in self:
            analytics.profit = analytics.revenue - analytics.cost
    
    @api.depends('revenue', 'profit')
    def _compute_profit_margin(self):
        for analytics in self:
            if analytics.revenue > 0:
                analytics.profit_margin = (analytics.profit / analytics.revenue) * 100
            else:
                analytics.profit_margin = 0.0
    
    @api.constrains('date', 'period', 'category_id')
    def _check_unique_analytics(self):
        for analytics in self:
            existing = self.search([
                ('category_id', '=', analytics.category_id.id),
                ('date', '=', analytics.date),
                ('period', '=', analytics.period),
                ('id', '!=', analytics.id)
            ])
            if existing:
                raise ValidationError(_('Analytics record already exists for this category, date, and period.'))
    
    def action_view_products(self):
        """Action to view products in this category"""
        action = self.env.ref('products.action_product_template').read()[0]
        action['domain'] = [('categ_id', '=', self.category_id.id)]
        return action
    
    def action_view_sales(self):
        """Action to view sales for this category"""
        # This would typically link to sales orders
        # For now, return a placeholder action
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales for Category',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('order_line.product_id.categ_id', '=', self.category_id.id)],
        }