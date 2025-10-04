# Ocean ERP - Indian Localization Addon

## Overview

The `l10n_in` addon provides comprehensive Indian localization for the Ocean ERP system, specifically designed for kids clothing retail businesses. This addon extends the core framework with Indian-specific models, views, and functionality.

## Features

### 🏢 Company Management
- **Indian Company Types**: Private Limited, Public Limited, Partnership, Sole Proprietorship, LLP, Trust, Society, NGO
- **Registration Numbers**: CIN, PAN, TAN, GSTIN, IEC validation
- **Address Management**: Complete Indian address hierarchy (State → District → Taluka → Village)
- **Kids Clothing Integration**: Age groups, sizes, seasons, brands, colors

### 👥 Partner Management
- **Indian Partner Types**: Customer, Supplier, Employee, Contact
- **Tax Identifiers**: PAN, GSTIN, Aadhar validation
- **Business Information**: Nature of business, industry type
- **Kids Clothing Specific**: Age groups, sizes, seasons, brands, colors

### 🗺️ Geographic Management
- **States**: Complete Indian states with Union Territories
- **Districts**: District-level management
- **Talukas**: Taluka/Tehsil/Block management
- **Villages**: Village-level granularity
- **Kids Clothing Integration**: Geographic-specific kids clothing data

### 🏦 Banking System
- **Bank Types**: Public Sector, Private Sector, Foreign, Cooperative, Payment, Small Finance Banks
- **IFSC/MICR**: Indian Financial System Code and MICR validation
- **Branch Management**: Complete branch hierarchy
- **Kids Clothing Integration**: Bank-specific kids clothing preferences

### 💱 Currency & Language
- **Indian Currency**: INR with proper formatting
- **Indian Languages**: Official, Regional, Local, Foreign language support
- **Kids Clothing Integration**: Currency and language-specific kids clothing data

## Models

### Core Models
- `res.company` - Indian Company with localization
- `res.partner` - Indian Partner with localization
- `res.country.state` - Indian States
- `res.country.district` - Indian Districts
- `res.country.taluka` - Indian Talukas
- `res.country.village` - Indian Villages
- `res.currency` - Indian Currency
- `res.language` - Indian Languages
- `res.bank` - Indian Banks
- `res.bank.branch` - Indian Bank Branches

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

## Validation

### PAN Validation
- Format: ABCDE1234F (5 letters + 4 digits + 1 letter)
- Real-time validation with error messages

### GSTIN Validation
- Format: 12ABCDE1234F1Z5 (2 digits + 5 letters + 4 digits + 1 letter + 1 letter + 1 letter + 1 letter)
- State code validation

### CIN Validation
- Format: A12345BC6789DEF012345 (1 letter + 5 digits + 2 letters + 4 digits + 3 letters + 6 digits)
- Corporate identification validation

### IFSC Validation
- Format: ABCD0123456 (4 letters + 0 + 6 alphanumeric)
- Bank and branch identification

### MICR Validation
- Format: 9 digits
- Magnetic ink character recognition

## Views

### Company Views
- **Tree View**: List companies with Indian fields
- **Form View**: Complete company form with validation
- **Search View**: Advanced search with filters

### Partner Views
- **Tree View**: List partners with Indian fields
- **Form View**: Complete partner form with validation
- **Search View**: Advanced search with filters

### Geographic Views
- **Hierarchical Views**: State → District → Taluka → Village
- **Cascading Dropdowns**: Automatic loading of dependent data
- **Kids Clothing Integration**: Geographic-specific kids clothing data

### Banking Views
- **Bank Management**: Complete bank and branch management
- **IFSC/MICR Validation**: Real-time validation
- **Kids Clothing Integration**: Bank-specific kids clothing preferences

## Static Assets

### CSS (`static/src/css/l10n_in_style.css`)
- **Company Styles**: Gradient headers, info cards
- **Partner Styles**: Hover effects, card layouts
- **Geographic Styles**: Tree-like hierarchical display
- **Banking Styles**: Bank cards with gradients
- **Kids Clothing Badges**: Age group, size, season badges
- **Responsive Design**: Mobile-friendly layouts
- **Animations**: Fade-in effects, hover transitions

### JavaScript (`static/src/js/l10n_in_script.js`)
- **CompanyManager**: PAN, GSTIN, CIN validation
- **GeographicManager**: Cascading dropdowns
- **BankingManager**: IFSC, MICR validation
- **Dashboard Integration**: Kids clothing data visualization
- **Utility Functions**: Indian currency and date formatting

## API Endpoints

### Company API
- `GET /api/companies/kids-clothing-data` - Get kids clothing company data
- `POST /api/companies/validate-pan` - Validate PAN number
- `POST /api/companies/validate-gstin` - Validate GSTIN

### Geographic API
- `GET /api/districts?state_id={id}` - Get districts by state
- `GET /api/talukas?district_id={id}` - Get talukas by district
- `GET /api/villages?taluka_id={id}` - Get villages by taluka
- `GET /api/geographic/kids-clothing-data` - Get geographic kids clothing data

### Banking API
- `GET /api/banking/kids-clothing-data` - Get banking kids clothing data
- `POST /api/banking/validate-ifsc` - Validate IFSC code
- `POST /api/banking/validate-micr` - Validate MICR code

## Installation

1. Copy the `l10n_in` addon to your Ocean ERP addons directory
2. Install the addon using the Ocean ERP CLI:
   ```bash
   ocean-cli addon install l10n_in
   ```
3. The addon will automatically create Indian localization data

## Dependencies

- `core_framework` - Ocean ERP core framework
- `core_base` - Base models and mixins

## Usage

### Creating a Company
```python
company_vals = {
    'name': 'Kids Clothing Store',
    'company_type': 'private_limited',
    'pan': 'ABCDE1234F',
    'gstin': '12ABCDE1234F1Z5',
    'cin': 'A12345BC6789DEF012345',
    'business_nature': 'retail',
    'industry_type': 'kids_clothing',
    'age_group': '4-6',
    'size': 'm',
    'season': 'all_season',
    'brand': 'Kids Brand',
    'color': 'Blue',
}
company = self.env['res.company'].create(company_vals)
```

### Filtering by Kids Clothing Criteria
```python
# Get companies for specific age group
baby_companies = self.env['res.company'].get_kids_clothing_companies(age_group='0-2')

# Get companies for specific size
medium_companies = self.env['res.company'].get_kids_clothing_companies(size='m')

# Get companies for specific season
summer_companies = self.env['res.company'].get_kids_clothing_companies(season='summer')
```

### Geographic Hierarchy
```python
# Get districts for a state
districts = self.env['res.country.district'].search([('state_id', '=', state_id)])

# Get talukas for a district
talukas = self.env['res.country.taluka'].search([('district_id', '=', district_id)])

# Get villages for a taluka
villages = self.env['res.country.village'].search([('taluka_id', '=', taluka_id)])
```

## Testing

Run the test suite:
```bash
python -m pytest addons/l10n_in/tests/
```

### Test Coverage
- Company model tests
- Partner model tests
- Geographic model tests
- Banking model tests
- Validation tests
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
- Complete Indian localization
- Kids clothing integration
- Comprehensive validation
- Geographic hierarchy
- Banking system
- Static assets and JavaScript
- Test coverage