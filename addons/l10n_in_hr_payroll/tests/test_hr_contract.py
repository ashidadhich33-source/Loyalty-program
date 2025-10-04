# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Contract Tests
====================================

Tests for Indian HR contract models.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in_hr_payroll.models.hr_contract import HrContract
import logging

_logger = logging.getLogger(__name__)


class TestHrContract(OceanTestCase):
    """Test cases for HrContract model"""
    
    def setUp(self):
        super(TestHrContract, self).setUp()
        self.employee_model = self.env['hr.employee']
        self.contract_model = self.env['hr.contract']
    
    def test_create_contract(self):
        """Test creating a contract"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'John Doe',
            'employee_id': 'EMP001'
        })
        
        contract_vals = {
            'name': 'Permanent Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'pf_applicable': True,
            'esi_applicable': True,
            'professional_tax_applicable': True,
            'income_tax_applicable': True,
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        contract = self.contract_model.create(contract_vals)
        
        self.assertEqual(contract.name, 'Permanent Contract')
        self.assertEqual(contract.employee_id.id, employee.id)
        self.assertEqual(contract.contract_type, 'permanent')
        self.assertEqual(contract.wage, 50000)
        self.assertEqual(contract.wage_type, 'monthly')
        self.assertEqual(contract.pf_applicable, True)
        self.assertEqual(contract.esi_applicable, True)
        self.assertEqual(contract.professional_tax_applicable, True)
        self.assertEqual(contract.income_tax_applicable, True)
        self.assertEqual(contract.age_group, '4-6')
        self.assertEqual(contract.size, 'm')
        self.assertEqual(contract.season, 'all_season')
        self.assertEqual(contract.brand, 'Kids Brand')
        self.assertEqual(contract.color, 'Blue')
        self.assertEqual(contract.state, 'draft')
    
    def test_contract_types(self):
        """Test different contract types"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        contract_types = [
            'permanent',
            'temporary',
            'contract',
            'intern',
            'consultant'
        ]
        
        for contract_type in contract_types:
            contract = self.contract_model.create({
                'name': f'Test {contract_type.title()} Contract',
                'employee_id': employee.id,
                'contract_type': contract_type,
                'wage': 50000,
                'wage_type': 'monthly',
                'date_start': '2024-01-01'
            })
            self.assertEqual(contract.contract_type, contract_type)
    
    def test_wage_types(self):
        """Test different wage types"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        wage_types = [
            'monthly',
            'weekly',
            'daily',
            'hourly'
        ]
        
        for wage_type in wage_types:
            contract = self.contract_model.create({
                'name': f'Test {wage_type.title()} Contract',
                'employee_id': employee.id,
                'contract_type': 'permanent',
                'wage': 50000,
                'wage_type': wage_type,
                'date_start': '2024-01-01'
            })
            self.assertEqual(contract.wage_type, wage_type)
    
    def test_action_confirm(self):
        """Test confirming contract"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        contract = self.contract_model.create({
            'name': 'Test Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'state': 'draft'
        })
        
        # Test confirming draft contract
        contract.action_confirm()
        self.assertEqual(contract.state, 'open')
        
        # Test confirming non-draft contract
        with self.assertRaises(UserError):
            contract.action_confirm()
    
    def test_action_close(self):
        """Test closing contract"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        contract = self.contract_model.create({
            'name': 'Test Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'state': 'open'
        })
        
        # Test closing open contract
        contract.action_close()
        self.assertEqual(contract.state, 'close')
        
        # Test closing non-open contract
        with self.assertRaises(UserError):
            contract.action_close()
    
    def test_action_cancel(self):
        """Test cancelling contract"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        contract = self.contract_model.create({
            'name': 'Test Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'state': 'draft'
        })
        
        # Test cancelling draft contract
        contract.action_cancel()
        self.assertEqual(contract.state, 'cancel')
        
        # Test cancelling open contract
        contract.state = 'open'
        contract.action_cancel()
        self.assertEqual(contract.state, 'cancel')
        
        # Test cancelling non-draft/open contract
        contract.state = 'close'
        with self.assertRaises(UserError):
            contract.action_cancel()
    
    def test_calculate_gross_salary(self):
        """Test gross salary calculation"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        contract = self.contract_model.create({
            'name': 'Test Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01'
        })
        
        # Test gross salary calculation
        gross_salary = contract.calculate_gross_salary()
        self.assertEqual(gross_salary, 50000.0)
    
    def test_calculate_deductions(self):
        """Test deductions calculation"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        contract = self.contract_model.create({
            'name': 'Test Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'pf_applicable': True,
            'esi_applicable': True,
            'professional_tax_applicable': True,
            'income_tax_applicable': True
        })
        
        # Test deductions calculation
        deductions = contract.calculate_deductions()
        self.assertGreater(deductions, 0)
        
        # Test PF deduction (12% of basic wage, max 1800)
        pf_amount = min(50000 * 0.12, 1800)
        self.assertIn(pf_amount, [6000, 1800])  # Should be 1800 (max limit)
        
        # Test ESI deduction (0.75% of gross salary, if gross <= 21000)
        # Since wage is 50000 > 21000, ESI should be 0
        esi_amount = 0 if 50000 > 21000 else 50000 * 0.0075
        self.assertEqual(esi_amount, 0)
    
    def test_calculate_net_salary(self):
        """Test net salary calculation"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        contract = self.contract_model.create({
            'name': 'Test Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'pf_applicable': True,
            'esi_applicable': True,
            'professional_tax_applicable': True,
            'income_tax_applicable': True
        })
        
        # Test net salary calculation
        net_salary = contract.calculate_net_salary()
        self.assertLess(net_salary, 50000)  # Should be less than gross due to deductions
        self.assertGreater(net_salary, 0)  # Should be positive
    
    def test_get_kids_clothing_contracts(self):
        """Test filtering contracts by kids clothing criteria"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        # Create test contracts
        contract1 = self.contract_model.create({
            'name': 'Baby Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink',
            'state': 'open'
        })
        
        contract2 = self.contract_model.create({
            'name': 'Toddler Contract',
            'employee_id': employee.id,
            'contract_type': 'temporary',
            'wage': 40000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue',
            'state': 'open'
        })
        
        contract3 = self.contract_model.create({
            'name': 'All Age Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 60000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green',
            'state': 'open'
        })
        
        # Test filtering by age group
        baby_contracts = self.contract_model.get_kids_clothing_contracts(age_group='0-2')
        self.assertIn(contract1, baby_contracts)
        self.assertNotIn(contract2, baby_contracts)
        self.assertIn(contract3, baby_contracts)  # 'all' should match
        
        # Test filtering by size
        xs_contracts = self.contract_model.get_kids_clothing_contracts(size='xs')
        self.assertIn(contract1, xs_contracts)
        self.assertNotIn(contract2, xs_contracts)
        self.assertIn(contract3, xs_contracts)  # 'all' should match
        
        # Test filtering by season
        summer_contracts = self.contract_model.get_kids_clothing_contracts(season='summer')
        self.assertIn(contract1, summer_contracts)
        self.assertNotIn(contract2, summer_contracts)
        self.assertIn(contract3, summer_contracts)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_contracts = self.contract_model.get_kids_clothing_contracts(brand='Baby Brand')
        self.assertIn(contract1, baby_brand_contracts)
        self.assertNotIn(contract2, baby_brand_contracts)
        self.assertNotIn(contract3, baby_brand_contracts)
        
        # Test filtering by color
        pink_contracts = self.contract_model.get_kids_clothing_contracts(color='Pink')
        self.assertIn(contract1, pink_contracts)
        self.assertNotIn(contract2, pink_contracts)
        self.assertNotIn(contract3, pink_contracts)