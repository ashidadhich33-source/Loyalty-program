# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleQuotation(models.Model):
    _name = 'sale.quotation'
    _description = 'Sales Quotation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_quotation desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Quotation Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        help="Unique reference for the quotation"
    )
    
    # Quotation Information
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        required=True,
        change_default=True,
        tracking=True,
        help="Customer for this quotation"
    )
    
    partner_invoice_id = fields.Many2one(
        'res.partner',
        string='Invoice Address',
        help="Invoice address for this quotation"
    )
    
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string='Delivery Address',
        help="Delivery address for this quotation"
    )
    
    # Quotation Dates
    date_quotation = fields.Datetime(
        string='Quotation Date',
        required=True,
        readonly=True,
        index=True,
        copy=False,
        default=fields.Datetime.now,
        help="Date when the quotation was created"
    )
    
    validity_date = fields.Date(
        string='Expiration Date',
        required=True,
        help="Date until which the quotation is valid"
    )
    
    # Quotation Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
        ('converted', 'Converted to Order'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='draft',
       help="Current status of the quotation")
    
    # Kids Clothing Specific Fields
    child_profile_id = fields.Many2one(
        'child.profile',
        string='Child Profile',
        help="Child profile for this quotation"
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
    ], string='Age Group', help="Target age group for this quotation")
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', help="Target gender for this quotation")
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help="Season for this quotation")
    
    # Quotation Lines
    quotation_line = fields.One2many(
        'sale.quotation.line',
        'quotation_id',
        string='Quotation Lines',
        copy=True,
        help="Quotation lines for this quotation"
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
        help="Currency for this quotation"
    )
    
    # Payment Information
    payment_term_id = fields.Many2one(
        'account.payment.term',
        string='Payment Terms',
        help="Payment terms for this quotation"
    )
    
    fiscal_position_id = fields.Many2one(
        'account.fiscal.position',
        string='Fiscal Position',
        help="Fiscal position for this quotation"
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
        help="Sales team responsible for this quotation"
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Salesperson',
        help="Salesperson responsible for this quotation"
    )
    
    # Territory
    territory_id = fields.Many2one(
        'sale.territory',
        string='Territory',
        help="Territory for this quotation"
    )
    
    # Commission
    commission_id = fields.Many2one(
        'sale.commission',
        string='Commission',
        help="Commission for this quotation"
    )
    
    # Related Order
    order_id = fields.Many2one(
        'sale.order',
        string='Related Order',
        help="Order created from this quotation"
    )
    
    # Analytics
    analytics_id = fields.Many2one(
        'sale.analytics',
        string='Analytics',
        help="Analytics for this quotation"
    )
    
    # Company and Multi-company
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        help="Company this quotation belongs to"
    )
    
    # Notes and Comments
    note = fields.Text(
        string='Notes',
        help="Internal notes for this quotation"
    )
    
    client_order_ref = fields.Char(
        string='Customer Reference',
        help="Customer reference for this quotation"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_items = fields.Integer(
        string='Total Kids Items',
        compute='_compute_kids_items',
        help="Total number of kids items in this quotation"
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
    
    @api.depends('quotation_line.price_total')
    def _compute_amount(self):
        for quotation in self:
            amount_untaxed = sum(line.price_subtotal for line in quotation.quotation_line)
            amount_tax = sum(line.price_tax for line in quotation.quotation_line)
            quotation.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })
    
    @api.depends('quotation_line', 'quotation_line.product_id', 'quotation_line.product_id.age_group')
    def _compute_kids_items(self):
        for quotation in self:
            kids_items = 0
            for line in quotation.quotation_line:
                if line.product_id and line.product_id.age_group != 'all':
                    kids_items += line.product_uom_qty
            quotation.total_kids_items = kids_items
    
    @api.depends('quotation_line', 'quotation_line.product_id', 'quotation_line.product_id.age_group')
    def _compute_age_group_distribution(self):
        for quotation in self:
            distribution = {}
            for line in quotation.quotation_line:
                if line.product_id and line.product_id.age_group:
                    age_group = line.product_id.age_group
                    if age_group not in distribution:
                        distribution[age_group] = 0
                    distribution[age_group] += line.product_uom_qty
            quotation.age_group_distribution = str(distribution)
    
    @api.depends('quotation_line', 'quotation_line.product_id', 'quotation_line.product_id.gender')
    def _compute_gender_distribution(self):
        for quotation in self:
            distribution = {}
            for line in quotation.quotation_line:
                if line.product_id and line.product_id.gender:
                    gender = line.product_id.gender
                    if gender not in distribution:
                        distribution[gender] = 0
                    distribution[gender] += line.product_uom_qty
            quotation.gender_distribution = str(distribution)
    
    @api.depends('quotation_line', 'quotation_line.product_id', 'quotation_line.product_id.season')
    def _compute_season_distribution(self):
        for quotation in self:
            distribution = {}
            for line in quotation.quotation_line:
                if line.product_id and line.product_id.season:
                    season = line.product_id.season
                    if season not in distribution:
                        distribution[season] = 0
                    distribution[season] += line.product_uom_qty
            quotation.season_distribution = str(distribution)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.quotation') or _('New')
        return super().create(vals)
    
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
            raise ValidationError(_('Only accepted quotations can be converted to orders.'))
        
        # Create sales order
        order_vals = {
            'partner_id': self.partner_id.id,
            'partner_invoice_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'child_profile_id': self.child_profile_id.id,
            'age_group': self.age_group,
            'gender': self.gender,
            'season': self.season,
            'team_id': self.team_id.id,
            'user_id': self.user_id.id,
            'territory_id': self.territory_id.id,
            'commission_id': self.commission_id.id,
            'payment_term_id': self.payment_term_id.id,
            'fiscal_position_id': self.fiscal_position_id.id,
            'gstin': self.gstin,
            'pan': self.pan,
            'note': self.note,
            'client_order_ref': self.client_order_ref,
        }
        
        order = self.env['sale.order'].create(order_vals)
        
        # Create order lines
        for line in self.quotation_line:
            order_line_vals = {
                'order_id': order.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_uom_qty,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
                'discount': line.discount,
                'tax_id': [(6, 0, line.tax_id.ids)],
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
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': order.id,
        }
    
    def action_view_order(self):
        """View related order"""
        if not self.order_id:
            raise ValidationError(_('No related order found.'))
        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.order_id.id,
        }
    
    def action_view_analytics(self):
        """View analytics for this quotation"""
        action = self.env.ref('sales.action_sale_analytics').read()[0]
        action['domain'] = [('quotation_id', '=', self.id)]
        return action


class SaleQuotationLine(models.Model):
    _name = 'sale.quotation.line'
    _description = 'Sales Quotation Line'
    _order = 'quotation_id, sequence, id'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this quotation line"
    )
    
    # Quotation Reference
    quotation_id = fields.Many2one(
        'sale.quotation',
        string='Quotation Reference',
        required=True,
        ondelete='cascade',
        help="Sales quotation this line belongs to"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of lines in the quotation"
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
        related='quotation_id.currency_id',
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
            taxes = line.tax_id.compute_all(price, line.quotation_id.currency_id, line.product_uom_qty, product=line.product_id, partner=line.quotation_id.partner_id)
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