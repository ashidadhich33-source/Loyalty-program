# -*- coding: utf-8 -*-
"""
Ocean ERP - Stock Alert Model
=============================

Stock alert management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class StockAlert(BaseModel, KidsClothingMixin):
    """Stock Alert Model for Ocean ERP"""
    
    _name = 'stock.alert'
    _description = 'Stock Alert'
    _order = 'priority desc, create_date desc'
    _rec_name = 'name'

    name = CharField(
        string='Alert Name',
        required=True,
        help='Name of the stock alert'
    )
    
    product_id = Many2OneField(
        'product.product',
        string='Product',
        required=True,
        help='Product for which the alert is generated'
    )
    
    product_template_id = Many2OneField(
        'product.template',
        string='Product Template',
        help='Product template for which the alert is generated'
    )
    
    alert_type = SelectionField(
        selection=[
            ('low_stock', 'Low Stock'),
            ('out_of_stock', 'Out of Stock'),
            ('overstock', 'Overstock'),
            ('expiry', 'Expiry Alert'),
            ('seasonal', 'Seasonal Alert'),
            ('size', 'Size Alert'),
            ('brand', 'Brand Alert'),
            ('color', 'Color Alert'),
        ],
        string='Alert Type',
        required=True,
        help='Type of stock alert'
    )
    
    priority = SelectionField(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent'),
        ],
        string='Priority',
        default='medium',
        help='Priority level of the alert'
    )
    
    status = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('resolved', 'Resolved'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the alert'
    )
    
    current_stock = FloatField(
        string='Current Stock',
        help='Current stock quantity'
    )
    
    minimum_stock = FloatField(
        string='Minimum Stock',
        help='Minimum stock level'
    )
    
    maximum_stock = FloatField(
        string='Maximum Stock',
        help='Maximum stock level'
    )
    
    reorder_point = FloatField(
        string='Reorder Point',
        help='Reorder point for the product'
    )
    
    reorder_quantity = FloatField(
        string='Reorder Quantity',
        help='Suggested reorder quantity'
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
    
    # Alert Details
    message = TextField(
        string='Message',
        help='Alert message'
    )
    
    action_required = CharField(
        string='Action Required',
        help='Action required to resolve the alert'
    )
    
    assigned_to = Many2OneField(
        'res.users',
        string='Assigned To',
        help='User assigned to handle this alert'
    )
    
    due_date = DateTimeField(
        string='Due Date',
        help='Due date for resolving the alert'
    )
    
    resolved_date = DateTimeField(
        string='Resolved Date',
        help='Date when the alert was resolved'
    )
    
    resolved_by = Many2OneField(
        'res.users',
        string='Resolved By',
        help='User who resolved the alert'
    )
    
    resolution_notes = TextField(
        string='Resolution Notes',
        help='Notes about how the alert was resolved'
    )
    
    # Location and Warehouse
    location_id = Many2OneField(
        'stock.location',
        string='Location',
        help='Stock location for this alert'
    )
    
    warehouse_id = Many2OneField(
        'stock.warehouse',
        string='Warehouse',
        help='Warehouse for this alert'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this alert belongs to'
    )
    
    def action_resolve(self):
        """Resolve the alert"""
        self.write({
            'status': 'resolved',
            'resolved_date': self.env.context.get('resolved_date'),
            'resolved_by': self.env.context.get('resolved_by'),
        })
    
    def action_cancel(self):
        """Cancel the alert"""
        self.write({'status': 'cancelled'})
    
    def action_reactivate(self):
        """Reactivate the alert"""
        self.write({'status': 'active'})
    
    def get_kids_clothing_alerts(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get alerts filtered by kids clothing criteria"""
        domain = [('status', '=', 'active')]
        
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
    
    def create_reorder_rule(self):
        """Create reorder rule from alert"""
        reorder_rule = self.env['stock.reorder.rule'].create({
            'product_id': self.product_id.id,
            'minimum_stock': self.minimum_stock,
            'maximum_stock': self.maximum_stock,
            'reorder_quantity': self.reorder_quantity,
            'age_group': self.age_group,
            'size': self.size,
            'season': self.season,
            'brand': self.brand,
            'color': self.color,
            'company_id': self.company_id.id,
        })
        
        return reorder_rule
    
    def generate_purchase_order(self):
        """Generate purchase order from alert"""
        # This would create a purchase order for the reorder quantity
        pass