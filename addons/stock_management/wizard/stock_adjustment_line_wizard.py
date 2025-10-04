# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class StockAdjustmentLineWizard(models.TransientModel):
    _name = 'stock.adjustment.line.wizard'
    _description = 'Stock Adjustment Line Wizard'

    adjustment_id = fields.Many2one(
        'stock.adjustment',
        string='Adjustment',
        required=True,
        help='Stock adjustment this line belongs to'
    )
    
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        required=True,
        help='Product to adjust'
    )
    
    theoretical_qty = fields.Float(
        string='Theoretical Quantity',
        digits='Product Unit of Measure',
        readonly=True,
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
        help='Difference between counted and theoretical quantity'
    )
    
    unit_cost = fields.Float(
        string='Unit Cost',
        digits='Product Price',
        readonly=True,
        help='Unit cost of the product'
    )
    
    value_adjusted = fields.Float(
        string='Value Adjusted',
        digits='Product Price',
        compute='_compute_value_adjusted',
        help='Value of the adjustment'
    )
    
    lot_id = fields.Many2one(
        'stock.production.lot',
        string='Lot/Serial Number',
        help='Lot or serial number if applicable'
    )
    
    notes = fields.Text(
        string='Notes',
        help='Additional notes for this line'
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
            
            # Get theoretical quantity
            if self.adjustment_id.location_id:
                self.theoretical_qty = self.env['stock.quant']._get_available_quantity(
                    self.product_id, self.adjustment_id.location_id
                )
    
    def action_add_line(self):
        """Add the line to the adjustment"""
        self.ensure_one()
        
        if not self.product_id:
            raise UserError(_('Please select a product.'))
        
        if not self.counted_qty:
            raise UserError(_('Please enter the counted quantity.'))
        
        # Create adjustment line
        line_vals = {
            'adjustment_id': self.adjustment_id.id,
            'product_id': self.product_id.id,
            'theoretical_qty': self.theoretical_qty,
            'counted_qty': self.counted_qty,
            'unit_cost': self.unit_cost,
            'lot_id': self.lot_id.id if self.lot_id else False,
            'notes': self.notes,
        }
        
        self.env['stock.adjustment.line'].create(line_vals)
        
        return {
            'type': 'ir.actions.act_window_close',
        }