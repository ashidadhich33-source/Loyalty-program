# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - POS Order
=============================

POS order management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class PosOrder(BaseModel):
    """POS order for sales transactions"""
    
    _name = 'pos.order'
    _description = 'POS Order'
    _table = 'pos_order'
    
    # Basic Information
    name = CharField(
        string='Order Reference',
        size=100,
        required=True,
        help='Order reference number'
    )
    
    session_id = Many2OneField(
        'pos.session',
        string='Session',
        required=True,
        help='POS session for this order'
    )
    
    config_id = Many2OneField(
        'pos.config',
        string='POS Configuration',
        related='session_id.config_id',
        store=True,
        help='POS configuration'
    )
    
    user_id = Many2OneField(
        'res.users',
        string='Cashier',
        required=True,
        help='Cashier who processed this order'
    )
    
    # Employee Performance Tracking
    employee_id = Many2OneField(
        'hr.employee',
        string='Sales Employee',
        help='Employee who made the sale (for performance tracking)'
    )
    
    sales_commission = FloatField(
        string='Sales Commission',
        digits=(12, 2),
        default=0.0,
        help='Commission earned by the sales employee'
    )
    
    commission_rate = FloatField(
        string='Commission Rate %',
        digits=(5, 2),
        default=0.0,
        help='Commission rate applied to this sale'
    )
    
    # Customer Information
    partner_id = Many2OneField(
        'res.partner',
        string='Customer',
        help='Customer for this order'
    )
    
    customer_id = Many2OneField(
        'contact.customer',
        string='Customer',
        required=True,
        help='Customer for this order'
    )
    
    customer_type = SelectionField(
        string='Customer Type',
        selection=[
            ('registered', 'Registered'),
            ('guest', 'Guest'),
        ],
        default='guest',
        help='Type of customer'
    )
    
    # Order State
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('paid', 'Paid'),
            ('done', 'Done'),
            ('invoiced', 'Invoiced'),
            ('cancel', 'Cancelled')
        ],
        default='draft',
        help='Current state of the order'
    )
    
    # Order Timing
    date_order = DateTimeField(
        string='Order Date',
        required=True,
        help='Date and time of the order'
    )
    
    # Order Lines
    lines = One2ManyField(
        string='Order Lines',
        comodel_name='pos.order.line',
        inverse_name='order_id',
        help='Order line items'
    )
    
    # Amounts
    amount_untaxed = FloatField(
        string='Untaxed Amount',
        digits=(12, 2),
        default=0.0,
        help='Amount without tax'
    )
    
    amount_tax = FloatField(
        string='Tax Amount',
        digits=(12, 2),
        default=0.0,
        help='Tax amount'
    )
    
    amount_discount = FloatField(
        string='Discount Amount',
        digits=(12, 2),
        default=0.0,
        help='Total discount amount'
    )
    
    amount_total = FloatField(
        string='Total Amount',
        digits=(12, 2),
        default=0.0,
        help='Total amount including tax'
    )
    
    # Payments
    payment_ids = One2ManyField(
        string='Payments',
        comodel_name='pos.payment',
        inverse_name='order_id',
        help='Payments for this order'
    )
    
    # Discount Information
    discount_type = SelectionField(
        string='Discount Type',
        selection=[
            ('percentage', 'Percentage'),
            ('fixed', 'Fixed Amount')
        ],
        help='Type of discount applied'
    )
    
    discount_rate = FloatField(
        string='Discount Rate',
        digits=(5, 2),
        help='Discount rate (percentage or amount)'
    )
    
    # Age-based Discount
    age_discount_applied = BooleanField(
        string='Age Discount Applied',
        default=False,
        help='Whether age-based discount was applied'
    )
    
    age_discount_percentage = FloatField(
        string='Age Discount %',
        digits=(5, 2),
        help='Age-based discount percentage'
    )
    
    # Loyalty Points
    loyalty_points_earned = IntegerField(
        string='Loyalty Points Earned',
        default=0,
        help='Loyalty points earned from this order'
    )
    
    loyalty_points_used = IntegerField(
        string='Loyalty Points Used',
        default=0,
        help='Loyalty points used in this order'
    )
    
    loyalty_discount_amount = FloatField(
        string='Loyalty Discount Amount',
        digits=(12, 2),
        default=0.0,
        help='Discount amount from loyalty points redemption'
    )
    
    loyalty_points_rate = FloatField(
        string='Points to Rupee Rate',
        digits=(5, 2),
        default=100.0,
        help='Points required per rupee discount (e.g., 100 points = 1 rupee)'
    )
    
    # Payment Information
    payment_method = SelectionField(
        string='Payment Method',
        selection=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('upi', 'UPI'),
            ('mixed', 'Mixed'),
        ],
        default='cash',
        help='Payment method used'
    )
    
    payment_details = TextField(
        string='Payment Details',
        help='Payment transaction details'
    )
    
    amount_received = FloatField(
        string='Amount Received',
        digits=(16, 2),
        help='Amount received from customer'
    )
    
    change_amount = FloatField(
        string='Change Amount',
        digits=(16, 2),
        help='Change given to customer'
    )
    
    # GST Summary Fields
    total_base_amount = FloatField(
        string='Total Base Amount',
        digits=(16, 2),
        compute='_compute_gst_totals',
        help='Total base amount for GST calculation'
    )
    
    total_cgst_amount = FloatField(
        string='Total CGST Amount',
        digits=(16, 2),
        compute='_compute_gst_totals',
        help='Total Central GST amount'
    )
    
    total_sgst_amount = FloatField(
        string='Total SGST Amount',
        digits=(16, 2),
        compute='_compute_gst_totals',
        help='Total State GST amount'
    )
    
    total_igst_amount = FloatField(
        string='Total IGST Amount',
        digits=(16, 2),
        compute='_compute_gst_totals',
        help='Total Integrated GST amount'
    )
    
    total_gst_amount = FloatField(
        string='Total GST Amount',
        digits=(16, 2),
        compute='_compute_gst_totals',
        help='Total GST amount'
    )
    
    grand_total = FloatField(
        string='Grand Total',
        digits=(16, 2),
        compute='_compute_gst_totals',
        help='Grand total amount'
    )
    
    # Receipt Information
    receipt_number = CharField(
        string='Receipt Number',
        size=50,
        help='Receipt number for this order'
    )
    
    print_receipt = BooleanField(
        string='Print Receipt',
        default=True,
        help='Whether to print receipt'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Order notes and comments'
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
        if 'name' not in vals:
            vals['name'] = self._generate_order_name()
        
        if 'date_order' not in vals:
            vals['date_order'] = datetime.now()
        
        if 'user_id' not in vals:
            vals['user_id'] = self.env.user.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update amounts"""
        result = super().write(vals)
        
        # Update amounts when lines change
        if 'lines' in vals or any(field in vals for field in ['discount_rate', 'discount_type']):
            self._update_amounts()
        
        return result
    
    def _generate_order_name(self):
        """Generate unique order name"""
        # This would typically use a sequence
        return f"POS-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _update_amounts(self):
        """Update order amounts based on lines"""
        for order in self:
            # Calculate line amounts
            untaxed_amount = sum(line.price_subtotal for line in order.lines)
            tax_amount = sum(line.price_tax for line in order.lines)
            discount_amount = sum(line.discount_amount for line in order.lines)
            
            # Apply order-level discount
            if order.discount_type == 'percentage' and order.discount_rate:
                order_discount = untaxed_amount * (order.discount_rate / 100)
                discount_amount += order_discount
                untaxed_amount -= order_discount
            elif order.discount_type == 'fixed' and order.discount_rate:
                discount_amount += order.discount_rate
                untaxed_amount -= order.discount_rate
            
            # Update amounts
            order.amount_untaxed = untaxed_amount
            order.amount_tax = tax_amount
            order.amount_discount = discount_amount
            order.amount_total = untaxed_amount + tax_amount
            
            # Calculate commission if employee is assigned
            if order.employee_id:
                order._calculate_commission()
    
    def action_confirm(self):
        """Confirm the order"""
        if self.state != 'draft':
            raise ValueError("Only draft orders can be confirmed")
        
        # Validate order
        self._validate_order()
        
        # Update state
        self.state = 'paid'
        
        # Generate receipt number
        if not self.receipt_number:
            self.receipt_number = self._generate_receipt_number()
        
        # Calculate loyalty points
        self._calculate_loyalty_points()
        
        return True
    
    def action_done(self):
        """Mark order as done"""
        if self.state not in ['paid', 'draft']:
            raise ValueError("Order must be paid or draft to mark as done")
        
        self.state = 'done'
        
        # Update inventory if needed
        self._update_inventory()
        
        return True
    
    def action_cancel(self):
        """Cancel the order"""
        if self.state == 'done':
            raise ValueError("Cannot cancel completed orders")
        
        self.state = 'cancel'
        return True
    
    def _compute_gst_totals(self):
        """Compute GST totals for the order"""
        for order in self:
            order.total_base_amount = sum(line.base_amount for line in order.lines)
            order.total_cgst_amount = sum(line.cgst_amount for line in order.lines)
            order.total_sgst_amount = sum(line.sgst_amount for line in order.lines)
            order.total_igst_amount = sum(line.igst_amount for line in order.lines)
            order.total_gst_amount = sum(line.total_gst_amount for line in order.lines)
            order.grand_total = sum(line.final_price for line in order.lines)
    
    def validate_payment(self):
        """Validate payment amount matches grand total"""
        for order in self:
            if order.amount_received != order.grand_total:
                raise ValueError(f"Payment amount ({order.amount_received}) must equal grand total ({order.grand_total})")
            return True
    
    def action_reprint_receipt(self):
        """Reprint receipt for this order"""
        for order in self:
            # Generate receipt data
            receipt_data = self._generate_receipt_data()
            
            # Log reprint action
            self.env['pos.order.audit.log'].create_audit_log(
                order_id=order.id,
                user_id=self.env.user.id,
                action='Receipt Reprint',
                old_value=None,
                new_value=receipt_data
            )
            
            return receipt_data
    
    def _generate_receipt_data(self):
        """Generate receipt data for printing"""
        return {
            'order_number': self.name,
            'date': self.date_order.strftime('%d-%m-%Y'),
            'time': self.date_order.strftime('%H:%M:%S'),
            'customer': self.customer_id.name,
            'customer_phone': self.customer_id.phone or '',
            'lines': [{
                'name': line.product_id.name,
                'qty': line.qty,
                'price': line.final_price,
                'total': line.final_price * line.qty
            } for line in self.lines],
            'subtotal': self.total_base_amount,
            'cgst': self.total_cgst_amount,
            'sgst': self.total_sgst_amount,
            'igst': self.total_igst_amount,
            'total_gst': self.total_gst_amount,
            'grand_total': self.grand_total,
            'payment_method': self.payment_method,
            'amount_received': self.amount_received,
            'change': self.change_amount
        }
    
    def _validate_order(self):
        """Validate order before confirmation"""
        errors = []
        
        # Check if order has lines
        if not self.lines:
            errors.append("Order must have at least one line")
        
        # Validate payment amount
        if self.amount_received != self.grand_total:
            errors.append(f"Payment amount ({self.amount_received}) must equal grand total ({self.grand_total})")
        
        if errors:
            raise ValueError('\n'.join(errors))
    
    def _generate_receipt_number(self):
        """Generate receipt number"""
        # This would typically use a sequence
        return f"RCP-{self.id:06d}"
    
    def _calculate_loyalty_points(self):
        """Calculate loyalty points for this order"""
        if not self.config_id.enable_loyalty:
            return
        
        # Calculate points earned
        points_per_rupee = self.config_id.loyalty_points_per_rupee
        self.loyalty_points_earned = int(self.amount_total * points_per_rupee)
        
        # Apply loyalty points if customer has them
        if self.partner_id and self.partner_id.loyalty_points > 0:
            # This would integrate with loyalty addon
            pass
    
    def action_redeem_loyalty_points(self, points_to_redeem):
        """Redeem loyalty points for this order"""
        for order in self:
            if not order.partner_id:
                raise UserError(_('Please select a customer to redeem loyalty points.'))
            
            if not order.config_id.enable_loyalty:
                raise UserError(_('Loyalty program is not enabled for this POS.'))
            
            # Get customer's available points
            customer = order.partner_id
            available_points = customer.loyalty_points
            
            if points_to_redeem > available_points:
                raise UserError(_('Insufficient loyalty points. Available: %d points') % available_points)
            
            if points_to_redeem <= 0:
                raise UserError(_('Points to redeem must be greater than 0.'))
            
            # Calculate discount amount
            discount_amount = points_to_redeem / order.loyalty_points_rate
            
            # Check if discount exceeds order amount
            if discount_amount > order.amount_total:
                discount_amount = order.amount_total
                points_to_redeem = int(discount_amount * order.loyalty_points_rate)
            
            # Update order
            order.loyalty_points_used = points_to_redeem
            order.loyalty_discount_amount = discount_amount
            
            # Apply discount to order total
            order.amount_total -= discount_amount
            
            # Create loyalty points transaction
            order._create_loyalty_points_transaction(points_to_redeem, 'redeemed')
            
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Loyalty Points Redeemed'),
                    'message': _('Successfully redeemed %d points for ₹%.2f discount') % (points_to_redeem, discount_amount),
                    'type': 'success',
                }
            }
    
    def action_remove_loyalty_points(self):
        """Remove loyalty points redemption from this order"""
        for order in self:
            if order.loyalty_points_used > 0:
                # Restore order total
                order.amount_total += order.loyalty_discount_amount
                
                # Reset loyalty fields
                order.loyalty_points_used = 0
                order.loyalty_discount_amount = 0.0
                
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Loyalty Points Removed'),
                        'message': _('Loyalty points redemption removed from order'),
                        'type': 'info',
                    }
                }
    
    def _create_loyalty_points_transaction(self, points, transaction_type):
        """Create loyalty points transaction"""
        if not self.partner_id:
            return
        
        # Create loyalty points record
        loyalty_points_vals = {
            'name': f"POS-{self.name}-{transaction_type.upper()}",
            'partner_id': self.partner_id.id,
            'points': points,
            'points_type': transaction_type,
            'transaction_type': 'purchase' if transaction_type == 'earned' else 'redemption',
            'transaction_id': self.id,
            'description': f'POS Order {self.name} - {transaction_type}',
        }
        
        # Get loyalty program
        loyalty_program = self.env['loyalty.program'].search([
            ('is_active', '=', True)
        ], limit=1)
        
        if loyalty_program:
            loyalty_points_vals['program_id'] = loyalty_program.id
        
        self.env['loyalty.points'].create(loyalty_points_vals)
    
    def get_customer_loyalty_info(self):
        """Get customer loyalty information for POS"""
        if not self.partner_id:
            return None
        
        customer = self.partner_id
        
        return {
            'customer_id': customer.id,
            'customer_name': customer.name,
            'available_points': customer.loyalty_points,
            'loyalty_level': customer.loyalty_level,
            'points_rate': self.loyalty_points_rate,
            'max_discount': customer.loyalty_points / self.loyalty_points_rate,
            'points_used': self.loyalty_points_used,
            'discount_amount': self.loyalty_discount_amount,
        }
    
    def _update_inventory(self):
        """Update inventory for sold products"""
        # This would integrate with inventory addon
        for line in self.lines:
            # Update stock quantities
            pass
    
    def action_view_lines(self):
        """View order lines"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Order Lines - {self.name}',
            'res_model': 'pos.order.line',
            'view_mode': 'tree,form',
            'domain': [('order_id', '=', self.id)],
            'context': {'default_order_id': self.id}
        }
    
    def action_view_payments(self):
        """View order payments"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Payments - {self.name}',
            'res_model': 'pos.payment',
            'view_mode': 'tree,form',
            'domain': [('order_id', '=', self.id)],
            'context': {'default_order_id': self.id}
        }
    
    def action_print_receipt(self):
        """Print receipt for this order"""
        return {
            'type': 'ir.actions.report',
            'report_name': 'pos.report_receipt',
            'report_type': 'qweb-pdf',
            'data': {'ids': [self.id]},
            'target': 'new'
        }
    
    def get_order_summary(self):
        """Get order summary data"""
        return {
            'order_name': self.name,
            'customer': self.partner_id.name if self.partner_id else 'Walk-in Customer',
            'cashier': self.user_id.name,
            'date': self.date_order,
            'state': self.state,
            'line_count': len(self.lines),
            'amount_untaxed': self.amount_untaxed,
            'amount_tax': self.amount_tax,
            'amount_discount': self.amount_discount,
            'amount_total': self.amount_total,
            'loyalty_points_earned': self.loyalty_points_earned,
            'payment_summary': self._get_payment_summary()
        }
    
    def _get_payment_summary(self):
        """Get payment method summary"""
        payment_summary = {}
        
        for payment in self.payment_ids:
            method_name = payment.payment_method_id.name
            if method_name not in payment_summary:
                payment_summary[method_name] = 0
            payment_summary[method_name] += payment.amount
        
        return payment_summary
    
    def _calculate_commission(self):
        """Calculate commission for the sales employee"""
        for order in self:
            if not order.employee_id:
                order.sales_commission = 0.0
                order.commission_rate = 0.0
                return
            
            # Get employee's commission rate
            employee = order.employee_id
            commission_rate = getattr(employee, 'commission_rate', 0.0)
            
            # If no commission rate set, use default from job position
            if not commission_rate and employee.job_id:
                commission_rate = getattr(employee.job_id, 'commission_rate', 0.0)
            
            # If still no rate, use default from department
            if not commission_rate and employee.department_id:
                commission_rate = getattr(employee.department_id, 'commission_rate', 0.0)
            
            # Calculate commission on untaxed amount
            order.commission_rate = commission_rate
            order.sales_commission = order.amount_untaxed * (commission_rate / 100)
    
    def get_employee_performance_data(self):
        """Get performance data for the sales employee"""
        if not self.employee_id:
            return None
        
        return {
            'employee_id': self.employee_id.id,
            'employee_name': self.employee_id.name,
            'order_amount': self.amount_total,
            'commission_earned': self.sales_commission,
            'commission_rate': self.commission_rate,
            'order_date': self.date_order,
            'age_group_focus': self._get_age_group_focus(),
            'season_focus': self._get_season_focus(),
            'brand_focus': self._get_brand_focus()
        }
    
    def _get_age_group_focus(self):
        """Get primary age group focus for this order"""
        age_groups = {}
        for line in self.lines:
            if hasattr(line.product_id, 'age_group'):
                age_group = line.product_id.age_group
                if age_group not in age_groups:
                    age_groups[age_group] = 0
                age_groups[age_group] += line.price_subtotal
        
        if age_groups:
            return max(age_groups, key=age_groups.get)
        return 'all'
    
    def _get_season_focus(self):
        """Get primary season focus for this order"""
        seasons = {}
        for line in self.lines:
            if hasattr(line.product_id, 'season'):
                season = line.product_id.season
                if season not in seasons:
                    seasons[season] = 0
                seasons[season] += line.price_subtotal
        
        if seasons:
            return max(seasons, key=seasons.get)
        return 'all_season'
    
    def _get_brand_focus(self):
        """Get primary brand focus for this order"""
        brands = {}
        for line in self.lines:
            if hasattr(line.product_id, 'brand_id') and line.product_id.brand_id:
                brand = line.product_id.brand_id.name
                if brand not in brands:
                    brands[brand] = 0
                brands[brand] += line.price_subtotal
        
        if brands:
            return max(brands, key=brands.get)
        return 'Multiple Brands'