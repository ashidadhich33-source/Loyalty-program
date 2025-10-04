# -*- coding: utf-8 -*-

from ocean.tests.common import TransactionCase
from ocean.exceptions import ValidationError, UserError


class TestHrEmployee(TransactionCase):
    
    def setUp(self):
        super(TestHrEmployee, self).setUp()
        self.employee_model = self.env['hr.employee']
        self.department_model = self.env['hr.department']
        self.job_model = self.env['hr.job']
        
        # Create test department
        self.test_department = self.department_model.create({
            'name': 'Test Department',
            'code': 'TEST_DEPT',
        })
        
        # Create test job
        self.test_job = self.job_model.create({
            'name': 'Test Job',
            'code': 'TEST_JOB',
        })
    
    def test_employee_creation(self):
        """Test employee creation"""
        employee = self.employee_model.create({
            'first_name': 'John',
            'last_name': 'Doe',
            'gender': 'male',
            'birth_date': '1990-01-01',
            'department_id': self.test_department.id,
            'job_id': self.test_job.id,
            'age_group_specialization': 'kids',
            'season_preference': 'summer',
        })
        
        self.assertEqual(employee.name, 'John Doe')
        self.assertEqual(employee.age_group_specialization, 'kids')
        self.assertEqual(employee.season_preference, 'summer')
        self.assertEqual(employee.state, 'draft')
    
    def test_employee_activation(self):
        """Test employee activation"""
        employee = self.employee_model.create({
            'first_name': 'Jane',
            'last_name': 'Smith',
            'gender': 'female',
            'department_id': self.test_department.id,
            'job_id': self.test_job.id,
        })
        
        employee.action_activate()
        self.assertEqual(employee.state, 'active')
    
    def test_employee_termination(self):
        """Test employee termination"""
        employee = self.employee_model.create({
            'first_name': 'Bob',
            'last_name': 'Johnson',
            'gender': 'male',
            'department_id': self.test_department.id,
            'job_id': self.test_job.id,
            'state': 'active',
        })
        
        employee.action_terminate()
        self.assertEqual(employee.state, 'terminated')
        self.assertTrue(employee.termination_date)
    
    def test_pan_number_validation(self):
        """Test PAN number validation"""
        with self.assertRaises(ValidationError):
            self.employee_model.create({
                'first_name': 'Test',
                'last_name': 'Employee',
                'pan_number': 'INVALID',  # Invalid PAN
                'department_id': self.test_department.id,
                'job_id': self.test_job.id,
            })
    
    def test_aadhar_number_validation(self):
        """Test Aadhar number validation"""
        with self.assertRaises(ValidationError):
            self.employee_model.create({
                'first_name': 'Test',
                'last_name': 'Employee',
                'aadhar_number': '123',  # Invalid Aadhar
                'department_id': self.test_department.id,
                'job_id': self.test_job.id,
            })