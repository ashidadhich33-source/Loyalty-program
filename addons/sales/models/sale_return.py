# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleReturn(models.Model):
    _name = 'sale.return'
    _description = 'Sales Return'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_return desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Return Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        help="Unique reference for the return"
    )
    
    # Order Reference
    order_id = fields.Many2one(
        'sale.order',
        string='Sales Order',
        required=True,
        ondelete='cascade',
        help="Sales order this return belongs to"
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        related='order_id.partner_id',
        store=True,
        help="Customer for this return"
    )
    
    partner_invoice_id = fields.Many2one(
        'res.partner',
        string='Invoice Address',
        related='order_id.partner_invoice_id',
        store=True,
        help="Invoice address for this return"
    )
    
    # Return Information
    date_return = fields.Datetime(
        string='Return Date',
        required=True,
        default=fields.Datetime.now,
        help="Date when the return was made"
    )
    
    date_received = fields.Datetime(
        string='Received Date',
        help="Date when the return was received"
    )
    
    # Return Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('requested', 'Return Requested'),
        ('approved', 'Approved'),
        ('received', 'Received'),
        ('processed', 'Processed'),
        ('refunded', 'Refunded'),
        ('exchanged', 'Exchanged'),
        ('cancelled', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='draft',
       help="Current status of the return")
    
    # Kids Clothing Specific Fields
    child_profile_id = fields.Many2one(
        'child.profile',
        string='Child Profile',
        related='order_id.child_profile_id',
        store=True,
        help="Child profile for this return"
    )
    
    age_group = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (Middle School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group', related='order_id.age_group', store=True,
       help="Target age group for this return")
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', related='order_id.gender', store=True,
       help="Target gender for this return")
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', related='order_id.season', store=True,
       help="Season for this return")
    
    # Return Lines
    return_line = fields.One2many(
        'sale.return.line',
        'return_id',
        string='Return Lines',
        copy=True,
        help="Return lines for this return"
    )
    
    # Return Information
    return_reason = fields.Selection([
        ('defective', 'Defective Product'),
        ('wrong_size', 'Wrong Size'),
        ('wrong_color', 'Wrong Color'),
        ('not_as_described', 'Not as Described'),
        ('changed_mind', 'Changed Mind'),
        ('duplicate_order', 'Duplicate Order'),
        ('late_delivery', 'Late Delivery'),
        ('damaged_shipping', 'Damaged in Shipping'),
        ('other', 'Other'),
    ], string='Return Reason', required=True,
       help="Reason for the return")
    
    return_notes = fields.Text(
        string='Return Notes',
        help="Notes for the return"
    )
    
    # Return Type
    return_type = fields.Selection([
        ('refund', 'Refund'),
        ('exchange', 'Exchange'),
        ('store_credit', 'Store Credit'),
    ], string='Return Type', default='refund',
       help="Type of return")
    
    # Refund Information
    refund_method = fields.Selection([
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('store_credit', 'Store Credit'),
    ], string='Refund Method',
       help="Method of refund")
    
    refund_amount = fields.Monetary(
        string='Refund Amount',
        compute='_compute_refund_amount',
        help="Amount to be refunded"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='order_id.currency_id',
        store=True,
        help="Currency for this return"
    )
    
    # Exchange Information
    exchange_order_id = fields.Many2one(
        'sale.order',
        string='Exchange Order',
        help="Order created for exchange"
    )
    
    # Return Address
    return_address = fields.Text(
        string='Return Address',
        help="Address for returning items"
    )
    
    # Return Status
    return_confirmed = fields.Boolean(
        string='Return Confirmed',
        default=False,
        help="Whether return is confirmed"
    )
    
    return_received = fields.Boolean(
        string='Return Received',
        default=False,
        help="Whether return is received"
    )
    
    return_processed = fields.Boolean(
        string='Return Processed',
        default=False,
        help="Whether return is processed"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_items = fields.Integer(
        string='Total Kids Items',
        compute='_compute_kids_items',
        help="Total number of kids items in this return"
    )
    
    age_group_distribution = fields.Text(
        string='Age Group Distribution',
        compute='_compute_age_group_distribution',
        help="Distribution of items by age group"
    )
    
    gender_distribution = fields.Text(
        string='Gender Distribution',
        compute='_compute_gender_distribution',
        help="Distribution of items by gender"
    )
    
    season_distribution = fields.Text(
        string='Season Distribution',
        compute='_compute_season_distribution',
        help="Distribution of items by season"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='order_id.company_id',
        store=True,
        help="Company this return belongs to"
    )
    
    @api.depends('return_line', 'return_line.product_id', 'return_line.product_id.age_group')
    def _compute_kids_items(self):
        for return_order in self:
            kids_items = 0
            for line in return_order.return_line:
                if line.product_id and line.product_id.age_group != 'all':
                    kids_items += line.product_uom_qty
            return_order.total_kids_items = kids_items
    
    @api.depends('return_line', 'return_line.product_id', 'return_line.product_id.age_group')
    def _compute_age_group_distribution(self):
        for return_order in self:
            distribution = {}
            for line in return_order.return_line:
                if line.product_id and line.product_id.age_group:
                    age_group = line.product_id.age_group
                    if age_group not in distribution:
                        distribution[age_group] = 0
                    distribution[age_group] += line.product_uom_qty
            return_order.age_group_distribution = str(distribution)
    
    @api.depends('return_line', 'return_line.product_id', 'return_line.product_id.gender')
    def _compute_gender_distribution(self):
        for return_order in self:
            distribution = {}
            for line in return_order.return_line:
                if line.product_id and line.product_id.gender:
                    gender = line.product_id.gender
                    if gender not in distribution:
                        distribution[gender] = 0
                    distribution[gender] += line.product_uom_qty
            return_order.gender_distribution = str(distribution)
    
    @api.depends('return_line', 'return_line.product_id', 'return_line.product_id.season')
    def _compute_season_distribution(self):
        for return_order in self:
            distribution = {}
            for line in return_order.return_line:
                if line.product_id and line.product_id.season:
                    season = line.product_id.season
                    if season not in distribution:
                        distribution[season] = 0
                    distribution[season] += line.product_uom_qty
            return_order.season_distribution = str(distribution)
    
    @api.depends('return_line', 'return_line.price_total')
    def _compute_refund_amount(self):
        for return_order in self:
            refund_amount = sum(line.price_total for line in return_order.return_line)
            return_order.refund_amount = refund_amount
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.return') or _('New')
        return super().create(vals)
    
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
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.order_id.id,
        }
    
    def action_view_exchange_order(self):
        """View exchange order"""
        if not self.exchange_order_id:
            raise ValidationError(_('No exchange order found.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Exchange Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.exchange_order_id.id,
        }
    
    def action_view_analytics(self):
        """View analytics for this return"""
        action = self.env.ref('sales.action_sale_analytics').read()[0]
        action['domain'] = [('return_id', '=', self.id)]
        return action


class SaleReturnLine(models.Model):
    _name = 'sale.return.line'
    _description = 'Sales Return Line'
    _order = 'return_id, sequence, id'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this return line"
    )
    
    # Return Reference
    return_id = fields.Many2one(
        'sale.return',
        string='Return Reference',
        required=True,
        ondelete='cascade',
        help="Sales return this line belongs to"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of lines in the return"
    )
    
    # Product Information
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        help="Product for this line"
    )
    
    product_template_id = fields.Many2one(
        'product.template',
        string='Product Template',
        related='product_id.product_tmpl_id',
        store=True,
        help="Product template for this line"
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', '0-2 Years (Baby)'),
        ('2-4', '2-4 Years (Toddler)'),
        ('4-6', '4-6 Years (Pre-school)'),
        ('6-8', '6-8 Years (Early School)'),
        ('8-10', '8-10 Years (Middle School)'),
        ('10-12', '10-12 Years (Pre-teen)'),
        ('12-14', '12-14 Years (Teen)'),
        ('14-16', '14-16 Years (Young Adult)'),
        ('all', 'All Ages'),
    ], string='Age Group', related='product_id.age_group', store=True,
       help="Age group for this product")
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', related='product_id.gender', store=True,
       help="Gender for this product")
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', related='product_id.season', store=True,
       help="Season for this product")
    
    size = fields.Char(
        string='Size',
        help="Size for this product"
    )
    
    color = fields.Char(
        string='Color',
        help="Color for this product"
    )
    
    brand = fields.Char(
        string='Brand',
        help="Brand for this product"
    )
    
    # Quantity and Pricing
    product_uom_qty = fields.Float(
        string='Quantity',
        required=True,
        default=1.0,
        help="Quantity of the product"
    )
    
    product_uom = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        required=True,
        help="Unit of measure for this line"
    )
    
    price_unit = fields.Float(
        string='Unit Price',
        required=True,
        digits='Product Price',
        help="Unit price for this line"
    )
    
    price_subtotal = fields.Monetary(
        string='Subtotal',
        store=True,
        readonly=True,
        compute='_compute_amount',
        help="Subtotal for this line"
    )
    
    price_tax = fields.Monetary(
        string='Tax',
        store=True,
        readonly=True,
        compute='_compute_amount',
        help="Tax amount for this line"
    )
    
    price_total = fields.Monetary(
        string='Total',
        store=True,
        readonly=True,
        compute='_compute_amount',
        help="Total amount for this line"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='return_id.currency_id',
        store=True,
        help="Currency for this line"
    )
    
    # Discount
    discount = fields.Float(
        string='Discount (%)',
        digits='Discount',
        default=0.0,
        help="Discount percentage for this line"
    )
    
    # Tax
    tax_id = fields.Many2many(
        'account.tax',
        string='Taxes',
        help="Taxes for this line"
    )
    
    # Return Status
    return_reason = fields.Selection([
        ('defective', 'Defective Product'),
        ('wrong_size', 'Wrong Size'),
        ('wrong_color', 'Wrong Color'),
        ('not_as_described', 'Not as Described'),
        ('changed_mind', 'Changed Mind'),
        ('duplicate_order', 'Duplicate Order'),
        ('late_delivery', 'Late Delivery'),
        ('damaged_shipping', 'Damaged in Shipping'),
        ('other', 'Other'),
    ], string='Return Reason',
       help="Reason for returning this item")
    
    # Kids Clothing Specific Analytics
    is_kids_item = fields.Boolean(
        string='Kids Item',
        compute='_compute_is_kids_item',
        help="Whether this is a kids item"
    )
    
    @api.depends('product_id', 'product_id.age_group')
    def _compute_display_name(self):
        for line in self:
            if line.product_id:
                line.display_name = f"{line.product_id.name} - {line.product_uom_qty} {line.product_uom.name}"
            else:
                line.display_name = "New Line"
    
    @api.depends('product_uom_qty', 'price_unit', 'discount', 'tax_id')
    def _compute_amount(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.return_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.return_id.partner_id)
            line.update({
                'price_subtotal': taxes['total_excluded'],
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
            })
    
    @api.depends('product_id', 'product_id.age_group')
    def _compute_is_kids_item(self):
        for line in self:
            line.is_kids_item = line.product_id and line.product_id.age_group != 'all'
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_uom = self.product_id.uom_id
            self.price_unit = self.product_id.list_price
            self.tax_id = self.product_id.taxes_id