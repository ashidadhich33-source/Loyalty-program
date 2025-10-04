#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Receipt Model
=====================================

POS receipt management for kids clothing retail.
"""

import logging
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PosReceipt(BaseModel):
    """POS receipt for order documentation"""
    
    _name = 'pos.receipt'
    _description = 'POS Receipt'
    _table = 'pos_receipt'
    _order = 'receipt_date desc'
    
    # Basic Information
    name = CharField(
        string='Receipt Number',
        size=100,
        required=True,
        help='Receipt number'
    )
    
    order_id = Many2OneField(
        'pos.order',
        string='Order',
        required=True,
        help='POS order for this receipt'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        related='order_id.session_id',
        store=True,
        help='POS session'
    )
    
    # Receipt Information
    receipt_date = DateTimeField(
        string='Receipt Date',
        required=True,
        help='Date and time of receipt generation'
    )
    
    receipt_type = SelectionField(
        string='Receipt Type',
        selection=[
            ('original', 'Original'),
            ('duplicate', 'Duplicate'),
            ('refund', 'Refund'),
            ('exchange', 'Exchange')
        ],
        default='original',
        help='Type of receipt'
    )
    
    # Company Information
    company_id = Many2OneField(
        'res.company',
        string='Company',
        related='order_id.config_id.company_id',
        store=True,
        help='Company for this receipt'
    )
    
    company_name = CharField(
        string='Company Name',
        size=200,
        help='Company name for receipt'
    )
    
    company_address = TextField(
        string='Company Address',
        help='Company address for receipt'
    )
    
    company_phone = CharField(
        string='Company Phone',
        size=20,
        help='Company phone number'
    )
    
    company_email = CharField(
        string='Company Email',
        size=100,
        help='Company email address'
    )
    
    company_gstin = CharField(
        string='Company GSTIN',
        size=20,
        help='Company GST registration number'
    )
    
    # Customer Information
    customer_name = CharField(
        string='Customer Name',
        size=200,
        help='Customer name for receipt'
    )
    
    customer_phone = CharField(
        string='Customer Phone',
        size=20,
        help='Customer phone number'
    )
    
    customer_email = CharField(
        string='Customer Email',
        size=100,
        help='Customer email address'
    )
    
    # Receipt Content
    receipt_header = TextField(
        string='Receipt Header',
        help='Header text for receipt'
    )
    
    receipt_footer = TextField(
        string='Receipt Footer',
        help='Footer text for receipt'
    )
    
    receipt_content = TextField(
        string='Receipt Content',
        help='Formatted receipt content'
    )
    
    # Receipt Status
    is_printed = BooleanField(
        string='Printed',
        default=False,
        help='Whether receipt has been printed'
    )
    
    print_date = DateTimeField(
        string='Print Date',
        help='Date and time when receipt was printed'
    )
    
    print_count = IntegerField(
        string='Print Count',
        default=0,
        help='Number of times receipt has been printed'
    )
    
    # Digital Receipt
    is_digital = BooleanField(
        string='Digital Receipt',
        default=False,
        help='Whether this is a digital receipt'
    )
    
    digital_sent = BooleanField(
        string='Digital Sent',
        default=False,
        help='Whether digital receipt has been sent'
    )
    
    digital_sent_date = DateTimeField(
        string='Digital Sent Date',
        help='Date and time when digital receipt was sent'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Receipt notes and comments'
    )
    
    # Timestamps
    create_date = DateTimeField(
        string='Created On',
        auto_now_add=True
    )
    
    write_date = DateTimeField(
        string='Updated On',
        auto_now=True
    )
    
    def create(self, vals):
        """Override create to set defaults"""
        if 'receipt_date' not in vals:
            vals['receipt_date'] = self.env['datetime'].now()
        
        if 'name' not in vals:
            vals['name'] = self._generate_receipt_number()
        
        # Set company information
        if 'order_id' in vals:
            order = self.env['pos.order'].browse(vals['order_id'])
            company = order.config_id.company_id
            vals['company_id'] = company.id
            vals['company_name'] = company.name
            vals['company_address'] = company.street or ''
            vals['company_phone'] = company.phone or ''
            vals['company_email'] = company.email or ''
            vals['company_gstin'] = company.vat or ''
        
        # Set customer information
        if 'order_id' in vals and order.partner_id:
            partner = order.partner_id
            vals['customer_name'] = partner.name
            vals['customer_phone'] = partner.phone or ''
            vals['customer_email'] = partner.email or ''
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update receipt content"""
        result = super().write(vals)
        
        # Update receipt content when order changes
        if any(field in vals for field in ['order_id', 'receipt_type']):
            self._generate_receipt_content()
        
        return result
    
    def _generate_receipt_number(self):
        """Generate unique receipt number"""
        # This would typically use a sequence
        return f"RCP-{self.env['datetime'].now().strftime('%Y%m%d%H%M%S')}"
    
    def _generate_receipt_content(self):
        """Generate formatted receipt content"""
        for receipt in self:
            content = self._format_receipt_content(receipt)
            receipt.receipt_content = content
    
    def _format_receipt_content(self, receipt):
        """Format receipt content"""
        content = []
        
        # Header
        if receipt.receipt_header:
            content.append(receipt.receipt_header)
        else:
            content.append("=" * 40)
            content.append(f"{receipt.company_name or 'Kids Clothing Store'}")
            content.append("=" * 40)
        
        # Receipt info
        content.append(f"Receipt No: {receipt.name}")
        content.append(f"Date: {receipt.receipt_date.strftime('%Y-%m-%d %H:%M')}")
        content.append(f"Order: {receipt.order_id.name}")
        
        # Customer info
        if receipt.customer_name:
            content.append(f"Customer: {receipt.customer_name}")
            if receipt.customer_phone:
                content.append(f"Phone: {receipt.customer_phone}")
        
        content.append("-" * 40)
        
        # Order lines
        content.append("Items:")
        for line in receipt.order_id.lines:
            content.append(f"{line.product_name} x{line.qty}")
            content.append(f"  @ {line.price_unit:.2f} = {line.price_subtotal:.2f}")
        
        content.append("-" * 40)
        
        # Totals
        content.append(f"Subtotal: {receipt.order_id.amount_untaxed:.2f}")
        if receipt.order_id.amount_discount > 0:
            content.append(f"Discount: -{receipt.order_id.amount_discount:.2f}")
        if receipt.order_id.amount_tax > 0:
            content.append(f"Tax: {receipt.order_id.amount_tax:.2f}")
        content.append(f"Total: {receipt.order_id.amount_total:.2f}")
        
        # Payments
        content.append("-" * 40)
        content.append("Payments:")
        for payment in receipt.order_id.payment_ids:
            content.append(f"{payment.payment_method_id.name}: {payment.amount:.2f}")
        
        # Footer
        content.append("-" * 40)
        if receipt.receipt_footer:
            content.append(receipt.receipt_footer)
        else:
            content.append("Thank you for your purchase!")
            content.append("Visit us again soon!")
        
        return '\n'.join(content)
    
    def action_print_receipt(self):
        """Print the receipt"""
        if not self.is_printed:
            self.is_printed = True
            self.print_date = self.env['datetime'].now()
        
        self.print_count += 1
        
        return {
            'type': 'ocean.actions.act_report',
            'report_name': 'pos.report_receipt',
            'report_type': 'qweb-pdf',
            'data': {'ids': [self.id]},
            'target': 'new'
        }
    
    def action_send_digital_receipt(self):
        """Send digital receipt to customer"""
        if not self.customer_email:
            raise ValidationError("Customer email is required for digital receipt")
        
        # This would integrate with email system
        # For now, just mark as sent
        self.digital_sent = True
        self.digital_sent_date = self.env['datetime'].now()
        
        return True
    
    def action_view_order(self):
        """View associated order"""
        return {
            'type': 'ocean.actions.act_window',
            'name': f'Order - {self.order_id.name}',
            'res_model': 'pos.order',
            'res_id': self.order_id.id,
            'view_mode': 'form',
            'target': 'new'
        }
    
    def get_receipt_summary(self):
        """Get receipt summary data"""
        return {
            'receipt_number': self.name,
            'receipt_type': self.receipt_type,
            'receipt_date': self.receipt_date,
            'order_name': self.order_id.name,
            'customer_name': self.customer_name,
            'company_name': self.company_name,
            'is_printed': self.is_printed,
            'print_count': self.print_count,
            'is_digital': self.is_digital,
            'digital_sent': self.digital_sent
        }