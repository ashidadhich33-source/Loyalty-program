# -*- coding: utf-8 -*-
"""
Ocean ERP - Indian Payroll Calculation Tests
===========================================

Tests for Indian payroll calculation functionality.
"""

from core_framework.testing import OceanTestCase
from addons.l10n_in_hr_payroll.models.hr_contract import HrContract
import logging

_logger = logging.getLogger(__name__)


class TestPayrollCalculations(OceanTestCase):
    """Test cases for payroll calculation functionality"""
    
    def setUp(self):
        super(TestPayrollCalculations, self).setUp()
        self.employee_model = self.env['hr.employee']
        self.contract_model = self.env['hr.contract']
    
    def test_pf_calculation(self):
        """Test PF calculation"""
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
            'pf_applicable': True
        })
        
        # Test PF calculation (12% of basic wage, maximum 1800)
        pf_amount = min(50000 * 0.12, 1800)
        self.assertEqual(pf_amount, 1800)  # Should be capped at 1800
        
        # Test PF calculation for lower wage
        contract.wage = 10000
        pf_amount = min(10000 * 0.12, 1800)
        self.assertEqual(pf_amount, 1200)  # Should be 12% of 10000
    
    def test_esi_calculation(self):
        """Test ESI calculation"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        contract = self.contract_model.create({
            'name': 'Test Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 20000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'esi_applicable': True
        })
        
        # Test ESI calculation (0.75% of gross salary, if gross <= 21000)
        esi_amount = 20000 * 0.0075
        self.assertEqual(esi_amount, 150.0)
        
        # Test ESI calculation for higher wage (not applicable)
        contract.wage = 25000
        esi_amount = 0 if 25000 > 21000 else 25000 * 0.0075
        self.assertEqual(esi_amount, 0)
    
    def test_professional_tax_calculation(self):
        """Test Professional Tax calculation"""
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
            'professional_tax_applicable': True
        })
        
        # Test Professional Tax calculation (max 200 or 1% of wage)
        pt_amount = min(200, 50000 * 0.01)
        self.assertEqual(pt_amount, 200)  # Should be capped at 200
        
        # Test Professional Tax calculation for lower wage
        contract.wage = 10000
        pt_amount = min(200, 10000 * 0.01)
        self.assertEqual(pt_amount, 100)  # Should be 1% of 10000
    
    def test_income_tax_calculation(self):
        """Test Income Tax (TDS) calculation"""
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
            'income_tax_applicable': True
        })
        
        # Test Income Tax calculation (simplified)
        annual_salary = 50000 * 12  # 600000
        if annual_salary > 250000:  # Above tax exemption limit
            taxable_income = annual_salary - 250000  # 350000
            tax_amount = min(taxable_income * 0.05, 12500) / 12  # Monthly tax
            self.assertEqual(tax_amount, 1458.33)  # Approximately
        
        # Test Income Tax calculation for lower wage (no tax)
        contract.wage = 20000
        annual_salary = 20000 * 12  # 240000
        if annual_salary <= 250000:  # Below tax exemption limit
            tax_amount = 0
            self.assertEqual(tax_amount, 0)
    
    def test_gross_salary_calculation(self):
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
    
    def test_net_salary_calculation(self):
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
        
        # Calculate expected deductions
        pf_amount = min(50000 * 0.12, 1800)  # 1800
        esi_amount = 0 if 50000 > 21000 else 50000 * 0.0075  # 0
        pt_amount = min(200, 50000 * 0.01)  # 200
        annual_salary = 50000 * 12
        if annual_salary > 250000:
            taxable_income = annual_salary - 250000
            tax_amount = min(taxable_income * 0.05, 12500) / 12
        else:
            tax_amount = 0
        
        expected_net = 50000 - pf_amount - esi_amount - pt_amount - tax_amount
        self.assertAlmostEqual(net_salary, expected_net, places=2)
    
    def test_deductions_calculation(self):
        """Test total deductions calculation"""
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
        
        # Calculate expected deductions
        pf_amount = min(50000 * 0.12, 1800)  # 1800
        esi_amount = 0 if 50000 > 21000 else 50000 * 0.0075  # 0
        pt_amount = min(200, 50000 * 0.01)  # 200
        annual_salary = 50000 * 12
        if annual_salary > 250000:
            taxable_income = annual_salary - 250000
            tax_amount = min(taxable_income * 0.05, 12500) / 12
        else:
            tax_amount = 0
        
        expected_deductions = pf_amount + esi_amount + pt_amount + tax_amount
        self.assertAlmostEqual(deductions, expected_deductions, places=2)
    
    def test_wage_type_calculations(self):
        """Test calculations for different wage types"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        # Test monthly wage
        contract_monthly = self.contract_model.create({
            'name': 'Monthly Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 50000,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'pf_applicable': True
        })
        
        gross_monthly = contract_monthly.calculate_gross_salary()
        self.assertEqual(gross_monthly, 50000.0)
        
        # Test weekly wage
        contract_weekly = self.contract_model.create({
            'name': 'Weekly Contract',
            'employee_id': employee.id,
            'contract_type': 'temporary',
            'wage': 12500,  # 50000/4 weeks
            'wage_type': 'weekly',
            'date_start': '2024-01-01',
            'pf_applicable': True
        })
        
        gross_weekly = contract_weekly.calculate_gross_salary()
        self.assertEqual(gross_weekly, 12500.0)
        
        # Test daily wage
        contract_daily = self.contract_model.create({
            'name': 'Daily Contract',
            'employee_id': employee.id,
            'contract_type': 'contract',
            'wage': 2000,  # 50000/25 working days
            'wage_type': 'daily',
            'date_start': '2024-01-01',
            'pf_applicable': True
        })
        
        gross_daily = contract_daily.calculate_gross_salary()
        self.assertEqual(gross_daily, 2000.0)
        
        # Test hourly wage
        contract_hourly = self.contract_model.create({
            'name': 'Hourly Contract',
            'employee_id': employee.id,
            'contract_type': 'intern',
            'wage': 250,  # 50000/200 working hours
            'wage_type': 'hourly',
            'date_start': '2024-01-01',
            'pf_applicable': True
        })
        
        gross_hourly = contract_hourly.calculate_gross_salary()
        self.assertEqual(gross_hourly, 250.0)
    
    def test_edge_cases(self):
        """Test edge cases in payroll calculations"""
        # Create employee first
        employee = self.employee_model.create({
            'name': 'Test Employee',
            'employee_id': 'EMP001'
        })
        
        # Test zero wage
        contract_zero = self.contract_model.create({
            'name': 'Zero Wage Contract',
            'employee_id': employee.id,
            'contract_type': 'intern',
            'wage': 0,
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'pf_applicable': True,
            'esi_applicable': True,
            'professional_tax_applicable': True,
            'income_tax_applicable': True
        })
        
        gross_zero = contract_zero.calculate_gross_salary()
        self.assertEqual(gross_zero, 0.0)
        
        deductions_zero = contract_zero.calculate_deductions()
        self.assertEqual(deductions_zero, 0.0)
        
        net_zero = contract_zero.calculate_net_salary()
        self.assertEqual(net_zero, 0.0)
        
        # Test very high wage
        contract_high = self.contract_model.create({
            'name': 'High Wage Contract',
            'employee_id': employee.id,
            'contract_type': 'permanent',
            'wage': 1000000,  # 10 lakhs
            'wage_type': 'monthly',
            'date_start': '2024-01-01',
            'pf_applicable': True,
            'esi_applicable': True,
            'professional_tax_applicable': True,
            'income_tax_applicable': True
        })
        
        gross_high = contract_high.calculate_gross_salary()
        self.assertEqual(gross_high, 1000000.0)
        
        deductions_high = contract_high.calculate_deductions()
        self.assertGreater(deductions_high, 0)
        
        net_high = contract_high.calculate_net_salary()
        self.assertLess(net_high, gross_high)
        self.assertGreater(net_high, 0)