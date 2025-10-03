# Addon Structure Guide

## Overview
This guide explains the correct addon structure for the Kids Clothing ERP system, following a modular architecture similar to Ocean ERP.

## 📁 **Project Structure**

```
/workspace/
├── addons/                          # Main addons folder
│   ├── core_base/                  # Core base addon
│   │   ├── __manifest__.py         # Addon manifest
│   │   ├── models/                 # Python models
│   │   │   ├── __init__.py
│   │   │   └── res_config.py       # System configuration
│   │   ├── views/                  # XML views
│   │   │   └── res_config_views.xml
│   │   ├── security/               # Security rules
│   │   │   └── ir.model.access.csv
│   │   ├── data/                   # Demo data
│   │   │   └── data.xml
│   │   ├── static/                 # Static assets
│   │   │   ├── src/css/
│   │   │   ├── src/js/
│   │   │   └── src/xml/
│   │   └── tests/                  # Unit tests
│   │       ├── __init__.py
│   │       └── test_res_config.py
│   ├── core_web/                   # Core web addon
│   ├── users/                      # Users addon
│   ├── company/                    # Company addon
│   ├── database/                   # Database addon
│   ├── contacts/                   # Contacts addon
│   ├── products/                   # Products addon
│   ├── sales/                      # Sales addon
│   ├── crm/                        # CRM addon
│   ├── pos/                        # POS addon
│   ├── inventory/                  # Inventory addon
│   ├── accounting/                 # Accounting addon
│   ├── hr/                         # HR addon
│   ├── reports/                    # Reports addon
│   └── ...                         # All other addons
├── clone_Version3.md               # Complete module blueprint
├── PROJECT_STATUS.md               # Project status tracking
├── DEVELOPMENT_CHECKLIST.md         # Development checklist
├── REMAINING_MODULES_ANALYSIS.md    # Remaining modules analysis
└── README.md                       # Project documentation
```

## 🏗️ **Addon Structure**

Each addon follows this standard structure:

```
addon_name/
├── __manifest__.py                 # Addon manifest file
├── models/                         # Python models
│   ├── __init__.py                 # Models init file
│   └── model_name.py               # Individual model files
├── views/                          # XML view files
│   ├── model_name_views.xml        # View definitions
│   └── menu.xml                    # Menu structure
├── security/                       # Security configuration
│   ├── ir.model.access.csv         # Access control lists
│   └── security.xml                # Security groups and rules
├── data/                           # Demo and initial data
│   └── data.xml                    # Data files
├── static/                         # Static assets
│   ├── src/css/                    # CSS files
│   ├── src/js/                     # JavaScript files
│   └── src/xml/                    # XML templates
├── tests/                          # Unit tests
│   ├── __init__.py                 # Tests init file
│   └── test_model_name.py          # Individual test files
├── wizard/                         # Wizards (optional)
│   ├── __init__.py
│   └── wizard_name.py
├── report/                         # Report templates (optional)
│   ├── __init__.py
│   └── report_name.xml
└── README.md                       # Addon documentation
```

## 📋 **Addon Manifest Template**

```python
# -*- coding: utf-8 -*-
{
    'name': 'Addon Name',
    'version': '1.0.0',
    'category': 'Category',
    'summary': 'Brief description',
    'description': """
        Detailed description of the addon
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'other_addon',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/menu.xml',
        'views/model_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'addon_name/static/src/css/style.css',
            'addon_name/static/src/js/script.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

## 🔧 **Development Workflow**

### **1. Create New Addon**
```bash
# Create addon directory
mkdir -p addons/addon_name

# Create standard structure
mkdir -p addons/addon_name/{models,views,security,data,static/src/{css,js,xml},tests,wizard,report}

