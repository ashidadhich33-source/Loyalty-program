# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Stock Picking
=================================

Stock picking management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField, Many2ManyField
from core_framework.orm import Field
from typing import Dict, Any, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class StockPicking(BaseModel):
    """Stock picking for inventory transfers"""
    
    _name = 'stock.picking'
    _description = 'Stock Picking'
    _table = 'stock_picking'
    
    # Basic Information
    name = CharField(
        string='Reference',
        size=100,
        required=True,
        help='Reference of the picking'
    )
    
    # Picking Type
    picking_type_id = Many2OneField(
        'stock.picking.type',
        string='Operation Type',
        required=True,
        help='Type of picking operation'
    )
    
    # Location Information
    location_id = Many2OneField(
        'stock.location',
        string='Source Location',
        required=True,
        help='Source location'
    )
    
    location_dest_id = Many2OneField(
        'stock.location',
        string='Destination Location',
        required=True,
        help='Destination location'
    )
    
    # Picking State
    state = SelectionField(
        string='State',
        selection=[
            ('draft', 'Draft'),
            ('waiting', 'Waiting Another Operation'),
            ('confirmed', 'Waiting'),
            ('assigned', 'Ready'),
            ('done', 'Done'),
            ('cancel', 'Cancelled')
        ],
        default='draft',
        help='Current state of the picking'
    )
    
    # Move Lines
    move_lines = One2ManyField(
        'stock.move',
        string='Stock Moves',
        inverse_name='picking_id',
        help='Stock moves for this picking'
    )
    
    # Origin Information
    origin = CharField(
        string='Source Document',
        size=200,
        help='Source document reference'
    )
    
    # Partner Information
    partner_id = Many2OneField(
        'res.partner',
        string='Contact',
        help='Contact for this picking'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        required=True,
        help='Company this picking belongs to'
    )
    
    # Date Information
    scheduled_date = DateTimeField(
        string='Scheduled Date',
        help='Scheduled date for the picking'
    )
    
    date_done = DateTimeField(
        string='Date Done',
        help='Date when picking was completed'
    )
    
    # Priority
    priority = SelectionField(
        string='Priority',
        selection=[
            ('0', 'Normal'),
            ('1', 'High'),
            ('2', 'Very High')
        ],
        default='0',
        help='Priority of the picking'
    )
    
    # Kids Clothing Specific
    customer_age = IntegerField(
        string='Customer Age',
        help='Age of the customer'
    )
    
    # Notes
    note = TextField(
        string='Notes',
        help='Additional notes about this picking'
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
            vals['name'] = self._generate_picking_name()
        
        if 'company_id' not in vals:
            vals['company_id'] = self.env.user.company_id.id
        
        return super().create(vals)
    
    def write(self, vals):
        """Override write to update state"""
        result = super().write(vals)
        
        # Update state when moves change
        if 'move_lines' in vals:
            self._update_state()
        
        return result
    
    def _generate_picking_name(self):
        """Generate unique picking name"""
        return f"PICK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    def _update_state(self):
        """Update picking state based on moves"""
        for picking in self:
            if not picking.move_lines:
                picking.state = 'draft'
                continue
            
            move_states = [move.state for move in picking.move_lines]
            
            if all(state == 'done' for state in move_states):
                picking.state = 'done'
                if not picking.date_done:
                    picking.date_done = datetime.now()
            elif any(state == 'assigned' for state in move_states):
                picking.state = 'assigned'
            elif any(state == 'confirmed' for state in move_states):
                picking.state = 'confirmed'
            elif any(state == 'waiting' for state in move_states):
                picking.state = 'waiting'
            else:
                picking.state = 'draft'
    
    def action_confirm(self):
        """Confirm the picking"""
        if self.state != 'draft':
            raise ValueError("Only draft pickings can be confirmed")
        
        # Confirm all moves
        for move in self.move_lines:
            move.action_confirm()
        
        self.state = 'confirmed'
        return True
    
    def action_assign(self):
        """Assign the picking"""
        if self.state not in ['confirmed', 'waiting']:
            raise ValueError("Picking must be confirmed or waiting to be assigned")
        
        # Assign all moves
        for move in self.move_lines:
            move.action_assign()
        
        self.state = 'assigned'
        return True
    
    def action_done(self):
        """Mark picking as done"""
        if self.state != 'assigned':
            raise ValueError("Picking must be assigned to be done")
        
        # Complete all moves
        for move in self.move_lines:
            move.action_done()
        
        self.state = 'done'
        self.date_done = datetime.now()
        return True
    
    def action_cancel(self):
        """Cancel the picking"""
        if self.state == 'done':
            raise ValueError("Cannot cancel completed pickings")
        
        # Cancel all moves
        for move in self.move_lines:
            move.action_cancel()
        
        self.state = 'cancel'
        return True
    
    def action_view_moves(self):
        """View moves for this picking"""
        return {
            'type': 'ir.actions.act_window',
            'name': f'Moves - {self.name}',
            'res_model': 'stock.move',
            'view_mode': 'tree,form',
            'domain': [('picking_id', '=', self.id)],
            'context': {'default_picking_id': self.id}
        }
    
    def get_picking_summary(self):
        """Get picking summary data"""
        return {
            'picking_name': self.name,
            'picking_type': self.picking_type_id.name if self.picking_type_id else 'None',
            'source_location': self.location_id.name,
            'destination_location': self.location_dest_id.name,
            'state': self.state,
            'move_count': len(self.move_lines),
            'origin': self.origin,
            'contact': self.partner_id.name if self.partner_id else 'None',
            'scheduled_date': self.scheduled_date,
            'date_done': self.date_done,
            'priority': self.priority,
            'customer_age': self.customer_age,
            'company': self.company_id.name
        }