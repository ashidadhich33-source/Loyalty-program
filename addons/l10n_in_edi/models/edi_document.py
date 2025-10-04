# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Document Model
=====================================

EDI document management for kids clothing retail.
"""

from core_framework.orm import BaseModel, CharField, TextField, BooleanField, IntegerField, DateTimeField, Many2OneField, SelectionField, FloatField, One2ManyField
from core_framework.exceptions import ValidationError, UserError
from addons.core_base.models.base_mixins import KidsClothingMixin
import logging

_logger = logging.getLogger(__name__)


class EdiDocument(BaseModel, KidsClothingMixin):
    """Indian EDI Document Model for Ocean ERP"""
    
    _name = 'edi.document'
    _description = 'EDI Document'
    _order = 'create_date desc, name'
    _rec_name = 'name'

    name = CharField(
        string='Document Name',
        required=True,
        help='Name of the EDI document'
    )
    
    # EDI Specific Fields
    document_type = SelectionField(
        selection=[
            ('invoice', 'Invoice'),
            ('credit_note', 'Credit Note'),
            ('debit_note', 'Debit Note'),
            ('purchase_order', 'Purchase Order'),
            ('sales_order', 'Sales Order'),
            ('delivery_note', 'Delivery Note'),
            ('receipt', 'Receipt'),
            ('payment', 'Payment'),
            ('remittance', 'Remittance'),
            ('other', 'Other'),
        ],
        string='Document Type',
        required=True,
        help='Type of EDI document'
    )
    
    edi_format = SelectionField(
        selection=[
            ('edifact', 'EDIFACT'),
            ('x12', 'X12'),
            ('xml', 'XML'),
            ('json', 'JSON'),
            ('csv', 'CSV'),
            ('custom', 'Custom'),
        ],
        string='EDI Format',
        required=True,
        help='Format of the EDI document'
    )
    
    edi_version = CharField(
        string='EDI Version',
        help='Version of the EDI standard'
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
        help='Status of the EDI document'
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
        help='Age group for this EDI document'
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
        help='Size for this EDI document'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this EDI document'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this EDI document'
    )
    
    color = CharField(
        string='Color',
        help='Color for this EDI document'
    )
    
    # Document Data
    document_data = TextField(
        string='Document Data',
        help='Raw EDI document data'
    )
    
    processed_data = TextField(
        string='Processed Data',
        help='Processed document data'
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
    document_date = DateTimeField(
        string='Document Date',
        help='Date of the document'
    )
    
    send_date = DateTimeField(
        string='Send Date',
        help='Date when document was sent'
    )
    
    receive_date = DateTimeField(
        string='Receive Date',
        help='Date when document was received'
    )
    
    process_date = DateTimeField(
        string='Process Date',
        help='Date when document was processed'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this document belongs to'
    )
    
    # Partner
    partner_id = Many2OneField(
        'res.partner',
        string='Partner',
        help='Partner this document is for'
    )
    
    # Transactions
    transaction_ids = One2ManyField(
        'edi.transaction',
        'document_id',
        string='Transactions',
        help='EDI transactions in this document'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the document'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('name'):
            doc_type = vals.get('document_type', '')
            doc_date = vals.get('document_date', '')
            vals['name'] = f"{doc_type.replace('_', ' ').title()} - {doc_date}"
        
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiDocument, self).create(vals)
    
    def action_prepare(self):
        """Prepare the EDI document"""
        for record in self:
            if record.state != 'draft':
                raise UserError('Only draft documents can be prepared.')
            
            # Generate EDI data
            edi_data = self._generate_edi_data(record)
            
            record.write({
                'state': 'ready',
                'document_data': edi_data,
            })
    
    def action_send(self):
        """Send the EDI document"""
        for record in self:
            if record.state != 'ready':
                raise UserError('Only ready documents can be sent.')
            
            # Send document via EDI
            transmission_id = self._send_via_edi(record)
            
            record.write({
                'state': 'sent',
                'send_date': self.env.context.get('send_date'),
                'transmission_id': transmission_id,
            })
    
    def action_process(self):
        """Process the EDI document"""
        for record in self:
            if record.state not in ['received', 'sent']:
                raise UserError('Only received or sent documents can be processed.')
            
            # Process the document
            processed_data = self._process_document(record)
            
            record.write({
                'state': 'processed',
                'process_date': self.env.context.get('process_date'),
                'processed_data': processed_data,
            })
    
    def _generate_edi_data(self, record):
        """Generate EDI data based on document type"""
        # This would generate the actual EDI data
        return '{}'
    
    def _send_via_edi(self, record):
        """Send document via EDI"""
        # This would integrate with EDI transmission system
        return 'EDI123456789'
    
    def _process_document(self, record):
        """Process the document"""
        # This would process the document data
        return '{}'
    
    def get_kids_clothing_documents(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get documents filtered by kids clothing criteria"""
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


class EdiTransaction(BaseModel, KidsClothingMixin):
    """Indian EDI Transaction Model for Ocean ERP"""
    
    _name = 'edi.transaction'
    _description = 'EDI Transaction'
    _order = 'sequence, name'
    _rec_name = 'name'

    name = CharField(
        string='Transaction Name',
        required=True,
        help='Name of the EDI transaction'
    )
    
    document_id = Many2OneField(
        'edi.document',
        string='Document',
        required=True,
        help='EDI document this transaction belongs to'
    )
    
    # EDI Specific Fields
    transaction_type = SelectionField(
        selection=[
            ('line_item', 'Line Item'),
            ('header', 'Header'),
            ('footer', 'Footer'),
            ('summary', 'Summary'),
            ('detail', 'Detail'),
            ('other', 'Other'),
        ],
        string='Transaction Type',
        required=True,
        help='Type of EDI transaction'
    )
    
    segment_type = CharField(
        string='Segment Type',
        help='EDI segment type'
    )
    
    segment_data = TextField(
        string='Segment Data',
        help='Raw segment data'
    )
    
    processed_data = TextField(
        string='Processed Data',
        help='Processed segment data'
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
        help='Age group for this transaction'
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
        help='Size for this transaction'
    )
    
    season = SelectionField(
        selection=[
            ('summer', 'Summer'),
            ('winter', 'Winter'),
            ('monsoon', 'Monsoon'),
            ('all_season', 'All Season'),
        ],
        string='Season',
        help='Season for this transaction'
    )
    
    brand = CharField(
        string='Brand',
        help='Brand for this transaction'
    )
    
    color = CharField(
        string='Color',
        help='Color for this transaction'
    )
    
    # Transaction Configuration
    sequence = IntegerField(
        string='Sequence',
        default=10,
        help='Sequence for ordering'
    )
    
    active = BooleanField(
        string='Active',
        default=True,
        help='Whether the transaction is active'
    )
    
    # Company
    company_id = Many2OneField(
        'res.company',
        string='Company',
        help='Company this transaction belongs to'
    )
    
    # Additional Information
    notes = TextField(
        string='Notes',
        help='Additional notes for the transaction'
    )
    
    def create(self, vals):
        """Override create to set default values"""
        if not vals.get('company_id'):
            vals['company_id'] = self.env.context.get('default_company_id')
        
        return super(EdiTransaction, self).create(vals)
    
    def get_kids_clothing_transactions(self, age_group=None, size=None, season=None, brand=None, color=None):
        """Get transactions filtered by kids clothing criteria"""
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