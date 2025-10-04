# Ocean ERP - Indian GST Addon

## Overview

The `l10n_in_gst` addon provides comprehensive GST (Goods and Services Tax) compliance for the Ocean ERP system, specifically designed for kids clothing retail businesses in India. This addon extends the core framework with Indian GST-specific models, views, and functionality.

## Features

### 🧾 Tax Management
- **GST Tax Types**: CGST, SGST, IGST, CESS, and other tax types
- **Tax Groups**: Organized tax groups by GST rates (0%, 5%, 12%, 18%, 28%)
- **HSN/SAC Codes**: Harmonized System of Nomenclature and Service Accounting Code support
- **Kids Clothing Integration**: Age groups, sizes, seasons, brands, colors

### 📋 GST Returns
- **GSTR Forms**: GSTR-1, GSTR-2, GSTR-3, GSTR-4, GSTR-5, GSTR-6, GSTR-7, GSTR-8, GSTR-9, GSTR-10
- **Return Periods**: Monthly return period management
- **Filing Status**: Draft, Ready, Filed, Accepted, Rejected status tracking
- **Acknowledgment**: GST portal acknowledgment number and date tracking

### 📊 GST Reports
- **GST Summary**: Comprehensive GST summary reports
- **GST Liability**: Tax liability analysis
- **Input/Output Tax**: Input and output tax reports
- **GST Reconciliation**: Tax reconciliation reports
- **GST Audit**: Audit trail and compliance reports
- **GST Compliance**: Compliance status and monitoring

### 🏢 Fiscal Positions
- **Inter/Intra State**: Inter-state and intra-state fiscal positions
- **Export/Import**: Export and import fiscal positions
- **SEZ**: Special Economic Zone fiscal positions
- **Deemed Export**: Deemed export fiscal positions

## Models

### Core Models
- `account.tax` - GST Tax with localization
- `account.tax.group` - GST Tax Groups
- `account.fiscal.position` - GST Fiscal Positions
- `account.fiscal.position.tax` - GST Fiscal Position Tax Mappings
- `gst.return` - GST Returns
- `gst.report` - GST Reports

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

## GST Tax Types

### CGST (Central GST)
- Central government tax
- Applicable for intra-state transactions
- Rate: 50% of total GST rate

### SGST (State GST)
- State government tax
- Applicable for intra-state transactions
- Rate: 50% of total GST rate

### IGST (Integrated GST)
- Central government tax
- Applicable for inter-state transactions
- Rate: 100% of total GST rate

### CESS
- Additional tax on specific goods
- Rate: Varies by product category

## GST Return Types

### GSTR-1
- Outward supplies return
- Filed by regular taxpayers
- Due date: 11th of next month

### GSTR-2
- Inward supplies return
- Filed by regular taxpayers
- Due date: 15th of next month

### GSTR-3
- Monthly return
- Filed by regular taxpayers
- Due date: 20th of next month

### GSTR-4
- Quarterly return
- Filed by composition taxpayers
- Due date: 18th of next quarter

### GSTR-5
- Non-resident taxpayer return
- Filed by non-resident taxpayers
- Due date: 20th of next month

## Validation

### HSN Code Validation
- Format: 4-8 digits
- Real-time validation with error messages
- Integration with GST portal

### SAC Code Validation
- Format: 6 digits
- Real-time validation with error messages
- Service-specific validation

### GST Rate Validation
- Standard rates: 0%, 5%, 12%, 18%, 28%
- Custom rates for specific products
- Rate calculation validation

## Views

### Tax Views
- **Tree View**: List GST taxes with Indian fields
- **Form View**: Complete tax form with validation
- **Search View**: Advanced search with filters

### Return Views
- **Tree View**: List GST returns with status
- **Form View**: Complete return form with workflow
- **Search View**: Advanced search with filters

### Report Views
- **Tree View**: List GST reports with status
- **Form View**: Complete report form with generation
- **Search View**: Advanced search with filters

## Static Assets

### CSS (`static/src/css/l10n_in_gst_style.css`)
- **GST Tax Styles**: Gradient headers, tax cards
- **GST Return Styles**: Status indicators, return cards
- **GST Report Styles**: Report cards, type badges
- **HSN/SAC Code Styles**: Monospace formatting
- **GST Calculation Styles**: Calculation display
- **GST Dashboard Styles**: Dashboard grids and cards
- **Kids Clothing Styles**: Age group, size, season badges
- **Responsive Design**: Mobile-friendly layouts
- **Animations**: Fade-in effects, hover transitions

