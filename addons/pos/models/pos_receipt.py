#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Receipt Model
====================================

POS receipt management and customization.
"""

import logging
from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)

class PosReceipt(BaseModel):
    """POS receipt management"""
    
    _name = 'pos.receipt'
    _description = 'POS Receipt'
    _table = 'pos_receipt'
    _order = 'create_date desc'
    
    # Basic Information
    name = CharField(
        string='Receipt Name',
        size=100,
        required=True,
        help='Name of the receipt'
    )
    
    order_id = Many2OneField(
        'pos.order',
        string='POS Order',
        required=True,
        help='Related POS order'
    )
    
    receipt_number = CharField(
        string='Receipt Number',
        size=50,
        required=True,
        help='Receipt number'
    )
    
    # Receipt Content
    header_text = TextField(
        string='Header Text',
        help='Header text for receipt'
    )
    
    footer_text = TextField(
        string='Footer Text',
        help='Footer text for receipt'
    )
    
    receipt_content = TextField(
        string='Receipt Content',
        help='Full receipt content'
    )
    
    # Receipt Settings
    receipt_type = SelectionField(
        string='Receipt Type',
        selection=[
            ('standard', 'Standard Receipt'),
            ('detailed', 'Detailed Receipt'),
            ('summary', 'Summary Receipt'),
            ('custom', 'Custom Receipt')
        ],
        default='standard',
        help='Type of receipt'
    )
    
    include_customer_info = BooleanField(
        string='Include Customer Info',
        default=True,
        help='Include customer information'
    )
    
    include_payment_info = BooleanField(
        string='Include Payment Info',
        default=True,
        help='Include payment information'
    )
    
    include_loyalty_info = BooleanField(
        string='Include Loyalty Info',
        default=True,
        help='Include loyalty information'
    )
    
    include_tax_breakdown = BooleanField(
        string='Include Tax Breakdown',
        default=True,
        help='Include tax breakdown'
    )
    
    # Print Settings
    print_status = SelectionField(
        string='Print Status',
        selection=[
            ('not_printed', 'Not Printed'),
            ('printed', 'Printed'),
            ('failed', 'Print Failed')
        ],
        default='not_printed',
        help='Print status'
    )
    
    print_date = DateTimeField(
        string='Print Date',
        help='Date when receipt was printed'
    )
    
    print_attempts = IntegerField(
        string='Print Attempts',
        default=0,
        help='Number of print attempts'
    )
    
    # Receipt Formatting
    paper_size = SelectionField(
        string='Paper Size',
        selection=[
            ('58mm', '58mm (Thermal)'),
            ('80mm', '80mm (Thermal)'),
            ('A4', 'A4'),
            ('A5', 'A5')
        ],
        default='58mm',
        help='Paper size for receipt'
    )
    
    font_size = SelectionField(
        string='Font Size',
        selection=[
            ('small', 'Small'),
            ('medium', 'Medium'),
            ('large', 'Large')
        ],
        default='medium',
        help='Font size for receipt'
    )
    
    # Company Information
    company_name = CharField(
        string='Company Name',
        size=200,
        help='Company name on receipt'
    )
    
    company_address = TextField(
        string='Company Address',
        help='Company address on receipt'
    )
    
    company_phone = CharField(
        string='Company Phone',
        size=20,
        help='Company phone on receipt'
    )
    
    company_email = CharField(
        string='Company Email',
        size=100,
        help='Company email on receipt'
    )
    
    company_website = CharField(
        string='Company Website',
        size=100,
        help='Company website on receipt'
    )
    
    # Legal Information
    gstin = CharField(
        string='GSTIN',
        size=20,
        help='GSTIN number'
    )
    
    license_number = CharField(
        string='License Number',
        size=50,
        help='Business license number'
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
        if 'receipt_number' not in vals:
            vals['receipt_number'] = self._generate_receipt_number()
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update content"""
        result = super().write(vals)
        
        # Update receipt content if order changed
        if 'order_id' in vals:
            for record in self:
                record._generate_receipt_content()
        
        return result
    
    def _generate_receipt_number(self):
        """Generate receipt number"""
        # This would use sequence generation
        return f"RCP{self.create_date.strftime('%Y%m%d%H%M%S')}"
    
    def _generate_receipt_content(self):
        """Generate receipt content"""
        for record in self:
            if not record.order_id:
                continue
            
            content = []
            
            # Header
            if record.header_text:
                content.append(record.header_text)
            
            # Company Information
            if record.company_name:
                content.append(f"Company: {record.company_name}")
            if record.company_address:
                content.append(f"Address: {record.company_address}")
            if record.company_phone:
                content.append(f"Phone: {record.company_phone}")
            if record.gstin:
                content.append(f"GSTIN: {record.gstin}")
            
            content.append("-" * 40)
            
            # Order Information
            content.append(f"Receipt: {record.receipt_number}")
            content.append(f"Date: {record.order_id.create_date.strftime('%Y-%m-%d %H:%M')}")
            content.append(f"Cashier: {record.order_id.user_id.name}")
            
            if record.order_id.partner_id and record.include_customer_info:
                content.append(f"Customer: {record.order_id.partner_id.name}")
                if record.order_id.partner_id.phone:
                    content.append(f"Phone: {record.order_id.partner_id.phone}")
            
            content.append("-" * 40)
            
            # Order Lines
            content.append("Items:")
            for line in record.order_id.order_line_ids:
                line_text = f"{line.product_name} x{line.quantity} @ {line.price_unit}"
                if line.size:
                    line_text += f" ({line.size})"
                if line.color:
                    line_text += f" ({line.color})"
                content.append(line_text)
                content.append(f"  Subtotal: {line.price_subtotal}")
            
            content.append("-" * 40)
            
            # Pricing Summary
            content.append(f"Subtotal: {record.order_id.amount_untaxed}")
            if record.order_id.discount_amount > 0:
                content.append(f"Discount: -{record.order_id.discount_amount}")
            if record.order_id.amount_tax > 0:
                content.append(f"Tax: {record.order_id.amount_tax}")
            content.append(f"Total: {record.order_id.amount_total}")
            
            # Payment Information
            if record.include_payment_info:
                content.append("-" * 40)
                content.append("Payment:")
                if record.order_id.cash_amount > 0:
                    content.append(f"Cash: {record.order_id.cash_amount}")
                if record.order_id.card_amount > 0:
                    content.append(f"Card: {record.order_id.card_amount}")
                if record.order_id.upi_amount > 0:
                    content.append(f"UPI: {record.order_id.upi_amount}")
                if record.order_id.wallet_amount > 0:
                    content.append(f"Wallet: {record.order_id.wallet_amount}")
            
            # Loyalty Information
            if record.include_loyalty_info and record.order_id.loyalty_points_earned > 0:
                content.append("-" * 40)
                content.append(f"Loyalty Points Earned: {record.order_id.loyalty_points_earned}")
            
            # Footer
            if record.footer_text:
                content.append("-" * 40)
                content.append(record.footer_text)
            
            record.receipt_content = '\n'.join(content)
    
    def action_print_receipt(self):
        """Print the receipt"""
        for record in self:
            try:
                # This would trigger actual printing
                record.print_status = 'printed'
                record.print_date = datetime.now()
                record.print_attempts += 1
                
                # Generate receipt content if not exists
                if not record.receipt_content:
                    record._generate_receipt_content()
                
                return {
                    'type': 'ocean.actions.act_url',
                    'url': f'/pos/print_receipt/{record.id}',
                    'target': 'new'
                }
            except Exception as e:
                record.print_status = 'failed'
                record.print_attempts += 1
                raise ValidationError(f"Print failed: {str(e)}")
    
    def action_preview_receipt(self):
        """Preview the receipt"""
        for record in self:
            if not record.receipt_content:
                record._generate_receipt_content()
            
            return {
                'type': 'ocean.actions.act_window',
                'name': f'Receipt Preview - {record.receipt_number}',
                'res_model': 'pos.receipt',
                'view_mode': 'form',
                'res_id': record.id,
                'context': {'preview_mode': True}
            }
    
    def action_regenerate_receipt(self):
        """Regenerate receipt content"""
        for record in self:
            record._generate_receipt_content()
    
    def get_receipt_summary(self):
        """Get receipt summary"""
        return {
            'receipt_info': {
                'name': self.name,
                'receipt_number': self.receipt_number,
                'order': self.order_id.name,
                'type': self.receipt_type,
                'print_status': self.print_status,
                'print_date': self.print_date
            },
            'content_info': {
                'has_content': bool(self.receipt_content),
                'content_length': len(self.receipt_content or ''),
                'includes_customer': self.include_customer_info,
                'includes_payment': self.include_payment_info,
                'includes_loyalty': self.include_loyalty_info
            },
            'format_info': {
                'paper_size': self.paper_size,
                'font_size': self.font_size
            }
        }