# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging
from datetime import datetime, timedelta

_logger = logging.getLogger(__name__)


class StockAnalysis(models.Model):
    _name = 'stock.analysis'
    _description = 'Stock Analysis'
    _order = 'date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Analysis Name',
        required=True,
        help='Name of the stock analysis'
    )
    
    date = fields.Date(
        string='Analysis Date',
        required=True,
        default=fields.Date.today,
        help='Date of the stock analysis'
    )
    
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        help='Warehouse for the analysis'
    )
    
    analysis_type = fields.Selection([
        ('turnover', 'Stock Turnover Analysis'),
        ('aging', 'Stock Aging Analysis'),
        ('seasonal', 'Seasonal Stock Analysis'),
        ('size_analysis', 'Size-wise Stock Analysis'),
        ('brand_analysis', 'Brand-wise Stock Analysis'),
        ('color_analysis', 'Color-wise Stock Analysis'),
        ('age_group_analysis', 'Age Group Stock Analysis'),
        ('abc_analysis', 'ABC Analysis'),
        ('xyz_analysis', 'XYZ Analysis'),
        ('comprehensive', 'Comprehensive Analysis'),
    ], string='Analysis Type', required=True, help='Type of stock analysis')
    
    # Analysis Period
    date_from = fields.Date(
        string='From Date',
        required=True,
        help='Start date for the analysis period'
    )
    
    date_to = fields.Date(
        string='To Date',
        required=True,
        default=fields.Date.today,
        help='End date for the analysis period'
    )
    
    # Kids Clothing Specific Filters
    age_group_ids = fields.Many2many(
        'product.category',
        'stock_analysis_age_group_rel',
        'analysis_id',
        'category_id',
        string='Age Groups',
        domain=[('name', 'ilike', 'age')],
        help='Age groups to include in analysis'
    )
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for the analysis')
    
    brand_ids = fields.Many2many(
        'res.partner',
        'stock_analysis_brand_rel',
        'analysis_id',
        'partner_id',
        string='Brands',
        domain=[('is_company', '=', True), ('supplier_rank', '>', 0)],
        help='Brands to include in analysis'
    )
    
    size_ids = fields.Many2many(
        'product.attribute.value',
        'stock_analysis_size_rel',
        'analysis_id',
        'value_id',
        string='Sizes',
        domain=[('attribute_id.name', 'ilike', 'size')],
        help='Sizes to include in analysis'
    )
    
    color_ids = fields.Many2many(
        'product.attribute.value',
        'stock_analysis_color_rel',
        'analysis_id',
        'value_id',
        string='Colors',
        domain=[('attribute_id.name', 'ilike', 'color')],
        help='Colors to include in analysis'
    )
    
    # Analysis Results
    analysis_line_ids = fields.One2many(
        'stock.analysis.line',
        'analysis_id',
        string='Analysis Lines',
        help='Lines of the stock analysis'
    )
    
    # Summary Statistics
    total_products = fields.Integer(
        string='Total Products',
        compute='_compute_summary_stats',
        help='Total number of products analyzed'
    )
    
    total_stock_value = fields.Float(
        string='Total Stock Value',
        digits='Product Price',
        compute='_compute_summary_stats',
        help='Total value of stock analyzed'
    )
    
    total_stock_quantity = fields.Float(
        string='Total Stock Quantity',
        digits='Product Unit of Measure',
        compute='_compute_summary_stats',
        help='Total quantity of stock analyzed'
    )
    
    average_turnover_rate = fields.Float(
        string='Average Turnover Rate',
        digits='Product Unit of Measure',
        compute='_compute_summary_stats',
        help='Average stock turnover rate'
    )
    
    # State
    state = fields.Selection([
        ('draft', 'Draft'),
        ('running', 'Running'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True, help='State of the analysis')
    
    # Timestamps
    create_date = fields.Datetime(
        string='Created On',
        readonly=True,
        help='Date when the analysis was created'
    )
    
    done_date = fields.Datetime(
        string='Done On',
        readonly=True,
        help='Date when the analysis was completed'
    )
    
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        help='User who created the analysis'
    )
    
    @api.depends('analysis_line_ids')
    def _compute_summary_stats(self):
        for record in self:
            lines = record.analysis_line_ids
            record.total_products = len(lines)
            record.total_stock_value = sum(line.stock_value for line in lines)
            record.total_stock_quantity = sum(line.stock_quantity for line in lines)
            
            if lines:
                record.average_turnover_rate = sum(line.turnover_rate for line in lines) / len(lines)
            else:
                record.average_turnover_rate = 0
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            analysis_type = vals.get('analysis_type', '')
            vals['name'] = f"{analysis_type.replace('_', ' ').title()} - {fields.Date.today()}"
        
        return super(StockAnalysis, self).create(vals)
    
    def action_run_analysis(self):
        """Run the stock analysis"""
        for record in self:
            if record.state == 'draft':
                record.write({'state': 'running'})
                
                try:
                    # Clear existing lines
                    record.analysis_line_ids.unlink()
                    
                    # Run analysis based on type
                    if record.analysis_type == 'turnover':
                        record._run_turnover_analysis()
                    elif record.analysis_type == 'aging':
                        record._run_aging_analysis()
                    elif record.analysis_type == 'seasonal':
                        record._run_seasonal_analysis()
                    elif record.analysis_type == 'size_analysis':
                        record._run_size_analysis()
                    elif record.analysis_type == 'brand_analysis':
                        record._run_brand_analysis()
                    elif record.analysis_type == 'color_analysis':
                        record._run_color_analysis()
                    elif record.analysis_type == 'age_group_analysis':
                        record._run_age_group_analysis()
                    elif record.analysis_type == 'abc_analysis':
                        record._run_abc_analysis()
                    elif record.analysis_type == 'xyz_analysis':
                        record._run_xyz_analysis()
                    elif record.analysis_type == 'comprehensive':
                        record._run_comprehensive_analysis()
                    
                    record.write({
                        'state': 'done',
                        'done_date': fields.Datetime.now(),
                    })
                    
                except Exception as e:
                    _logger.error(f"Analysis failed: {e}")
                    record.write({'state': 'draft'})
                    raise UserError(_('Analysis failed: %s') % str(e))
    
    def _run_turnover_analysis(self):
        """Run stock turnover analysis"""
        products = self._get_filtered_products()
        
        for product in products:
            # Calculate turnover rate
            turnover_rate = self._calculate_turnover_rate(product)
            
            # Get current stock
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': current_stock,
                'stock_value': stock_value,
                'turnover_rate': turnover_rate,
                'age_group': product.age_group,
                'size': product.size,
                'brand': product.brand,
                'color': product.color,
                'season': product.season,
            })
    
    def _run_aging_analysis(self):
        """Run stock aging analysis"""
        products = self._get_filtered_products()
        
        for product in products:
            # Calculate stock aging
            aging_data = self._calculate_stock_aging(product)
            
            # Get current stock
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': current_stock,
                'stock_value': stock_value,
                'aging_0_30': aging_data.get('0-30', 0),
                'aging_31_60': aging_data.get('31-60', 0),
                'aging_61_90': aging_data.get('61-90', 0),
                'aging_91_180': aging_data.get('91-180', 0),
                'aging_181_365': aging_data.get('181-365', 0),
                'aging_365_plus': aging_data.get('365+', 0),
                'age_group': product.age_group,
                'size': product.size,
                'brand': product.brand,
                'color': product.color,
                'season': product.season,
            })
    
    def _run_seasonal_analysis(self):
        """Run seasonal stock analysis"""
        products = self._get_filtered_products()
        
        for product in products:
            # Calculate seasonal performance
            seasonal_data = self._calculate_seasonal_performance(product)
            
            # Get current stock
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': current_stock,
                'stock_value': stock_value,
                'seasonal_performance': seasonal_data.get('performance', 0),
                'seasonal_trend': seasonal_data.get('trend', 'stable'),
                'age_group': product.age_group,
                'size': product.size,
                'brand': product.brand,
                'color': product.color,
                'season': product.season,
            })
    
    def _run_size_analysis(self):
        """Run size-wise stock analysis"""
        products = self._get_filtered_products()
        
        for product in products:
            # Get current stock
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': current_stock,
                'stock_value': stock_value,
                'size': product.size,
                'age_group': product.age_group,
                'brand': product.brand,
                'color': product.color,
                'season': product.season,
            })
    
    def _run_brand_analysis(self):
        """Run brand-wise stock analysis"""
        products = self._get_filtered_products()
        
        for product in products:
            # Get current stock
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': current_stock,
                'stock_value': stock_value,
                'brand': product.brand,
                'age_group': product.age_group,
                'size': product.size,
                'color': product.color,
                'season': product.season,
            })
    
    def _run_color_analysis(self):
        """Run color-wise stock analysis"""
        products = self._get_filtered_products()
        
        for product in products:
            # Get current stock
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': current_stock,
                'stock_value': stock_value,
                'color': product.color,
                'age_group': product.age_group,
                'size': product.size,
                'brand': product.brand,
                'season': product.season,
            })
    
    def _run_age_group_analysis(self):
        """Run age group stock analysis"""
        products = self._get_filtered_products()
        
        for product in products:
            # Get current stock
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': current_stock,
                'stock_value': stock_value,
                'age_group': product.age_group,
                'size': product.size,
                'brand': product.brand,
                'color': product.color,
                'season': product.season,
            })
    
    def _run_abc_analysis(self):
        """Run ABC analysis"""
        products = self._get_filtered_products()
        
        # Calculate total value for each product
        product_values = []
        for product in products:
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            product_values.append((product, stock_value))
        
        # Sort by value descending
        product_values.sort(key=lambda x: x[1], reverse=True)
        
        # Calculate cumulative percentage
        total_value = sum(value for _, value in product_values)
        cumulative_percentage = 0
        
        for product, stock_value in product_values:
            cumulative_percentage += (stock_value / total_value) * 100
            
            # Determine ABC category
            if cumulative_percentage <= 80:
                abc_category = 'A'
            elif cumulative_percentage <= 95:
                abc_category = 'B'
            else:
                abc_category = 'C'
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': self._get_current_stock(product),
                'stock_value': stock_value,
                'abc_category': abc_category,
                'cumulative_percentage': cumulative_percentage,
                'age_group': product.age_group,
                'size': product.size,
                'brand': product.brand,
                'color': product.color,
                'season': product.season,
            })
    
    def _run_xyz_analysis(self):
        """Run XYZ analysis based on demand variability"""
        products = self._get_filtered_products()
        
        for product in products:
            # Calculate demand variability
            demand_variability = self._calculate_demand_variability(product)
            
            # Determine XYZ category
            if demand_variability <= 0.25:
                xyz_category = 'X'
            elif demand_variability <= 0.5:
                xyz_category = 'Y'
            else:
                xyz_category = 'Z'
            
            # Get current stock
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': current_stock,
                'stock_value': stock_value,
                'xyz_category': xyz_category,
                'demand_variability': demand_variability,
                'age_group': product.age_group,
                'size': product.size,
                'brand': product.brand,
                'color': product.color,
                'season': product.season,
            })
    
    def _run_comprehensive_analysis(self):
        """Run comprehensive stock analysis"""
        products = self._get_filtered_products()
        
        for product in products:
            # Calculate all metrics
            turnover_rate = self._calculate_turnover_rate(product)
            aging_data = self._calculate_stock_aging(product)
            seasonal_data = self._calculate_seasonal_performance(product)
            demand_variability = self._calculate_demand_variability(product)
            
            # Get current stock
            current_stock = self._get_current_stock(product)
            stock_value = current_stock * product.standard_price
            
            self.env['stock.analysis.line'].create({
                'analysis_id': self.id,
                'product_id': product.id,
                'product_name': product.name,
                'stock_quantity': current_stock,
                'stock_value': stock_value,
                'turnover_rate': turnover_rate,
                'aging_0_30': aging_data.get('0-30', 0),
                'aging_31_60': aging_data.get('31-60', 0),
                'aging_61_90': aging_data.get('61-90', 0),
                'aging_91_180': aging_data.get('91-180', 0),
                'aging_181_365': aging_data.get('181-365', 0),
                'aging_365_plus': aging_data.get('365+', 0),
                'seasonal_performance': seasonal_data.get('performance', 0),
                'seasonal_trend': seasonal_data.get('trend', 'stable'),
                'demand_variability': demand_variability,
                'age_group': product.age_group,
                'size': product.size,
                'brand': product.brand,
                'color': product.color,
                'season': product.season,
            })
    
    def _get_filtered_products(self):
        """Get products based on filters"""
        domain = [('type', '=', 'product')]
        
        if self.warehouse_id:
            # Filter products that have stock in this warehouse
            domain.append(('stock_quant_ids.location_id.warehouse_id', '=', self.warehouse_id.id))
        
        if self.age_group_ids:
            domain.append(('categ_id', 'in', self.age_group_ids.ids))
        
        if self.brand_ids:
            domain.append(('brand', 'in', self.brand_ids.mapped('name')))
        
        if self.size_ids:
            domain.append(('size', 'in', self.size_ids.mapped('name')))
        
        if self.color_ids:
            domain.append(('color', 'in', self.color_ids.mapped('name')))
        
        return self.env['product.product'].search(domain)
    
    def _get_current_stock(self, product):
        """Get current stock for a product"""
        if self.warehouse_id:
            location = self.warehouse_id.lot_stock_id
        else:
            location = self.env.ref('stock.stock_location_stock')
        
        return self.env['stock.quant']._get_available_quantity(product, location)
    
    def _calculate_turnover_rate(self, product):
        """Calculate turnover rate for a product"""
        # This would calculate based on sales data
        # For now, return a placeholder value
        return 0.0
    
    def _calculate_stock_aging(self, product):
        """Calculate stock aging for a product"""
        # This would calculate based on stock move dates
        # For now, return placeholder values
        return {
            '0-30': 0,
            '31-60': 0,
            '61-90': 0,
            '91-180': 0,
            '181-365': 0,
            '365+': 0,
        }
    
    def _calculate_seasonal_performance(self, product):
        """Calculate seasonal performance for a product"""
        # This would calculate based on seasonal sales data
        # For now, return placeholder values
        return {
            'performance': 0,
            'trend': 'stable',
        }
    
    def _calculate_demand_variability(self, product):
        """Calculate demand variability for a product"""
        # This would calculate based on demand variance
        # For now, return a placeholder value
        return 0.0


