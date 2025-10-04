# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)


class StockAdjustment(models.Model):
    _name = 'stock.adjustment'
    _description = 'Stock Adjustment'
    _order = 'date desc, id desc'
    _rec_name = 'name'

    name = fields.Char(
        string='Adjustment Reference',
        required=True,
        copy=False,
        readonly=True,
        default=lambda self: _('New'),
        help='Reference of the stock adjustment'
    )
    
    date = fields.Datetime(
        string='Date',
        required=True,
        default=fields.Datetime.now,
        help='Date of the stock adjustment'
    )
    
    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string='Warehouse',
        required=True,
        help='Warehouse where the adjustment is made'
    )
    
    location_id = fields.Many2one(
        'stock.location',
        string='Location',
        required=True,
        help='Location where the adjustment is made'
    )
    
    adjustment_type = fields.Selection([
        ('physical_count', 'Physical Count'),
        ('cycle_count', 'Cycle Count'),
        ('damage', 'Damage'),
        ('theft', 'Theft'),
        ('expiry', 'Expiry'),
        ('seasonal', 'Seasonal Adjustment'),
        ('size_adjustment', 'Size Adjustment'),
        ('brand_adjustment', 'Brand Adjustment'),
        ('color_adjustment', 'Color Adjustment'),
        ('quality_issue', 'Quality Issue'),
        ('return', 'Return'),
        ('donation', 'Donation'),
        ('disposal', 'Disposal'),
        ('other', 'Other'),
    ], string='Adjustment Type', required=True, help='Type of stock adjustment')
    
    reason = fields.Text(
        string='Reason',
        required=True,
        help='Reason for the stock adjustment'
    )
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='State', default='draft', required=True, help='State of the adjustment')
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-16', 'Young Adult (14-16 years)'),
    ], string='Age Group', help='Age group for the adjustment')
    
    season = fields.Selection([
        ('summer', 'Summer'),
        ('winter', 'Monsoon'),
        ('monsoon', 'Monsoon'),
        ('all_season', 'All Season'),
    ], string='Season', help='Season for the adjustment')
    
    brand = fields.Char(
        string='Brand',
        help='Brand for the adjustment'
    )
    
    color = fields.Char(
        string='Color',
        help='Color for the adjustment'
    )
    
    # Adjustment Lines
    adjustment_line_ids = fields.One2many(
        'stock.adjustment.line',
        'adjustment_id',
        string='Adjustment Lines',
        help='Lines of the stock adjustment'
    )
    
    # Approval Fields
    require_approval = fields.Boolean(
        string='Require Approval',
        default=True,
        help='Whether this adjustment requires approval'
    )
    
    approver_id = fields.Many2one(
        'res.users',
        string='Approver',
        help='User who approved the adjustment'
    )
    
    approval_date = fields.Datetime(
        string='Approval Date',
        readonly=True,
        help='Date when the adjustment was approved'
    )
    
    approval_notes = fields.Text(
        string='Approval Notes',
        help='Notes from the approver'
    )
    
    # Impact Analysis
    total_quantity_adjusted = fields.Float(
        string='Total Quantity Adjusted',
        compute='_compute_total_quantity_adjusted',
        help='Total quantity adjusted across all lines'
    )
    
    total_value_adjusted = fields.Float(
        string='Total Value Adjusted',
        compute='_compute_total_value_adjusted',
        digits='Product Price',
        help='Total value adjusted across all lines'
    )
    
    impact_on_inventory = fields.Selection([
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ], string='Impact on Inventory', compute='_compute_impact_on_inventory', help='Overall impact on inventory')
    
    # Timestamps
    create_date = fields.Datetime(
        string='Created On',
        readonly=True,
        help='Date when the adjustment was created'
    )
    
    confirm_date = fields.Datetime(
        string='Confirmed On',
        readonly=True,
        help='Date when the adjustment was confirmed'
    )
    
    done_date = fields.Datetime(
        string='Done On',
        readonly=True,
        help='Date when the adjustment was completed'
    )
    
    created_by = fields.Many2one(
        'res.users',
        string='Created By',
        default=lambda self: self.env.user,
        readonly=True,
        help='User who created the adjustment'
    )
    
    confirmed_by = fields.Many2one(
        'res.users',
        string='Confirmed By',
        readonly=True,
        help='User who confirmed the adjustment'
    )
    
    done_by = fields.Many2one(
        'res.users',
        string='Done By',
        readonly=True,
        help='User who completed the adjustment'
    )
    
    @api.depends('adjustment_line_ids.quantity_adjusted')
    def _compute_total_quantity_adjusted(self):
        for record in self:
            record.total_quantity_adjusted = sum(line.quantity_adjusted for line in record.adjustment_line_ids)
    
    @api.depends('adjustment_line_ids.value_adjusted')
    def _compute_total_value_adjusted(self):
        for record in self:
            record.total_value_adjusted = sum(line.value_adjusted for line in record.adjustment_line_ids)
    
    @api.depends('total_quantity_adjusted')
    def _compute_impact_on_inventory(self):
        for record in self:
            if record.total_quantity_adjusted > 0:
                record.impact_on_inventory = 'positive'
            elif record.total_quantity_adjusted < 0:
                record.impact_on_inventory = 'negative'
            else:
                record.impact_on_inventory = 'neutral'
    
    @api.model
    def create(self, vals):
        """Override create to generate sequence"""
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.adjustment') or _('New')
        return super(StockAdjustment, self).create(vals)
    
    def action_confirm(self):
        """Confirm the stock adjustment"""
        for record in self:
            if record.state == 'draft':
                record.write({
                    'state': 'confirmed',
                    'confirm_date': fields.Datetime.now(),
                    'confirmed_by': self.env.user.id,
                })
    
    def action_approve(self):
        """Approve the stock adjustment"""
        for record in self:
            if record.state == 'confirmed':
                record.write({
                    'state': 'approved',
                    'approval_date': fields.Datetime.now(),
                    'approver_id': self.env.user.id,
                })
    
    def action_done(self):
        """Complete the stock adjustment"""
        for record in self:
            if record.state in ['confirmed', 'approved']:
                # Create stock moves for each adjustment line
                for line in record.adjustment_line_ids:
                    line._create_stock_move()
                
                record.write({
                    'state': 'done',
                    'done_date': fields.Datetime.now(),
                    'done_by': self.env.user.id,
                })
    
    def action_cancel(self):
        """Cancel the stock adjustment"""
        for record in self:
            if record.state in ['draft', 'confirmed']:
                record.write({'state': 'cancelled'})
    
    def action_reset_to_draft(self):
        """Reset to draft state"""
        for record in self:
            if record.state == 'cancelled':
                record.write({'state': 'draft'})
    
    @api.constrains('adjustment_line_ids')
    def _check_adjustment_lines(self):
        for record in self:
            if not record.adjustment_line_ids:
                raise ValidationError(_('At least one adjustment line is required.'))
    
    def action_add_product_line(self):
        """Add a new product line to the adjustment"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Add Product Line'),
            'res_model': 'stock.adjustment.line.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_adjustment_id': self.id},
        }


class StockAdjustmentLine(models.Model):
    _name = 'stock.adjustment.line'
    _description = 'Stock Adjustment Line'
    _order = 'product_id'

    adjustment_id = fields.Many2one(
        'stock.adjustment',
        string='Adjustment',
        required=True,
        ondelete='cascade',
        help='Stock adjustment this line belongs to'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        help='Product to adjust'
    )
    
    product_template_id = fields.Many2one(
        'product.template',
        related='product_id.product_tmpl_id',
        string='Product Template',
        store=True,
        help='Product template'
    )
    
    # Stock Information
    theoretical_qty = fields.Float(
        string='Theoretical Quantity',
        digits='Product Unit of Measure',
        help='Theoretical quantity in stock'
    )
    
    counted_qty = fields.Float(
        string='Counted Quantity',
        digits='Product Unit of Measure',
        required=True,
        help='Actual counted quantity'
    )
    
    quantity_adjusted = fields.Float(
        string='Quantity Adjusted',
        digits='Product Unit of Measure',
        compute='_compute_quantity_adjusted',
        store=True,
        help='Difference between counted and theoretical quantity'
    )
    
    # Value Information
    unit_cost = fields.Float(
        string='Unit Cost',
        digits='Product Price',
        help='Unit cost of the product'
    )
    
    value_adjusted = fields.Float(
        string='Value Adjusted',
        digits='Product Price',
        compute='_compute_value_adjusted',
        store=True,
        help='Value of the adjustment'
    )
    
    # Kids Clothing Specific Fields
    age_group = fields.Selection([
        ('0-2', 'Baby (0-2 years)'),
        ('2-4', 'Toddler (2-4 years)'),
        ('4-6', 'Pre-school (4-6 years)'),
        ('6-8', 'Early School (6-8 years)'),
        ('8-10', 'Middle School (8-10 years)'),
        ('10-12', 'Late School (10-12 years)'),
        ('12-14', 'Teen (12-14 years)'),
        ('14-16', 'Young Adult (14-16 years)'),
    ], string='Age Group', help='Age group for the product')
    
    size = fields.Selection([
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
        ('xxxl', 'XXXL'),
    ], string='Size', help='Size of the product')
    
    brand = fields.Char(
        string='Brand',
        help='Brand of the product'
    )
    
    color = fields.Char(
        string='Color',
        help='Color of the product'
    )
    
    # Additional Information
    lot_id = fields.Many2one(
        'stock.production.lot',
        string='Lot/Serial Number',
        help='Lot or serial number if applicable'
    )
    
    notes = fields.Text(
        string='Notes',
        help='Additional notes for this line'
    )
    
    # Stock Move
    stock_move_id = fields.Many2one(
        'stock.move',
        string='Stock Move',
        readonly=True,
        help='Stock move created for this adjustment'
    )
    
    @api.depends('theoretical_qty', 'counted_qty')
    def _compute_quantity_adjusted(self):
        for record in self:
            record.quantity_adjusted = record.counted_qty - record.theoretical_qty
    
    @api.depends('quantity_adjusted', 'unit_cost')
    def _compute_value_adjusted(self):
        for record in self:
            record.value_adjusted = record.quantity_adjusted * record.unit_cost
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.unit_cost = self.product_id.standard_price
            self.age_group = self.product_id.age_group
            self.size = self.product_id.size
            self.brand = self.product_id.brand
            self.color = self.product_id.color
            
            # Get theoretical quantity
            if self.adjustment_id.location_id:
                self.theoretical_qty = self.env['stock.quant']._get_available_quantity(
                    self.product_id, self.adjustment_id.location_id
                )
    
    def _create_stock_move(self):
        """Create stock move for this adjustment line"""
        if self.quantity_adjusted == 0:
            return
        
        # Determine source and destination locations
        if self.quantity_adjusted > 0:
            # Positive adjustment - stock in
            location_id = self.adjustment_id.location_id.id
            location_dest_id = self.adjustment_id.location_id.id
        else:
            # Negative adjustment - stock out
            location_id = self.adjustment_id.location_id.id
            location_dest_id = self.env.ref('stock.location_scrapped').id
        
        # Create stock move
        move_vals = {
            'name': f"Stock Adjustment: {self.adjustment_id.name}",
            'product_id': self.product_id.id,
            'product_uom_qty': abs(self.quantity_adjusted),
            'product_uom': self.product_id.uom_id.id,
            'location_id': location_id,
            'location_dest_id': location_dest_id,
            'origin': self.adjustment_id.name,
            'state': 'done',
            'quantity_done': abs(self.quantity_adjusted),
        }
        
        stock_move = self.env['stock.move'].create(move_vals)
        self.stock_move_id = stock_move.id
        
        return stock_move