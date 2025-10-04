# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian EDI Transmission Tests
==========================================

Tests for Indian EDI transmission models.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in_edi.models.edi_transmission import EdiTransmission, EdiAcknowledgment
import logging

_logger = logging.getLogger(__name__)


class TestEdiTransmission(OceanTestCase):
    """Test cases for EdiTransmission model"""
    
    def setUp(self):
        super(TestEdiTransmission, self).setUp()
        self.transmission_model = self.env['edi.transmission']
        self.acknowledgment_model = self.env['edi.acknowledgment']
    
    def test_create_edi_transmission(self):
        """Test creating an EDI transmission"""
        transmission_vals = {
            'name': 'FTP Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp',
            'host': 'ftp.example.com',
            'port': 21,
            'username': 'user',
            'password': 'pass',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        transmission = self.transmission_model.create(transmission_vals)
        
        self.assertEqual(transmission.name, 'FTP Transmission')
        self.assertEqual(transmission.transmission_type, 'send')
        self.assertEqual(transmission.protocol, 'ftp')
        self.assertEqual(transmission.host, 'ftp.example.com')
        self.assertEqual(transmission.port, 21)
        self.assertEqual(transmission.username, 'user')
        self.assertEqual(transmission.password, 'pass')
        self.assertEqual(transmission.age_group, '4-6')
        self.assertEqual(transmission.size, 'm')
        self.assertEqual(transmission.season, 'all_season')
        self.assertEqual(transmission.brand, 'Kids Brand')
        self.assertEqual(transmission.color, 'Blue')
        self.assertEqual(transmission.state, 'draft')
    
    def test_transmission_types(self):
        """Test different transmission types"""
        transmission_types = [
            'send',
            'receive',
            'bidirectional'
        ]
        
        for trans_type in transmission_types:
            transmission = self.transmission_model.create({
                'name': f'{trans_type.title()} Transmission',
                'transmission_type': trans_type,
                'protocol': 'ftp'
            })
            self.assertEqual(transmission.transmission_type, trans_type)
    
    def test_protocols(self):
        """Test different protocols"""
        protocols = [
            'ftp',
            'sftp',
            'http',
            'https',
            'as2',
            'email',
            'api',
            'other'
        ]
        
        for protocol in protocols:
            transmission = self.transmission_model.create({
                'name': f'{protocol.upper()} Transmission',
                'transmission_type': 'send',
                'protocol': protocol
            })
            self.assertEqual(transmission.protocol, protocol)
    
    def test_action_start(self):
        """Test starting EDI transmission"""
        transmission = self.transmission_model.create({
            'name': 'Test Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp',
            'state': 'ready'
        })
        
        # Test starting ready transmission
        transmission.action_start()
        self.assertEqual(transmission.state, 'sending')
        self.assertTrue(transmission.start_date)
        
        # Test starting non-ready transmission
        transmission.state = 'draft'
        with self.assertRaises(UserError):
            transmission.action_start()
    
    def test_action_complete(self):
        """Test completing EDI transmission"""
        transmission = self.transmission_model.create({
            'name': 'Test Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp',
            'state': 'sending'
        })
        
        # Test completing sending transmission
        transmission.action_complete()
        self.assertEqual(transmission.state, 'sent')
        self.assertTrue(transmission.end_date)
        
        # Test completing non-sending transmission
        transmission.state = 'draft'
        with self.assertRaises(UserError):
            transmission.action_complete()
    
    def test_action_process(self):
        """Test processing EDI transmission"""
        transmission = self.transmission_model.create({
            'name': 'Test Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp',
            'state': 'sent'
        })
        
        # Test processing sent transmission
        transmission.action_process()
        self.assertEqual(transmission.state, 'processed')
        self.assertTrue(transmission.processed_data)
        
        # Test processing received transmission
        transmission.state = 'received'
        transmission.action_process()
        self.assertEqual(transmission.state, 'processed')
        
        # Test processing non-sent/received transmission
        transmission.state = 'draft'
        with self.assertRaises(UserError):
            transmission.action_process()
    
    def test_get_kids_clothing_transmissions(self):
        """Test filtering transmissions by kids clothing criteria"""
        # Create test transmissions
        trans1 = self.transmission_model.create({
            'name': 'Baby Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink',
            'state': 'processed'
        })
        
        trans2 = self.transmission_model.create({
            'name': 'Toddler Transmission',
            'transmission_type': 'receive',
            'protocol': 'sftp',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue',
            'state': 'processed'
        })
        
        trans3 = self.transmission_model.create({
            'name': 'All Age Transmission',
            'transmission_type': 'bidirectional',
            'protocol': 'http',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green',
            'state': 'processed'
        })
        
        # Test filtering by age group
        baby_trans = self.transmission_model.get_kids_clothing_transmissions(age_group='0-2')
        self.assertIn(trans1, baby_trans)
        self.assertNotIn(trans2, baby_trans)
        self.assertIn(trans3, baby_trans)  # 'all' should match
        
        # Test filtering by size
        xs_trans = self.transmission_model.get_kids_clothing_transmissions(size='xs')
        self.assertIn(trans1, xs_trans)
        self.assertNotIn(trans2, xs_trans)
        self.assertIn(trans3, xs_trans)  # 'all' should match
        
        # Test filtering by season
        summer_trans = self.transmission_model.get_kids_clothing_transmissions(season='summer')
        self.assertIn(trans1, summer_trans)
        self.assertNotIn(trans2, summer_trans)
        self.assertIn(trans3, summer_trans)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_trans = self.transmission_model.get_kids_clothing_transmissions(brand='Baby Brand')
        self.assertIn(trans1, baby_brand_trans)
        self.assertNotIn(trans2, baby_brand_trans)
        self.assertNotIn(trans3, baby_brand_trans)
        
        # Test filtering by color
        pink_trans = self.transmission_model.get_kids_clothing_transmissions(color='Pink')
        self.assertIn(trans1, pink_trans)
        self.assertNotIn(trans2, pink_trans)
        self.assertNotIn(trans3, pink_trans)


class TestEdiAcknowledgment(OceanTestCase):
    """Test cases for EdiAcknowledgment model"""
    
    def setUp(self):
        super(TestEdiAcknowledgment, self).setUp()
        self.transmission_model = self.env['edi.transmission']
        self.acknowledgment_model = self.env['edi.acknowledgment']
    
    def test_create_edi_acknowledgment(self):
        """Test creating an EDI acknowledgment"""
        # Create parent transmission first
        transmission = self.transmission_model.create({
            'name': 'Test Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp'
        })
        
        acknowledgment_vals = {
            'name': 'Technical Acknowledgment',
            'transmission_id': transmission.id,
            'acknowledgment_type': 'ta',
            'acknowledgment_code': 'TA001',
            'acknowledgment_message': 'Transmission received successfully',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        acknowledgment = self.acknowledgment_model.create(acknowledgment_vals)
        
        self.assertEqual(acknowledgment.name, 'Technical Acknowledgment')
        self.assertEqual(acknowledgment.transmission_id.id, transmission.id)
        self.assertEqual(acknowledgment.acknowledgment_type, 'ta')
        self.assertEqual(acknowledgment.acknowledgment_code, 'TA001')
        self.assertEqual(acknowledgment.acknowledgment_message, 'Transmission received successfully')
        self.assertEqual(acknowledgment.age_group, '4-6')
        self.assertEqual(acknowledgment.size, 'm')
        self.assertEqual(acknowledgment.season, 'all_season')
        self.assertEqual(acknowledgment.brand, 'Kids Brand')
        self.assertEqual(acknowledgment.color, 'Blue')
        self.assertEqual(acknowledgment.state, 'pending')
    
    def test_acknowledgment_types(self):
        """Test different acknowledgment types"""
        # Create parent transmission first
        transmission = self.transmission_model.create({
            'name': 'Test Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp'
        })
        
        acknowledgment_types = [
            'ta',
            'fa',
            'ua',
            'other'
        ]
        
        for ack_type in acknowledgment_types:
            acknowledgment = self.acknowledgment_model.create({
                'name': f'{ack_type.upper()} Acknowledgment',
                'transmission_id': transmission.id,
                'acknowledgment_type': ack_type
            })
            self.assertEqual(acknowledgment.acknowledgment_type, ack_type)
    
    def test_get_kids_clothing_acknowledgments(self):
        """Test filtering acknowledgments by kids clothing criteria"""
        # Create parent transmission first
        transmission = self.transmission_model.create({
            'name': 'Test Transmission',
            'transmission_type': 'send',
            'protocol': 'ftp'
        })
        
        # Create test acknowledgments
        ack1 = self.acknowledgment_model.create({
            'name': 'Baby Acknowledgment',
            'transmission_id': transmission.id,
            'acknowledgment_type': 'ta',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink',
            'state': 'processed'
        })
        
        ack2 = self.acknowledgment_model.create({
            'name': 'Toddler Acknowledgment',
            'transmission_id': transmission.id,
            'acknowledgment_type': 'fa',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue',
            'state': 'processed'
        })
        
        ack3 = self.acknowledgment_model.create({
            'name': 'All Age Acknowledgment',
            'transmission_id': transmission.id,
            'acknowledgment_type': 'ua',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green',
            'state': 'processed'
        })
        
        # Test filtering by age group
        baby_acks = self.acknowledgment_model.get_kids_clothing_acknowledgments(age_group='0-2')
        self.assertIn(ack1, baby_acks)
        self.assertNotIn(ack2, baby_acks)
        self.assertIn(ack3, baby_acks)  # 'all' should match
        
        # Test filtering by size
        xs_acks = self.acknowledgment_model.get_kids_clothing_acknowledgments(size='xs')
        self.assertIn(ack1, xs_acks)
        self.assertNotIn(ack2, xs_acks)
        self.assertIn(ack3, xs_acks)  # 'all' should match
        
        # Test filtering by season
        summer_acks = self.acknowledgment_model.get_kids_clothing_acknowledgments(season='summer')
        self.assertIn(ack1, summer_acks)
        self.assertNotIn(ack2, summer_acks)
        self.assertIn(ack3, summer_acks)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_acks = self.acknowledgment_model.get_kids_clothing_acknowledgments(brand='Baby Brand')
        self.assertIn(ack1, baby_brand_acks)
        self.assertNotIn(ack2, baby_brand_acks)
        self.assertNotIn(ack3, baby_brand_acks)
        
        # Test filtering by color
        pink_acks = self.acknowledgment_model.get_kids_clothing_acknowledgments(color='Pink')
        self.assertIn(ack1, pink_acks)
        self.assertNotIn(ack2, pink_acks)
        self.assertNotIn(ack3, pink_acks)