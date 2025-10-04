# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Message Model
====================================

EDI message management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class EdiMessage(BaseModel, KidsClothingMixin):
    """Indian EDI Message Model for Ocean ERP"""
    
    _name = 'edi.message'
    _description = 'EDI Message'
    _order = 'create_date desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Message Name',
        required=True,
        help='Name of the EDI message'
    )
    
    # EDI Specific Fields
    message_type = SelectionField(
        selection=[
            ('ordrsp', 'ORDERS Response'),
            ('ordrpt', 'ORDERS Report'),
            ('desadv', 'DESADV'),
            ('invoic', 'INVOIC'),
            ('cremte', 'Credit Note'),
            ('debmte', 'Debit Note'),
            ('remadv', 'REMDV'),
            ('paymul', 'Payment Multiple'),
            ('other', 'Other'),
        ],
        string='Message Type',
        required=True,
        help='Type of EDI message'
    )
    
    message_format = SelectionField(
        selection=[
            ('edifact', 'EDIFACT'),
            ('x12', 'X12'),
            ('xml', 'XML'),
            ('json', 'JSON'),
            ('csv', 'CSV'),
            ('custom', 'Custom'),
        ],
        string='Message Format',
        required=True,
        help='Format of the EDI message'
    )
    
    message_version = CharField(
        string='Message Version',
        help='Version of the EDI message standard'
    )
    
    state = SelectionField(
        selection=[
            ('draft', 'Draft'),
            ('ready', 'Ready'),
            ('sent', 'Sent'),
            ('received', 'Received'),
            ('processed', 'Processed'),
            ('error', 'Error'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        help='Status of the EDI message'
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
        help='Age group for this EDI message'
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
        help='Size for this EDI message'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this EDI message'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this EDI message'
    )
    
    color = CharField(
        string='Color',
        help='Color for this EDI message'
    )
    
    # Message Data
    message_data = TextField(
        string='Message Data',
        help='Raw EDI message data'
    )
    
    processed_data = TextField(
        string='Processed Data',
        help='Processed message data'
    )
    
    # Transmission Information
    transmission_id = CharField(
        string='Transmission ID',
        help='Unique transmission identifier'
    )
    
    sender_id = CharField(
        string='Sender ID',
        help='Sender identifier'
    )
    
    receiver_id = CharField(
        string='Receiver ID',
        help='Receiver identifier'
    )
    
    # Dates
    message_date = DateTimeField(
        string='Message Date',
        help='Date of the message'
    )
    
    send_date = DateTimeField(
        string='Send Date',
        help='Date when message was sent'
    )
    
    receive_date = DateTimeField(
        string='Receive Date',
        help='Date when message was received'
    )
    
    process_date = DateTimeField(
        string='Process Date',
        help='Date when message was processed'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this message belongs to'
    )
    
    # Partner
    partner_id = Many2OneField(
        'res.partner',
        string='Partner',
        help='Partner this message is for'
    )
    
    # Envelopes
    envelope_ids = One2ManyField(
        'edi.envelope',
        'message_id',
        string='Envelopes',
        help='EDI envelopes in this message'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the message'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            msg_type = vals.get('message_type', '')
            msg_date = vals.get('message_date', '')
            vals['name'] = f"{msg_type.upper()} - {msg_date}"
        
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiMessage, self).create(vals)
    
    def action_prepare(self):
        """Prepare the EDI message"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft messages can be prepared.')
            
            # Generate EDI message data
            message_data = self._generate_message_data(record)
            
            record.write({
                'state': 'ready',
                'message_data': message_data,
            })
    
    def action_send(self):
        """Send the EDI message"""
        for record in self:
            if record.state != 'ready':
                raise UserError('Only ready messages can be sent.')
            
            # Send message via EDI
            transmission_id = self._send_via_edi(record)
            
            record.write({
                'state': 'sent',
                'send_date': self.env.context.get('send_date'),
                'transmission_id': transmission_id,
            })
    
    def action_process(self):
        """Process the EDI message"""
        for record in self:
            if record.state not in ['received', 'sent']:
                raise UserError('Only received or sent messages can be processed.')
            
            # Process the message
            processed_data = self._process_message(record)
            
            record.write({
                'state': 'processed',
                'process_date': self.env.context.get('process_date'),
                'processed_data': processed_data,
            })
    
    def _generate_message_data(self, record):
        """Generate EDI message data based on type"""
        # This would generate the actual EDI message data
        return '{}'
    
    def _send_via_edi(self, record):
        """Send message via EDI"""
        # This would integrate with EDI transmission system
        return 'EDI123456789'
    
    def _process_message(self, record):
        """Process the message"""
        # This would process the message data
        return '{}'
    
    def get_kids_clothing_messages(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get messages filtered by kids clothing criteria"""
        domain = [('state', '=', 'processed')]
        
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


class EdiEnvelope(BaseModel, KidsClothingMixin):
    """Indian EDI Envelope Model for Ocean ERP"""
    
    _name = 'edi.envelope'
    _description = 'EDI Envelope'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Envelope Name',
        required=True,
        help='Name of the EDI envelope'
    )
    
    message_id = Many2OneField(
        'edi.message',
        string='Message',
        required=True,
        help='EDI message this envelope belongs to'
    )
    
    # EDI Specific Fields
    envelope_type = SelectionField(
        selection=[
            ('interchange', 'Interchange'),
            ('group', 'Group'),
            ('message', 'Message'),
            ('segment', 'Segment'),
            ('element', 'Element'),
            ('other', 'Other'),
        ],
        string='Envelope Type',
        required=True,
        help='Type of EDI envelope'
    )
    
    envelope_data = TextField(
        string='Envelope Data',
        help='Raw envelope data'
    )
    
    processed_data = TextField(
        string='Processed Data',
        help='Processed envelope data'
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
        help='Age group for this envelope'
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
        help='Size for this envelope'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this envelope'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this envelope'
    )
    
    color = CharField(
        string='Color',
        help='Color for this envelope'
    )
    
    # Envelope Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the envelope is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this envelope belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the envelope'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiEnvelope, self).create(vals)
    
    def get_kids_clothing_envelopes(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get envelopes filtered by kids clothing criteria"""
        domain = [('active', '=', True)]
        
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