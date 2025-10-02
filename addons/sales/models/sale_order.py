# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _name = 'sale.order'
    _description = 'Sales Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_order desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Order Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        help="Unique reference for the sales order"
    )
    
    # Order Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        change_default=True,
        tracking=True,
        help="Customer for this sales order"
    )
    
    partner_invoice_id = fields.Many2one(
        'res.partner',
        string='Invoice Address',
        help="Invoice address for this sales order"
    )
    
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string='Delivery Address',
        help="Delivery address for this sales order"
    )
    
    # Order Dates
    date_order = fields.Datetime(
        string='Order Date',
        required=True,
        readonly=True,
        index=True,
        copy=False,
        default=fields.Datetime.now,
        help="Date when the order was created"
    )
    
    validity_date = fields.Date(
        string='Expiration Date',
        help="Date until which the quotation is valid"
    )
    
    # Order Status
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='draft',
       help="Current status of the sales order")
    
    # Kids Clothing Specific Fields
    child_profile_id = fields.Many2one(
        'child.profile',
        string='Child Profile',
        help="Child profile for this order"
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
    ], string='Age Group', help="Target age group for this order")
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', help="Target gender for this order")
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help="Season for this order")
    
    # Order Lines
    order_line = fields.One2many(
        'sale.order.line',
        'order_id',
        string='Order Lines',
        copy=True,
        help="Order lines for this sales order"
    )
    
    # Pricing and Taxes
    amount_untaxed = fields.Monetary(
        string='Untaxed Amount',
        store=True,
        readonly=True,
        compute='_compute_amount',
        help="Amount without tax"
    )
    
    amount_tax = fields.Monetary(
        string='Tax Amount',
        store=True,
        readonly=True,
        compute='_compute_amount',
        help="Amount of tax"
    )
    
    amount_total = fields.Monetary(
        string='Total',
        store=True,
        readonly=True,
        compute='_compute_amount',
        help="Total amount including tax"
    )
    
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
        help="Currency for this sales order"
    )
    
    # Payment Information
    payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Payment Terms',
        help="Payment terms for this order"
    )
    
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position',
        string='Fiscal Position',
        help="Fiscal position for this order"
    )
    
    # Indian Localization
    gstin = fields.Char(
        string='GSTIN',
        help="GSTIN of the customer"
    )
    
    pan = fields.Char(
        string='PAN',
        help="PAN of the customer"
    )
    
    # Sales Team
    team_id = fields.Many2one(
        'sale.team',
        string='Sales Team',
        help="Sales team responsible for this order"
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        help="Salesperson responsible for this order"
    )
    
    # Territory
    territory_id = fields.Many2one(
        'sale.territory',
        string='Territory',
        help="Territory for this order"
    )
    
    # Commission
    commission_id = fields.Many2one(
        'sale.commission',
        string='Commission',
        help="Commission for this order"
    )
    
    # Delivery Information
    delivery_count = fields.Integer(
        string='Delivery Count',
        compute='_compute_delivery_count',
        help="Number of deliveries for this order"
    )
    
    delivery_ids = fields.One2many(
        'sale.delivery',
        'order_id',
        string='Deliveries',
        help="Deliveries for this order"
    )
    
    # Return Information
    return_count = fields.Integer(
        string='Return Count',
        compute='_compute_return_count',
        help="Number of returns for this order"
    )
    
    return_ids = fields.One2many(
        'sale.return',
        'order_id',
        string='Returns',
        help="Returns for this order"
    )
    
    # Analytics
    analytics_id = fields.Many2one(
        'sale.analytics',
        string='Analytics',
        help="Analytics for this order"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help="Company this order belongs to"
    )
    
    # Notes and Comments
    note = fields.Text(
        string='Notes',
        help="Internal notes for this order"
    )
    
    client_order_ref = fields.Char(
        string='Customer Reference',
        help="Customer reference for this order"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_items = fields.Integer(
        string='Total Kids Items',
        compute='_compute_kids_items',
        help="Total number of kids items in this order"
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
    
    @api.depends('order_line.price_total')
    def _compute_amount(self):
        for order in self:
            amount_untaxed = sum(line.price_subtotal for line in order.order_line)
            amount_tax = sum(line.price_tax for line in order.order_line)
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })
    
    @api.depends('delivery_ids')
    def _compute_delivery_count(self):
        for order in self:
            order.delivery_count = len(order.delivery_ids)
    
    @api.depends('return_ids')
    def _compute_return_count(self):
        for order in self:
            order.return_count = len(order.return_ids)
    
    @api.depends('order_line', 'order_line.product_id', 'order_line.product_id.age_group')
    def _compute_kids_items(self):
        for order in self:
            kids_items = 0
            for line in order.order_line:
                if line.product_id and line.product_id.age_group != 'all':
                    kids_items += line.product_uom_qty
            order.total_kids_items = kids_items
    
    @api.depends('order_line', 'order_line.product_id', 'order_line.product_id.age_group')
    def _compute_age_group_distribution(self):
        for order in self:
            distribution = {}
            for line in order.order_line:
                if line.product_id and line.product_id.age_group:
                    age_group = line.product_id.age_group
                    if age_group not in distribution:
                        distribution[age_group] = 0
                    distribution[age_group] += line.product_uom_qty
            order.age_group_distribution = str(distribution)
    
    @api.depends('order_line', 'order_line.product_id', 'order_line.product_id.gender')
    def _compute_gender_distribution(self):
        for order in self:
            distribution = {}
            for line in order.order_line:
                if line.product_id and line.product_id.gender:
                    gender = line.product_id.gender
                    if gender not in distribution:
                        distribution[gender] = 0
                    distribution[gender] += line.product_uom_qty
            order.gender_distribution = str(distribution)
    
    @api.depends('order_line', 'order_line.product_id', 'order_line.product_id.season')
    def _compute_season_distribution(self):
        for order in self:
            distribution = {}
            for line in order.order_line:
                if line.product_id and line.product_id.season:
                    season = line.product_id.season
                    if season not in distribution:
                        distribution[season] = 0
                    distribution[season] += line.product_uom_qty
            order.season_distribution = str(distribution)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.order') or _('New')
        return super().create(vals)
    
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
        action = self.env.ref('sales.action_sale_delivery').read()[0]
        action['domain'] = [('order_id', '=', self.id)]
        return action
    
    def action_view_returns(self):
        """View returns for this order"""
        action = self.env.ref('sales.action_sale_return').read()[0]
        action['domain'] = [('order_id', '=', self.id)]
        return action
    
    def action_view_analytics(self):
        """View analytics for this order"""
        action = self.env.ref('sales.action_sale_analytics').read()[0]
        action['domain'] = [('order_id', '=', self.id)]
        return action


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _description = 'Sales Order Line'
    _order = 'order_id, sequence, id'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this order line"
    )
    
    # Order Reference
    order_id = fields.Many2one(
        'sale.order',
        string='Order Reference',
        required=True,
        ondelete='cascade',
        help="Sales order this line belongs to"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of lines in the order"
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
        related='order_id.currency_id',
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
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.order_id.partner_id)
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