# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales - Sales Return
======================================

Standalone version of the sales return model for kids clothing retail.
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

class SaleReturn(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Return for Kids Clothing Retail"""
    
    _name = 'sale.return'
    _description = 'Sales Return'
    _table = 'sale_return'
    
    # Return Information
    name = CharField(
        string='Return Reference',
        size=64,
        required=True,
        help="Unique reference for the return"
    )
    
    # Order Reference
    order_id = Many2OneField(
        comodel_name='sale.order',
        string='Sales Order',
        required=True,
        help="Sales order this return belongs to"
    )
    
    partner_id = Many2OneField(
        comodel_name='res.partner',
        string='Customer',
        help="Customer for this return"
    )
    
    partner_invoice_id = Many2OneField(
        comodel_name='res.partner',
        string='Invoice Address',
        help="Invoice address for this return"
    )
    
    # Return Information
    date_return = DateTimeField(
        string='Return Date',
        required=True,
        help="Date when the return was made"
    )
    
    date_received = DateTimeField(
        string='Received Date',
        help="Date when the return was received"
    )
    
    # Return Status
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('requested', 'Return Requested'),
            ('approved', 'Approved'),
            ('received', 'Received'),
            ('processed', 'Processed'),
            ('refunded', 'Refunded'),
            ('exchanged', 'Exchanged'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help="Current status of the return"
    )
    
    # Kids Clothing Specific Fields
    child_profile_id = Many2OneField(
        comodel_name='child.profile',
        string='Child Profile',
        help="Child profile for this return"
    )
    
    # Return Lines
    return_line_ids = One2ManyField(
        comodel_name='sale.return.line',
        inverse_name='return_id',
        string='Return Lines',
        help="Return lines for this return"
    )
    
    # Return Information
    return_reason = SelectionField(
        selection=[
            ('defective', 'Defective Product'),
            ('wrong_size', 'Wrong Size'),
            ('wrong_color', 'Wrong Color'),
            ('not_as_described', 'Not as Described'),
            ('changed_mind', 'Changed Mind'),
            ('duplicate_order', 'Duplicate Order'),
            ('late_delivery', 'Late Delivery'),
            ('damaged_shipping', 'Damaged in Shipping'),
            ('other', 'Other'),
        ],
        string='Return Reason',
        required=True,
        help="Reason for the return"
    )
    
    return_notes = TextField(
        string='Return Notes',
        help="Notes for the return"
    )
    
    # Return Type
    return_type = SelectionField(
        selection=[
            ('refund', 'Refund'),
            ('exchange', 'Exchange'),
            ('store_credit', 'Store Credit'),
        ],
        string='Return Type',
        default='refund',
        help="Type of return"
    )
    
    # Refund Information
    refund_method = SelectionField(
        selection=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('bank_transfer', 'Bank Transfer'),
            ('store_credit', 'Store Credit'),
        ],
        string='Refund Method',
        help="Method of refund"
    )
    
    refund_amount = FloatField(
        string='Refund Amount',
        help="Amount to be refunded"
    )
    
    # Exchange Information
    exchange_order_id = Many2OneField(
        comodel_name='sale.order',
        string='Exchange Order',
        help="Order created for exchange"
    )
    
    # Return Address
    return_address = TextField(
        string='Return Address',
        help="Address for returning items"
    )
    
    # Return Status
    return_confirmed = BooleanField(
        string='Return Confirmed',
        default=False,
        help="Whether return is confirmed"
    )
    
    return_received = BooleanField(
        string='Return Received',
        default=False,
        help="Whether return is received"
    )
    
    return_processed = BooleanField(
        string='Return Processed',
        default=False,
        help="Whether return is processed"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_items = IntegerField(
        string='Total Kids Items',
        default=0,
        help="Total number of kids items in this return"
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        comodel_name='res.company',
        string='Company',
        required=True,
        help="Company this return belongs to"
    )
    
    def _compute_kids_items(self):
        """Compute kids items count"""
        for return_order in self:
            kids_items = 0
            for line in return_order.return_line_ids:
                if line.product_id and line.product_id.age_group != 'all':
                    kids_items += line.product_uom_qty
            return_order.total_kids_items = kids_items
    
    def _compute_refund_amount(self):
        """Compute refund amount"""
        for return_order in self:
            refund_amount = sum(line.price_total for line in return_order.return_line_ids)
            return_order.refund_amount = refund_amount
    
    def action_request_return(self):
        """Request return"""
        self.write({'state': 'requested'})
        return True
    
    def action_approve_return(self):
        """Approve return"""
        self.write({'state': 'approved'})
        return True
    
    def action_receive_return(self):
        """Receive return"""
        self.write({
            'state': 'received',
            'return_received': True,
        })
        return True
    
    def action_process_return(self):
        """Process return"""
        self.write({
            'state': 'processed',
            'return_processed': True,
        })
        return True
    
    def action_refund_return(self):
        """Refund return"""
        self.write({'state': 'refunded'})
        return True
    
    def action_exchange_return(self):
        """Exchange return"""
        self.write({'state': 'exchanged'})
        return True
    
    def action_cancel_return(self):
        """Cancel return"""
        self.write({'state': 'cancelled'})
        return True
    
    def action_view_order(self):
        """View related order"""
        return self.order_id
    
    def action_view_exchange_order(self):
        """View exchange order"""
        if not self.exchange_order_id:
            raise ValueError('No exchange order found.')
        return self.exchange_order_id
    
    def action_view_analytics(self):
        """View analytics for this return"""
        # This would return an action to view analytics
        return True


class SaleReturnLine(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Return Line for Kids Clothing"""
    
    _name = 'sale.return.line'
    _description = 'Sales Return Line'
    _table = 'sale_return_line'
    
    # Return Reference
    return_id = Many2OneField(
        comodel_name='sale.return',
        string='Return Reference',
        required=True,
        help="Sales return this line belongs to"
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help="Order of lines in the return"
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
    
    # Return Status
    return_reason = SelectionField(
        selection=[
            ('defective', 'Defective Product'),
            ('wrong_size', 'Wrong Size'),
            ('wrong_color', 'Wrong Color'),
            ('not_as_described', 'Not as Described'),
            ('changed_mind', 'Changed Mind'),
            ('duplicate_order', 'Duplicate Order'),
            ('late_delivery', 'Late Delivery'),
            ('damaged_shipping', 'Damaged in Shipping'),
            ('other', 'Other'),
        ],
        string='Return Reason',
        help="Reason for returning this item"
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