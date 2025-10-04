# 🌊 Ocean ERP - Complete Setup Guide

## Overview

Ocean ERP now includes a **complete setup wizard** similar to Odoo's database creation wizard, plus offline and 404 pages with logo support. This guide will walk you through the entire setup process for **Linux, macOS, and Windows** users.

## 🚀 Quick Start

### 1. Bootstrap the System

#### Linux/macOS:
```bash
# Run the bootstrap script to set up the environment
python3 bootstrap_ocean_erp.py
```

#### Windows:
```cmd
# Run the bootstrap script to set up the environment
python bootstrap_ocean_erp.py
```

### 2. Set Up PostgreSQL Database

#### Linux/macOS:
```bash
# Create database and user
sudo -u postgres createdb ocean_erp
sudo -u postgres createuser erp_user
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;"
sudo -u postgres psql -c "ALTER USER erp_user CREATEDB;"
```

#### Windows:
```cmd
# Open Command Prompt as Administrator
# Navigate to PostgreSQL bin directory
cd "C:\Program Files\PostgreSQL\15\bin"

# Create database and user
createdb -U postgres ocean_erp
createuser -U postgres erp_user
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;"
psql -U postgres -c "ALTER USER erp_user CREATEDB;"
```

### 3. Start Ocean ERP Server

#### Linux/macOS:
```bash
# Start the server
python3 run_erp.py
```

#### Windows:
```cmd
# Start the server
python run_erp.py
```

### 4. Complete Setup Wizard
1. Open your browser: `http://localhost:8069`
2. You'll be automatically redirected to the setup wizard
3. Follow the 4-step setup process:
   - **Step 1**: Database Configuration
   - **Step 2**: Administrator Account
   - **Step 3**: Company Information
   - **Step 4**: Logo Upload & Summary

### 5. Login and Start Using
- After setup completion, you'll be redirected to the login page
- Use the admin credentials you created during setup
- Start managing your kids clothing retail business!

## 📋 Detailed Setup Process

### Database Setup Wizard

The setup wizard automatically:
- ✅ Creates database tables for all models
- ✅ Creates admin user with secure password
- ✅ Creates default company
- ✅ Loads master data (age groups, seasons, genders)
- ✅ Initializes system settings
- ✅ Sets up logo management

### Setup Wizard Steps

#### Step 1: Database Configuration
- **Database Name**: `ocean_erp` (default)
- **Database User**: `erp_user` (default)
- **Database Password**: `erp_password` (default)

#### Step 2: Administrator Account
- **Full Name**: Administrator
- **Username**: `admin` (default)
- **Email**: `admin@example.com`
- **Password**: Minimum 8 characters

#### Step 3: Company Information
- **Company Name**: Your business name
- **Email, Phone, Website**: Contact details
- **Address**: Street, City, ZIP

#### Step 4: Logo Upload & Summary
- **Logo Upload**: Optional company logo (PNG, JPG, SVG)
- **Setup Summary**: Review all settings before completion

## 🎨 Logo Management System

### Features
- ✅ **Logo Upload**: Support for PNG, JPG, SVG formats
- ✅ **Logo Display**: Automatically shown on all pages
- ✅ **Default Logo**: Beautiful Ocean ERP default logo
- ✅ **Logo URLs**: Automatic URL generation for templates

### Logo Locations
- **Main Logo**: `/static/images/logo/main_logo.png`
- **Default Logo**: `/static/images/logo/default_logo.svg`
- **Favicon**: `/static/images/logo/favicon.ico`

### Logo Usage
The logo system automatically:
- Displays on offline page
- Shows on 404 error page
- Appears in setup wizard
- Used throughout the application

## 🔧 Advanced Configuration

### Environment Variables
```bash
# Database Configuration
export DB_HOST=localhost
export DB_PORT=5432
export DB_USER=erp_user
export DB_PASSWORD=your_secure_password
export DB_NAME=ocean_erp

# Security
export SECRET_KEY=your_super_secure_secret_key
export JWT_SECRET=your_jwt_secret_key

# Server
export SERVER_HOST=0.0.0.0
export SERVER_PORT=8069
```

### Configuration File
Edit `erp.conf` for advanced settings:
```json
{
  "database": {
    "host": "localhost",
    "port": 5432,
    "user": "erp_user",
    "password": "erp_password",
    "name": "ocean_erp"
  },
  "web": {
    "logo_path": "static/images/logo",
    "theme": "kids_clothing"
  }
}
```