# Create init files
touch addons/addon_name/models/__init__.py
touch addons/addon_name/tests/__init__.py
```

### **2. Addon Development Steps**
1. **Create manifest**: `__manifest__.py`
2. **Define models**: Python model files
3. **Create views**: XML view files
4. **Setup security**: Access control and permissions
5. **Add data**: Demo and initial data
6. **Create tests**: Unit tests for all functionality
7. **Add assets**: CSS, JS, XML templates
8. **Documentation**: README and inline documentation

### **3. Testing Addon**
```bash
# Run tests for specific addon
python3 -m pytest addons/addon_name/tests/ -v

# Run all tests
python3 -m pytest addons/ -v
```

## 📦 **Addon Categories**

### **Core Addons**
- **core_base**: System configuration, utilities, translations
- **core_web**: Web client, UI assets, menus, notifications
- **users**: User management, groups, permissions
- **company**: Company setup, multi-company support
- **database**: Multi-database management

### **Master Data Addons**
- **contacts**: Customer, supplier, vendor management
- **products**: Product catalog with variants
- **categories**: Product categories and attributes
- **bulk_import**: Excel/CSV import system

### **Sales & CRM Addons**
- **sales**: Quotations, sales orders, invoicing
- **crm**: Leads, opportunities, activities
- **loyalty**: Points, rewards, vouchers
- **discounts**: Discount programs, promotions

### **POS Addons**
- **pos**: Point of sale system
- **pos_exchange**: Exchange handling
- **pos_return**: Return handling
- **pos_payment**: Multi-payment integration

### **Inventory Addons**
- **inventory**: Stock management
- **warehouse**: Warehouse management
- **purchase**: Procurement management
- **stock_management**: Stock alerts, reorder rules

### **Accounting Addons**
- **accounting**: Chart of accounts, journals
- **invoicing**: Customer/supplier invoicing
- **payments**: Payment processing
- **bank_integration**: Bank statement integration

### **Indian Localization Addons**
- **l10n_in**: Indian Chart of Accounts
- **l10n_in_gst**: GST compliance
- **l10n_in_edi**: E-invoice, E-way bill
- **l10n_in_hr_payroll**: Indian payroll

### **HR Addons**
- **hr**: Employee management
- **payroll**: Payroll processing
- **attendance**: Attendance management
- **leaves**: Leave management

### **E-commerce Addons**
- **ecommerce**: Online storefront
- **website**: Website builder
- **customer_portal**: Customer self-service
- **logistics**: Shipping integration

### **Reporting Addons**
- **reports**: Pre-built reports
- **dashboard**: Customizable dashboards
- **analytics**: Advanced analytics
- **custom_reports**: Custom report builder

### **Customization Addons**
- **studio**: Low-code customizer
- **custom_fields**: Dynamic fields
- **workflows**: User-defined workflows
- **automated_actions**: Automated processes

### **Utilities Addons**
- **notifications**: Alerts and notifications
- **documents**: Document management
- **integrations**: API integrations
- **helpdesk**: Support ticket system

## 🚀 **Next Steps**

1. **Start with Core Addons**: Begin with core_base, core_web, users, company, database
2. **Follow Dependencies**: Install addons in dependency order
3. **Test Each Addon**: Ensure each addon works independently
4. **Integration Testing**: Test addon interactions
5. **Documentation**: Document each addon thoroughly

## 📚 **Best Practices**

### **Addon Development**
- **Single Responsibility**: Each addon should have one clear purpose
- **Dependency Management**: Clearly define addon dependencies
- **Error Handling**: Comprehensive error handling in all addons
- **Testing**: 100% test coverage for all addons
- **Documentation**: Clear documentation for each addon

### **Code Quality**
- **Python PEP 8**: Follow Python coding standards
- **Type Hints**: Use Python type annotations
- **Comments**: Clear and comprehensive comments
- **Naming**: Descriptive variable and function names
- **Structure**: Clean and organized code structure

### **Security**
- **Access Control**: Proper security rules for all models
- **Input Validation**: Validate all user inputs
- **SQL Injection**: Use parameterized queries
- **XSS Protection**: Sanitize all outputs
- **Authentication**: Secure authentication system

---

**This structure ensures a clean, modular, and maintainable ERP system that can be easily extended and customized!** 🚀