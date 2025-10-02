# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales - Sale Order Model
===========================================

Standalone version of the sale order model for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField
from core_framework.orm import DateField, DateTimeField, Many2OneField, One2ManyField, SelectionField
from addons.core_base.models.base_mixins import KidsClothingMixin, PriceMixin
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
    
    # Customer Information
    partner_id = Many2OneField(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        help="Customer for this sales order"
    )
    
    partner_invoice_id = Many2OneField(
        comodel_name='res.partner',
        string='Invoice Address',
        help="Invoice address for this order"
    )
    
    partner_shipping_id = Many2OneField(
        comodel_name='res.partner',
        string='Shipping Address',
        help="Shipping address for this order"
    )
    
    # Order Details
    order_date = DateField(
        string='Order Date',
        required=True,
        help="Date when the order was placed"
    )
    
    # Order Status
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
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
    
    # Pricing
    amount_untaxed = FloatField(
        string='Untaxed Amount',
        help="Total amount without taxes"
    )
    
    amount_tax = FloatField(
        string='Tax Amount',
        help="Total tax amount"
    )
    
    amount_total = FloatField(
        string='Total Amount',
        help="Total amount including taxes"
    )
    
    # Currency
    currency_id = Many2OneField(
        comodel_name='res.currency',
        string='Currency',
        help="Currency of the sales order"
    )
    
    # Company and User
    company_id = Many2OneField(
        comodel_name='res.company',
        string='Company',
        required=True,
        help="Company this order belongs to"
    )
    
    user_id = Many2OneField(
        comodel_name='res.users',
        string='Salesperson',
        help="Salesperson responsible for this order"
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help="Internal notes for this order"
    )
    
    # Active
    active = BooleanField(
        string='Active',
        default=True,
        help="Whether this order is active"
    )
    
    def _compute_amount_all(self):
        """Compute all amounts for the order"""
        for order in self:
            amount_untaxed = sum(line.price_subtotal for line in order.order_line_ids)
            amount_tax = sum(line.price_tax for line in order.order_line_ids)
            order.amount_untaxed = amount_untaxed
            order.amount_tax = amount_tax
            order.amount_total = amount_untaxed + amount_tax
    
    def action_quotation_send(self):
        """Send quotation to customer"""
        for order in self:
            order.state = 'sent'
        return True
    
    def action_confirm(self):
        """Confirm the sales order"""
        for order in self:
            order.state = 'sale'
        return True
    
    def action_done(self):
        """Mark order as done"""
        for order in self:
            order.state = 'done'
        return True
    
    def action_cancel(self):
        """Cancel the sales order"""
        for order in self:
            order.state = 'cancel'
        return True


class SaleOrderLine(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Order Line for Kids Clothing Retail"""
    
    _name = 'sale.order.line'
    _description = 'Sales Order Line'
    _table = 'sale_order_line'
    
    # Order Reference
    order_id = Many2OneField(
        comodel_name='sale.order',
        string='Sales Order',
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
        string='Tax Amount',
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
    
    # Kids Clothing Specific Fields
    size_id = Many2OneField(
        comodel_name='product.attribute.value',
        string='Size',
        domain=[('attribute_id.name', '=', 'Size')],
        help="Size of the product"
    )
    
    color_id = Many2OneField(
        comodel_name='product.attribute.value',
        string='Color',
        domain=[('attribute_id.name', '=', 'Color')],
        help="Color of the product"
    )
    
    # Tax
    tax_id = Many2OneField(
        comodel_name='account.tax',
        string='Taxes',
        help="Taxes applied to this line"
    )
    
    # Notes
    name = TextField(
        string='Description',
        help="Description of this line"
    )
    
    def _compute_amount(self):
        """Compute line amounts"""
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            line.price_subtotal = price * line.product_uom_qty
            line.price_tax = 0.0  # Tax calculation would be implemented
            line.price_total = line.price_subtotal + line.price_tax
    
    def _onchange_product_id(self):
        """Onchange product_id"""
        if self.product_id:
            self.product_uom = self.product_id.uom_id
            self.price_unit = self.product_id.list_price
            # Set kids clothing specific fields
            self.age_group = self.product_id.age_group
            self.gender = self.product_id.gender
            self.season = self.product_id.season