class StockAnalysisLine(models.Model):
    _name = 'stock.analysis.line'
    _description = 'Stock Analysis Line'
    _order = 'product_id'

    analysis_id = fields.Many2one(
        'stock.analysis',
        string='Analysis',
        required=True,
        ondelete='cascade',
        help='Stock analysis this line belongs to'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        help='Product analyzed'
    )
    
    product_name = fields.Char(
        string='Product Name',
        help='Name of the product'
    )
    
    # Stock Information
    stock_quantity = fields.Float(
        string='Stock Quantity',
        digits='Product Unit of Measure',
        help='Current stock quantity'
    )
    
    stock_value = fields.Float(
        string='Stock Value',
        digits='Product Price',
        help='Current stock value'
    )
    
    # Analysis Metrics
    turnover_rate = fields.Float(
        string='Turnover Rate',
        digits='Product Unit of Measure',
        help='Stock turnover rate'
    )
    
    # Aging Analysis
    aging_0_30 = fields.Float(
        string='0-30 Days',
        digits='Product Unit of Measure',
        help='Stock aging 0-30 days'
    )
    
    aging_31_60 = fields.Float(
        string='31-60 Days',
        digits='Product Unit of Measure',
        help='Stock aging 31-60 days'
    )
    
    aging_61_90 = fields.Float(
        string='61-90 Days',
        digits='Product Unit of Measure',
        help='Stock aging 61-90 days'
    )
    
    aging_91_180 = fields.Float(
        string='91-180 Days',
        digits='Product Unit of Measure',
        help='Stock aging 91-180 days'
    )
    
    aging_181_365 = fields.Float(
        string='181-365 Days',
        digits='Product Unit of Measure',
        help='Stock aging 181-365 days'
    )
    
    aging_365_plus = fields.Float(
        string='365+ Days',
        digits='Product Unit of Measure',
        help='Stock aging 365+ days'
    )
    
    # Seasonal Analysis
    seasonal_performance = fields.Float(
        string='Seasonal Performance',
        digits='Product Unit of Measure',
        help='Seasonal performance metric'
    )
    
    seasonal_trend = fields.Selection([
        ('increasing', 'Increasing'),
        ('decreasing', 'Decreasing'),
        ('stable', 'Stable'),
    ], string='Seasonal Trend', help='Seasonal trend')
    
    # ABC Analysis
    abc_category = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
    ], string='ABC Category', help='ABC analysis category')
    
    cumulative_percentage = fields.Float(
        string='Cumulative Percentage',
        digits='Product Unit of Measure',
        help='Cumulative percentage in ABC analysis'
    )
    
    # XYZ Analysis
    xyz_category = fields.Selection([
        ('X', 'X'),
        ('Y', 'Y'),
        ('Z', 'Z'),
    ], string='XYZ Category', help='XYZ analysis category')
    
    demand_variability = fields.Float(
        string='Demand Variability',
        digits='Product Unit of Measure',
        help='Demand variability metric'
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-16', 'Young Adult (14-16 years)'),
    ], string='Age Group', help='Age group for the product')
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
    ], string='Size', help='Size of the product')
    
    brand = fields.Char(
        string='Brand',
        help='Brand of the product'
    )
    
    color = fields.Char(
        string='Color',
        help='Color of the product'
    )
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for the product')