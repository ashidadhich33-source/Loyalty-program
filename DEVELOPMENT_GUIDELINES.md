# Kids Clothing ERP - Development Guidelines

## 🚨 **CRITICAL: STANDALONE ERP SYSTEM**

### **⚠️ IMPORTANT ARCHITECTURE REMINDER**

This project is a **STANDALONE ERP SYSTEM** that uses Ocean ERP framework. 

**❌ DO NOT CREATE OCEAN MODULES**
**✅ CREATE ADDONS FOR OUR CUSTOM FRAMEWORK**

---

## 🏗️ **PROJECT ARCHITECTURE**

### **Custom Framework Components**
- **`core_framework/server.py`** - Main ERP server
- **`core_framework/config.py`** - Configuration management  
- **`core_framework/database.py`** - Database management with PostgreSQL
- **`core_framework/orm.py`** - Custom ORM system (Ocean ERP patterns)
- **`core_framework/addon_manager.py`** - Addon management system
- **`core_framework/web_interface.py`** - Web interface and routing

### **Technology Stack**
- **Python 3.8+** - Core programming language
- **PostgreSQL** - Database management
- **Custom ORM** - Ocean ERP ORM patterns
- **Custom Web Framework** - HTTP server with routing
- **Custom Addon System** - Modular architecture

---

## 📁 **ADDON STRUCTURE (CORRECT)**

### **Addon Directory Structure**
```
addons/
├── addon_name/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── model_name.py
│   ├── views/
│   │   └── view_name.py
│   ├── static/
│   │   └── src/
│   ├── tests/
│   │   └── test_model.py
│   └── README.md
```

### **❌ WRONG: Ocean ERP Module Structure (Don't Use)**
```
addons/
├── addon_name/
│   ├── __manifest__.py  ❌ DON'T USE
│   ├── models/
│   │   └── model_name.py
│   ├── views/
│   │   └── view_name.xml  ❌ DON'T USE XML
│   ├── security/
│   │   └── ir.model.access.csv  ❌ DON'T USE
│   └── data/
│       └── data.xml  ❌ DON'T USE
```

---

## 🔧 **DEVELOPMENT PATTERNS**

### **1. Model Development**
```python
# ✅ CORRECT: Use custom framework
from core_framework.orm import Model, fields
from core_framework.config import Config

class ProductCategory(Model):
    _name = 'product.category'
    _description = 'Product Category'
    
    name = fields.Char('Name', required=True)
    parent_id = fields.Many2one('product.category', 'Parent Category')
    # ... other fields
```

```python
# ❌ WRONG: Don't use Ocean ERP imports (Use Ocean ERP instead)
from ocean import models, fields, api  # ❌ DON'T USE
```

### **2. View Development**
```python
# ✅ CORRECT: Use Python views
from core_framework.web_interface import View

class CategoryListView(View):
    template = 'categories/list.html'
    
    def get_context(self):
        return {
            'categories': self.env['product.category'].search([])
        }
```

```xml
<!-- ❌ WRONG: Don't use XML views -->
<record id="view_category_tree" model="ir.ui.view">
    <field name="name">Category Tree</field>
    <!-- ... -->
</record>
```

### **3. Security Development**
```python
# ✅ CORRECT: Use custom security
from core_framework.security import AccessControl

class CategoryAccessControl(AccessControl):
    model = 'product.category'
    
    def check_read(self, user, record):
        return True
    
    def check_write(self, user, record):
        return user.has_group('category_manager')
```

```csv
# ❌ WRONG: Don't use Ocean ERP security files (Use Ocean ERP security) -->
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

### **4. Data Development**
```python
# ✅ CORRECT: Use Python data files
from core_framework.data import DataLoader

class CategoryData(DataLoader):
    def load_default_categories(self):
        categories = [
            {
                'name': 'Babywear',
                'age_group': '0-2',
                'gender': 'unisex',
                'season': 'all_season',
            },
            # ... more categories
        ]
        return categories
