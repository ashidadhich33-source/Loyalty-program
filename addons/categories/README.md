# Product Categories Addon

## Overview
The Product Categories addon provides comprehensive product categorization system specifically designed for kids clothing retail. It offers hierarchical category management, templates, rules, and analytics to help organize and manage product categories effectively.

## Features

### Core Functionality
- **Hierarchical Categories**: Create parent-child category relationships
- **Category Templates**: Predefined templates for quick category creation
- **Category Rules**: Automated categorization based on conditions
- **Category Analytics**: Performance tracking and reporting
- **Category Tags**: Flexible tagging system for organization

### Kids Clothing Specific Features
- **Age Group Categorization**: 0-2, 2-4, 4-6, 6-8, 8-10, 10-12, 12-14, 14-16 years
- **Gender Categorization**: Boys, Girls, Unisex
- **Season Categorization**: Summer, Winter, Monsoon, All Season
- **Brand Type Categorization**: Premium, Mid Range, Budget, All Brands
- **Style Type Categorization**: Casual, Formal, Party, Sports, Ethnic, All Styles
- **Color Family Categorization**: Primary, Pastel, Neutral, Bright, All Colors
- **Size Range Categorization**: XS-S, M-L, XL-XXL, XXXL+, All Sizes

### Business Logic Features
- **Age Range Validation**: Min/max age in months
- **Height Range Validation**: Min/max height in cm
- **Weight Range Validation**: Min/max weight in kg
- **Margin Management**: Default, min, and max margin percentages
- **Category Performance**: Sales, quantity, and customer analytics
- **Growth Tracking**: Sales, quantity, customer, and product growth
- **Seasonal Analysis**: Peak and low period identification

### Technical Features
- **Multi-company Support**: Company-specific categories
- **Access Control**: Role-based permissions
- **Data Validation**: Comprehensive constraint checking
- **Computed Fields**: Dynamic field calculations
- **Search and Filtering**: Advanced search capabilities
- **Import/Export**: Bulk operations support
- **API Integration**: REST API for external systems

## Models

### Product Category
- **Name**: `product.category`
- **Purpose**: Main category model with hierarchical structure
- **Key Fields**: name, parent_id, age_group, gender, season, brand_type, style_type, color_family, size_range
- **Business Rules**: age_range, height_range, weight_range, margin_range
- **Analytics**: product_count, total_sales, avg_rating

### Category Template
- **Name**: `product.category.template`
- **Purpose**: Template for quick category creation
- **Key Fields**: name, age_group, gender, season, brand_type, style_type, color_family, size_range
- **Usage**: Create categories from templates, apply templates to existing categories

### Category Rule
- **Name**: `product.category.rule`
- **Purpose**: Automated categorization rules
- **Key Fields**: condition_type, condition_operator, condition_value, action_type, target_category_id
- **Actions**: assign_category, assign_template, set_margin, set_price, set_tag, send_notification, create_task

### Category Analytics
- **Name**: `product.category.analytics`
- **Purpose**: Performance tracking and reporting
- **Key Fields**: total_sales, total_quantity, total_orders, total_products, total_customers
- **Metrics**: conversion_rate, return_rate, average_rating, stock_turnover, customer_retention_rate

### Category Tag
- **Name**: `product.category.tag`
- **Purpose**: Flexible tagging system
- **Key Fields**: name, color, active
- **Usage**: Organize and filter categories

## Views

### Category Views
- **Tree View**: Hierarchical category listing
- **Form View**: Detailed category information
- **Search View**: Advanced filtering and grouping
- **Kanban View**: Visual category management
- **Calendar View**: Date-based category tracking
- **Pivot View**: Category analytics
- **Graph View**: Category performance charts

### Template Views
- **Tree View**: Template listing
- **Form View**: Template details
- **Search View**: Template filtering
- **Kanban View**: Visual template management

### Rule Views
- **Tree View**: Rule listing
- **Form View**: Rule configuration
- **Search View**: Rule filtering
- **Kanban View**: Visual rule management

