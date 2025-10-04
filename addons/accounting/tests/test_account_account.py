# -*- coding: utf-8 -*-
"""
Ocean ERP - Account Account Tests
=================================

Tests for account account model in Ocean ERP.
"""

import unittest
from core_framework.testing import OceanTestCase
from core_framework.exceptions import ValidationError, UserError


class TestAccountAccount(OceanTestCase):
    """Test Account Account Model"""
    
    def setUp(self):
        """Set up test data"""
        super().setUp()
        
        # Create test company
        self.company = self.env['res.company'].create({
            'name': 'Test Company',
            'currency_id': self.env.ref('base.INR').id,
        })
        
        # Create test account type
        self.account_type = self.env['account.account.type'].create({
            'name': 'Test Account Type',
            'type': 'asset',
            'sequence': 10,
        })
    
    def test_create_account(self):
        """Test creating an account"""
        account = self.env['account.account'].create({
            'name': 'Test Account',
            'code': '1000',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        self.assertEqual(account.name, 'Test Account')
        self.assertEqual(account.code, '1000')
        self.assertEqual(account.account_type, 'asset')
        self.assertEqual(account.account_subtype, 'current_asset')
        self.assertTrue(account.active)
    
    def test_account_code_generation(self):
        """Test automatic account code generation"""
        account = self.env['account.account'].create({
            'name': 'Test Account',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        # Should generate code starting with '1' for asset
        self.assertTrue(account.code.startswith('1'))
        self.assertEqual(len(account.code), 4)  # 1XXX format
    
    def test_account_hierarchy(self):
        """Test account hierarchy"""
        parent_account = self.env['account.account'].create({
            'name': 'Parent Account',
            'code': '1000',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        child_account = self.env['account.account'].create({
            'name': 'Child Account',
            'code': '1001',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'parent_id': parent_account.id,
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        self.assertEqual(child_account.parent_id, parent_account)
        self.assertEqual(child_account.level, 1)
        self.assertEqual(child_account.full_code, '1000.1001')
    
    def test_account_balance_computation(self):
        """Test account balance computation"""
        account = self.env['account.account'].create({
            'name': 'Test Account',
            'code': '1000',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        # Create journal entry with debit
        journal_entry = self.env['account.move'].create({
            'name': 'TEST001',
            'date': '2024-01-01',
            'journal_id': self.env.ref('account.journal_general').id,
            'company_id': self.company.id,
        })
        
        # Create move line with debit
        self.env['account.move.line'].create({
            'move_id': journal_entry.id,
            'account_id': account.id,
            'name': 'Test Debit',
            'debit': 1000.00,
            'company_id': self.company.id,
        })
        
        # Create move line with credit
        self.env['account.move.line'].create({
            'move_id': journal_entry.id,
            'account_id': account.id,
            'name': 'Test Credit',
            'credit': 300.00,
            'company_id': self.company.id,
        })
        
        # Compute balance
        account._compute_balance()
        
        self.assertEqual(account.debit, 1000.00)
        self.assertEqual(account.credit, 300.00)
        self.assertEqual(account.balance, 700.00)
    
    def test_account_code_uniqueness(self):
        """Test account code uniqueness within company"""
        # Create first account
        self.env['account.account'].create({
            'name': 'First Account',
            'code': '1000',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        # Try to create second account with same code
        with self.assertRaises(ValidationError):
            self.env['account.account'].create({
                'name': 'Second Account',
                'code': '1000',
                'account_type': 'asset',
                'account_subtype': 'current_asset',
                'user_type_id': self.account_type.id,
                'company_id': self.company.id,
            })
    
    def test_circular_reference_prevention(self):
        """Test prevention of circular references in account hierarchy"""
        parent_account = self.env['account.account'].create({
            'name': 'Parent Account',
            'code': '1000',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        child_account = self.env['account.account'].create({
            'name': 'Child Account',
            'code': '1001',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'parent_id': parent_account.id,
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        # Try to create circular reference
        with self.assertRaises(ValidationError):
            parent_account.write({'parent_id': child_account.id})
    
    def test_kids_clothing_accounts(self):
        """Test kids clothing specific account filtering"""
        # Create accounts with different age groups
        baby_account = self.env['account.account'].create({
            'name': 'Baby Account',
            'code': '1000',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'age_group': '0-2',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        toddler_account = self.env['account.account'].create({
            'name': 'Toddler Account',
            'code': '1001',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'age_group': '2-4',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        all_age_account = self.env['account.account'].create({
            'name': 'All Age Account',
            'code': '1002',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'age_group': 'all',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        # Test filtering by age group
        baby_accounts = self.env['account.account'].get_kids_clothing_accounts(age_group='0-2')
        self.assertIn(baby_account, baby_accounts)
        self.assertIn(all_age_account, baby_accounts)
        self.assertNotIn(toddler_account, baby_accounts)
    
    def test_account_reconciliation(self):
        """Test account reconciliation functionality"""
        account = self.env['account.account'].create({
            'name': 'Reconcilable Account',
            'code': '1000',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'reconcile': True,
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        # Test reconciliation action
        result = account.action_reconcile()
        self.assertEqual(result['res_model'], 'account.reconciliation')
        self.assertEqual(result['context']['default_account_id'], account.id)
    
    def test_account_report_generation(self):
        """Test account report generation"""
        account = self.env['account.account'].create({
            'name': 'Report Account',
            'code': '1000',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        # Test report generation action
        result = account.action_generate_report()
        self.assertEqual(result['res_model'], 'account.report')
        self.assertEqual(result['context']['default_account_id'], account.id)
    
    def test_account_move_lines_view(self):
        """Test account move lines view"""
        account = self.env['account.account'].create({
            'name': 'Move Lines Account',
            'code': '1000',
            'account_type': 'asset',
            'account_subtype': 'current_asset',
            'user_type_id': self.account_type.id,
            'company_id': self.company.id,
        })
        
        # Test move lines view action
        result = account.action_view_move_lines()
        self.assertEqual(result['res_model'], 'account.move.line')
        self.assertEqual(result['domain'], [('account_id', '=', account.id)])
        self.assertEqual(result['context']['default_account_id'], account.id)


class TestAccountAccountType(OceanTestCase):
    """Test Account Account Type Model"""
    
    def setUp(self):
        """Set up test data"""
        super().setUp()
        
        # Create test company
        self.company = self.env['res.company'].create({
            'name': 'Test Company',
            'currency_id': self.env.ref('base.INR').id,
        })
    
    def test_create_account_type(self):
        """Test creating an account type"""
        account_type = self.env['account.account.type'].create({
            'name': 'Test Account Type',
            'type': 'asset',
            'sequence': 10,
            'include_initial_balance': True,
            'reconcile': False,
            'company_id': self.company.id,
        })
        
        self.assertEqual(account_type.name, 'Test Account Type')
        self.assertEqual(account_type.type, 'asset')
        self.assertEqual(account_type.sequence, 10)
        self.assertTrue(account_type.include_initial_balance)
        self.assertFalse(account_type.reconcile)
        self.assertTrue(account_type.active)
    
    def test_account_type_kids_clothing_fields(self):
        """Test kids clothing specific fields in account type"""
        account_type = self.env['account.account.type'].create({
            'name': 'Kids Clothing Account Type',
            'type': 'asset',
            'sequence': 10,
            'age_group': '0-2',
            'season': 'summer',
            'brand': 'Kids Brand',
            'color': 'Blue',
            'company_id': self.company.id,
        })
        
        self.assertEqual(account_type.age_group, '0-2')
        self.assertEqual(account_type.season, 'summer')
        self.assertEqual(account_type.brand, 'Kids Brand')
        self.assertEqual(account_type.color, 'Blue')


if __name__ == '__main__':
    unittest.main()