### JavaScript (`static/src/js/l10n_in_gst_script.js`)
- **GstTaxManager**: HSN/SAC validation, tax calculations
- **GstReturnManager**: Return period validation
- **GstReportManager**: Date range validation
- **GstCalculationUtility**: GST amount calculations
- **GstPortalIntegration**: GST portal status checking
- **Dashboard Integration**: GST data visualization
- **Utility Functions**: GST formatting and validation

## API Endpoints

### Tax API
- `GET /api/gst/tax-data` - Get GST tax data
- `POST /api/gst/validate-hsn` - Validate HSN code
- `POST /api/gst/validate-sac` - Validate SAC code

### Return API
- `GET /api/gst/return-data` - Get GST return data
- `POST /api/gst/prepare-return` - Prepare GST return
- `POST /api/gst/file-return` - File GST return

### Report API
- `GET /api/gst/report-data` - Get GST report data
- `POST /api/gst/generate-report` - Generate GST report

### Portal API
- `GET /api/gst/portal-status` - Get GST portal status
- `POST /api/gst/sync-data` - Sync data with GST portal

## Installation

1. Copy the `l10n_in_gst` addon to your Ocean ERP addons directory
2. Install the addon using the Ocean ERP CLI:
   ```bash
   ocean-cli addon install l10n_in_gst
   ```
3. The addon will automatically create GST tax configurations

## Dependencies

- `core_framework` - Ocean ERP core framework
- `core_base` - Base models and mixins
- `l10n_in` - Indian localization addon

## Usage

### Creating a GST Tax
```python
tax_vals = {
    'name': 'GST 18%',
    'tax_type': 'gst',
    'gst_type': 'cgst',
    'amount': 18.0,
    'amount_type': 'percent',
    'gst_rate': 18.0,
    'hsn_code': '6203',
    'age_group': '4-6',
    'size': 'm',
    'season': 'all_season',
    'brand': 'Kids Brand',
    'color': 'Blue',
}
tax = self.env['account.tax'].create(tax_vals)
```

### Creating a GST Return
```python
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
gst_return = self.env['gst.return'].create(return_vals)
```

### Calculating GST
```python
# Calculate GST amount
gst_amount = tax.compute_gst_amount(1000.0)  # Returns 180.0 for 18% tax

# Get GST breakdown
breakdown = tax.get_gst_breakdown(1000.0)
# Returns: {'igst': 180.0, 'cgst': 0, 'sgst': 0, 'cess': 0, 'total': 1180.0}
```

### Filtering by Kids Clothing Criteria
```python
# Get taxes for specific age group
baby_taxes = self.env['account.tax'].get_kids_clothing_taxes(age_group='0-2')

# Get taxes for specific size
medium_taxes = self.env['account.tax'].get_kids_clothing_taxes(size='m')

# Get taxes for specific season
summer_taxes = self.env['account.tax'].get_kids_clothing_taxes(season='summer')
```

## GST Compliance

### Return Filing
1. **Prepare Return**: Generate return data from transactions
2. **Validate Data**: Check for errors and inconsistencies
3. **File Return**: Submit to GST portal
4. **Track Status**: Monitor acknowledgment and acceptance

### Report Generation
1. **Select Report Type**: Choose from available report types
2. **Set Date Range**: Define the reporting period
3. **Generate Report**: Create the report with data
4. **Export/Print**: Export or print the report

### Tax Calculations
1. **Base Amount**: Enter the base amount
2. **Select Tax**: Choose the appropriate GST tax
3. **Calculate**: Automatically calculate GST amounts
4. **Breakdown**: View detailed tax breakdown

## Testing

Run the test suite:
```bash
python -m pytest addons/l10n_in_gst/tests/
```

### Test Coverage
- Tax model tests
- Tax group model tests
- GST return model tests
- GST report model tests
- Validation tests
- Calculation tests
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
- Complete GST compliance
- Kids clothing integration
- Comprehensive validation
- GST returns and reports
- Static assets and JavaScript
- Test coverage