### Analytics Views
- **Tree View**: Analytics listing
- **Form View**: Analytics details
- **Search View**: Analytics filtering
- **Pivot View**: Analytics aggregation
- **Graph View**: Analytics charts
- **Calendar View**: Date-based analytics

## Security

### Access Control
- **Public Access**: Read-only access to categories
- **User Access**: Full access to categories and templates
- **Manager Access**: Full access including rules and analytics
- **Analytics Access**: Read-only access to analytics

### Record Rules
- **Category Rules**: Public read, user write, manager full access
- **Template Rules**: User write, manager full access
- **Rule Rules**: User write, manager full access
- **Analytics Rules**: Analytics read, manager full access
- **Tag Rules**: User write, manager full access

## Data

### Default Categories
- **Babywear**: 0-2 years, unisex, all season
- **Toddler**: 2-4 years, unisex, all season
- **Teen**: 12-16 years, unisex, all season
- **Sub-categories**: Boys and Girls for each main category

### Default Templates
- **Babywear Template**: 0-2 years, 40% margin
- **Toddler Template**: 2-4 years, 35% margin
- **Teen Template**: 12-16 years, 30% margin

### Default Tags
- **Premium**: Premium quality products
- **Budget**: Budget-friendly products
- **Seasonal**: Seasonal products
- **Trending**: Trending products
- **New Arrival**: New arrival products
- **Clearance**: Clearance products

### Default Rules
- **Age Group Validation**: Validate age group consistency
- **Margin Validation**: Validate margin within acceptable range

## Demo Data

### Demo Categories
- **Summer Babywear**: Summer clothing for babies
- **Winter Babywear**: Winter clothing for babies
- **Party Toddler**: Party clothing for toddlers
- **Sports Teen**: Sports clothing for teens

### Demo Templates
- **Summer Template**: Summer category template
- **Winter Template**: Winter category template
- **Party Template**: Party category template

### Demo Tags
- **Organic**: Organic cotton products
- **Handmade**: Handmade products
- **Limited Edition**: Limited edition products

### Demo Rules
- **Summer Discount Rule**: Apply summer discount
- **Winter Premium Rule**: Apply premium pricing
- **Party Premium Rule**: Apply premium pricing

## Usage

### Creating Categories
1. Navigate to Categories > Product Categories
2. Click Create
3. Fill in category details
4. Set age group, gender, season, etc.
5. Configure business rules
6. Save

### Using Templates
1. Navigate to Categories > Category Templates
2. Select a template
3. Click "Create Category from Template"
4. Enter category name
5. Save

### Setting Up Rules
1. Navigate to Categories > Category Rules
2. Click Create
3. Set condition type and operator
4. Set action type and target
5. Configure apply to scope
6. Save and test

### Viewing Analytics
1. Navigate to Categories > Category Analytics
2. Generate analytics for specific period
3. View performance metrics
4. Export reports

## API

### Category API
```python
# Create category
category = env['product.category'].create({
    'name': 'New Category',
    'age_group': '2-4',
    'gender': 'unisex',
    'season': 'all_season',
    'brand_type': 'all',
    'style_type': 'all',
    'color_family': 'all',
    'size_range': 'all',
})

# Get category products
products = category.get_products()

# Get category path
path = category.get_category_path()

# Get children recursively
children = category.get_children_recursive()

# Get parents
parents = category.get_parents()

# Check if child of
is_child = category.is_child_of(parent_category)

# Get siblings
siblings = category.get_siblings()

# Move to parent
category.move_to_parent(new_parent)

# Archive/Unarchive
category.archive()
category.unarchive()

# Duplicate
duplicated = category.duplicate()
```

### Template API
```python
# Create template
template = env['product.category.template'].create({
    'name': 'New Template',
    'age_group': '2-4',
    'gender': 'unisex',
    'season': 'all_season',
    'brand_type': 'all',
    'style_type': 'all',
    'color_family': 'all',
    'size_range': 'all',
})

# Create category from template
category = template.create_category_from_template('New Category')

# Apply template to category
template.apply_to_category(category)

# Duplicate template
duplicated = template.duplicate_template()
```

