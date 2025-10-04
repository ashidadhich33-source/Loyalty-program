# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian GST Return Tests
===================================

Tests for Indian GST return models.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in_gst.models.gst_return import GstReturn, GstReport
import logging

_logger = logging.getLogger(__name__)


class TestGstReturn(OceanTestCase):
    """Test cases for GstReturn model"""
    
    def setUp(self):
        super(TestGstReturn, self).setUp()
        self.gst_return_model = self.env['gst.return']
        self.gst_report_model = self.env['gst.report']
    
    def test_create_gst_return(self):
        """Test creating a GST return"""
        return_vals = {
            'name': 'GSTR-1 - 202403',
            'return_type': 'gstr1',
            'return_period': '202403',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        gst_return = self.gst_return_model.create(return_vals)
        
        self.assertEqual(gst_return.name, 'GSTR-1 - 202403')
        self.assertEqual(gst_return.return_type, 'gstr1')
        self.assertEqual(gst_return.return_period, '202403')
        self.assertEqual(gst_return.age_group, '4-6')
        self.assertEqual(gst_return.size, 'm')
        self.assertEqual(gst_return.season, 'all_season')
        self.assertEqual(gst_return.brand, 'Kids Brand')
        self.assertEqual(gst_return.color, 'Blue')
        self.assertEqual(gst_return.state, 'draft')
    
    def test_return_types(self):
        """Test different return types"""
        return_types = [
            'gstr1',
            'gstr2',
            'gstr3',
            'gstr4',
            'gstr5',
            'gstr6',
            'gstr7',
            'gstr8',
            'gstr9',
            'gstr10'
        ]
        
        for return_type in return_types:
            gst_return = self.gst_return_model.create({
                'name': f'{return_type.upper()} - 202403',
                'return_type': return_type,
                'return_period': '202403'
            })
            self.assertEqual(gst_return.return_type, return_type)
    
    def test_action_prepare_return(self):
        """Test preparing GST return"""
        gst_return = self.gst_return_model.create({
            'name': 'GSTR-1 - 202403',
            'return_type': 'gstr1',
            'return_period': '202403'
        })
        
        # Test preparing draft return
        gst_return.action_prepare_return()
        self.assertEqual(gst_return.state, 'ready')
        
        # Test preparing non-draft return
        with self.assertRaises(UserError):
            gst_return.action_prepare_return()
    
    def test_action_file_return(self):
        """Test filing GST return"""
        gst_return = self.gst_return_model.create({
            'name': 'GSTR-1 - 202403',
            'return_type': 'gstr1',
            'return_period': '202403'
        })
        
        # Prepare return first
        gst_return.action_prepare_return()
        
        # Test filing ready return
        gst_return.action_file_return()
        self.assertEqual(gst_return.state, 'filed')
        self.assertTrue(gst_return.filing_date)
        self.assertTrue(gst_return.ack_number)
        
        # Test filing non-ready return
        gst_return.state = 'draft'
        with self.assertRaises(UserError):
            gst_return.action_file_return()
    
    def test_get_kids_clothing_returns(self):
        """Test filtering returns by kids clothing criteria"""
        # Create test returns
        return1 = self.gst_return_model.create({
            'name': 'Baby GSTR-1',
            'return_type': 'gstr1',
            'return_period': '202403',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink',
            'state': 'filed'
        })
        
        return2 = self.gst_return_model.create({
            'name': 'Toddler GSTR-1',
            'return_type': 'gstr1',
            'return_period': '202403',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue',
            'state': 'filed'
        })
        
        return3 = self.gst_return_model.create({
            'name': 'All Age GSTR-1',
            'return_type': 'gstr1',
            'return_period': '202403',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green',
            'state': 'filed'
        })
        
        # Test filtering by age group
        baby_returns = self.gst_return_model.get_kids_clothing_returns(age_group='0-2')
        self.assertIn(return1, baby_returns)
        self.assertNotIn(return2, baby_returns)
        self.assertIn(return3, baby_returns)  # 'all' should match
        
        # Test filtering by size
        xs_returns = self.gst_return_model.get_kids_clothing_returns(size='xs')
        self.assertIn(return1, xs_returns)
        self.assertNotIn(return2, xs_returns)
        self.assertIn(return3, xs_returns)  # 'all' should match
        
        # Test filtering by season
        summer_returns = self.gst_return_model.get_kids_clothing_returns(season='summer')
        self.assertIn(return1, summer_returns)
        self.assertNotIn(return2, summer_returns)
        self.assertIn(return3, summer_returns)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_returns = self.gst_return_model.get_kids_clothing_returns(brand='Baby Brand')
        self.assertIn(return1, baby_brand_returns)
        self.assertNotIn(return2, baby_brand_returns)
        self.assertNotIn(return3, baby_brand_returns)
        
        # Test filtering by color
        pink_returns = self.gst_return_model.get_kids_clothing_returns(color='Pink')
        self.assertIn(return1, pink_returns)
        self.assertNotIn(return2, pink_returns)
        self.assertNotIn(return3, pink_returns)


class TestGstReport(OceanTestCase):
    """Test cases for GstReport model"""
    
    def setUp(self):
        super(TestGstReport, self).setUp()
        self.gst_report_model = self.env['gst.report']
    
    def test_create_gst_report(self):
        """Test creating a GST report"""
        report_vals = {
            'name': 'GST Summary Report - March 2024',
            'report_type': 'summary',
            'date_from': '2024-03-01',
            'date_to': '2024-03-31',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        gst_report = self.gst_report_model.create(report_vals)
        
        self.assertEqual(gst_report.name, 'GST Summary Report - March 2024')
        self.assertEqual(gst_report.report_type, 'summary')
        self.assertEqual(gst_report.age_group, '4-6')
        self.assertEqual(gst_report.size, 'm')
        self.assertEqual(gst_report.season, 'all_season')
        self.assertEqual(gst_report.brand, 'Kids Brand')
        self.assertEqual(gst_report.color, 'Blue')
        self.assertEqual(gst_report.state, 'draft')
    
    def test_report_types(self):
        """Test different report types"""
        report_types = [
            'summary',
            'liability',
            'input_tax',
            'output_tax',
            'reconciliation',
            'audit',
            'compliance'
        ]
        
        for report_type in report_types:
            gst_report = self.gst_report_model.create({
                'name': f'GST {report_type.title()} Report',
                'report_type': report_type,
                'date_from': '2024-03-01',
                'date_to': '2024-03-31'
            })
            self.assertEqual(gst_report.report_type, report_type)
    
    def test_action_generate_report(self):
        """Test generating GST report"""
        gst_report = self.gst_report_model.create({
            'name': 'GST Summary Report',
            'report_type': 'summary',
            'date_from': '2024-03-01',
            'date_to': '2024-03-31'
        })
        
        # Test generating draft report
        gst_report.action_generate_report()
        self.assertEqual(gst_report.state, 'generated')
        
        # Test generating non-draft report
        with self.assertRaises(UserError):
            gst_report.action_generate_report()
    
    def test_action_export_report(self):
        """Test exporting GST report"""
        gst_report = self.gst_report_model.create({
            'name': 'GST Summary Report',
            'report_type': 'summary',
            'date_from': '2024-03-01',
            'date_to': '2024-03-31'
        })
        
        # Generate report first
        gst_report.action_generate_report()
        
        # Test exporting generated report
        gst_report.action_export_report()
        self.assertEqual(gst_report.state, 'exported')
        
        # Test exporting non-generated report
        gst_report.state = 'draft'
        with self.assertRaises(UserError):
            gst_report.action_export_report()
    
    def test_action_print_report(self):
        """Test printing GST report"""
        gst_report = self.gst_report_model.create({
            'name': 'GST Summary Report',
            'report_type': 'summary',
            'date_from': '2024-03-01',
            'date_to': '2024-03-31'
        })
        
        # Generate report first
        gst_report.action_generate_report()
        
        # Test printing generated report
        gst_report.action_print_report()
        self.assertEqual(gst_report.state, 'printed')
        
        # Test printing non-generated report
        gst_report.state = 'draft'
        with self.assertRaises(UserError):
            gst_report.action_print_report()
    
    def test_get_kids_clothing_reports(self):
        """Test filtering reports by kids clothing criteria"""
        # Create test reports
        report1 = self.gst_report_model.create({
            'name': 'Baby GST Summary',
            'report_type': 'summary',
            'date_from': '2024-03-01',
            'date_to': '2024-03-31',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink',
            'state': 'generated'
        })
        
        report2 = self.gst_report_model.create({
            'name': 'Toddler GST Summary',
            'report_type': 'summary',
            'date_from': '2024-03-01',
            'date_to': '2024-03-31',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue',
            'state': 'generated'
        })
        
        report3 = self.gst_report_model.create({
            'name': 'All Age GST Summary',
            'report_type': 'summary',
            'date_from': '2024-03-01',
            'date_to': '2024-03-31',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green',
            'state': 'generated'
        })
        
        # Test filtering by age group
        baby_reports = self.gst_report_model.get_kids_clothing_reports(age_group='0-2')
        self.assertIn(report1, baby_reports)
        self.assertNotIn(report2, baby_reports)
        self.assertIn(report3, baby_reports)  # 'all' should match
        
        # Test filtering by size
        xs_reports = self.gst_report_model.get_kids_clothing_reports(size='xs')
        self.assertIn(report1, xs_reports)
        self.assertNotIn(report2, xs_reports)
        self.assertIn(report3, xs_reports)  # 'all' should match
        
        # Test filtering by season
        summer_reports = self.gst_report_model.get_kids_clothing_reports(season='summer')
        self.assertIn(report1, summer_reports)
        self.assertNotIn(report2, summer_reports)
        self.assertIn(report3, summer_reports)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_reports = self.gst_report_model.get_kids_clothing_reports(brand='Baby Brand')
        self.assertIn(report1, baby_brand_reports)
        self.assertNotIn(report2, baby_brand_reports)
        self.assertNotIn(report3, baby_brand_reports)
        
        # Test filtering by color
        pink_reports = self.gst_report_model.get_kids_clothing_reports(color='Pink')
        self.assertIn(report1, pink_reports)
        self.assertNotIn(report2, pink_reports)
        self.assertNotIn(report3, pink_reports)