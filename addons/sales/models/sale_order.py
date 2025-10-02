# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales - Sales Order
======================================

Standalone version of the sales order model for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField
from core_framework.orm import DateField, DateTimeField, Many2OneField, One2ManyField, SelectionField
from core_framework.orm import ImageField, BinaryField
from addons.core_base.models.base_mixins import KidsClothingMixin, PriceMixin
from addons.contacts.models.res_partner import ResPartner
from addons.contacts.models.child_profile import ChildProfile
from addons.products.models.product_product import ProductProduct
from addons.company.models.res_company import ResCompany
from addons.users.models.res_users import ResUsers
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, date

logger = logging.getLogger(__name__)

class SaleOrder(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Order for Kids Clothing Retail"""
    
    _name = 'sale.order'
    _description = 'Sales Order'
    _table = 'sale_order'
    
    # Order Information
    name = CharField(
        string='Order Reference',
        size=64,
        required=True,
        help="Unique reference for the sales order"
    )
    
    partner_id = Many2OneField(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        help="Customer for this sales order"
    )
    
    partner_invoice_id = Many2OneField(
        comodel_name='res.partner',
        string='Invoice Address',
        help="Invoice address for this sales order"
    )
    
    partner_shipping_id = Many2OneField(
        comodel_name='res.partner',
        string='Delivery Address',
        help="Delivery address for this sales order"
    )
    
    # Order Dates
    date_order = DateTimeField(
        string='Order Date',
        required=True,
        help="Date when the order was created"
    )
    
    validity_date = DateField(
        string='Expiration Date',
        help="Date until which the quotation is valid"
    )
    
    # Order Status
    state = SelectionField(
        selection=[
            ('draft', 'Quotation'),
            ('sent', 'Quotation Sent'),
            ('sale', 'Sales Order'),
            ('done', 'Locked'),
            ('cancel', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help="Current status of the sales order"
    )
    
    # Kids Clothing Specific Fields
    child_profile_id = Many2OneField(
        comodel_name='child.profile',
        string='Child Profile',
        help="Child profile for this order"
    )
    
    # Order Lines
    order_line_ids = One2ManyField(
        comodel_name='sale.order.line',
        inverse_name='order_id',
        string='Order Lines',
        help="Order lines for this sales order"
    )
    
    # Sales Team
    team_id = Many2OneField(
        comodel_name='sale.team',
        string='Sales Team',
        help="Sales team responsible for this order"
    )
    
    user_id = Many2OneField(
        comodel_name='res.users',
        string='Salesperson',
        help="Salesperson responsible for this order"
    )
    
    # Territory
    territory_id = Many2OneField(
        comodel_name='sale.territory',
        string='Territory',
        help="Territory for this order"
    )
    
    # Commission
    commission_id = Many2OneField(
        comodel_name='sale.commission',
        string='Commission',
        help="Commission for this order"
    )
    
    # Delivery Information
    delivery_count = IntegerField(
        string='Delivery Count',
        default=0,
        help="Number of deliveries for this order"
    )
    
    # Return Information
    return_count = IntegerField(
        string='Return Count',
        default=0,
        help="Number of returns for this order"
    )
    
    # Analytics
    analytics_id = Many2OneField(
        comodel_name='sale.analytics',
        string='Analytics',
        help="Analytics for this order"
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        comodel_name='res.company',
        string='Company',
        required=True,
        help="Company this order belongs to"
    )
    
    # Notes and Comments
    note = TextField(
        string='Notes',
        help="Internal notes for this order"
    )
    
    client_order_ref = CharField(
        string='Customer Reference',
        size=64,
        help="Customer reference for this order"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_items = IntegerField(
        string='Total Kids Items',
        default=0,
        help="Total number of kids items in this order"
    )
    
    def _compute_amount(self):
        """Compute order amounts"""
        for order in self:
            amount_untaxed = sum(line.price_subtotal for line in order.order_line_ids)
            amount_tax = sum(line.price_tax for line in order.order_line_ids)
            order.amount_untaxed = amount_untaxed
            order.amount_tax = amount_tax
            order.amount_total = amount_untaxed + amount_tax
    
    def _compute_delivery_count(self):
        """Compute delivery count"""
        for order in self:
            # This would count deliveries in a real implementation
            order.delivery_count = 0
    
    def _compute_return_count(self):
        """Compute return count"""
        for order in self:
            # This would count returns in a real implementation
            order.return_count = 0
    
    def _compute_kids_items(self):
        """Compute kids items count"""
        for order in self:
            kids_items = 0
            for line in order.order_line_ids:
                if line.product_id and line.product_id.age_group != 'all':
                    kids_items += line.product_uom_qty
            order.total_kids_items = kids_items
    
    def action_quotation_send(self):
        """Send quotation to customer"""
        self.write({'state': 'sent'})
        return True
    
    def action_confirm(self):
        """Confirm sales order"""
        self.write({'state': 'sale'})
        return True
    
    def action_done(self):
        """Mark order as done"""
        self.write({'state': 'done'})
        return True
    
    def action_cancel(self):
        """Cancel sales order"""
        self.write({'state': 'cancel'})
        return True
    
    def action_view_deliveries(self):
        """View deliveries for this order"""
        # This would return an action to view deliveries
        return True
    
    def action_view_returns(self):
        """View returns for this order"""
        # This would return an action to view returns
        return True
    
    def action_view_analytics(self):
        """View analytics for this order"""
        # This would return an action to view analytics
        return True


class SaleOrderLine(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Order Line for Kids Clothing"""
    
    _name = 'sale.order.line'
    _description = 'Sales Order Line'
    _table = 'sale_order_line'
    
    # Order Reference
    order_id = Many2OneField(
        comodel_name='sale.order',
        string='Order Reference',
        required=True,
        help="Sales order this line belongs to"
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help="Order of lines in the order"
    )
    
    # Product Information
    product_id = Many2OneField(
        comodel_name='product.product',
        string='Product',
        required=True,
        help="Product for this line"
    )
    
    # Kids Clothing Specific Fields
    size = CharField(
        string='Size',
        size=32,
        help="Size for this product"
    )
    
    color = CharField(
        string='Color',
        size=32,
        help="Color for this product"
    )
    
    brand = CharField(
        string='Brand',
        size=64,
        help="Brand for this product"
    )
    
    # Quantity and Pricing
    product_uom_qty = FloatField(
        string='Quantity',
        required=True,
        default=1.0,
        help="Quantity of the product"
    )
    
    product_uom = Many2OneField(
        comodel_name='uom.uom',
        string='Unit of Measure',
        required=True,
        help="Unit of measure for this line"
    )
    
    price_unit = FloatField(
        string='Unit Price',
        required=True,
        help="Unit price for this line"
    )
    
    price_subtotal = FloatField(
        string='Subtotal',
        help="Subtotal for this line"
    )
    
    price_tax = FloatField(
        string='Tax',
        help="Tax amount for this line"
    )
    
    price_total = FloatField(
        string='Total',
        help="Total amount for this line"
    )
    
    # Discount
    discount = FloatField(
        string='Discount (%)',
        default=0.0,
        help="Discount percentage for this line"
    )
    
    # Kids Clothing Specific Analytics
    is_kids_item = BooleanField(
        string='Kids Item',
        default=False,
        help="Whether this is a kids item"
    )
    
    def _compute_amount(self):
        """Compute line amounts"""
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            line.price_subtotal = price * line.product_uom_qty
            line.price_tax = 0.0  # Tax calculation would be implemented
            line.price_total = line.price_subtotal + line.price_tax
    
    def _compute_is_kids_item(self):
        """Compute if this is a kids item"""
        for line in self:
            line.is_kids_item = line.product_id and line.product_id.age_group != 'all'
    
    def _onchange_product_id(self):
        """Onchange product_id"""
        if self.product_id:
            self.product_uom = self.product_id.uom_id
            self.price_unit = self.product_id.list_price
            # Set kids clothing specific fields
            self.age_group = self.product_id.age_group
            self.gender = self.product_id.gender
            self.season = self.product_id.season