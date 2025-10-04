# -*- coding: utf-8 -*-
"""
Ocean ERP - Stock Adjustment Model
==================================

Stock adjustment management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class StockAdjustment(BaseModel, KidsClothingMixin):
    """Stock Adjustment Model for Ocean ERP"""
    
    _name = 'stock.adjustment'
    _description = 'Stock Adjustment'
    _order = 'date desc, name desc'
    _rec_name = 'name'

    name = CharField(
        string='Adjustment Number',
        required=True,
        help='Number of the stock adjustment'
    )
    
    date = DateTimeField(
        string='Date',
        required=True,
        help='Date of the adjustment'
    )
    
    adjustment_type = SelectionField(
        selection=[
            ('physical_count', 'Physical Count'),
            ('damage', 'Damage'),
            ('theft', 'Theft'),
            ('expiry', 'Expiry'),
            ('seasonal', 'Seasonal Adjustment'),
            ('size', 'Size Adjustment'),
            ('brand', 'Brand Adjustment'),
            ('color', 'Color Adjustment'),
            ('quality_issue', 'Quality Issue'),
            ('return', 'Return'),
            ('donation', 'Donation'),
            ('disposal', 'Disposal'),
        ],
        string='Adjustment Type',
        required=True,
        help='Type of stock adjustment'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('pending_approval', 'Pending Approval'),
            ('approved', 'Approved'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the adjustment'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        selection=[
            ('0-2', 'Baby (0-2 years)'),
            ('2-4', 'Toddler (2-4 years)'),
            ('4-6', 'Pre-school (4-6 years)'),
            ('6-8', 'Early School (6-8 years)'),
            ('8-10', 'Middle School (8-10 years)'),
            ('10-12', 'Late School (10-12 years)'),
            ('12-14', 'Teen (12-14 years)'),
            ('14-16', 'Young Adult (14-16 years)'),
            ('all', 'All Age Groups'),
        ],
        string='Age Group',
        help='Age group for the adjustment'
    )
    
    size = SelectionField(
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('xxxl', 'XXXL'),
            ('all', 'All Sizes'),
        ],
        string='Size',
        help='Size for the adjustment'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for the adjustment'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for the adjustment'
    )
    
    color = CharField(
        string='Color',
        help='Color for the adjustment'
    )
    
    # Adjustment Lines
    line_ids = One2ManyField(
        'stock.adjustment.line',
        'adjustment_id',
        string='Adjustment Lines',
        help='Lines for this adjustment'
    )
    
    # Location and Warehouse
    location_id = Many2OneField(
        'stock.location',
        string='Location',
        required=True,
        help='Stock location for this adjustment'
    )
    
    warehouse_id = Many2OneField(
        'stock.warehouse',
        string='Warehouse',
        help='Warehouse for this adjustment'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this adjustment belongs to'
    )
    
    # Approval
    require_approval = BooleanField(
        string='Require Approval',
        default=True,
        help='Require approval for this adjustment'
    )
    
    approved_by = Many2OneField(
        'res.users',
        string='Approved By',
        help='User who approved this adjustment'
    )
    
    approved_date = DateTimeField(
        string='Approved Date',
        help='Date when this adjustment was approved'
    )
    
    # Amounts
    total_amount = FloatField(
        string='Total Amount',
        compute='_compute_amounts',
        help='Total amount of the adjustment'
    )
    
    total_quantity = FloatField(
        string='Total Quantity',
        compute='_compute_amounts',
        help='Total quantity of the adjustment'
    )
    
    # Notes
    notes = TextField(
        string='Notes',
        help='Notes for this adjustment'
    )
    
    # Reason
    reason = CharField(
        string='Reason',
        help='Reason for this adjustment'
    )
    
    def _compute_amounts(self):
        """Compute amounts from adjustment lines"""
        for record in self:
            total_amount = sum(record.line_ids.mapped('amount'))
            total_quantity = sum(record.line_ids.mapped('quantity'))
            record.total_amount = total_amount
            record.total_quantity = total_quantity
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            # Generate name from sequence
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.adjustment')
        
        return super(StockAdjustment, self).create(vals)
    
    def action_submit_for_approval(self):
        """Submit for approval"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft adjustments can be submitted for approval.')
            
            if record.require_approval:
                record.write({'state': 'pending_approval'})
            else:
                record.write({'state': 'approved'})
    
    def action_approve(self):
        """Approve the adjustment"""
        for record in self:
            if record.state != 'pending_approval':
                raise UserError('Only pending adjustments can be approved.')
            
            record.write({
                'state': 'approved',
                'approved_by': self.env.context.get('approved_by'),
                'approved_date': self.env.context.get('approved_date'),
            })
    
    def action_done(self):
        """Mark adjustment as done"""
        for record in self:
            if record.state != 'approved':
                raise UserError('Only approved adjustments can be marked as done.')
            
            # Create stock moves
            self._create_stock_moves(record)
            
            record.write({'state': 'done'})
    
    def action_cancel(self):
        """Cancel the adjustment"""
        for record in self:
            if record.state == 'done':
                raise UserError('Done adjustments cannot be cancelled.')
            
            record.write({'state': 'cancelled'})
    
    def _create_stock_moves(self, record):
        """Create stock moves for adjustment lines"""
        for line in record.line_ids:
            # Create stock move
            move_vals = {
                'name': f"ADJ-{record.name}-{line.product_id.name}",
                'product_id': line.product_id.id,
                'product_uom_qty': abs(line.quantity),
                'product_uom': line.product_id.uom_id.id,
                'location_id': record.location_id.id,
                'location_dest_id': record.location_id.id,
                'date': record.date,
                'company_id': record.company_id.id,
                'age_group': line.age_group,
                'size': line.size,
                'season': line.season,
                'brand': line.brand,
                'color': line.color,
            }
            
            if line.quantity > 0:
                # Positive adjustment - increase stock
                move_vals['location_id'] = self.env.ref('stock.location_inventory').id
                move_vals['location_dest_id'] = record.location_id.id
            else:
                # Negative adjustment - decrease stock
                move_vals['location_id'] = record.location_id.id
                move_vals['location_dest_id'] = self.env.ref('stock.location_inventory').id
            
            self.env['stock.move'].create(move_vals)
    
    def action_view_lines(self):
        """View adjustment lines"""
        return {
            'type': 'ocean.actions.act_window',
            'name': 'Adjustment Lines',
            'res_model': 'stock.adjustment.line',
            'view_mode': 'tree,form',
            'domain': [('adjustment_id', '=', self.id)],
            'context': {'default_adjustment_id': self.id},
        }
    
    def get_kids_clothing_adjustments(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get adjustments filtered by kids clothing criteria"""
        domain = [('state', '=', 'done')]
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if size:
            domain.append(('size', 'in', [size, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)


class StockAdjustmentLine(BaseModel, KidsClothingMixin):
    """Stock Adjustment Line Model for Ocean ERP"""
    
    _name = 'stock.adjustment.line'
    _description = 'Stock Adjustment Line'
    _order = 'adjustment_id, sequence, id'

    adjustment_id = Many2OneField(
        'stock.adjustment',
        string='Adjustment',
        required=True,
        help='Adjustment this line belongs to'
    )
    
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    product_id = Many2OneField(
        'product.product',
        string='Product',
        required=True,
        help='Product for this line'
    )
    
    product_template_id = Many2OneField(
        'product.template',
        string='Product Template',
        help='Product template for this line'
    )
    
    quantity = FloatField(
        string='Quantity',
        required=True,
        help='Quantity to adjust (positive for increase, negative for decrease)'
    )
    
    theoretical_quantity = FloatField(
        string='Theoretical Quantity',
        help='Theoretical quantity in stock'
    )
    
    actual_quantity = FloatField(
        string='Actual Quantity',
        help='Actual quantity counted'
    )
    
    # Kids Clothing Specific Fields
    age_group = SelectionField(
        selection=[
            ('0-2', 'Baby (0-2 years)'),
            ('2-4', 'Toddler (2-4 years)'),
            ('4-6', 'Pre-school (4-6 years)'),
            ('6-8', 'Early School (6-8 years)'),
            ('8-10', 'Middle School (8-10 years)'),
            ('10-12', 'Late School (10-12 years)'),
            ('12-14', 'Teen (12-14 years)'),
            ('14-16', 'Young Adult (14-16 years)'),
            ('all', 'All Age Groups'),
        ],
        string='Age Group',
        help='Age group for this line'
    )
    
    size = SelectionField(
        selection=[
            ('xs', 'XS'),
            ('s', 'S'),
            ('m', 'M'),
            ('l', 'L'),
            ('xl', 'XL'),
            ('xxl', 'XXL'),
            ('xxxl', 'XXXL'),
            ('all', 'All Sizes'),
        ],
        string='Size',
        help='Size for this line'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this line'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this line'
    )
    
    color = CharField(
        string='Color',
        help='Color for this line'
    )
    
    # Unit of Measure
    product_uom_id = Many2OneField(
        'product.uom',
        string='Unit of Measure',
        help='Unit of measure for this line'
    )
    
    # Cost
    unit_cost = FloatField(
        string='Unit Cost',
        help='Unit cost of the product'
    )
    
    amount = FloatField(
        string='Amount',
        compute='_compute_amount',
        help='Amount of this line'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this line belongs to'
    )
    
    def _compute_amount(self):
        """Compute amount from quantity and unit cost"""
        for record in self:
            record.amount = record.quantity * record.unit_cost
    
    def get_kids_clothing_lines(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get lines filtered by kids clothing criteria"""
        domain = []
        
        if age_group:
            domain.append(('age_group', 'in', [age_group, 'all']))
        
        if size:
            domain.append(('size', 'in', [size, 'all']))
        
        if season:
            domain.append(('season', 'in', [season, 'all_season']))
        
        if brand:
            domain.append(('brand', '=', brand))
        
        if color:
            domain.append(('color', '=', color))
        
        return self.search(domain)