# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleDelivery(models.Model):
    _name = 'sale.delivery'
    _description = 'Sales Delivery'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_delivery desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Delivery Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        help="Unique reference for the delivery"
    )
    
    # Order Reference
    order_id = fields.Many2one(
        'sale.order',
        string='Sales Order',
        required=True,
        ondelete='cascade',
        help="Sales order this delivery belongs to"
    )
    
    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        related='order_id.partner_id',
        store=True,
        help="Customer for this delivery"
    )
    
    partner_shipping_id = fields.Many2one(
        'res.partner',
        string='Delivery Address',
        related='order_id.partner_shipping_id',
        store=True,
        help="Delivery address for this delivery"
    )
    
    # Delivery Information
    date_delivery = fields.Datetime(
        string='Delivery Date',
        required=True,
        default=fields.Datetime.now,
        help="Date when the delivery was made"
    )
    
    date_scheduled = fields.Datetime(
        string='Scheduled Date',
        help="Scheduled delivery date"
    )
    
    # Delivery Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ready', 'Ready for Delivery'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=True, default='draft',
       help="Current status of the delivery")
    
    # Kids Clothing Specific Fields
    child_profile_id = fields.Many2one(
        'child.profile',
        string='Child Profile',
        related='order_id.child_profile_id',
        store=True,
        help="Child profile for this delivery"
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
       help="Target age group for this delivery")
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', related='order_id.gender', store=True,
       help="Target gender for this delivery")
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', related='order_id.season', store=True,
       help="Season for this delivery")
    
    # Delivery Lines
    delivery_line = fields.One2many(
        'sale.delivery.line',
        'delivery_id',
        string='Delivery Lines',
        copy=True,
        help="Delivery lines for this delivery"
    )
    
    # Delivery Information
    delivery_method = fields.Selection([
        ('pickup', 'Customer Pickup'),
        ('home_delivery', 'Home Delivery'),
        ('store_delivery', 'Store Delivery'),
        ('express', 'Express Delivery'),
    ], string='Delivery Method', default='home_delivery',
       help="Method of delivery")
    
    delivery_company = fields.Char(
        string='Delivery Company',
        help="Company handling the delivery"
    )
    
    tracking_number = fields.Char(
        string='Tracking Number',
        help="Tracking number for the delivery"
    )
    
    delivery_notes = fields.Text(
        string='Delivery Notes',
        help="Notes for the delivery"
    )
    
    # Delivery Address
    delivery_address = fields.Text(
        string='Delivery Address',
        related='partner_shipping_id.street',
        help="Delivery address"
    )
    
    delivery_city = fields.Char(
        string='City',
        related='partner_shipping_id.city',
        help="Delivery city"
    )
    
    delivery_state = fields.Char(
        string='State',
        related='partner_shipping_id.state_id.name',
        help="Delivery state"
    )
    
    delivery_zip = fields.Char(
        string='ZIP',
        related='partner_shipping_id.zip',
        help="Delivery ZIP code"
    )
    
    delivery_country = fields.Char(
        string='Country',
        related='partner_shipping_id.country_id.name',
        help="Delivery country"
    )
    
    # Delivery Person
    delivery_person = fields.Char(
        string='Delivery Person',
        help="Person handling the delivery"
    )
    
    delivery_contact = fields.Char(
        string='Delivery Contact',
        help="Contact number for delivery"
    )
    
    # Delivery Status
    delivery_confirmed = fields.Boolean(
        string='Delivery Confirmed',
        default=False,
        help="Whether delivery is confirmed"
    )
    
    delivery_signed = fields.Boolean(
        string='Delivery Signed',
        default=False,
        help="Whether delivery is signed for"
    )
    
    delivery_photo = fields.Binary(
        string='Delivery Photo',
        help="Photo of the delivery"
    )
    
    # Kids Clothing Specific Analytics
    total_kids_items = fields.Integer(
        string='Total Kids Items',
        compute='_compute_kids_items',
        help="Total number of kids items in this delivery"
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
        help="Company this delivery belongs to"
    )
    
    @api.depends('delivery_line', 'delivery_line.product_id', 'delivery_line.product_id.age_group')
    def _compute_kids_items(self):
        for delivery in self:
            kids_items = 0
            for line in delivery.delivery_line:
                if line.product_id and line.product_id.age_group != 'all':
                    kids_items += line.product_uom_qty
            delivery.total_kids_items = kids_items
    
    @api.depends('delivery_line', 'delivery_line.product_id', 'delivery_line.product_id.age_group')
    def _compute_age_group_distribution(self):
        for delivery in self:
            distribution = {}
            for line in delivery.delivery_line:
                if line.product_id and line.product_id.age_group:
                    age_group = line.product_id.age_group
                    if age_group not in distribution:
                        distribution[age_group] = 0
                    distribution[age_group] += line.product_uom_qty
            delivery.age_group_distribution = str(distribution)
    
    @api.depends('delivery_line', 'delivery_line.product_id', 'delivery_line.product_id.gender')
    def _compute_gender_distribution(self):
        for delivery in self:
            distribution = {}
            for line in delivery.delivery_line:
                if line.product_id and line.product_id.gender:
                    gender = line.product_id.gender
                    if gender not in distribution:
                        distribution[gender] = 0
                    distribution[gender] += line.product_uom_qty
            delivery.gender_distribution = str(distribution)
    
    @api.depends('delivery_line', 'delivery_line.product_id', 'delivery_line.product_id.season')
    def _compute_season_distribution(self):
        for delivery in self:
            distribution = {}
            for line in delivery.delivery_line:
                if line.product_id and line.product_id.season:
                    season = line.product_id.season
                    if season not in distribution:
                        distribution[season] = 0
                    distribution[season] += line.product_uom_qty
            delivery.season_distribution = str(distribution)
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.delivery') or _('New')
        return super().create(vals)
    
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
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Order',
            'res_model': 'sale.order',
            'view_mode': 'form',
            'res_id': self.order_id.id,
        }
    
    def action_view_analytics(self):
        """View analytics for this delivery"""
        action = self.env.ref('sales.action_sale_analytics').read()[0]
        action['domain'] = [('delivery_id', '=', self.id)]
        return action


class SaleDeliveryLine(models.Model):
    _name = 'sale.delivery.line'
    _description = 'Sales Delivery Line'
    _order = 'delivery_id, sequence, id'
    _rec_name = 'display_name'

    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True,
        help="Display name for this delivery line"
    )
    
    # Delivery Reference
    delivery_id = fields.Many2one(
        'sale.delivery',
        string='Delivery Reference',
        required=True,
        ondelete='cascade',
        help="Sales delivery this line belongs to"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of lines in the delivery"
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
    
    # Quantity
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
    
    # Delivery Status
    delivered_qty = fields.Float(
        string='Delivered Quantity',
        default=0.0,
        help="Quantity delivered"
    )
    
    remaining_qty = fields.Float(
        string='Remaining Quantity',
        compute='_compute_remaining_qty',
        help="Remaining quantity to deliver"
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
    
    @api.depends('product_uom_qty', 'delivered_qty')
    def _compute_remaining_qty(self):
        for line in self:
            line.remaining_qty = line.product_uom_qty - line.delivered_qty
    
    @api.depends('product_id', 'product_id.age_group')
    def _compute_is_kids_item(self):
        for line in self:
            line.is_kids_item = line.product_id and line.product_id.age_group != 'all'