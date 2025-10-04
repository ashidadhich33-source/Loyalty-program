# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Validation Tests
=======================================

Tests for Indian EDI validation functionality.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in_edi.models.edi_document import EdiDocument
import logging

_logger = logging.getLogger(__name__)


class TestEdiValidation(OceanTestCase):
    """Test cases for EDI validation functionality"""
    
    def setUp(self):
        super(TestEdiValidation, self).setUp()
        self.document_model = self.env['edi.document']
    
    def test_document_type_validation(self):
        """Test document type validation"""
        document_types = [
            'invoice',
            'credit_note',
            'debit_note',
            'purchase_order',
            'sales_order',
            'delivery_note',
            'receipt',
            'payment',
            'remittance',
            'other'
        ]
        
        for doc_type in document_types:
            document = self.document_model.create({
                'name': f'Test {doc_type.title()} Document',
                'document_type': doc_type,
                'edi_format': 'edifact'
            })
            self.assertEqual(document.document_type, doc_type)
    
    def test_edi_format_validation(self):
        """Test EDI format validation"""
        edi_formats = [
            'edifact',
            'x12',
            'xml',
            'json',
            'csv',
            'custom'
        ]
        
        for edi_format in edi_formats:
            document = self.document_model.create({
                'name': f'Test {edi_format.upper()} Document',
                'document_type': 'invoice',
                'edi_format': edi_format
            })
            self.assertEqual(document.edi_format, edi_format)
    
    def test_document_workflow(self):
        """Test document workflow"""
        document = self.document_model.create({
            'name': 'Test Invoice Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        
        # Test initial state
        self.assertEqual(document.state, 'draft')
        
        # Test prepare action
        document.action_prepare()
        self.assertEqual(document.state, 'ready')
        self.assertTrue(document.document_data)
        
        # Test send action
        document.action_send()
        self.assertEqual(document.state, 'sent')
        self.assertTrue(document.transmission_id)
        self.assertTrue(document.send_date)
        
        # Test process action
        document.action_process()
        self.assertEqual(document.state, 'processed')
        self.assertTrue(document.processed_data)
        self.assertTrue(document.process_date)
    
    def test_transaction_workflow(self):
        """Test transaction workflow"""
        # Create parent document first
        document = self.document_model.create({
            'name': 'Test Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        
        transaction = self.env['edi.transaction'].create({
            'name': 'Test Line Item',
            'document_id': document.id,
            'transaction_type': 'line_item',
            'segment_type': 'LIN'
        })
        
        self.assertEqual(transaction.document_id.id, document.id)
        self.assertEqual(transaction.transaction_type, 'line_item')
        self.assertEqual(transaction.segment_type, 'LIN')
        self.assertTrue(transaction.active)
    
    def test_message_workflow(self):
        """Test message workflow"""
        message = self.env['edi.message'].create({
            'name': 'Test ORDERS Message',
            'message_type': 'ordrsp',
            'message_format': 'edifact'
        })
        
        # Test initial state
        self.assertEqual(message.state, 'draft')
        
        # Test prepare action
        message.action_prepare()
        self.assertEqual(message.state, 'ready')
        self.assertTrue(message.message_data)
        
        # Test send action
        message.action_send()
        self.assertEqual(message.state, 'sent')
        self.assertTrue(message.transmission_id)
        self.assertTrue(message.send_date)
        
        # Test process action
        message.action_process()
        self.assertEqual(message.state, 'processed')
        self.assertTrue(message.processed_data)
        self.assertTrue(message.process_date)
    
    def test_transmission_workflow(self):
        """Test transmission workflow"""
        transmission = self.env['edi.transmission'].create({
            'name': 'Test FTP Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp',
            'host': 'ftp.example.com',
            'port': 21,
            'state': 'ready'
        })
        
        # Test start action
        transmission.action_start()
        self.assertEqual(transmission.state, 'sending')
        self.assertTrue(transmission.start_date)
        
        # Test complete action
        transmission.action_complete()
        self.assertEqual(transmission.state, 'sent')
        self.assertTrue(transmission.end_date)
        
        # Test process action
        transmission.action_process()
        self.assertEqual(transmission.state, 'processed')
        self.assertTrue(transmission.processed_data)
    
    def test_acknowledgment_workflow(self):
        """Test acknowledgment workflow"""
        # Create parent transmission first
        transmission = self.env['edi.transmission'].create({
            'name': 'Test Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp'
        })
        
        acknowledgment = self.env['edi.acknowledgment'].create({
            'name': 'Test Technical Acknowledgment',
            'transmission_id': transmission.id,
            'acknowledgment_type': 'ta',
            'acknowledgment_code': 'TA001',
            'acknowledgment_message': 'Transmission received successfully'
        })
        
        self.assertEqual(acknowledgment.transmission_id.id, transmission.id)
        self.assertEqual(acknowledgment.acknowledgment_type, 'ta')
        self.assertEqual(acknowledgment.acknowledgment_code, 'TA001')
        self.assertEqual(acknowledgment.state, 'pending')
    
    def test_error_handling(self):
        """Test error handling in workflows"""
        document = self.document_model.create({
            'name': 'Test Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        
        # Test prepare action on non-draft document
        document.state = 'ready'
        with self.assertRaises(UserError):
            document.action_prepare()
        
        # Test send action on non-ready document
        document.state = 'draft'
        with self.assertRaises(UserError):
            document.action_send()
        
        # Test process action on non-sent/received document
        with self.assertRaises(UserError):
            document.action_process()
    
    def test_data_validation(self):
        """Test data validation"""
        # Test required fields
        with self.assertRaises(ValidationError):
            self.document_model.create({
                'name': 'Test Document'
                # Missing required fields
            })
        
        # Test valid document creation
        document = self.document_model.create({
            'name': 'Test Invoice Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        self.assertTrue(document.id)
    
    def test_kids_clothing_integration(self):
        """Test kids clothing integration"""
        document = self.document_model.create({
            'name': 'Kids Clothing Invoice',
            'document_type': 'invoice',
            'edi_format': 'edifact',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue'
        })
        
        self.assertEqual(document.age_group, '4-6')
        self.assertEqual(document.size, 'm')
        self.assertEqual(document.season, 'all_season')
        self.assertEqual(document.brand, 'Kids Brand')
        self.assertEqual(document.color, 'Blue')
        
        # Test filtering by kids clothing criteria
        kids_docs = self.document_model.get_kids_clothing_documents(age_group='4-6')
        self.assertIn(document, kids_docs)
        
        kids_docs = self.document_model.get_kids_clothing_documents(size='m')
        self.assertIn(document, kids_docs)
        
        kids_docs = self.document_model.get_kids_clothing_documents(season='all_season')
        self.assertIn(document, kids_docs)
        
        kids_docs = self.document_model.get_kids_clothing_documents(brand='Kids Brand')
        self.assertIn(document, kids_docs)
        
        kids_docs = self.document_model.get_kids_clothing_documents(color='Blue')
        self.assertIn(document, kids_docs)