## 🌐 Web Interface Features

### Setup Wizard
- **4-Step Process**: Database → Admin → Company → Logo
- **Progress Indicator**: Visual progress tracking
- **Form Validation**: Real-time validation
- **Error Handling**: Clear error messages
- **Responsive Design**: Works on all devices

### Offline Page
- **Connection Status**: Real-time connection checking
- **Auto-Retry**: Automatic retry every 30 seconds
- **Error Details**: Technical error information
- **Logo Display**: Company logo prominently shown
- **Responsive Design**: Mobile-friendly interface

### 404 Page
- **Search Functionality**: Built-in search box
- **Popular Pages**: Quick navigation links
- **Breadcrumb Navigation**: Easy navigation
- **Logo Display**: Company branding
- **Keyboard Shortcuts**: Ctrl+K for search, Escape to go back

## 🛠️ Troubleshooting

### Common Issues

#### 1. Setup Wizard Not Loading

##### Linux/macOS:
```bash
# Check if server is running
python3 run_erp.py

# Check logs
tail -f erp.log
```

##### Windows:
```cmd
# Check if server is running
python run_erp.py

# Check logs
type erp.log
```

#### 2. Database Connection Failed

##### Linux/macOS:
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U erp_user -d ocean_erp
```

##### Windows:
```cmd
# Check PostgreSQL service
sc query postgresql-x64-15

# Test connection
psql -h localhost -U erp_user -d ocean_erp
```

#### 3. Logo Not Displaying

##### Linux/macOS:
```bash
# Check logo file exists
ls -la static/images/logo/