### Rule API
```python
# Create rule
rule = env['product.category.rule'].create({
    'name': 'New Rule',
    'condition_type': 'age_group',
    'condition_operator': 'equals',
    'condition_value': '2-4',
    'action_type': 'assign_category',
    'target_category_id': category.id,
})

# Execute rule
result = rule.execute_rule(products)

# Test rule
test_result = rule.test_rule(products)

# Reset statistics
rule.reset_statistics()

# Duplicate rule
duplicated = rule.duplicate_rule()
```

### Analytics API
```python
# Generate analytics
analytics = env['product.category.analytics'].generate_analytics(
    category_id, date_from, date_to, period_type
)

# Get category performance
performance = env['product.category.analytics'].get_category_performance(
    category_id, period_days
)

# Get top categories
top_categories = env['product.category.analytics'].get_top_categories(
    limit=10, period_days=30
)

# Get seasonal analysis
seasonal = env['product.category.analytics'].get_seasonal_analysis(
    category_id, year
)
```

## Dependencies

### Required Addons
- **core_base**: Core system configuration and utilities
- **core_web**: Web interface and notifications
- **users**: User management and permissions
- **company**: Company management
- **products**: Product management

### Optional Addons
- **contacts**: Customer and supplier management
- **sales**: Sales order management
- **inventory**: Inventory management
- **accounting**: Accounting and invoicing

## Installation

### Manual Installation
1. Copy the addon to your addons directory
2. Update the addon list
3. Install the addon
4. Configure security groups
5. Set up default data

### Automated Installation
```bash
# Install addon
python3 run_erp.py --install categories

# Update addon
python3 run_erp.py --update categories

# Test addon
python3 run_erp.py --test categories
```

## Configuration

### Security Groups
- **Category Manager**: Full access to all category features
- **Category User**: Access to categories and templates
- **Category Analytics**: Read-only access to analytics

### Access Rights
- **Public**: Read-only access to categories
- **User**: Full access to categories and templates
- **Manager**: Full access including rules and analytics

### Record Rules
- **Category Rules**: Public read, user write, manager full access
- **Template Rules**: User write, manager full access
- **Rule Rules**: User write, manager full access
- **Analytics Rules**: Analytics read, manager full access
- **Tag Rules**: User write, manager full access

## Troubleshooting

### Common Issues
1. **Category not showing**: Check active status and permissions
2. **Template not working**: Verify template configuration
3. **Rule not executing**: Check condition and action settings
4. **Analytics not generating**: Verify date range and permissions

### Debug Mode
```python
# Enable debug mode
import logging
logging.getLogger('categories').setLevel(logging.DEBUG)

# Check category status
category = env['product.category'].browse(category_id)
print(f"Category: {category.name}")
print(f"Active: {category.active}")
print(f"Products: {category.product_count}")
```

## Support

### Documentation
- **User Guide**: Complete user documentation
- **API Reference**: Full API documentation
- **Developer Guide**: Development guidelines

### Community
- **Forum**: Community support forum
- **GitHub**: Issue tracking and contributions
- **Email**: Direct support contact

### Professional Support
- **Consulting**: Custom implementation
- **Training**: User and developer training
- **Maintenance**: Ongoing support and updates

## License

This addon is licensed under LGPL-3. See the LICENSE file for details.

## Changelog

### Version 1.0.0
- Initial release
- Basic category management
- Template system
- Rule engine
- Analytics system
- Security implementation
- Documentation

## Contributing

### Development
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

### Testing
1. Run unit tests
2. Run integration tests
3. Test with demo data
4. Verify security

### Documentation
1. Update user documentation
2. Update API documentation
3. Update developer guide
4. Update changelog

## Contact

- **Website**: https://kidsclothingerp.com
- **Email**: support@kidsclothingerp.com
- **GitHub**: https://github.com/kidsclothingerp/categories
- **Forum**: https://forum.kidsclothingerp.com

---

*This addon is part of the Kids Clothing ERP system, designed specifically for kids clothing retail businesses.*