# Ocean ERP - Indian HR Payroll Addon

## Overview

The `l10n_in_hr_payroll` addon provides comprehensive Indian HR payroll compliance for the Ocean ERP system, specifically designed for kids clothing retail businesses in India. This addon extends the core framework with Indian HR payroll-specific models, views, and functionality.

## Features

### 👥 Employee Management
- **Employee Information**: Complete employee profiles with Indian-specific fields
- **Indian Identifiers**: PAN, Aadhar, PF Number, ESI Number, UAN
- **Address Management**: Complete Indian address hierarchy
- **Contact Information**: Phone, mobile, email details
- **Kids Clothing Integration**: Age groups, sizes, seasons, brands, colors

### 📋 Contract Management
- **Contract Types**: Permanent, Temporary, Contract, Intern, Consultant
- **Salary Information**: Basic wage, wage type, salary structure
- **Indian Payroll Applicability**: PF, ESI, Professional Tax, Income Tax
- **Contract Workflow**: Draft → Running → Expired/Cancelled
- **Kids Clothing Integration**: Contract-specific kids clothing data

### 💰 Payslip Management
- **Payslip Generation**: Automated payslip creation and computation
- **Salary Components**: Basic wage, allowances, deductions
- **Indian Deductions**: PF, ESI, Professional Tax, Income Tax (TDS)
- **Payslip Workflow**: Draft → Verify → Done
- **Kids Clothing Integration**: Payslip-specific kids clothing data

### 📊 Payroll Calculations
- **PF Calculation**: 12% of basic wage, maximum 1800
- **ESI Calculation**: 0.75% of gross salary (if gross <= 21000)
- **Professional Tax**: State-specific professional tax
- **Income Tax**: Simplified TDS calculation
- **Net Salary**: Gross salary minus all deductions

## Models

### Core Models
- `hr.employee` - HR Employee with Indian localization
- `hr.contract` - HR Contract with Indian payroll
- `hr.payslip` - HR Payslip with Indian deductions
- `hr.payslip.line` - HR Payslip Line components

## Kids Clothing Integration

All models include kids clothing specific fields:

### Age Groups
- Baby (0-2 years)
- Toddler (2-4 years)
- Pre-school (4-6 years)
- Early School (6-8 years)
- Middle School (8-10 years)
- Late School (10-12 years)
- Teen (12-14 years)
- Young Adult (14-16 years)
- All Age Groups

### Sizes
- XS, S, M, L, XL, XXL, XXXL
- All Sizes

### Seasons
- Summer, Winter, Monsoon
- All Season

### Brands & Colors
- Custom brand and color fields
- Integration with kids clothing business logic

## Indian Payroll Components

### Provident Fund (PF)
- **Employee Contribution**: 12% of basic wage
- **Maximum Contribution**: ₹1,800 per month
- **PF Number Format**: State code + 7 digits + 3 digits
- **UAN**: Universal Account Number (12 digits)

### Employee State Insurance (ESI)
- **Employee Contribution**: 0.75% of gross salary
- **Applicability**: Only if gross salary ≤ ₹21,000
- **ESI Number**: 10-digit number
- **Coverage**: Medical and cash benefits

### Professional Tax
- **State-specific**: Varies by state
- **Maximum**: ₹200 per month
- **Calculation**: Based on salary slabs
- **Deduction**: Monthly from salary

### Income Tax (TDS)
- **Tax Exemption**: Up to ₹2,50,000 annually
- **Tax Rate**: 5% on taxable income
- **TDS Calculation**: Monthly deduction
- **Annual Return**: Form 16 generation

## Validation

### PAN Validation
- Format: ABCDE1234F (5 letters + 4 digits + 1 letter)
- Real-time validation with error messages

### Aadhar Validation
- Format: 12 digits
- Real-time validation with error messages

### PF Number Validation
- Format: State code + 7 digits + 3 digits
- State code validation

### ESI Number Validation
- Format: 10 digits
- Real-time validation with error messages

### UAN Validation
- Format: 12 digits
- Real-time validation with error messages

## Views

### Employee Views
- **Tree View**: List employees with Indian fields
- **Form View**: Complete employee form with validation
- **Search View**: Advanced search with filters

### Contract Views
- **Tree View**: List contracts with status
- **Form View**: Complete contract form with workflow
- **Search View**: Advanced search with filters

### Payslip Views
- **Tree View**: List payslips with status
- **Form View**: Complete payslip form with computation
- **Search View**: Advanced search with filters

## Static Assets

### CSS (`static/src/css/l10n_in_hr_payroll_style.css`)
- **HR Employee Styles**: Gradient headers, employee cards
- **HR Contract Styles**: Contract type badges, status indicators
- **HR Payslip Styles**: Payslip status badges, salary breakdown
- **Indian Payroll Styles**: PF/ESI info, tax information
- **Salary Calculation Styles**: Payroll breakdown, calculation display
- **Kids Clothing Styles**: Age group, size, season badges
- **Responsive Design**: Mobile-friendly layouts
- **Animations**: Fade-in effects, hover transitions

