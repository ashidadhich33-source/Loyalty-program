# Sales Management Addon

## Overview

The Sales Management addon provides comprehensive sales functionality for the Kids Clothing ERP system. It includes sales orders, quotations, deliveries, returns, team management, territory management, commission tracking, and analytics.

## Features

### Core Sales Features
- **Sales Orders**: Create and manage sales orders with order lines
- **Sales Quotations**: Send price quotes to customers
- **Sales Deliveries**: Manage product deliveries to customers
- **Sales Returns**: Handle product returns and refunds

### Sales Team Management
- **Sales Teams**: Organize and manage sales teams
- **Team Members**: Assign team members and roles
- **Team Performance**: Track team performance metrics

### Sales Territory Management
- **Sales Territories**: Define and manage sales territories
- **Territory Hierarchy**: Support for parent-child territory relationships
- **Territory Performance**: Track territory performance metrics

### Sales Commission Management
- **Commission Rules**: Define commission calculation rules
- **Commission Tracking**: Track and manage sales commissions
- **Commission Payments**: Process commission payments

### Sales Analytics
- **Sales Performance**: Track sales performance metrics
- **Kids Clothing Analytics**: Specialized analytics for kids clothing
- **Age Group Analytics**: Sales analysis by age group
- **Gender Analytics**: Sales analysis by gender
- **Season Analytics**: Sales analysis by season

## Models

### Sale Order Models
- `sale.order`: Main sales order model
- `sale.order.line`: Sales order line model

### Kids Clothing Specific Features
- **Age Group Support**: Infant, Toddler, Preschool, Child, Teen
- **Gender Support**: Boys, Girls, Unisex
- **Season Support**: Spring, Summer, Fall, Winter
- **Size & Color Variants**: Product variant management
- **Child Profiles**: Child-specific order tracking

## Indian Localization
- **GST Support**: GST treatment and compliance
- **Currency Support**: Indian Rupee formatting
- **Address Support**: Indian address format
- **Multi-company Support**: Company-specific data isolation

## Installation

1. Ensure the addon is in the `addons/sales/` directory
2. Install the addon using the ERP system's addon manager
3. Configure the addon settings
4. Set up initial data

## Usage

### Creating Sales Orders
1. Navigate to Sales > Sales Orders
2. Click "Create" to create a new order
3. Fill in customer details
4. Add order lines with products
5. Set quantities and prices
6. Save and confirm the order

## License

This addon is licensed under the LGPL-3 license.

## Changelog

### Version 1.0.0
- Initial release
- Basic sales order functionality
- Sales team management
- Sales territory management
- Sales commission tracking
- Sales analytics
- Kids clothing specific features
- Indian localization support