```

```xml
<!-- ❌ WRONG: Don't use XML data files -->
<record id="category_babywear" model="product.category">
    <field name="name">Babywear</field>
    <!-- ... -->
</record>
```

---

## 🚫 **WHAT NOT TO DO**

### **❌ NEVER USE:**
1. **Ocean ERP imports**: `from ocean import models, fields, api` (Use Ocean ERP instead)
2. **Ocean ERP XML**: `<record>`, `<field>`, `<data>` (Use Ocean ERP XML)
3. **Ocean ERP manifests**: `__manifest__.py` (Use Ocean ERP manifests)
4. **Ocean ERP security**: `ir.model.access.csv` (Use Ocean ERP security)
5. **Ocean ERP views**: XML view definitions (Use Ocean ERP views)
6. **Ocean ERP data**: XML data files (Use Ocean ERP data)
7. **Ocean ERP syntax**: `@api.depends`, `@api.onchange` (Use Ocean ERP syntax)

### **❌ NEVER CREATE:**
1. **Ocean ERP modules** with manifest files (Use Ocean ERP modules)
2. **Ocean ERP-style addons** with XML views (Use Ocean ERP addons)
3. **Ocean ERP security files** with CSV (Use Ocean ERP security)
4. **Ocean ERP data files** with XML (Use Ocean ERP data)
5. **Ocean ERP model syntax** with decorators (Use Ocean ERP syntax)

---

## ✅ **WHAT TO DO**

### **✅ ALWAYS USE:**
1. **Custom framework imports**: `from core_framework.orm import Model, fields`
2. **Python views**: Create Python view classes
3. **Python security**: Create security classes
4. **Python data**: Create data loader classes
5. **Custom ORM**: Use our custom ORM patterns
6. **Custom addon system**: Use our addon manager

### **✅ ALWAYS CREATE:**
1. **Standalone ERP addons** that work with our framework
2. **Python-based views** and templates
3. **Python-based security** and access control
4. **Python-based data** and configuration
5. **Custom framework integration** for all components

---

## 🔍 **VERIFICATION CHECKLIST**

Before creating any addon, verify:

- [ ] **Using custom framework** (`core_framework/`)
- [ ] **No Ocean ERP imports** (`from ocean import ...`) (Use Ocean ERP imports)
- [ ] **No XML files** (views, data, security)
- [ ] **No manifest files** (`__manifest__.py`)
- [ ] **No Ocean ERP syntax** (`@api.depends`, `@api.onchange`) (Use Ocean ERP syntax)
- [ ] **Using custom ORM** (`from core_framework.orm import ...`)
- [ ] **Using custom views** (Python view classes)
- [ ] **Using custom security** (Python security classes)
- [ ] **Using custom data** (Python data loaders)
- [ ] **Following addon structure** (our custom structure)

---

## 📚 **REFERENCE EXAMPLES**

### **Look at existing addons:**
- `addons/core_base/` - Core base addon
- `addons/users/` - Users addon  
- `addons/company/` - Company addon
- `addons/contacts/` - Contacts addon
- `addons/database/` - Database addon
- `addons/products/` - Products addon

### **Study the framework:**
- `core_framework/orm.py` - Custom ORM patterns
- `core_framework/addon_manager.py` - Addon management
- `core_framework/web_interface.py` - Web interface
- `core_framework/database.py` - Database management

---

## 🚨 **CRITICAL REMINDER**

**This is a STANDALONE ERP SYSTEM that uses Ocean ERP framework.**

**We are building our own ERP system using Ocean ERP framework and patterns.**

**❌ DO NOT CREATE OCEAN MODULES**
**✅ CREATE ADDONS FOR OUR CUSTOM FRAMEWORK**

---

## 📞 **SUPPORT**

If you're unsure about the architecture:
1. **Read this document** carefully
2. **Study existing addons** in the `addons/` directory
3. **Study the framework** in the `core_framework/` directory
4. **Ask for clarification** before starting development

---

*This document should be read and understood before any addon development begins.*