# Ocean ERP - Accounting Addon

## Overview

The Accounting addon provides comprehensive financial management capabilities for the Ocean ERP system, specifically designed for kids clothing retail businesses.

## Features

### Chart of Accounts Management
- Complete chart of accounts structure with hierarchy
- Account types (Assets, Liabilities, Equity, Income, Expenses)
- Account subtypes for detailed categorization
- Kids clothing specific accounts (Inventory, Sales, Cost of Goods Sold)
- Multi-currency support and account reconciliation
- Account analytics and reporting capabilities

### Kids Clothing Specific Features
- Age-group specific accounting (baby, toddler, teen)
- Seasonal accounting periods (summer, winter, monsoon)
- Size-wise cost tracking (XS, S, M, L, XL, XXL, XXXL)
- Brand-wise profitability analysis
- Color-wise sales tracking
- Special occasion accounting (festivals, back-to-school)
- Growth-based accounting adjustments
- Quality control cost tracking

## Models

### AccountAccount
- **Purpose**: Chart of accounts management
- **Key Fields**: name, code, account_type, account_subtype, parent_id, balance
- **Kids Clothing Fields**: age_group, size, season, brand, color

### AccountAccountType
- **Purpose**: Account type definitions
- **Key Fields**: name, type, sequence, include_initial_balance, reconcile
- **Kids Clothing Fields**: age_group, season, brand, color

## Views

### Tree Views
- `account.account.tree` - Chart of accounts tree view
- `account.account.type.tree` - Account types tree view

### Form Views
- `account.account.form` - Account form view
- `account.account.type.form` - Account type form view

### Search Views
- `account.account.search` - Account search view

### Kanban Views
- `account.account.kanban` - Account kanban view

## Actions

### ActWindow Actions
- `action_account_account` - Chart of accounts action
- `action_account_account_type` - Account types action

## Static Assets

### CSS
- `accounting_style.css` - Styling for accounting components
- Account type specific styling
- Kids clothing specific styling
- Responsive design

### JavaScript
- `accounting_script.js` - JavaScript functionality
- Form validation and interaction
- Dashboard data loading
- Real-time updates

## Tests

### Unit Tests
- `test_account_account.py` - Account model tests
- Account creation and validation tests
- Hierarchy and balance computation tests
- Kids clothing specific tests

## Usage

### Creating Accounts
```python
account = self.env['account.account'].create({
    'name': 'Kids Clothing Sales',
    'code': '4100',
    'account_type': 'income',
    'account_subtype': 'sales',
    'age_group': 'all',
    'season': 'all_season',
    'brand': 'Kids Brand',
    'color': 'Blue',
})
```

### Filtering by Kids Clothing Criteria
```python
baby_accounts = self.env['account.account'].get_kids_clothing_accounts(
    age_group='0-2',
    season='summer',
    brand='Kids Brand'
)
```

## Dependencies

- `core_framework` - Ocean ERP core framework
- `users` - User management
- `company` - Company management
- `contacts` - Contact management
- `products` - Product management

## Installation

The accounting addon is automatically installed when the Ocean ERP system starts up, as it's a core component of the financial management system.

## Configuration

### Account Types
Configure account types in the Account Types menu to define the categories for your chart of accounts.

### Chart of Accounts
Set up your chart of accounts in the Chart of Accounts menu, organizing accounts by type and hierarchy.

## API Endpoints

### REST API
- `GET /api/accounting/accounts` - List accounts
- `POST /api/accounting/accounts` - Create account
- `GET /api/accounting/accounts/{id}` - Get account details
- `PUT /api/accounting/accounts/{id}` - Update account
- `DELETE /api/accounting/accounts/{id}` - Delete account

### Statistics
- `GET /api/accounting/statistics/accounts` - Account statistics
- `GET /api/accounting/statistics/journals` - Journal statistics
- `GET /api/accounting/statistics/periods` - Period statistics

## Security

### Access Control
- Account management permissions
- Read/write access control
- Company-based data isolation

### Data Validation
- Account code uniqueness validation
- Circular reference prevention
- Required field validation

## Performance

### Optimization
- Efficient balance computation
- Cached account hierarchy
- Optimized database queries

### Monitoring
- Account balance monitoring
- Transaction volume tracking
- Performance metrics

## Troubleshooting

### Common Issues
1. **Account code conflicts**: Ensure unique codes within company
2. **Circular references**: Check parent-child relationships
3. **Balance discrepancies**: Verify move line calculations

### Debug Mode
Enable debug mode in Ocean ERP configuration to see detailed error messages and SQL queries.

## Contributing

### Development Guidelines
- Follow Ocean ERP coding standards
- Write comprehensive tests
- Document all new features
- Use proper error handling

### Testing
Run tests using the Ocean ERP test framework:
```bash
python -m pytest addons/accounting/tests/
```

## License

This addon is part of the Ocean ERP system and follows the same licensing terms.

## Support

For support and questions about the accounting addon, please refer to the Ocean ERP documentation or contact the development team.