# Check file permissions
chmod 644 static/images/logo/*
```

##### Windows:
```cmd
# Check logo file exists
dir static\images\logo\

# Check file permissions
icacls static\images\logo\ /grant Everyone:F
```

#### 4. Setup Already Complete

##### Linux/macOS:
```bash
# Remove setup completion marker
rm .ocean_setup_complete

# Restart server
python3 run_erp.py
```

##### Windows:
```cmd
# Remove setup completion marker
del .ocean_setup_complete

# Restart server
python run_erp.py
```

#### 5. Windows-Specific Issues

##### Python Not Found
```cmd
# Add Python to PATH
setx PATH "%PATH%;C:\Python311;C:\Python311\Scripts"

# Restart Command Prompt
```

##### PostgreSQL Connection Issues
```cmd
# Check PostgreSQL service
services.msc

# Start PostgreSQL service
net start postgresql-x64-15

# Check if port 5432 is listening
netstat -an | findstr 5432
```

##### Permission Issues
```cmd
# Run Command Prompt as Administrator
# Grant full permissions to Ocean ERP directory
icacls "C:\ocean-erp" /grant Everyone:F /T
```

##### Firewall Issues
```cmd
# Open Windows Firewall
wf.msc

# Add inbound rule for port 8069
# Add inbound rule for port 5432
```

### Debug Mode

##### Linux/macOS:
```bash
# Enable debug mode
python3 run_erp.py --debug

# Check detailed logs
tail -f erp.log
```

##### Windows:
```cmd
# Enable debug mode
python run_erp.py --debug

# Check detailed logs
type erp.log
```

### Platform-Specific Debugging

#### Windows Debugging Tools
```cmd
# Check Python installation
python --version
pip --version

# Check PostgreSQL installation
psql --version

# Check network connectivity
ping localhost
telnet localhost 8069
telnet localhost 5432

# Check running processes
tasklist | findstr python
tasklist | findstr postgres
```

#### Linux Debugging Tools
```bash
# Check Python installation
python3 --version
pip3 --version

# Check PostgreSQL installation
psql --version

# Check network connectivity
ping localhost
nc -zv localhost 8069
nc -zv localhost 5432

# Check running processes
ps aux | grep python
ps aux | grep postgres
```

#### macOS Debugging Tools
```bash
# Check Python installation
python3 --version
pip3 --version

# Check PostgreSQL installation
psql --version

# Check network connectivity
ping localhost
nc -zv localhost 8069
nc -zv localhost 5432

# Check running processes
ps aux | grep python
ps aux | grep postgres
```

## 🔒 Security Features

### Setup Security
- ✅ **Password Validation**: Minimum 8 characters
- ✅ **Secure Hashing**: PBKDF2 with salt
- ✅ **Secret Key Generation**: Cryptographically secure
- ✅ **Database Isolation**: Separate user with limited privileges

### Production Security
- ✅ **HTTPS Support**: SSL/TLS encryption
- ✅ **Session Security**: HTTP-only cookies
- ✅ **CSRF Protection**: Cross-site request forgery protection
- ✅ **Rate Limiting**: Login attempt limiting

## 📊 System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, Windows 10/11
- **Python**: 3.8+
- **PostgreSQL**: 12+
- **RAM**: 4GB
- **Storage**: 10GB
- **Network**: Port 8069 available

### Recommended Requirements
- **OS**: Ubuntu 20.04+, CentOS 8+, Windows 11
- **Python**: 3.11+
- **PostgreSQL**: 14+
- **RAM**: 8GB+
- **Storage**: 50GB+
- **Network**: Dedicated server

## 🖥️ Platform-Specific Installation

### Windows Installation

#### Prerequisites
1. **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
2. **PostgreSQL**: Download from [postgresql.org](https://www.postgresql.org/download/windows/)
3. **Git**: Download from [git-scm.com](https://git-scm.com/download/win)

#### Step-by-Step Windows Setup

##### 1. Install Python
```cmd
# Download Python installer from python.org
# During installation, check "Add Python to PATH"
# Verify installation
python --version
pip --version
```

##### 2. Install PostgreSQL
```cmd
# Download PostgreSQL installer from postgresql.org
# During installation:
# - Set password for postgres user
# - Remember the port (default: 5432)
# - Add PostgreSQL to PATH
# Verify installation
psql --version
```

##### 3. Clone Ocean ERP
```cmd
# Open Command Prompt or PowerShell
git clone <your-ocean-erp-repo>
cd ocean-erp
```

##### 4. Bootstrap System
```cmd
# Run bootstrap script
python bootstrap_ocean_erp.py
```

##### 5. Create Database (Windows)
```cmd
# Open Command Prompt as Administrator
# Navigate to PostgreSQL bin directory
cd "C:\Program Files\PostgreSQL\15\bin"

# Create database and user
createdb -U postgres ocean_erp
createuser -U postgres erp_user
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;"
psql -U postgres -c "ALTER USER erp_user CREATEDB;"
```

##### 6. Start Ocean ERP
```cmd
# Start the server
python run_erp.py
```

##### 7. Access Setup Wizard
- Open browser: `http://localhost:8069`
- Complete the setup wizard
- Login with admin credentials

#### Alternative: Automated Windows Setup

For easier Windows setup, use the provided setup scripts:

##### Option 1: Batch Script (setup_windows.bat)
```cmd
# Double-click setup_windows.bat or run from Command Prompt
setup_windows.bat
```

##### Option 2: PowerShell Script (setup_windows.ps1)
```powershell
# Right-click and "Run with PowerShell" or run from PowerShell
.\setup_windows.ps1
```

These scripts will:
- ✅ Check system requirements
- ✅ Install Python dependencies
- ✅ Create necessary directories
- ✅ Set up PostgreSQL database
- ✅ Configure Windows Firewall
- ✅ Set file permissions
- ✅ Optionally start the server

### Linux Installation (Ubuntu/Debian)

#### Prerequisites
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Install Git
sudo apt install git -y
```

#### Step-by-Step Linux Setup

##### 1. Clone Ocean ERP
```bash
git clone <your-ocean-erp-repo>
cd ocean-erp
```

##### 2. Bootstrap System
```bash
python3 bootstrap_ocean_erp.py
```

##### 3. Create Database
```bash
# Switch to postgres user
sudo -u postgres createdb ocean_erp
sudo -u postgres createuser erp_user
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;"
sudo -u postgres psql -c "ALTER USER erp_user CREATEDB;"
```

##### 4. Start Ocean ERP
```bash
python3 run_erp.py
```

### macOS Installation

#### Prerequisites
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and PostgreSQL
brew install python3 postgresql
```

#### Step-by-Step macOS Setup

##### 1. Start PostgreSQL Service
```bash
brew services start postgresql
```

##### 2. Clone and Setup
```bash
git clone <your-ocean-erp-repo>
cd ocean-erp
python3 bootstrap_ocean_erp.py
```

##### 3. Create Database
```bash
createdb ocean_erp
createuser erp_user
psql -c "GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;"
psql -c "ALTER USER erp_user CREATEDB;"
```

##### 4. Start Ocean ERP
```bash
python3 run_erp.py
```

## 🎯 Production Deployment

### Linux/macOS Production Setup

#### Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/ocean-erp.service

# Service file content:
[Unit]
Description=Ocean ERP Server
After=network.target postgresql.service

[Service]
Type=simple
User=erp
Group=erp
WorkingDirectory=/opt/ocean-erp
ExecStart=/usr/bin/python3 /opt/ocean-erp/run_erp.py
Restart=always
RestartSec=10
Environment=PATH=/usr/bin:/usr/local/bin
Environment=PYTHONPATH=/opt/ocean-erp

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl enable ocean-erp
sudo systemctl start ocean-erp
```

#### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static/ {
        alias /opt/ocean-erp/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

#### SSL Certificate
```bash
# Install Let's Encrypt
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com
```

### Windows Production Setup

#### Windows Service (NSSM)
```cmd
# Download NSSM from https://nssm.cc/download
# Extract and run as Administrator

# Install Ocean ERP as Windows Service
nssm install OceanERP "C:\Python311\python.exe" "C:\ocean-erp\run_erp.py"
nssm set OceanERP AppDirectory "C:\ocean-erp"
nssm set OceanERP DisplayName "Ocean ERP Server"
nssm set OceanERP Description "Ocean ERP Kids Clothing Management System"

# Start service
nssm start OceanERP
```

#### IIS Configuration
```xml
<!-- web.config for IIS -->
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <rewrite>
            <rules>
                <rule name="OceanERP" stopProcessing="true">
                    <match url=".*" />
                    <conditions>
                        <add input="{REQUEST_FILENAME}" matchType="IsFile" negate="true" />
                        <add input="{REQUEST_FILENAME}" matchType="IsDirectory" negate="true" />
                    </conditions>
                    <action type="Rewrite" url="http://localhost:8069/{R:0}" />
                </rule>
            </rules>
        </rewrite>
    </system.webServer>
</configuration>
```

#### Windows Firewall
```cmd
# Open Command Prompt as Administrator
# Allow Ocean ERP port
netsh advfirewall firewall add rule name="Ocean ERP" dir=in action=allow protocol=TCP localport=8069

# Allow PostgreSQL port
netsh advfirewall firewall add rule name="PostgreSQL" dir=in action=allow protocol=TCP localport=5432
```

## 💾 Backup & Restore System

Ocean ERP includes a comprehensive backup and restore system:

### **Backup Features**
- ✅ **Full Database Backups**: Complete database dumps using pg_dump
- ✅ **Incremental Backups**: Only changed data
- ✅ **Compression**: Automatic gzip compression
- ✅ **Verification**: Backup integrity checking
- ✅ **Scheduled Backups**: Automated daily/weekly/monthly backups
- ✅ **Retention Management**: Automatic cleanup of old backups
- ✅ **Multiple Formats**: SQL dumps with schema and data options

### **Restore Features**
- ✅ **Full Restore**: Complete database restoration
- ✅ **Selective Restore**: Restore specific tables or data
- ✅ **Clean Restore**: Drop existing objects before restore
- ✅ **Verification**: Pre-restore backup verification
- ✅ **Rollback Support**: Quick rollback to previous state

### **Using Backup System**

#### **Web Interface**
1. Go to **Database Management** → **Backups**
2. Click **Create Backup** to start manual backup
3. Use **Restore Backup** to restore from existing backup
4. Configure **Scheduled Backups** for automation

#### **Command Line**
```bash
# Create backup
python backup_cli.py backup --name "daily_backup" --type full

# List backups
python backup_cli.py list

# Restore backup
python backup_cli.py restore --backup backups/daily_backup_20231201_020000.sql

# Verify backup
python backup_cli.py verify --backup backups/daily_backup_20231201_020000.sql

# Cleanup old backups
python backup_cli.py cleanup --days 30
```

#### **Backup Service**
```bash
# Start backup service (runs scheduled backups)
python backup_service.py --daemon

# Create immediate backup
python backup_service.py --backup "emergency_backup"
```

### **Backup Configuration**
Edit `erp.conf` to configure backup settings:
```json
{
  "backup": {
    "path": "backups",
    "retention_days": 30,
    "compression_enabled": true,
    "encryption_enabled": false,
    "auto_cleanup": true,
    "scheduled_backups": true
  }
}
```

## 🔌 Addon Management System

Ocean ERP includes a comprehensive addon management system similar to Odoo:

### **Addon Features**
- ✅ **Addon Discovery**: Automatic scanning of addons directory
- ✅ **Install/Uninstall**: Easy addon installation and removal
- ✅ **Dependency Management**: Automatic dependency resolution
- ✅ **Addon Marketplace**: Third-party addon marketplace
- ✅ **Development Tools**: Addon development templates and tools
- ✅ **Version Management**: Addon version tracking and updates
- ✅ **Compatibility Checking**: Pre-installation compatibility checks

### **Using Addon System**

#### **Web Interface**
1. Go to **Addon Manager** → **Addon Manager**
2. Browse **Available Addons** to see uninstalled addons
3. View **Installed Addons** to manage current addons
4. Use **Applications** to see application-type addons
5. Check **Addon Marketplace** for third-party addons
6. Use **Addon Development** for creating new addons

#### **Command Line**
```bash
# List all addons
python addon_cli.py list

# List installed addons
python addon_cli.py list --installed

# Install addon
python addon_cli.py install addon_name

# Uninstall addon
python addon_cli.py uninstall addon_name

# Show addon information
python addon_cli.py info addon_name

# Check dependencies
python addon_cli.py deps addon_name

# Create new addon
python addon_cli.py create my_addon --template basic --author "Your Name"
```

### **Addon Development**

#### **Creating New Addons**
1. Use the **Addon Development** interface
2. Choose from templates: Basic, Model, View, Wizard, Report, Integration
3. Fill in addon details and requirements
4. Generate addon structure automatically

#### **Addon Structure**
```
addons/my_addon/
├── __manifest__.py          # Addon metadata
├── __init__.py              # Python package init
├── models/                  # Data models
│   ├── __init__.py
│   └── my_model.py
├── views/                   # User interface
│   ├── menu.xml
│   └── my_views.xml
├── security/                # Access control
│   ├── ir.model.access.csv
│   └── security.xml
├── data/                    # Initial data
│   └── data.xml
├── demo/                    # Demo data
│   └── demo.xml
└── static/                 # Web assets
    ├── src/css/
    └── src/js/
```

#### **Addon Manifest**
```python
{
    'name': 'My Addon',
    'version': '1.0.0',
    'category': 'Custom',
    'summary': 'Short description',
    'description': 'Detailed description',
    'author': 'Your Name',
    'website': 'https://www.yourwebsite.com',
    'license': 'LGPL-3',
    'depends': ['core_base', 'users'],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
    ],
    'demo': [],
    'assets': {
        'web.assets_backend': [],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

### **Third-Party Addons**

#### **Marketplace Integration**
- ✅ **Browse Addons**: Search and filter marketplace addons
- ✅ **Reviews & Ratings**: User reviews and ratings system
- ✅ **Pricing**: Free and paid addons support
- ✅ **Downloads**: Direct download and installation
- ✅ **Categories**: Organized by business function

#### **Installing from Marketplace**
1. Go to **Addon Manager** → **Addon Marketplace**
2. Browse or search for addons
3. Click **Install** on desired addon
4. System automatically downloads and installs

## 🎉 Success!

After completing the setup wizard, you'll have:

- ✅ **Complete ERP System**: All modules installed and configured
- ✅ **Admin Account**: Secure administrator access
- ✅ **Company Setup**: Business information configured
- ✅ **Logo System**: Company branding in place
- ✅ **Master Data**: Age groups, seasons, genders loaded
- ✅ **System Settings**: All configurations optimized
- ✅ **Backup System**: Comprehensive backup and restore functionality
- ✅ **Addon Management**: Full addon system like Odoo

## 📞 Support

If you encounter any issues:

1. **Check Logs**: `tail -f erp.log`
2. **Verify Database**: `psql -h localhost -U erp_user -d ocean_erp`
3. **Test Setup**: `python3 run_erp.py --debug`
4. **Restart Service**: `sudo systemctl restart ocean-erp`

---

**Ocean ERP** - Complete Kids Clothing Retail Management System 🌊👶👕