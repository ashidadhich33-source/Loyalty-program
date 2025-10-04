# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian HR Employee Tests
====================================

Tests for Indian HR employee models.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in_hr_payroll.models.hr_employee import HrEmployee
import logging

_logger = logging.getLogger(__name__)


class TestHrEmployee(OceanTestCase):
    """Test cases for HrEmployee model"""
    
    def setUp(self):
        super(TestHrEmployee, self).setUp()
        self.employee_model = self.env['hr.employee']
    
    def test_create_employee(self):
        """Test creating an employee"""
        employee_vals = {
            'name': 'John Doe',
            'employee_id': 'EMP001',
            'gender': 'male',
            'marital_status': 'single',
            'pan': 'ABCDE1234F',
            'aadhar': '123456789012',
            'pf_number': 'MH1234567890',
            'esi_number': '1234567890',
            'uan': '123456789012',
            'age_group': '4-6',
            'size': 'm',
            'season': 'all_season',
            'brand': 'Kids Brand',
            'color': 'Blue',
        }
        
        employee = self.employee_model.create(employee_vals)
        
        self.assertEqual(employee.name, 'John Doe')
        self.assertEqual(employee.employee_id, 'EMP001')
        self.assertEqual(employee.gender, 'male')
        self.assertEqual(employee.marital_status, 'single')
        self.assertEqual(employee.pan, 'ABCDE1234F')
        self.assertEqual(employee.aadhar, '123456789012')
        self.assertEqual(employee.pf_number, 'MH1234567890')
        self.assertEqual(employee.esi_number, '1234567890')
        self.assertEqual(employee.uan, '123456789012')
        self.assertEqual(employee.age_group, '4-6')
        self.assertEqual(employee.size, 'm')
        self.assertEqual(employee.season, 'all_season')
        self.assertEqual(employee.brand, 'Kids Brand')
        self.assertEqual(employee.color, 'Blue')
        self.assertTrue(employee.active)
    
    def test_validate_pan(self):
        """Test PAN validation"""
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001',
            'pan': 'ABCDE1234F'
        })
        
        # Valid PAN
        self.assertTrue(employee.validate_pan('ABCDE1234F'))
        
        # Invalid PAN
        self.assertFalse(employee.validate_pan('ABCDE123'))
        self.assertFalse(employee.validate_pan('ABCDE1234G'))
        self.assertFalse(employee.validate_pan('1234567890'))
    
    def test_validate_aadhar(self):
        """Test Aadhar validation"""
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001',
            'aadhar': '123456789012'
        })
        
        # Valid Aadhar
        self.assertTrue(employee.validate_aadhar('123456789012'))
        
        # Invalid Aadhar
        self.assertFalse(employee.validate_aadhar('12345678901'))
        self.assertFalse(employee.validate_aadhar('1234567890123'))
        self.assertFalse(employee.validate_aadhar('ABCD123456789'))
    
    def test_validate_pf_number(self):
        """Test PF number validation"""
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001',
            'pf_number': 'MH1234567890'
        })
        
        # Valid PF number
        self.assertTrue(employee.validate_pf_number('MH1234567890'))
        
        # Invalid PF number
        self.assertFalse(employee.validate_pf_number('MH123456789'))
        self.assertFalse(employee.validate_pf_number('MH12345678901'))
        self.assertFalse(employee.validate_pf_number('123456789012'))
    
    def test_validate_esi_number(self):
        """Test ESI number validation"""
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001',
            'esi_number': '1234567890'
        })
        
        # Valid ESI number
        self.assertTrue(employee.validate_esi_number('1234567890'))
        
        # Invalid ESI number
        self.assertFalse(employee.validate_esi_number('123456789'))
        self.assertFalse(employee.validate_esi_number('12345678901'))
        self.assertFalse(employee.validate_esi_number('ABCD123456'))
    
    def test_validate_uan(self):
        """Test UAN validation"""
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001',
            'uan': '123456789012'
        })
        
        # Valid UAN
        self.assertTrue(employee.validate_uan('123456789012'))
        
        # Invalid UAN
        self.assertFalse(employee.validate_uan('12345678901'))
        self.assertFalse(employee.validate_uan('1234567890123'))
        self.assertFalse(employee.validate_uan('ABCD123456789'))
    
    def test_get_kids_clothing_employees(self):
        """Test filtering employees by kids clothing criteria"""
        # Create test employees
        emp1 = self.employee_model.create({
            'name': 'Baby Employee',
            'employee_id': 'EMP001',
            'age_group': '0-2',
            'size': 'xs',
            'season': 'summer',
            'brand': 'Baby Brand',
            'color': 'Pink'
        })
        
        emp2 = self.employee_model.create({
            'name': 'Toddler Employee',
            'employee_id': 'EMP002',
            'age_group': '2-4',
            'size': 's',
            'season': 'winter',
            'brand': 'Toddler Brand',
            'color': 'Blue'
        })
        
        emp3 = self.employee_model.create({
            'name': 'All Age Employee',
            'employee_id': 'EMP003',
            'age_group': 'all',
            'size': 'all',
            'season': 'all_season',
            'brand': 'All Brand',
            'color': 'Green'
        })
        
        # Test filtering by age group
        baby_emps = self.employee_model.get_kids_clothing_employees(age_group='0-2')
        self.assertIn(emp1, baby_emps)
        self.assertNotIn(emp2, baby_emps)
        self.assertIn(emp3, baby_emps)  # 'all' should match
        
        # Test filtering by size
        xs_emps = self.employee_model.get_kids_clothing_employees(size='xs')
        self.assertIn(emp1, xs_emps)
        self.assertNotIn(emp2, xs_emps)
        self.assertIn(emp3, xs_emps)  # 'all' should match
        
        # Test filtering by season
        summer_emps = self.employee_model.get_kids_clothing_employees(season='summer')
        self.assertIn(emp1, summer_emps)
        self.assertNotIn(emp2, summer_emps)
        self.assertIn(emp3, summer_emps)  # 'all_season' should match
        
        # Test filtering by brand
        baby_brand_emps = self.employee_model.get_kids_clothing_employees(brand='Baby Brand')
        self.assertIn(emp1, baby_brand_emps)
        self.assertNotIn(emp2, baby_brand_emps)
        self.assertNotIn(emp3, baby_brand_emps)
        
        # Test filtering by color
        pink_emps = self.employee_model.get_kids_clothing_employees(color='Pink')
        self.assertIn(emp1, pink_emps)
        self.assertNotIn(emp2, pink_emps)
        self.assertNotIn(emp3, pink_emps)
    
    def test_gender_types(self):
        """Test different gender types"""
        gender_types = [
            'male',
            'female',
            'other'
        ]
        
        for gender in gender_types:
            employee = self.employee_model.create({
                'name': f'Test {gender.title()} Employee',
                'employee_id': f'EMP{gender.upper()}',
                'gender': gender
            })
            self.assertEqual(employee.gender, gender)
    
    def test_marital_status_types(self):
        """Test different marital status types"""
        marital_statuses = [
            'single',
            'married',
            'divorced',
            'widowed'
        ]
        
        for status in marital_statuses:
            employee = self.employee_model.create({
                'name': f'Test {status.title()} Employee',
                'employee_id': f'EMP{status.upper()}',
                'marital_status': status
            })
            self.assertEqual(employee.marital_status, status)
    
    def test_calculate_age(self):
        """Test age calculation"""
        from datetime import date, timedelta
        
        # Test with birth date
        birth_date = date.today() - timedelta(days=365*25)  # 25 years ago
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001',
            'birth_date': birth_date
        })
        
        age = employee.calculate_age()
        self.assertEqual(age, 25)
        
        # Test without birth date
        employee_no_birth = self.employee_model.create({
            'name': 'Test Employee No Birth',
            'employee_id': 'EMP002'
        })
        
        age_no_birth = employee_no_birth.calculate_age()
        self.assertEqual(age_no_birth, 0)
    
    def test_get_current_contract(self):
        """Test getting current contract"""
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        # Test with no contracts
        current_contract = employee.get_current_contract()
        self.assertFalse(current_contract)
        
        # Test with active contract
        contract = self.env['hr.contract'].create({
            'name': 'Test Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'state': 'open'
        })
        
        current_contract = employee.get_current_contract()
        self.assertEqual(current_contract.id, contract.id)
    
    def test_get_current_salary(self):
        """Test getting current salary"""
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        # Test with no contract
        salary = employee.get_current_salary()
        self.assertEqual(salary, 0.0)
        
        # Test with active contract
        contract = self.env['hr.contract'].create({
            'name': 'Test Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'state': 'open'
        })
        
        salary = employee.get_current_salary()
        self.assertEqual(salary, 50000.0)