### JavaScript (`static/src/js/l10n_in_hr_payroll_script.js`)
- **HrEmployeeManager**: PAN, Aadhar, PF, ESI, UAN validation
- **HrContractManager**: Contract date validation, wage validation
- **HrPayslipManager**: Payslip date validation
- **IndianPayrollCalculator**: PF, ESI, tax calculations
- **Dashboard Integration**: HR data visualization
- **Utility Functions**: Indian currency and date formatting

## API Endpoints

### Employee API
- `GET /api/hr/employee-data` - Get HR employee data
- `POST /api/hr/validate-pan` - Validate PAN number
- `POST /api/hr/validate-aadhar` - Validate Aadhar number
- `POST /api/hr/validate-pf` - Validate PF number
- `POST /api/hr/validate-esi` - Validate ESI number
- `POST /api/hr/validate-uan` - Validate UAN

### Contract API
- `GET /api/hr/contract-data` - Get HR contract data
- `POST /api/hr/validate-contract-dates` - Validate contract dates
- `POST /api/hr/validate-wage` - Validate wage amount

### Payslip API
- `GET /api/hr/payslip-data` - Get HR payslip data
- `POST /api/hr/compute-payslip` - Compute payslip
- `POST /api/hr/verify-payslip` - Verify payslip
- `POST /api/hr/process-payslip` - Process payslip

### Payroll API
- `POST /api/hr/calculate-pf` - Calculate PF
- `POST /api/hr/calculate-esi` - Calculate ESI
- `POST /api/hr/calculate-tax` - Calculate tax
- `POST /api/hr/calculate-net-salary` - Calculate net salary

## Installation

1. Copy the `l10n_in_hr_payroll` addon to your Ocean ERP addons directory
2. Install the addon using the Ocean ERP CLI:
   ```bash
   ocean-cli addon install l10n_in_hr_payroll
   ```
3. The addon will automatically create Indian payroll configurations

## Dependencies

- `core_framework` - Ocean ERP core framework
- `core_base` - Base models and mixins
- `l10n_in` - Indian localization addon

## Usage

### Creating an Employee
```python
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
employee = self.env['hr.employee'].create(employee_vals)
```

### Creating a Contract
```python
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
contract = self.env['hr.contract'].create(contract_vals)
```

### Creating a Payslip
```python
payslip_vals = {
    'name': 'January 2024 Payslip',
    'employee_id': employee.id,
    'contract_id': contract.id,
    'date_from': '2024-01-01',
    'date_to': '2024-01-31',
    'age_group': '4-6',
    'size': 'm',
    'season': 'all_season',
    'brand': 'Kids Brand',
    'color': 'Blue',
}
payslip = self.env['hr.payslip'].create(payslip_vals)
```

### Payroll Calculations
```python
# Calculate PF
pf_amount = contract.calculate_pf()  # Returns PF amount

# Calculate ESI
esi_amount = contract.calculate_esi()  # Returns ESI amount

# Calculate net salary
net_salary = contract.calculate_net_salary()  # Returns net salary

# Get payroll breakdown
breakdown = contract.get_payroll_breakdown()
# Returns: {'gross': 50000, 'deductions': {...}, 'net': 45000}
```

### Filtering by Kids Clothing Criteria
```python
# Get employees for specific age group
baby_employees = self.env['hr.employee'].get_kids_clothing_employees(age_group='0-2')

# Get employees for specific size
medium_employees = self.env['hr.employee'].get_kids_clothing_employees(size='m')

# Get employees for specific season
summer_employees = self.env['hr.employee'].get_kids_clothing_employees(season='summer')
```

## Payroll Compliance

### PF Compliance
1. **Registration**: Register with EPFO
2. **Monthly Returns**: File monthly PF returns
3. **Annual Returns**: File annual PF returns
4. **UAN Management**: Maintain UAN for employees

### ESI Compliance
1. **Registration**: Register with ESIC
2. **Monthly Returns**: File monthly ESI returns
3. **Medical Benefits**: Provide medical benefits
4. **Cash Benefits**: Provide cash benefits

### Tax Compliance
1. **TDS Deduction**: Deduct TDS from salary
2. **TDS Returns**: File quarterly TDS returns
3. **Form 16**: Generate Form 16 for employees
4. **Annual Returns**: File annual tax returns

### Professional Tax Compliance
1. **State Registration**: Register with state tax authority
2. **Monthly Returns**: File monthly professional tax returns
3. **Certificate**: Obtain professional tax certificate
4. **Display**: Display certificate at workplace

## Testing

Run the test suite:
```bash
python -m pytest addons/l10n_in_hr_payroll/tests/
```

### Test Coverage
- Employee model tests
- Contract model tests
- Payslip model tests
- Validation tests
- Calculation tests
- Workflow tests
- Kids clothing integration tests

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This addon is part of the Ocean ERP system and follows the same licensing terms.

## Support

For support and questions:
- Check the Ocean ERP documentation
- Create an issue in the repository
- Contact the development team

## Changelog

### Version 1.0.0
- Initial release
- Complete Indian HR payroll compliance
- Kids clothing integration
- Comprehensive validation
- PF, ESI, tax calculations
- Static assets and JavaScript
- Test coverage