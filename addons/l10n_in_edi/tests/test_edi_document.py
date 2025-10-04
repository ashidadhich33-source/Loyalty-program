# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Document Tests
=====================================

Tests for Indian EDI document models.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in_edi.models.edi_document import EdiDocument, EdiTransaction
import logging

_logger = logging.getLogger(__name__)


class TestEdiDocument(OceanTestCase):
    """Test cases for EdiDocument model"""
    
    def setUp(self):
        super(TestEdiDocument, self).setUp()
        self.document_model = self.env['edi.document']
        self.transaction_model = self.env['edi.transaction']
    
    def test_create_edi_document(self):
        """Test creating an EDI document"""
        document_vals = {
            'name': 'Test Invoice Document',
            'document_type': 'invoice',
            'edi_format': 'edifact',
            'edi_version': 'D.96A',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        document = self.document_model.create(document_vals)
        
        self.assertEqual(document.name, 'Test Invoice Document')
        self.assertEqual(document.document_type, 'invoice')
        self.assertEqual(document.edi_format, 'edifact')
        self.assertEqual(document.edi_version, 'D.96A')
        self.assertEqual(document.age_group, '4-6')
        self.assertEqual(document.size, 'm')
        self.assertEqual(document.season, 'all_season')
        self.assertEqual(document.brand, 'Kids Brand')
        self.assertEqual(document.color, 'Blue')
        self.assertEqual(document.state, 'draft')
    
    def test_document_types(self):
        """Test different document types"""
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
    
    def test_edi_formats(self):
        """Test different EDI formats"""
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
    
    def test_action_prepare(self):
        """Test preparing EDI document"""
        document = self.document_model.create({
            'name': 'Test Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        
        # Test preparing draft document
        document.action_prepare()
        self.assertEqual(document.state, 'ready')
        self.assertTrue(document.document_data)
        
        # Test preparing non-draft document
        with self.assertRaises(UserError):
            document.action_prepare()
    
    def test_action_send(self):
        """Test sending EDI document"""
        document = self.document_model.create({
            'name': 'Test Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        
        # Prepare document first
        document.action_prepare()
        
        # Test sending ready document
        document.action_send()
        self.assertEqual(document.state, 'sent')
        self.assertTrue(document.transmission_id)
        self.assertTrue(document.send_date)
        
        # Test sending non-ready document
        document.state = 'draft'
        with self.assertRaises(UserError):
            document.action_send()
    
    def test_action_process(self):
        """Test processing EDI document"""
        document = self.document_model.create({
            'name': 'Test Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        
        # Test processing sent document
        document.state = 'sent'
        document.action_process()
        self.assertEqual(document.state, 'processed')
        self.assertTrue(document.processed_data)
        self.assertTrue(document.process_date)
        
        # Test processing received document
        document.state = 'received'
        document.action_process()
        self.assertEqual(document.state, 'processed')
        
        # Test processing non-sent/received document
        document.state = 'draft'
        with self.assertRaises(UserError):
            document.action_process()
    
    def test_get_kids_clothing_documents(self):
        """Test filtering documents by kids clothing criteria"""
        # Create test documents
        doc1 = self.document_model.create({
            'name': 'Baby Invoice',
            'document_type': 'invoice',
            'edi_format': 'edifact',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink',
            'state': 'processed'
        })
        
        doc2 = self.document_model.create({
            'name': 'Toddler Invoice',
            'document_type': 'invoice',
            'edi_format': 'edifact',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue',
            'state': 'processed'
        })
        
        doc3 = self.document_model.create({
            'name': 'All Age Invoice',
            'document_type': 'invoice',
            'edi_format': 'edifact',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green',
            'state': 'processed'
        })
        
        # Test filtering by age group
        baby_docs = self.document_model.get_kids_clothing_documents(age_group='0-2')
        self.assertIn(doc1, baby_docs)
        self.assertNotIn(doc2, baby_docs)
        self.assertIn(doc3, baby_docs)  # 'all' should match
        
        # Test filtering by size
        xs_docs = self.document_model.get_kids_clothing_documents(size='xs')
        self.assertIn(doc1, xs_docs)
        self.assertNotIn(doc2, xs_docs)
        self.assertIn(doc3, xs_docs)  # 'all' should match
        
        # Test filtering by season
        summer_docs = self.document_model.get_kids_clothing_documents(season='summer')
        self.assertIn(doc1, summer_docs)
        self.assertNotIn(doc2, summer_docs)
        self.assertIn(doc3, summer_docs)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_docs = self.document_model.get_kids_clothing_documents(brand='Baby Brand')
        self.assertIn(doc1, baby_brand_docs)
        self.assertNotIn(doc2, baby_brand_docs)
        self.assertNotIn(doc3, baby_brand_docs)
        
        # Test filtering by color
        pink_docs = self.document_model.get_kids_clothing_documents(color='Pink')
        self.assertIn(doc1, pink_docs)
        self.assertNotIn(doc2, pink_docs)
        self.assertNotIn(doc3, pink_docs)


class TestEdiTransaction(OceanTestCase):
    """Test cases for EdiTransaction model"""
    
    def setUp(self):
        super(TestEdiTransaction, self).setUp()
        self.document_model = self.env['edi.document']
        self.transaction_model = self.env['edi.transaction']
    
    def test_create_edi_transaction(self):
        """Test creating an EDI transaction"""
        # Create parent document first
        document = self.document_model.create({
            'name': 'Test Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        
        transaction_vals = {
            'name': 'Test Line Item',
            'document_id': document.id,
            'transaction_type': 'line_item',
            'segment_type': 'LIN',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        transaction = self.transaction_model.create(transaction_vals)
        
        self.assertEqual(transaction.name, 'Test Line Item')
        self.assertEqual(transaction.document_id.id, document.id)
        self.assertEqual(transaction.transaction_type, 'line_item')
        self.assertEqual(transaction.segment_type, 'LIN')
        self.assertEqual(transaction.age_group, '4-6')
        self.assertEqual(transaction.size, 'm')
        self.assertEqual(transaction.season, 'all_season')
        self.assertEqual(transaction.brand, 'Kids Brand')
        self.assertEqual(transaction.color, 'Blue')
        self.assertTrue(transaction.active)
    
    def test_transaction_types(self):
        """Test different transaction types"""
        # Create parent document first
        document = self.document_model.create({
            'name': 'Test Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        
        transaction_types = [
            'line_item',
            'header',
            'footer',
            'summary',
            'detail',
            'other'
        ]
        
        for trans_type in transaction_types:
            transaction = self.transaction_model.create({
                'name': f'Test {trans_type.title()} Transaction',
                'document_id': document.id,
                'transaction_type': trans_type
            })
            self.assertEqual(transaction.transaction_type, trans_type)
    
    def test_get_kids_clothing_transactions(self):
        """Test filtering transactions by kids clothing criteria"""
        # Create parent document first
        document = self.document_model.create({
            'name': 'Test Document',
            'document_type': 'invoice',
            'edi_format': 'edifact'
        })
        
        # Create test transactions
        trans1 = self.transaction_model.create({
            'name': 'Baby Line Item',
            'document_id': document.id,
            'transaction_type': 'line_item',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink'
        })
        
        trans2 = self.transaction_model.create({
            'name': 'Toddler Line Item',
            'document_id': document.id,
            'transaction_type': 'line_item',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue'
        })
        
        trans3 = self.transaction_model.create({
            'name': 'All Age Line Item',
            'document_id': document.id,
            'transaction_type': 'line_item',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green'
        })
        
        # Test filtering by age group
        baby_trans = self.transaction_model.get_kids_clothing_transactions(age_group='0-2')
        self.assertIn(trans1, baby_trans)
        self.assertNotIn(trans2, baby_trans)
        self.assertIn(trans3, baby_trans)  # 'all' should match
        
        # Test filtering by size
        xs_trans = self.transaction_model.get_kids_clothing_transactions(size='xs')
        self.assertIn(trans1, xs_trans)
        self.assertNotIn(trans2, xs_trans)
        self.assertIn(trans3, xs_trans)  # 'all' should match
        
        # Test filtering by season
        summer_trans = self.transaction_model.get_kids_clothing_transactions(season='summer')
        self.assertIn(trans1, summer_trans)
        self.assertNotIn(trans2, summer_trans)
        self.assertIn(trans3, summer_trans)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_trans = self.transaction_model.get_kids_clothing_transactions(brand='Baby Brand')
        self.assertIn(trans1, baby_brand_trans)
        self.assertNotIn(trans2, baby_brand_trans)
        self.assertNotIn(trans3, baby_brand_trans)
        
        # Test filtering by color
        pink_trans = self.transaction_model.get_kids_clothing_transactions(color='Pink')
        self.assertIn(trans1, pink_trans)
        self.assertNotIn(trans2, pink_trans)
        self.assertNotIn(trans3, pink_trans)