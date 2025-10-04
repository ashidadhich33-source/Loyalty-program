# Ocean ERP - Stock Management Addon

## Overview

The Stock Management addon provides comprehensive inventory management capabilities for the Ocean ERP system, specifically designed for kids clothing retail businesses.

## Features

### Stock Alert Management
- Real-time stock level monitoring
- Automated alert generation for low stock, out of stock, and overstock situations
- Priority-based alert system (Low, Medium, High, Urgent)
- Alert status tracking (Draft, Active, Resolved, Cancelled)
- Kids clothing specific alerts (size, brand, color, seasonal)

### Reorder Rules
- Automated reorder point management
- Economic Order Quantity (EOQ) calculations
- Safety stock management
- Lead time considerations
- Kids clothing specific reorder rules

### Stock Adjustments
- Physical inventory count management
- Stock adjustment workflows with approval processes
- Damage, theft, and expiry tracking
- Seasonal adjustments for kids clothing
- Quality control adjustments

### Stock Analysis
- Turnover analysis by age group, size, season, brand, and color
- Aging analysis for inventory management
- ABC and XYZ analysis for kids clothing
- Seasonal trend analysis
- Profitability analysis by product attributes

## Models

### StockAlert
- **Purpose**: Stock alert management
- **Key Fields**: name, product_id, alert_type, priority, status, current_stock
- **Kids Clothing Fields**: age_group, size, season, brand, color

### ReorderRule
- **Purpose**: Automated reorder management
- **Key Fields**: product_id, minimum_stock, maximum_stock, reorder_quantity, lead_time
- **Kids Clothing Fields**: age_group, size, season, brand, color

### StockAdjustment
- **Purpose**: Stock adjustment management
- **Key Fields**: name, adjustment_type, status, total_amount
- **Kids Clothing Fields**: age_group, size, season, brand, color

### StockAnalysis
- **Purpose**: Stock analysis and reporting
- **Key Fields**: name, analysis_type, date_from, date_to
- **Kids Clothing Fields**: age_group, size, season, brand, color

## Views

### Tree Views
- `stock.alert.tree` - Stock alerts tree view
- `reorder.rule.tree` - Reorder rules tree view
- `stock.adjustment.tree` - Stock adjustments tree view
- `stock.analysis.tree` - Stock analysis tree view

### Form Views
- `stock.alert.form` - Stock alert form view
- `reorder.rule.form` - Reorder rule form view
- `stock.adjustment.form` - Stock adjustment form view
- `stock.analysis.form` - Stock analysis form view

### Search Views
- `stock.alert.search` - Stock alert search view
- `reorder.rule.search` - Reorder rule search view
- `stock.adjustment.search` - Stock adjustment search view
- `stock.analysis.search` - Stock analysis search view

### Kanban Views
- `stock.alert.kanban` - Stock alert kanban view
- `reorder.rule.kanban` - Reorder rule kanban view
- `stock.adjustment.kanban` - Stock adjustment kanban view
- `stock.analysis.kanban` - Stock analysis kanban view

## Actions

### ActWindow Actions
- `action_stock_alert` - Stock alerts action
- `action_reorder_rule` - Reorder rules action
- `action_stock_adjustment` - Stock adjustments action
- `action_stock_analysis` - Stock analysis action

## Static Assets

### CSS
- `stock_management_style.css` - Styling for stock management components
- Alert priority and status styling
- Kids clothing specific styling
- Responsive design

### JavaScript
- `stock_management_script.js` - JavaScript functionality
- Form validation and interaction
- Dashboard data loading
- Real-time updates

## Tests

### Unit Tests
- `test_stock_alert.py` - Stock alert model tests
- `test_reorder_rule.py` - Reorder rule model tests
- `test_stock_adjustment.py` - Stock adjustment model tests
- `test_stock_analysis.py` - Stock analysis model tests

## Usage

### Creating Stock Alerts
```python
alert = self.env['stock.alert'].create({
    'name': 'Low Stock Alert',
    'product_id': product.id,
    'alert_type': 'low_stock',
    'priority': 'medium',
    'current_stock': 10.0,
    'minimum_stock': 20.0,
    'age_group': '0-2',
    'size': 's',
    'season': 'summer',
    'brand': 'Kids Brand',
    'color': 'Blue',
})
```

### Creating Reorder Rules
```python
rule = self.env['stock.reorder.rule'].create({
    'product_id': product.id,
    'minimum_stock': 20.0,
    'maximum_stock': 100.0,
    'reorder_quantity': 50.0,
    'lead_time': 7,
    'age_group': '0-2',
    'season': 'summer',
})
```

### Filtering by Kids Clothing Criteria
```python
baby_alerts = self.env['stock.alert'].get_kids_clothing_alerts(
    age_group='0-2',
    season='summer',
    brand='Kids Brand'
)
```

## Dependencies

- `core_framework` - Ocean ERP core framework
- `products` - Product management
- `warehouse` - Warehouse management
- `contacts` - Contact management
- `purchase` - Purchase management

## Installation

The stock management addon is automatically installed when the Ocean ERP system starts up, as it's a core component of the inventory management system.

## Configuration

### Stock Alerts
Configure stock alert thresholds in the Stock Alerts menu to set up automated monitoring.

### Reorder Rules
Set up reorder rules in the Reorder Rules menu to automate purchase order generation.

### Stock Adjustments
Configure stock adjustment workflows in the Stock Adjustments menu.

## API Endpoints

### REST API
- `GET /api/stock/alerts` - List stock alerts
- `POST /api/stock/alerts` - Create stock alert
- `GET /api/stock/alerts/{id}` - Get stock alert details
- `PUT /api/stock/alerts/{id}` - Update stock alert
- `DELETE /api/stock/alerts/{id}` - Delete stock alert

### Statistics
- `GET /api/stock/statistics/alerts` - Alert statistics
- `GET /api/stock/statistics/stock` - Stock statistics
- `GET /api/stock/statistics/reorder` - Reorder statistics

## Security

### Access Control
- Stock management permissions
- Read/write access control
- Company-based data isolation

### Data Validation
- Stock level validation
- Alert priority validation
- Required field validation

## Performance

### Optimization
- Efficient stock level computation
- Cached alert calculations
- Optimized database queries

### Monitoring
- Stock level monitoring
- Alert generation tracking
- Performance metrics

## Troubleshooting

### Common Issues
1. **Stock level discrepancies**: Verify inventory counts and adjustments
2. **Alert not generated**: Check alert thresholds and product configuration
3. **Reorder rule not working**: Verify product and supplier settings

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
python -m pytest addons/stock_management/tests/
```

## License

This addon is part of the Ocean ERP system and follows the same licensing terms.

## Support

For support and questions about the stock management addon, please refer to the Ocean ERP documentation or contact the development team.