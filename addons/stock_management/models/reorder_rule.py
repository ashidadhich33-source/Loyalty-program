# -*- coding: utf-8 -*-
"""
Ocean ERP - Reorder Rule Model
==============================

Reorder rule management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class StockReorderRule(BaseModel, KidsClothingMixin):
    """Stock Reorder Rule Model for Ocean ERP"""
    
    _name = 'stock.reorder.rule'
    _description = 'Stock Reorder Rule'
    _order = 'priority desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Rule Name',
        required=True,
        help='Name of the reorder rule'
    )
    
    product_id = Many2OneField(
        'product.product',
        string='Product',
        required=True,
        help='Product for this reorder rule'
    )
    
    product_template_id = Many2OneField(
        'product.template',
        string='Product Template',
        help='Product template for this reorder rule'
    )
    
    minimum_stock = FloatField(
        string='Minimum Stock',
        required=True,
        help='Minimum stock level'
    )
    
    maximum_stock = FloatField(
        string='Maximum Stock',
        help='Maximum stock level'
    )
    
    reorder_quantity = FloatField(
        string='Reorder Quantity',
        required=True,
        help='Quantity to reorder'
    )
    
    reorder_point = FloatField(
        string='Reorder Point',
        required=True,
        help='Stock level at which to reorder'
    )
    
    lead_time = IntegerField(
        string='Lead Time (Days)',
        default=7,
        help='Lead time in days'
    )
    
    safety_stock = FloatField(
        string='Safety Stock',
        default=0.0,
        help='Safety stock level'
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
        help='Age group for the product'
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
        help='Size of the product'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for the product'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand of the product'
    )
    
    color = CharField(
        string='Color',
        help='Color of the product'
    )
    
    # Rule Configuration
    priority = SelectionField(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],
        string='Priority',
        default='medium',
        help='Priority of the reorder rule'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('suspended', 'Suspended'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the reorder rule'
    )
    
    # EOQ Configuration
    use_eoq = BooleanField(
        string='Use EOQ',
        default=False,
        help='Use Economic Order Quantity calculation'
    )
    
    annual_demand = FloatField(
        string='Annual Demand',
        help='Annual demand for EOQ calculation'
    )
    
    ordering_cost = FloatField(
        string='Ordering Cost',
        help='Cost per order for EOQ calculation'
    )
    
    holding_cost = FloatField(
        string='Holding Cost',
        help='Cost to hold inventory for EOQ calculation'
    )
    
    eoq_quantity = FloatField(
        string='EOQ Quantity',
        compute='_compute_eoq',
        help='Economic Order Quantity'
    )
    
    # Location and Warehouse
    location_id = Many2OneField(
        'stock.location',
        string='Location',
        help='Stock location for this rule'
    )
    
    warehouse_id = Many2OneField(
        'stock.warehouse',
        string='Warehouse',
        help='Warehouse for this rule'
    )
    
    # Supplier
    supplier_id = Many2OneField(
        'res.partner',
        string='Supplier',
        help='Preferred supplier for reorders'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this rule belongs to'
    )
    
    # Auto-reorder
    auto_reorder = BooleanField(
        string='Auto Reorder',
        default=False,
        help='Automatically create purchase orders'
    )
    
    # Last Reorder
    last_reorder_date = DateTimeField(
        string='Last Reorder Date',
        help='Date of last reorder'
    )
    
    # Next Reorder
    next_reorder_date = DateTimeField(
        string='Next Reorder Date',
        help='Date of next scheduled reorder'
    )
    
    def _compute_eoq(self):
        """Compute Economic Order Quantity"""
        for record in self:
            if record.use_eoq and record.annual_demand and record.ordering_cost and record.holding_cost:
                # EOQ = sqrt(2 * Annual Demand * Ordering Cost / Holding Cost)
                eoq = (2 * record.annual_demand * record.ordering_cost / record.holding_cost) ** 0.5
                record.eoq_quantity = eoq
            else:
                record.eoq_quantity = 0.0
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            # Generate name from product
            product = self.env['product.product'].browse(vals.get('product_id'))
            vals['name'] = f"Reorder Rule - {product.name}"
        
        return super(StockReorderRule, self).create(vals)
    
    def action_activate(self):
        """Activate the reorder rule"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft rules can be activated.')
            
            record.write({'state': 'active'})
    
    def action_suspend(self):
        """Suspend the reorder rule"""
        for record in self:
            if record.state != 'active':
                raise UserError('Only active rules can be suspended.')
            
            record.write({'state': 'suspended'})
    
    def action_cancel(self):
        """Cancel the reorder rule"""
        for record in self:
            if record.state == 'active':
                raise UserError('Active rules cannot be cancelled.')
            
            record.write({'state': 'cancelled'})
    
    def action_reactivate(self):
        """Reactivate the reorder rule"""
        for record in self:
            if record.state != 'suspended':
                raise UserError('Only suspended rules can be reactivated.')
            
            record.write({'state': 'active'})
    
    def check_reorder_point(self):
        """Check if reorder point is reached"""
        for record in self:
            if record.state != 'active':
                continue
            
            # Get current stock
            current_stock = self._get_current_stock(record)
            
            if current_stock <= record.reorder_point:
                # Create reorder alert
                self._create_reorder_alert(record, current_stock)
                
                # Auto-reorder if enabled
                if record.auto_reorder:
                    self._create_purchase_order(record)
    
    def _get_current_stock(self, record):
        """Get current stock for the product"""
        # This would get the actual stock from the inventory system
        return 0.0
    
    def _create_reorder_alert(self, record, current_stock):
        """Create reorder alert"""
        alert_vals = {
            'name': f"Reorder Alert - {record.product_id.name}",
            'product_id': record.product_id.id,
            'alert_type': 'low_stock',
            'priority': record.priority,
            'current_stock': current_stock,
            'minimum_stock': record.minimum_stock,
            'reorder_point': record.reorder_point,
            'reorder_quantity': record.reorder_quantity,
            'age_group': record.age_group,
            'size': record.size,
            'season': record.season,
            'brand': record.brand,
            'color': record.color,
            'location_id': record.location_id.id,
            'warehouse_id': record.warehouse_id.id,
            'company_id': record.company_id.id,
        }
        
        self.env['stock.alert'].create(alert_vals)
    
    def _create_purchase_order(self, record):
        """Create purchase order for reorder"""
        # This would create a purchase order
        pass
    
    def get_kids_clothing_rules(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get rules filtered by kids clothing criteria"""
        domain = [('state', '=', 'active')]
        
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
    
    def calculate_eoq(self):
        """Calculate Economic Order Quantity"""
        for record in self:
            if record.annual_demand and record.ordering_cost and record.holding_cost:
                record._compute_eoq()
            else:
                raise UserError('Annual demand, ordering cost, and holding cost are required for EOQ calculation.')
    
    def action_view_alerts(self):
        """View alerts for this rule"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Stock Alerts',
            'res_model': 'stock.alert',
            'view_mode': 'tree,form',
            'domain': [
                ('product_id', '=', self.product_id.id),
                ('alert_type', '=', 'low_stock')
            ],
            'context': {'default_product_id': self.product_id.id},
        }
    
    def action_view_purchase_orders(self):
        """View purchase orders for this rule"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Purchase Orders',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [
                ('order_line.product_id', '=', self.product_id.id)
            ],
            'context': {'default_order_line.product_id': self.product_id.id},
        }