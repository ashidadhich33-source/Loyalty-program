# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Sales - Sales Quotation
===========================================

Standalone version of the sales quotation model for kids clothing retail.
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

class SaleQuotation(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Quotation for Kids Clothing Retail"""
    
    _name = 'sale.quotation'
    _description = 'Sales Quotation'
    _table = 'sale_quotation'
    
    # Quotation Information
    name = CharField(
        string='Quotation Reference',
        size=64,
        required=True,
        help="Unique reference for the quotation"
    )
    
    partner_id = Many2OneField(
        comodel_name='res.partner',
        string='Customer',
        required=True,
        help="Customer for this quotation"
    )
    
    partner_invoice_id = Many2OneField(
        comodel_name='res.partner',
        string='Invoice Address',
        help="Invoice address for this quotation"
    )
    
    partner_shipping_id = Many2OneField(
        comodel_name='res.partner',
        string='Delivery Address',
        help="Delivery address for this quotation"
    )
    
    # Quotation Dates
    date_quotation = DateTimeField(
        string='Quotation Date',
        required=True,
        help="Date when the quotation was created"
    )
    
    validity_date = DateField(
        string='Expiration Date',
        required=True,
        help="Date until which the quotation is valid"
    )
    
    # Quotation Status
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
            ('expired', 'Expired'),
            ('converted', 'Converted to Order'),
        ],
        string='Status',
        default='draft',
        help="Current status of the quotation"
    )
    
    # Kids Clothing Specific Fields
    child_profile_id = Many2OneField(
        comodel_name='child.profile',
        string='Child Profile',
        help="Child profile for this quotation"
    )
    
    # Quotation Lines
    quotation_line_ids = One2ManyField(
        comodel_name='sale.quotation.line',
        inverse_name='quotation_id',
        string='Quotation Lines',
        help="Quotation lines for this quotation"
    )
    
    # Sales Team
    team_id = Many2OneField(
        comodel_name='sale.team',
        string='Sales Team',
        help="Sales team responsible for this quotation"
    )
    
    user_id = Many2OneField(
        comodel_name='res.users',
        string='Salesperson',
        help="Salesperson responsible for this quotation"
    )
    
    # Territory
    territory_id = Many2OneField(
        comodel_name='sale.territory',
        string='Territory',
        help="Territory for this quotation"
    )
    
    # Commission
    commission_id = Many2OneField(
        comodel_name='sale.commission',
        string='Commission',
        help="Commission for this quotation"
    )
    
    # Related Order
    order_id = Many2OneField(
        comodel_name='sale.order',
        string='Related Order',
        help="Order created from this quotation"
    )
    
    # Analytics
    analytics_id = Many2OneField(
        comodel_name='sale.analytics',
        string='Analytics',
        help="Analytics for this quotation"
    )
    
    # Company and Multi-company
    company_id = Many2OneField(
        comodel_name='res.company',
        string='Company',
        required=True,
        help="Company this quotation belongs to"
    )
    
    # Notes and Comments
    note = TextField(
        string='Notes',
        help="Internal notes for this quotation"
    )
    
    client_order_ref = CharField(
        string='Customer Reference',
        size=64,
        help="Customer reference for this quotation"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_items = IntegerField(
        string='Total Kids Items',
        default=0,
        help="Total number of kids items in this quotation"
    )
    
    def _compute_amount(self):
        """Compute quotation amounts"""
        for quotation in self:
            amount_untaxed = sum(line.price_subtotal for line in quotation.quotation_line_ids)
            amount_tax = sum(line.price_tax for line in quotation.quotation_line_ids)
            quotation.amount_untaxed = amount_untaxed
            quotation.amount_tax = amount_tax
            quotation.amount_total = amount_untaxed + amount_tax
    
    def _compute_kids_items(self):
        """Compute kids items count"""
        for quotation in self:
            kids_items = 0
            for line in quotation.quotation_line_ids:
                if line.product_id and line.product_id.age_group != 'all':
                    kids_items += line.product_uom_qty
            quotation.total_kids_items = kids_items
    
    def action_send_quotation(self):
        """Send quotation to customer"""
        self.write({'state': 'sent'})
        return True
    
    def action_accept_quotation(self):
        """Accept quotation"""
        self.write({'state': 'accepted'})
        return True
    
    def action_reject_quotation(self):
        """Reject quotation"""
        self.write({'state': 'rejected'})
        return True
    
    def action_convert_to_order(self):
        """Convert quotation to sales order"""
        if self.state != 'accepted':
            raise ValueError('Only accepted quotations can be converted to orders.')
        
        # Create sales order
        order_vals = {
            'partner_id': self.partner_id.id,
            'partner_invoice_id': self.partner_invoice_id.id if self.partner_invoice_id else False,
            'partner_shipping_id': self.partner_shipping_id.id if self.partner_shipping_id else False,
            'child_profile_id': self.child_profile_id.id if self.child_profile_id else False,
            'age_group': self.age_group,
            'gender': self.gender,
            'season': self.season,
            'team_id': self.team_id.id if self.team_id else False,
            'user_id': self.user_id.id if self.user_id else False,
            'territory_id': self.territory_id.id if self.territory_id else False,
            'commission_id': self.commission_id.id if self.commission_id else False,
            'note': self.note,
            'client_order_ref': self.client_order_ref,
        }
        
        order = self.env['sale.order'].create(order_vals)
        
        # Create order lines
        for line in self.quotation_line_ids:
            order_line_vals = {
                'order_id': order.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'size': line.size,
                'color': line.color,
                'brand': line.brand,
            }
            self.env['sale.order.line'].create(order_line_vals)
        
        # Update quotation
        self.write({
            'state': 'converted',
            'order_id': order.id,
        })
        
        return order
    
    def action_view_order(self):
        """View related order"""
        if not self.order_id:
            raise ValueError('No related order found.')
        return self.order_id
    
    def action_view_analytics(self):
        """View analytics for this quotation"""
        # This would return an action to view analytics
        return True


class SaleQuotationLine(BaseModel, KidsClothingMixin, PriceMixin):
    """Sales Quotation Line for Kids Clothing"""
    
    _name = 'sale.quotation.line'
    _description = 'Sales Quotation Line'
    _table = 'sale_quotation_line'
    
    # Quotation Reference
    quotation_id = Many2OneField(
        comodel_name='sale.quotation',
        string='Quotation Reference',
        required=True,
        help="Sales quotation this line belongs to"
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help="Order of lines in the quotation"
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