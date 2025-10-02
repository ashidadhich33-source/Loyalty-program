# Categories Addon

## Overview
The Categories addon provides comprehensive product category management specifically designed for kids clothing retail. It offers hierarchical category structure, age group categorization, gender-based organization, season-based categorization, and brand-based categorization.

## Key Features

### 1. Hierarchical Category Structure
- Parent-child category relationships
- Complete category path display
- Recursive category prevention
- Category hierarchy visualization

### 2. Kids Clothing Specific Categorization
- **Age Groups**: 0-2 (Baby), 2-4 (Toddler), 4-6 (Pre-school), 6-8 (Early School), 8-10 (Middle School), 10-12 (Pre-teen), 12-14 (Teen), 14-16 (Young Adult)
- **Gender**: Boys, Girls, Unisex
- **Season**: Summer, Winter, Monsoon, All Season
- **Brand Type**: Premium, Mid Range, Budget, All Brands

### 3. Category Management
- Category creation and editing
- Category activation/deactivation
- Category sequencing
- Category images and icons
- Category colors and themes
- Category descriptions

### 4. Category Attributes
- Custom attributes for each category
- Attribute types: Text, Number, Boolean, Selection, Date, DateTime, Float, Integer
- Validation rules for attributes
- Kids-specific attribute filtering
- Age group and gender filtering for attributes

### 5. Category Rules
- Business rules for categories
- Rule types: Pricing, Discount, Inventory, Marketing, Validation, Workflow
- Condition-based rule execution
- Action-based rule implementation
- Rule priority management
- Rule execution tracking

### 6. Category Analytics
- Sales analytics by category
- Product count analytics
- Customer analytics
- Inventory analytics
- Financial analytics
- Performance metrics
- Market share analysis
- Growth rate tracking

## Models

### 1. Product Category (`product.category`)
Main category model with hierarchical structure and kids clothing specific fields.

**Key Fields:**
- `name`: Category name
- `parent_id`: Parent category
- `age_group`: Target age group
- `gender`: Target gender
- `season`: Season
- `brand_type`: Brand type
- `is_active`: Active status
- `description`: Category description
- `image`: Category image
- `icon`: Category icon
- `color`: Category color
- `min_price`: Minimum price
- `max_price`: Maximum price
- `default_margin`: Default margin percentage

**Computed Fields:**
- `complete_name`: Full category path
- `product_count`: Number of products
- `total_sales`: Total sales amount
- `avg_rating`: Average rating

### 2. Category Analytics (`category.analytics`)
Analytics and reporting for categories.

**Key Fields:**
- `category_id`: Category reference
- `date`: Analytics date
- `period`: Analytics period (daily, weekly, monthly, quarterly, yearly)
- `total_sales`: Total sales amount
- `sales_count`: Number of sales
- `avg_order_value`: Average order value
- `product_count`: Product count
- `customer_count`: Customer count
- `revenue`: Revenue
- `profit`: Profit
- `profit_margin`: Profit margin percentage

### 3. Category Attribute (`category.attribute`)
Custom attributes for categories.

**Key Fields:**
- `name`: Attribute name
- `category_id`: Category reference
- `attribute_type`: Type of attribute
- `required`: Required status
- `default_value`: Default value
- `selection_options`: Options for selection type
- `min_value`: Minimum value
- `max_value`: Maximum value
- `is_kids_specific`: Kids specific flag
- `age_group_filter`: Age group filter
- `gender_filter`: Gender filter

### 4. Category Rule (`category.rule`)
Business rules for categories.

**Key Fields:**
- `name`: Rule name
- `category_id`: Category reference
- `rule_type`: Type of rule
- `condition_type`: Condition type
- `action_type`: Action type
- `is_active`: Active status
- `priority`: Rule priority
- `execution_count`: Execution count
- `success_count`: Success count
- `failure_count`: Failure count

## Views

### 1. Category Views
- **Tree View**: List of categories with hierarchy
- **Form View**: Detailed category form with tabs
- **Kanban View**: Visual category cards
- **Search View**: Advanced search and filters

### 2. Analytics Views
- **Dashboard View**: Analytics dashboard
- **Graph Views**: Various analytics graphs
- **Pivot Views**: Pivot tables for analytics
- **Cohort Views**: Cohort analysis

### 3. Attribute Views
- **Tree View**: List of attributes
- **Form View**: Detailed attribute form

### 4. Rule Views
- **Tree View**: List of rules
- **Form View**: Detailed rule form

## Security

### Groups
- **Category Manager**: Full access to category management
- **Category User**: Basic access to category management
- **Category Analyst**: Access to category analytics and reporting

### Access Control
- Multi-company data isolation
- Record-level security rules
- Field-level security
- User-based access control

## Data

### Default Categories
- Age group categories (Baby, Toddler, Pre-school, etc.)
- Gender categories (Boys, Girls)
- Season categories (Summer, Winter, Monsoon)
- Brand type categories (Premium, Mid Range, Budget)

### Demo Data
- Sample categories with hierarchy
- Sample attributes
- Sample rules
- Sample analytics data

## Static Assets

### JavaScript
- Category widgets
- Analytics widgets
- Rule widgets
- Attribute widgets

### CSS
- Category styling
- Analytics styling
- Rule styling
- Attribute styling
- Responsive design
- Dark theme support

## Testing

### Test Coverage
- Unit tests for all models
- Integration tests for workflows
- Security tests for access control
- Performance tests for analytics

### Test Files
- `test_product_category.py`: Product category tests
- `test_category_analytics.py`: Analytics tests
- `test_category_attribute.py`: Attribute tests
- `test_category_rule.py`: Rule tests

## Installation

### Dependencies
- `core_base`: Core system configuration
- `core_web`: Web interface
- `users`: User management
- `company`: Company management
- `products`: Product management

### Installation Steps
1. Install dependencies
2. Install categories addon
3. Configure category structure
4. Set up analytics
5. Configure rules

## Usage

### Creating Categories
1. Navigate to Categories > Category Management > Categories
2. Click Create
3. Fill in category details
4. Set age group, gender, season, and brand type
5. Save category

### Setting Up Attributes
1. Go to Categories > Category Management > Category Attributes
2. Create attributes for categories
3. Set validation rules
4. Configure display options

### Creating Rules
1. Navigate to Categories > Category Management > Category Rules
2. Create business rules
3. Set conditions and actions
4. Activate rules

### Viewing Analytics
1. Go to Categories > Category Analytics > Analytics Dashboard
2. View various analytics reports
3. Analyze category performance
4. Track growth and trends

## Configuration

### Category Settings
- Default age groups
- Default genders
- Default seasons
- Default brand types
- Category colors and icons

### Analytics Settings
- Analytics periods
- Performance metrics
- Reporting intervals
- Data retention

### Rule Settings
- Rule priorities
- Execution intervals
- Notification settings
- Action configurations

## Troubleshooting

### Common Issues
1. **Category recursion**: Check parent-child relationships
2. **Analytics not updating**: Verify data sources
3. **Rules not executing**: Check rule conditions and actions
4. **Attributes not showing**: Verify attribute configuration

### Debug Mode
- Enable debug mode for detailed logging
- Check rule execution logs
- Verify analytics calculations
- Test attribute validations

## Support

### Documentation
- User manual
- Developer guide
- API documentation
- Troubleshooting guide

### Community
- Forum support
- Community contributions
- Bug reports
- Feature requests

## License
LGPL-3

## Author
Kids Clothing ERP Team

## Website
https://kidsclothingerp.com