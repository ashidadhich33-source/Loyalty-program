# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    # Kids Clothing specific inventory fields
    size_variant = fields.Char(
        string='Size Variant',
        help='Size variant of the product (e.g., S, M, L)'
    )
    
    color_variant = fields.Char(
        string='Color Variant',
        help='Color variant of the product (e.g., Red, Blue)'
    )
    
    age_group = fields.Selection([
        ('newborn', 'Newborn (0-3 Months)'),
        ('infant', 'Infant (3-12 Months)'),
        ('toddler', 'Toddler (1-3 Years)'),
        ('preschool', 'Preschool (3-5 Years)'),
        ('child', 'Child (5-12 Years)'),
        ('teen', 'Teen (12+ Years)'),
    ], string='Age Group', help='Age group for the product')
    
    gender = fields.Selection([
        ('unisex', 'Unisex'),
        ('boys', 'Boys'),
        ('girls', 'Girls'),
    ], string='Gender', help='Gender for the product')
    
    season = fields.Selection([
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('fall', 'Fall'),
        ('winter', 'Winter'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for the product')
    
    # Safety information
    safety_certification = fields.Char(
        string='Safety Certification',
        help='Safety certification for the product'
    )
    
    choking_hazard = fields.Boolean(
        string='Choking Hazard',
        help='Contains small parts that may pose choking hazard'
    )
    
    # Inventory management
    min_stock_level = fields.Float(
        string='Minimum Stock Level',
        help='Minimum stock level before reorder'
    )
    
    max_stock_level = fields.Float(
        string='Maximum Stock Level',
        help='Maximum stock level for this product'
    )
    
    reorder_point = fields.Float(
        string='Reorder Point',
        help='Stock level at which to reorder'
    )
    
    reorder_qty = fields.Float(
        string='Reorder Quantity',
        help='Quantity to reorder when stock is low'
    )
    
    # Sales tracking
    last_sale_date = fields.Datetime(
        string='Last Sale Date',
        help='Date of last sale for this product'
    )
    
    total_sales = fields.Float(
        string='Total Sales',
        compute='_compute_total_sales',
        store=True,
        help='Total sales quantity for this product'
    )
    
    avg_daily_sales = fields.Float(
        string='Average Daily Sales',
        compute='_compute_avg_daily_sales',
        store=True,
        help='Average daily sales for this product'
    )
    
    days_of_stock = fields.Float(
        string='Days of Stock',
        compute='_compute_days_of_stock',
        store=True,
        help='Number of days of stock remaining'
    )
    
    # Expiry and seasonality
    expiry_date = fields.Date(
        string='Expiry Date',
        help='Expiry date for seasonal products'
    )
    
    is_seasonal = fields.Boolean(
        string='Is Seasonal',
        help='Whether this product is seasonal'
    )
    
    season_start_date = fields.Date(
        string='Season Start Date',
        help='Start date of the season for this product'
    )
    
    season_end_date = fields.Date(
        string='Season End Date',
        help='End date of the season for this product'
    )
    
    @api.depends('product_id', 'location_id')
    def _compute_total_sales(self):
        """Compute total sales for this product"""
        for quant in self:
            if quant.product_id and quant.location_id:
                # Get sales from stock moves
                moves = self.env['stock.move'].search([
                    ('product_id', '=', quant.product_id.id),
                    ('location_id', '=', quant.location_id.id),
                    ('state', '=', 'done'),
                    ('picking_type_id.code', '=', 'outgoing'),
                ])
                quant.total_sales = sum(moves.mapped('product_uom_qty'))
            else:
                quant.total_sales = 0.0
    
    @api.depends('total_sales', 'product_id')
    def _compute_avg_daily_sales(self):
        """Compute average daily sales"""
        for quant in self:
            if quant.product_id:
                # Calculate days since product creation
                days_since_creation = (datetime.now() - quant.product_id.create_date).days
                if days_since_creation > 0:
                    quant.avg_daily_sales = quant.total_sales / days_since_creation
                else:
                    quant.avg_daily_sales = 0.0
            else:
                quant.avg_daily_sales = 0.0
    
    @api.depends('quantity', 'avg_daily_sales')
    def _compute_days_of_stock(self):
        """Compute days of stock remaining"""
        for quant in self:
            if quant.avg_daily_sales > 0:
                quant.days_of_stock = quant.quantity / quant.avg_daily_sales
            else:
                quant.days_of_stock = 0.0
    
    def check_stock_levels(self):
        """Check if stock levels are below minimum"""
        low_stock_products = []
        for quant in self:
            if quant.quantity <= quant.min_stock_level:
                low_stock_products.append({
                    'product': quant.product_id.name,
                    'current_stock': quant.quantity,
                    'min_stock': quant.min_stock_level,
                    'reorder_qty': quant.reorder_qty,
                })
        return low_stock_products
    
    def get_seasonal_products(self, season):
        """Get products for a specific season"""
        return self.search([
            ('season', '=', season),
            ('quantity', '>', 0),
        ])
    
    def get_age_group_products(self, age_group):
        """Get products for a specific age group"""
        return self.search([
            ('age_group', '=', age_group),
            ('quantity', '>', 0),
        ])
    
    def get_gender_products(self, gender):
        """Get products for a specific gender"""
        return self.search([
            ('gender', '=', gender),
            ('quantity', '>', 0),
        ])
    
    def get_expiring_products(self, days=30):
        """Get products expiring within specified days"""
        expiry_date = datetime.now() + timedelta(days=days)
        return self.search([
            ('expiry_date', '<=', expiry_date),
            ('expiry_date', '>', datetime.now()),
            ('quantity', '>', 0),
        ])
    
    def get_slow_moving_products(self, days=90):
        """Get slow moving products (no sales in specified days)"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return self.search([
            ('last_sale_date', '<=', cutoff_date),
            ('quantity', '>', 0),
        ])
    
    def get_fast_moving_products(self, threshold=10):
        """Get fast moving products (high daily sales)"""
        return self.search([
            ('avg_daily_sales', '>=', threshold),
            ('quantity', '>', 0),
        ])
    
    def get_inventory_analytics(self):
        """Get comprehensive inventory analytics"""
        return {
            'total_products': len(self),
            'low_stock': len(self.filtered(lambda q: q.quantity <= q.min_stock_level)),
            'out_of_stock': len(self.filtered(lambda q: q.quantity == 0)),
            'overstocked': len(self.filtered(lambda q: q.quantity > q.max_stock_level)),
            'seasonal_products': len(self.filtered('is_seasonal')),
            'expiring_soon': len(self.get_expiring_products(30)),
            'slow_moving': len(self.get_slow_moving_products(90)),
            'fast_moving': len(self.get_fast_moving_products(10)),
        }