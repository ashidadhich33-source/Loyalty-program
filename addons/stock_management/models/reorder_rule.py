# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class StockReorderRule(models.Model):
    _name = 'stock.reorder.rule'
    _description = 'Stock Reorder Rule'
    _order = 'product_id, warehouse_id'
    _rec_name = 'name'

    name = fields.Char(
        string='Rule Name',
        required=True,
        help='Name of the reorder rule'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        help='Product for which the reorder rule applies'
    )
    
    product_template_id = fields.Many2one(
        'product.template',
        related='product_id.product_tmpl_id',
        string='Product Template',
        store=True,
        help='Product template'
    )
    
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        required=True,
        help='Warehouse for which the reorder rule applies'
    )
    
    location_id = fields.Many2one(
        'stock.location',
        string='Location',
        help='Specific location within the warehouse'
    )
    
    # Stock Thresholds
    minimum_stock = fields.Float(
        string='Minimum Stock',
        digits='Product Unit of Measure',
        required=True,
        help='Minimum stock level before reordering'
    )
    
    maximum_stock = fields.Float(
        string='Maximum Stock',
        digits='Product Unit of Measure',
        help='Maximum stock level for reordering'
    )
    
    reorder_qty = fields.Float(
        string='Reorder Quantity',
        digits='Product Unit of Measure',
        required=True,
        help='Quantity to reorder when minimum stock is reached'
    )
    
    # Lead Time and Safety Stock
    lead_time_days = fields.Integer(
        string='Lead Time (Days)',
        default=7,
        help='Lead time in days for procurement'
    )
    
    safety_stock = fields.Float(
        string='Safety Stock',
        digits='Product Unit of Measure',
        help='Safety stock buffer'
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
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for the product')
    
    brand = fields.Char(
        string='Brand',
        help='Brand of the product'
    )
    
    color = fields.Char(
        string='Color',
        help='Color of the product'
    )
    
    # Supplier Information
    supplier_id = fields.Many2one(
        'res.partner',
        string='Preferred Supplier',
        domain=[('is_company', '=', True), ('supplier_rank', '>', 0)],
        help='Preferred supplier for this product'
    )
    
    supplier_product_code = fields.Char(
        string='Supplier Product Code',
        help='Product code used by the supplier'
    )
    
    supplier_price = fields.Float(
        string='Supplier Price',
        digits='Product Price',
        help='Price from the supplier'
    )
    
    # Rule Configuration
    active = fields.Boolean(
        string='Active',
        default=True,
        help='Whether the reorder rule is active'
    )
    
    auto_create_po = fields.Boolean(
        string='Auto Create Purchase Order',
        default=False,
        help='Automatically create purchase order when reorder point is reached'
    )
    
    auto_approve_po = fields.Boolean(
        string='Auto Approve Purchase Order',
        default=False,
        help='Automatically approve purchase order'
    )
    
    # Economic Order Quantity (EOQ)
    annual_demand = fields.Float(
        string='Annual Demand',
        digits='Product Unit of Measure',
        help='Annual demand for the product'
    )
    
    ordering_cost = fields.Float(
        string='Ordering Cost',
        digits='Product Price',
        help='Cost of placing an order'
    )
    
    holding_cost = fields.Float(
        string='Holding Cost',
        digits='Product Price',
        help='Cost of holding inventory per unit per year'
    )
    
    eoq = fields.Float(
        string='Economic Order Quantity',
        digits='Product Unit of Measure',
        compute='_compute_eoq',
        help='Economic order quantity calculated using EOQ formula'
    )
    
    # Computed Fields
    current_stock = fields.Float(
        string='Current Stock',
        digits='Product Unit of Measure',
        compute='_compute_current_stock',
        help='Current stock level'
    )
    
    stock_status = fields.Selection([
        ('adequate', 'Adequate'),
        ('low', 'Low Stock'),
        ('critical', 'Critical'),
        ('overstock', 'Overstock'),
    ], string='Stock Status', compute='_compute_stock_status', help='Current stock status')
    
    days_to_reorder = fields.Integer(
        string='Days to Reorder',
        compute='_compute_days_to_reorder',
        help='Estimated days until reorder point is reached'
    )
    
    @api.depends('annual_demand', 'ordering_cost', 'holding_cost')
    def _compute_eoq(self):
        for record in self:
            if record.annual_demand > 0 and record.ordering_cost > 0 and record.holding_cost > 0:
                # EOQ = sqrt(2 * Annual Demand * Ordering Cost / Holding Cost)
                record.eoq = (2 * record.annual_demand * record.ordering_cost / record.holding_cost) ** 0.5
            else:
                record.eoq = 0
    
    @api.depends('product_id', 'warehouse_id')
    def _compute_current_stock(self):
        for record in self:
            if record.product_id and record.warehouse_id:
                stock_location = record.warehouse_id.lot_stock_id
                record.current_stock = self.env['stock.quant']._get_available_quantity(
                    record.product_id, stock_location
                )
            else:
                record.current_stock = 0
    
    @api.depends('current_stock', 'minimum_stock', 'maximum_stock')
    def _compute_stock_status(self):
        for record in self:
            if record.current_stock <= 0:
                record.stock_status = 'critical'
            elif record.current_stock <= record.minimum_stock:
                record.stock_status = 'low'
            elif record.maximum_stock and record.current_stock > record.maximum_stock:
                record.stock_status = 'overstock'
            else:
                record.stock_status = 'adequate'
    
    @api.depends('current_stock', 'minimum_stock', 'annual_demand')
    def _compute_days_to_reorder(self):
        for record in self:
            if record.annual_demand > 0 and record.current_stock > record.minimum_stock:
                daily_demand = record.annual_demand / 365
                stock_deficit = record.current_stock - record.minimum_stock
                record.days_to_reorder = int(stock_deficit / daily_demand) if daily_demand > 0 else 0
            else:
                record.days_to_reorder = 0
    
    @api.model
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            product = self.env['product.product'].browse(vals.get('product_id'))
            warehouse = self.env['stock.warehouse'].browse(vals.get('warehouse_id'))
            vals['name'] = f"{product.name} - {warehouse.name} - Reorder Rule"
        
        return super(StockReorderRule, self).create(vals)
    
    @api.constrains('minimum_stock', 'maximum_stock', 'reorder_qty')
    def _check_stock_values(self):
        for record in self:
            if record.minimum_stock < 0:
                raise ValidationError(_('Minimum stock cannot be negative.'))
            
            if record.maximum_stock and record.maximum_stock < record.minimum_stock:
                raise ValidationError(_('Maximum stock must be greater than minimum stock.'))
            
            if record.reorder_qty <= 0:
                raise ValidationError(_('Reorder quantity must be positive.'))
    
    def action_create_purchase_order(self):
        """Create purchase order based on reorder rule"""
        for record in self:
            if not record.supplier_id:
                raise UserError(_('Please specify a supplier for this reorder rule.'))
            
            # Create purchase order
            po_vals = {
                'partner_id': record.supplier_id.id,
                'warehouse_id': record.warehouse_id.id,
                'order_line': [(0, 0, {
                    'product_id': record.product_id.id,
                    'product_qty': record.reorder_qty,
                    'price_unit': record.supplier_price or record.product_id.standard_price,
                    'name': record.product_id.name,
                })]
            }
            
            purchase_order = self.env['purchase.order'].create(po_vals)
            
            if record.auto_approve_po:
                purchase_order.button_confirm()
            
            return {
                'type': 'ir.actions.act_window',
                'name': _('Purchase Order'),
                'res_model': 'purchase.order',
                'res_id': purchase_order.id,
                'view_mode': 'form',
                'target': 'current',
            }
    
    def action_update_eoq(self):
        """Update reorder quantity based on EOQ calculation"""
        for record in self:
            if record.eoq > 0:
                record.reorder_qty = record.eoq
    
    @api.model
    def check_reorder_points(self):
        """Check reorder points and create purchase orders if needed"""
        # This method would be called by a cron job
        active_rules = self.search([('active', '=', True)])
        
        for rule in active_rules:
            if rule.stock_status in ['low', 'critical'] and rule.auto_create_po:
                try:
                    rule.action_create_purchase_order()
                except Exception as e:
                    _logger.error(f"Failed to create purchase order for rule {rule.name}: {e}")
    
    def action_analyze_demand(self):
        """Analyze demand patterns for the product"""
        # This would analyze historical sales data to predict demand
        # Implementation would depend on sales data availability
        pass
    
    def action_optimize_rule(self):
        """Optimize reorder rule based on historical data"""
        # This would analyze historical data and suggest optimal parameters
        # Implementation would depend on historical data availability
        pass