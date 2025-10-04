# 🌊 Ocean ERP - Complete Setup Guide

## Overview

Ocean ERP now includes a **complete setup wizard** similar to Odoo's database creation wizard, plus offline and 404 pages with logo support. This guide will walk you through the entire setup process.

## 🚀 Quick Start

### 1. Bootstrap the System
```bash
# Run the bootstrap script to set up the environment
python3 bootstrap_ocean_erp.py
```

### 2. Set Up PostgreSQL Database
```bash
# Create database and user
sudo -u postgres createdb ocean_erp
sudo -u postgres createuser erp_user
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;"
sudo -u postgres psql -c "ALTER USER erp_user CREATEDB;"
```

### 3. Start Ocean ERP Server
```bash
# Start the server
python3 run_erp.py
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
```bash
# Check if server is running
python3 run_erp.py

# Check logs
tail -f erp.log
```

#### 2. Database Connection Failed
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Test connection
psql -h localhost -U erp_user -d ocean_erp
```

#### 3. Logo Not Displaying
```bash
# Check logo file exists
ls -la static/images/logo/

# Check file permissions
chmod 644 static/images/logo/*
```

#### 4. Setup Already Complete
```bash
# Remove setup completion marker
rm .ocean_setup_complete

# Restart server
python3 run_erp.py
```

### Debug Mode
```bash
# Enable debug mode
python3 run_erp.py --debug

# Check detailed logs
tail -f erp.log
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
- **OS**: Linux, macOS, Windows with WSL2
- **Python**: 3.8+
- **PostgreSQL**: 12+
- **RAM**: 4GB
- **Storage**: 10GB
- **Network**: Port 8069 available

### Recommended Requirements
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **Python**: 3.11+
- **PostgreSQL**: 14+
- **RAM**: 8GB+
- **Storage**: 50GB+
- **Network**: Dedicated server

## 🎯 Production Deployment

### Systemd Service
```bash
# Create service file
sudo nano /etc/systemd/system/ocean-erp.service

# Enable and start service
sudo systemctl enable ocean-erp
sudo systemctl start ocean-erp
```

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### SSL Certificate
```bash
# Install Let's Encrypt
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com
```

## 🎉 Success!

After completing the setup wizard, you'll have:

- ✅ **Complete ERP System**: All modules installed and configured
- ✅ **Admin Account**: Secure administrator access
- ✅ **Company Setup**: Business information configured
- ✅ **Logo System**: Company branding in place
- ✅ **Master Data**: Age groups, seasons, genders loaded
- ✅ **System Settings**: All configurations optimized

## 📞 Support

If you encounter any issues:

1. **Check Logs**: `tail -f erp.log`
2. **Verify Database**: `psql -h localhost -U erp_user -d ocean_erp`
3. **Test Setup**: `python3 run_erp.py --debug`
4. **Restart Service**: `sudo systemctl restart ocean-erp`

---

**Ocean ERP** - Complete Kids Clothing Retail Management System 🌊👶👕