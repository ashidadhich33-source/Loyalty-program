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
- **Brand Type Categorization**: Premium, Mid Range, Budget
- **Style Type Categorization**: Casual, Formal, Party, Sports, Ethnic
- **Color Family Categorization**: Primary, Pastel, Neutral, Bright
- **Size Range Categorization**: XS-S, M-L, XL-XXL, XXXL+

### Business Logic Features
- **Age Range Validation**: Min/max age in months
- **Height Range Validation**: Min/max height in cm
- **Weight Range Validation**: Min/max weight in kg
- **Margin Management**: Default, min, and max margin percentages
- **Category Performance**: Sales, quantity, and customer analytics
- **Growth Tracking**: Sales, quantity, customer, and product growth
- **Seasonal Analysis**: Peak and low period identification

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

## Dependencies

### Required Addons
- **core_base**: Core system configuration and utilities
- **core_web**: Web interface and notifications
- **users**: User management and permissions
- **company**: Company management
- **products**: Product management

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

## Testing

### Run Tests
```bash
# Run all tests
python3 -m pytest addons/categories/tests/

# Run specific test
python3 -m pytest addons/categories/tests/test_product_category.py
```

### Test Coverage
- **Unit Tests**: Model functionality
- **Integration Tests**: Cross-model interactions
- **Validation Tests**: Business rule validation
- **Method Tests**: Category methods

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

## License

This addon is licensed under LGPL-3. See the LICENSE file for details.

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

## Contact

- **Website**: https://kidsclothingerp.com
- **Email**: support@kidsclothingerp.com
- **GitHub**: https://github.com/kidsclothingerp/categories

---

*This addon is part of the Kids Clothing ERP system, designed specifically for kids clothing retail businesses.*