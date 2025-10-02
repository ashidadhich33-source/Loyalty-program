# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales - Sales Delivery
=========================================

Standalone version of the sales delivery model for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, IntegerField, FloatField, BooleanField
from core_framework.orm import DateField, DateTimeField, Many2OneField, One2ManyField, SelectionField
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

class SaleDelivery(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Delivery for Kids Clothing Retail"""
    
    _name = 'sale.delivery'
    _description = 'Sales Delivery'
    _table = 'sale_delivery'
    
    # Delivery Information
    name = CharField(
        string='Delivery Reference',
        size=64,
        required=True,
        help="Unique reference for the delivery"
    )
    
    # Order Reference
    order_id = Many2OneField(
        comodel_name='sale.order',
        string='Sales Order',
        required=True,
        help="Sales order this delivery belongs to"
    )
    
    partner_id = Many2OneField(
        comodel_name='erp.partner',
        string='Customer',
        help="Customer for this delivery"
    )
    
    partner_shipping_id = Many2OneField(
        comodel_name='erp.partner',
        string='Delivery Address',
        help="Delivery address for this delivery"
    )
    
    # Delivery Information
    date_delivery = DateTimeField(
        string='Delivery Date',
        required=True,
        help="Date when the delivery was made"
    )
    
    date_scheduled = DateTimeField(
        string='Scheduled Date',
        help="Scheduled delivery date"
    )
    
    # Delivery Status
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('ready', 'Ready for Delivery'),
            ('in_transit', 'In Transit'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help="Current status of the delivery"
    )
    
    # Kids Clothing Specific Fields
    child_profile_id = Many2OneField(
        comodel_name='child.profile',
        string='Child Profile',
        help="Child profile for this delivery"
    )
    
    # Delivery Lines
    delivery_line_ids = One2ManyField(
        comodel_name='sale.delivery.line',
        inverse_name='delivery_id',
        string='Delivery Lines',
        help="Delivery lines for this delivery"
    )
    
    # Delivery Information
    delivery_method = SelectionField(
        selection=[
            ('pickup', 'Customer Pickup'),
            ('home_delivery', 'Home Delivery'),
            ('store_delivery', 'Store Delivery'),
            ('express', 'Express Delivery'),
        ],
        string='Delivery Method',
        default='home_delivery',
        help="Method of delivery"
    )
    
    delivery_company = CharField(
        string='Delivery Company',
        size=128,
        help="Company handling the delivery"
    )
    
    tracking_number = CharField(
        string='Tracking Number',
        size=64,
        help="Tracking number for the delivery"
    )
    
    delivery_notes = TextField(
        string='Delivery Notes',
        help="Notes for the delivery"
    )
    
    # Delivery Address
    delivery_address = TextField(
        string='Delivery Address',
        help="Delivery address"
    )
    
    delivery_city = CharField(
        string='City',
        size=64,
        help="Delivery city"
    )
    
    delivery_state = CharField(
        string='State',
        size=64,
        help="Delivery state"
    )
    
    delivery_zip = CharField(
        string='ZIP',
        size=16,
        help="Delivery ZIP code"
    )
    
    delivery_country = CharField(
        string='Country',
        size=64,
        help="Delivery country"
    )
    
    # Delivery Person
    delivery_person = CharField(
        string='Delivery Person',
        size=128,
        help="Person handling the delivery"
    )
    
    delivery_contact = CharField(
        string='Delivery Contact',
        size=32,
        help="Contact number for delivery"
    )
    
    # Delivery Status
    delivery_confirmed = BooleanField(
        string='Delivery Confirmed',
        default=False,
        help="Whether delivery is confirmed"
    )
    
    delivery_signed = BooleanField(
        string='Delivery Signed',
        default=False,
        help="Whether delivery is signed for"
    )
    
    delivery_photo = CharField(
        string='Delivery Photo',
        size=255,
        help="Photo of the delivery"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_items = IntegerField(
        string='Total Kids Items',
        default=0,
        help="Total number of kids items in this delivery"
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        comodel_name='erp.company',
        string='Company',
        required=True,
        help="Company this delivery belongs to"
    )
    
    def _compute_kids_items(self):
        """Compute kids items count"""
        for delivery in self:
            kids_items = 0
            for line in delivery.delivery_line_ids:
                if line.product_id and line.product_id.age_group != 'all':
                    kids_items += line.product_uom_qty
            delivery.total_kids_items = kids_items
    
    def action_ready_delivery(self):
        """Mark delivery as ready"""
        self.write({'state': 'ready'})
        return True
    
    def action_start_delivery(self):
        """Start delivery"""
        self.write({'state': 'in_transit'})
        return True
    
    def action_deliver(self):
        """Mark as delivered"""
        self.write({
            'state': 'delivered',
            'delivery_confirmed': True,
        })
        return True
    
    def action_cancel_delivery(self):
        """Cancel delivery"""
        self.write({'state': 'cancelled'})
        return True
    
    def action_view_order(self):
        """View related order"""
        return self.order_id
    
    def action_view_analytics(self):
        """View analytics for this delivery"""
        # This would return an action to view analytics
        return True


class SaleDeliveryLine(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Delivery Line for Kids Clothing"""
    
    _name = 'sale.delivery.line'
    _description = 'Sales Delivery Line'
    _table = 'sale_delivery_line'
    
    # Delivery Reference
    delivery_id = Many2OneField(
        comodel_name='sale.delivery',
        string='Delivery Reference',
        required=True,
        help="Sales delivery this line belongs to"
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help="Order of lines in the delivery"
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
    
    # Quantity
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
    
    # Delivery Status
    delivered_qty = FloatField(
        string='Delivered Quantity',
        default=0.0,
        help="Quantity delivered"
    )
    
    remaining_qty = FloatField(
        string='Remaining Quantity',
        help="Remaining quantity to deliver"
    )
    
    # Kids Clothing Specific Analytics
    is_kids_item = BooleanField(
        string='Kids Item',
        default=False,
        help="Whether this is a kids item"
    )
    
    def _compute_remaining_qty(self):
        """Compute remaining quantity"""
        for line in self:
            line.remaining_qty = line.product_uom_qty - line.delivered_qty
    
    def _compute_is_kids_item(self):
        """Compute if this is a kids item"""
        for line in self:
            line.is_kids_item = line.product_id and line.product_id.age_group != 'all'