# -*- coding: utf-8 -*-

from ocean import models, fields, api, _
from ocean.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class AccountInvoiceLine(models.Model):
    _name = 'account.invoice.line'
    _description = 'Invoice Line'
    _order = 'invoice_id, sequence, id'

    # Basic Information
    name = fields.Text(
        string='Description',
        required=True
    )
    sequence = fields.Integer(
        string='Sequence',
        default=10
    )
    
    # Invoice Reference
    invoice_id = fields.Many2one(
        'account.invoice',
        string='Invoice',
        required=True,
        ondelete='cascade',
        index=True
    )
    
    # Product Information
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        domain=[('sale_ok', '=', True)]
    )
    product_template_id = fields.Many2one(
        'product.template',
        string='Product Template',
        related='product_id.product_tmpl_id',
        store=True
    )
    
    # Quantity and Pricing
    quantity = fields.Float(
        string='Quantity',
        digits='Product Unit of Measure',
        required=True,
        default=1.0
    )
    uom_id = fields.Many2one(
        'uom.uom',
        string='Unit of Measure',
        required=True
    )
    price_unit = fields.Float(
        string='Unit Price',
        required=True,
        digits='Product Price'
    )
    price_subtotal = fields.Monetary(
        string='Subtotal',
        store=True,
        readonly=True,
        compute='_compute_price_subtotal'
    )
    price_total = fields.Monetary(
        string='Total',
        store=True,
        readonly=True,
        compute='_compute_price_total'
    )
    
    # Tax Information
    tax_ids = fields.Many2many(
        'account.tax',
        'account_invoice_line_tax_rel',
        'invoice_line_id',
        'tax_id',
        string='Taxes'
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='invoice_id.currency_id',
        store=True
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('baby', 'Baby (0-2 years)'),
        ('toddler', 'Toddler (2-5 years)'),
        ('kids', 'Kids (5-12 years)'),
        ('teen', 'Teen (12-16 years)'),
    ], string='Age Group', help='Age group for this product')
    
    size = fields.Char(
        string='Size',
        help='Size of the clothing item'
    )
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for this product')
    
    brand = fields.Char(
        string='Brand',
        help='Brand of the product'
    )
    
    color = fields.Char(
        string='Color',
        help='Color of the product'
    )
    
    gender = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('unisex', 'Unisex'),
    ], string='Gender', help='Gender for this product')
    
    special_occasion = fields.Selection([
        ('birthday', 'Birthday'),
        ('festival', 'Festival'),
        ('wedding', 'Wedding'),
        ('school', 'School'),
        ('casual', 'Casual'),
        ('formal', 'Formal'),
    ], string='Special Occasion', help='Special occasion for this product')
    
    # Additional Fields
    discount = fields.Float(
        string='Discount (%)',
        digits='Discount',
        default=0.0
    )
    discount_amount = fields.Monetary(
        string='Discount Amount',
        store=True,
        readonly=True,
        compute='_compute_discount_amount'
    )
    
    @api.depends('quantity', 'price_unit', 'discount')
    def _compute_price_subtotal(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            line.price_subtotal = line.quantity * price
    
    @api.depends('price_subtotal', 'tax_ids')
    def _compute_price_total(self):
        for line in self:
            tax_amount = sum(tax.amount for tax in line.tax_ids)
            line.price_total = line.price_subtotal * (1 + tax_amount / 100.0)
    
    @api.depends('quantity', 'price_unit', 'discount')
    def _compute_discount_amount(self):
        for line in self:
            line.discount_amount = line.quantity * line.price_unit * (line.discount or 0.0) / 100.0
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.uom_id = self.product_id.uom_id
            self.price_unit = self.product_id.list_price
            
            # Set kids clothing specific fields
            if hasattr(self.product_id, 'age_group'):
                self.age_group = self.product_id.age_group
            if hasattr(self.product_id, 'size'):
                self.size = self.product_id.size
            if hasattr(self.product_id, 'season'):
                self.season = self.product_id.season
            if hasattr(self.product_id, 'brand'):
                self.brand = self.product_id.brand
            if hasattr(self.product_id, 'color'):
                self.color = self.product_id.color
            if hasattr(self.product_id, 'gender'):
                self.gender = self.product_id.gender
            if hasattr(self.product_id, 'special_occasion'):
                self.special_occasion = self.product_id.special_occasion
    
    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        if self.uom_id and self.product_id:
            if self.uom_id != self.product_id.uom_id:
                self.price_unit = self.product_id.uom_id._compute_price(
                    self.price_unit, self.uom_id
                )
    
    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError(_('Quantity must be greater than 0.'))
    
    @api.constrains('price_unit')
    def _check_price_unit(self):
        for line in self:
            if line.price_unit < 0:
                raise ValidationError(_('Unit price cannot be negative.'))