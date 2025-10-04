# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Calculation Tests
=========================================

Tests for Indian GST calculation functionality.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in_gst.models.account_tax import AccountTax
import logging

_logger = logging.getLogger(__name__)


class TestGstCalculation(OceanTestCase):
    """Test cases for GST calculation functionality"""
    
    def setUp(self):
        super(TestGstCalculation, self).setUp()
        self.tax_model = self.env['account.tax']
    
    def test_cgst_calculation(self):
        """Test CGST calculation"""
        cgst_tax = self.tax_model.create({
            'name': 'CGST 18%',
            'tax_type': 'gst',
            'gst_type': 'cgst',
            'amount': 18.0,
            'amount_type': 'percent',
            'gst_rate': 18.0
        })
        
        # Test CGST calculation
        base_amount = 1000.0
        cgst_amount = cgst_tax.compute_gst_amount(base_amount)
        self.assertEqual(cgst_amount, 180.0)
        
        # Test CGST breakdown
        breakdown = cgst_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['cgst'], 180.0)
        self.assertEqual(breakdown['sgst'], 180.0)
        self.assertEqual(breakdown['igst'], 0)
        self.assertEqual(breakdown['cess'], 0)
        self.assertEqual(breakdown['total'], 1360.0)
    
    def test_sgst_calculation(self):
        """Test SGST calculation"""
        sgst_tax = self.tax_model.create({
            'name': 'SGST 18%',
            'tax_type': 'gst',
            'gst_type': 'sgst',
            'amount': 18.0,
            'amount_type': 'percent',
            'gst_rate': 18.0
        })
        
        # Test SGST calculation
        base_amount = 1000.0
        sgst_amount = sgst_tax.compute_gst_amount(base_amount)
        self.assertEqual(sgst_amount, 180.0)
        
        # Test SGST breakdown
        breakdown = sgst_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['cgst'], 180.0)
        self.assertEqual(breakdown['sgst'], 180.0)
        self.assertEqual(breakdown['igst'], 0)
        self.assertEqual(breakdown['cess'], 0)
        self.assertEqual(breakdown['total'], 1360.0)
    
    def test_igst_calculation(self):
        """Test IGST calculation"""
        igst_tax = self.tax_model.create({
            'name': 'IGST 18%',
            'tax_type': 'gst',
            'gst_type': 'igst',
            'amount': 18.0,
            'amount_type': 'percent',
            'gst_rate': 18.0
        })
        
        # Test IGST calculation
        base_amount = 1000.0
        igst_amount = igst_tax.compute_gst_amount(base_amount)
        self.assertEqual(igst_amount, 180.0)
        
        # Test IGST breakdown
        breakdown = igst_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['igst'], 180.0)
        self.assertEqual(breakdown['cgst'], 0)
        self.assertEqual(breakdown['sgst'], 0)
        self.assertEqual(breakdown['cess'], 0)
        self.assertEqual(breakdown['total'], 1180.0)
    
    def test_cess_calculation(self):
        """Test CESS calculation"""
        cess_tax = self.tax_model.create({
            'name': 'CESS 1%',
            'tax_type': 'gst',
            'gst_type': 'cess',
            'amount': 1.0,
            'amount_type': 'percent',
            'gst_rate': 1.0
        })
        
        # Test CESS calculation
        base_amount = 1000.0
        cess_amount = cess_tax.compute_gst_amount(base_amount)
        self.assertEqual(cess_amount, 10.0)
        
        # Test CESS breakdown
        breakdown = cess_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['cess'], 10.0)
        self.assertEqual(breakdown['cgst'], 0)
        self.assertEqual(breakdown['sgst'], 0)
        self.assertEqual(breakdown['igst'], 0)
        self.assertEqual(breakdown['total'], 1010.0)
    
    def test_fixed_amount_calculation(self):
        """Test fixed amount calculation"""
        fixed_tax = self.tax_model.create({
            'name': 'Fixed Tax ₹50',
            'tax_type': 'gst',
            'gst_type': 'other',
            'amount': 50.0,
            'amount_type': 'fixed',
            'gst_rate': 50.0
        })
        
        # Test fixed amount calculation
        base_amount = 1000.0
        fixed_amount = fixed_tax.compute_gst_amount(base_amount)
        self.assertEqual(fixed_amount, 50.0)
        
        # Test fixed amount breakdown
        breakdown = fixed_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['total'], 1050.0)
    
    def test_zero_rate_calculation(self):
        """Test zero rate calculation"""
        zero_tax = self.tax_model.create({
            'name': 'GST 0%',
            'tax_type': 'gst',
            'gst_type': 'cgst',
            'amount': 0.0,
            'amount_type': 'percent',
            'gst_rate': 0.0
        })
        
        # Test zero rate calculation
        base_amount = 1000.0
        zero_amount = zero_tax.compute_gst_amount(base_amount)
        self.assertEqual(zero_amount, 0.0)
        
        # Test zero rate breakdown
        breakdown = zero_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['total'], 1000.0)
    
    def test_high_rate_calculation(self):
        """Test high rate calculation (28%)"""
        high_tax = self.tax_model.create({
            'name': 'GST 28%',
            'tax_type': 'gst',
            'gst_type': 'cgst',
            'amount': 28.0,
            'amount_type': 'percent',
            'gst_rate': 28.0
        })
        
        # Test high rate calculation
        base_amount = 1000.0
        high_amount = high_tax.compute_gst_amount(base_amount)
        self.assertEqual(high_amount, 280.0)
        
        # Test high rate breakdown
        breakdown = high_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['cgst'], 280.0)
        self.assertEqual(breakdown['sgst'], 280.0)
        self.assertEqual(breakdown['total'], 1560.0)
    
    def test_decimal_calculation(self):
        """Test decimal calculation"""
        decimal_tax = self.tax_model.create({
            'name': 'GST 12.5%',
            'tax_type': 'gst',
            'gst_type': 'cgst',
            'amount': 12.5,
            'amount_type': 'percent',
            'gst_rate': 12.5
        })
        
        # Test decimal calculation
        base_amount = 1000.0
        decimal_amount = decimal_tax.compute_gst_amount(base_amount)
        self.assertEqual(decimal_amount, 125.0)
        
        # Test decimal breakdown
        breakdown = decimal_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['cgst'], 125.0)
        self.assertEqual(breakdown['sgst'], 125.0)
        self.assertEqual(breakdown['total'], 1250.0)
    
    def test_large_amount_calculation(self):
        """Test large amount calculation"""
        large_tax = self.tax_model.create({
            'name': 'GST 18%',
            'tax_type': 'gst',
            'gst_type': 'cgst',
            'amount': 18.0,
            'amount_type': 'percent',
            'gst_rate': 18.0
        })
        
        # Test large amount calculation
        base_amount = 1000000.0  # 10 lakhs
        large_amount = large_tax.compute_gst_amount(base_amount)
        self.assertEqual(large_amount, 180000.0)
        
        # Test large amount breakdown
        breakdown = large_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['cgst'], 180000.0)
        self.assertEqual(breakdown['sgst'], 180000.0)
        self.assertEqual(breakdown['total'], 1360000.0)
    
    def test_negative_amount_calculation(self):
        """Test negative amount calculation"""
        negative_tax = self.tax_model.create({
            'name': 'GST 18%',
            'tax_type': 'gst',
            'gst_type': 'cgst',
            'amount': 18.0,
            'amount_type': 'percent',
            'gst_rate': 18.0
        })
        
        # Test negative amount calculation
        base_amount = -1000.0
        negative_amount = negative_tax.compute_gst_amount(base_amount)
        self.assertEqual(negative_amount, -180.0)
        
        # Test negative amount breakdown
        breakdown = negative_tax.get_gst_breakdown(base_amount)
        self.assertEqual(breakdown['cgst'], -180.0)
        self.assertEqual(breakdown['sgst'], -180.0)
        self.assertEqual(breakdown['total'], -1360.0)