# 🚀 Kids Clothing ERP - Installation Guide

## 📋 **SYSTEM REQUIREMENTS**

### **Minimum Requirements**
- **OS**: Ubuntu 20.04+ / CentOS 8+ / Windows 10+ / macOS 10.15+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 20GB free space
- **CPU**: 2 cores minimum, 4 cores recommended

### **Software Requirements**
- **Python**: 3.8 or higher
- **PostgreSQL**: 12 or higher
- **Node.js**: 16 or higher (for frontend assets)
- **Git**: Latest version

---

## 🔧 **INSTALLATION STEPS**

### **Step 1: System Preparation**

#### **Ubuntu/Debian**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib git curl

# Install Node.js
curl -fsSL https://deb.nodesource.com/setup_16.x | sudo -E bash -
sudo apt install -y nodejs
```

#### **CentOS/RHEL**
```bash
# Update system
sudo yum update -y

# Install required packages
sudo yum install -y python3 python3-pip postgresql-server postgresql-contrib git curl

# Install Node.js
curl -fsSL https://rpm.nodesource.com/setup_16.x | sudo bash -
sudo yum install -y nodejs
```

#### **Windows**
1. Install Python 3.8+ from [python.org](https://python.org)
2. Install PostgreSQL from [postgresql.org](https://postgresql.org)
3. Install Node.js from [nodejs.org](https://nodejs.org)
4. Install Git from [git-scm.com](https://git-scm.com)

#### **macOS**
```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install required packages
brew install python3 postgresql node git
```

### **Step 2: Database Setup**

#### **PostgreSQL Configuration**
```bash
# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create database and user
sudo -u postgres psql
```

```sql
-- Create database
CREATE DATABASE kids_clothing_erp;

-- Create user
CREATE USER erp_user WITH PASSWORD 'erp_password';

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE kids_clothing_erp TO erp_user;

-- Exit PostgreSQL
\q
```

### **Step 3: Project Setup**

#### **Clone Repository**
```bash
# Clone the project
git clone https://github.com/your-org/kids-clothing-erp.git
cd kids-clothing-erp
```

#### **Python Environment Setup**
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### **Environment Configuration**
```bash
# Create environment file
cp erp.conf.example erp.conf

# Edit configuration
nano erp.conf
```

**Configuration Example:**
```ini
[database]
host = localhost
port = 5432
database = kids_clothing_erp
user = erp_user
password = erp_password

[server]
host = 0.0.0.0
port = 8069
workers = 4

[logging]
level = INFO
file = /var/log/erp.log

[security]
secret_key = your-secret-key-here
```

### **Step 4: Database Initialization**

```bash
# Initialize database
python3 run_erp.py --init-db

# Create superuser
python3 run_erp.py --create-superuser
```

### **Step 5: Start the Application**

#### **Development Mode**
```bash
# Start development server
python3 run_erp.py --dev

# Access the application
# Open browser: http://localhost:8069
```

#### **Production Mode**
```bash
# Start production server
python3 run_erp.py --prod

# Or use systemd service
sudo systemctl start kids-clothing-erp
sudo systemctl enable kids-clothing-erp
```

---

## 🔧 **CONFIGURATION**

### **Database Configuration**

#### **PostgreSQL Optimization**
```sql
-- Edit postgresql.conf
sudo nano /etc/postgresql/12/main/postgresql.conf

# Add these settings:
shared_buffers = 256MB
effective_cache_size = 1GB
work_mem = 4MB
maintenance_work_mem = 64MB
checkpoint_completion_target = 0.9
wal_buffers = 16MB
default_statistics_target = 100
```

#### **Restart PostgreSQL**
```bash
sudo systemctl restart postgresql
```

### **Application Configuration**

#### **ERP Configuration File**
```ini
[core]
addons_path = addons
data_dir = /var/lib/kids-clothing-erp
log_level = INFO

[database]
host = localhost
port = 5432
database = kids_clothing_erp
user = erp_user
password = erp_password
max_conn = 20

[server]
host = 0.0.0.0
port = 8069
workers = 4
timeout = 300

[security]
secret_key = your-secret-key-here
session_timeout = 3600

[email]
smtp_server = smtp.gmail.com
smtp_port = 587
smtp_user = your-email@gmail.com
smtp_password = your-app-password

[notifications]
email_enabled = true
sms_enabled = false
push_enabled = false
```

### **Addon Configuration**

#### **Enable Addons**
```bash
# Install all addons
python3 run_erp.py --install-addons

# Install specific addons
python3 run_erp.py --install-addon reports
python3 run_erp.py --install-addon dashboard
python3 run_erp.py --install-addon analytics
```

---

## 🚀 **DEPLOYMENT**

### **Production Deployment**

#### **Using Docker**
```bash
# Build Docker image
docker build -t kids-clothing-erp .

# Run with Docker Compose
docker-compose up -d
```

#### **Using Systemd**
```bash
# Create systemd service file
sudo nano /etc/systemd/system/kids-clothing-erp.service
```

**Service File:**
```ini
[Unit]
Description=Kids Clothing ERP
After=network.target postgresql.service

[Service]
Type=simple
User=erp
Group=erp
WorkingDirectory=/opt/kids-clothing-erp
ExecStart=/opt/kids-clothing-erp/venv/bin/python run_erp.py --prod
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable kids-clothing-erp
sudo systemctl start kids-clothing-erp
```

#### **Using Nginx**
```bash
# Install Nginx
sudo apt install nginx

# Create Nginx configuration
sudo nano /etc/nginx/sites-available/kids-clothing-erp
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8069;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /opt/kids-clothing-erp/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/kids-clothing-erp /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 🔒 **SECURITY CONFIGURATION**

### **SSL Certificate**
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your-domain.com
```

### **Firewall Configuration**
```bash
# Configure UFW
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

### **Database Security**
```sql
-- Create read-only user
CREATE USER erp_readonly WITH PASSWORD 'readonly_password';
GRANT CONNECT ON DATABASE kids_clothing_erp TO erp_readonly;
GRANT USAGE ON SCHEMA public TO erp_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO erp_readonly;
```

---

## 📊 **MONITORING & MAINTENANCE**

### **Log Monitoring**
```bash
# View application logs
tail -f /var/log/kids-clothing-erp.log

# View system logs
journalctl -u kids-clothing-erp -f
```

### **Database Backup**
```bash
# Create backup script
nano backup.sh
```

**Backup Script:**
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/kids-clothing-erp"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="kids_clothing_erp"

# Create backup directory
mkdir -p $BACKUP_DIR

# Create database backup
pg_dump -h localhost -U erp_user $DB_NAME > $BACKUP_DIR/erp_backup_$DATE.sql

# Compress backup
gzip $BACKUP_DIR/erp_backup_$DATE.sql

# Keep only last 7 days of backups
find $BACKUP_DIR -name "erp_backup_*.sql.gz" -mtime +7 -delete
```

```bash
# Make executable and schedule
chmod +x backup.sh
crontab -e

# Add daily backup at 2 AM
0 2 * * * /opt/kids-clothing-erp/backup.sh
```

### **Performance Monitoring**
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs

# Monitor system resources
htop
iotop
nethogs
```

---

## 🧪 **TESTING**

### **Run Tests**
```bash
# Run all tests
python3 run_erp.py --test

# Run specific addon tests
python3 run_erp.py --test-addon reports
python3 run_erp.py --test-addon dashboard
python3 run_erp.py --test-addon analytics
```

### **Load Testing**
```bash
# Install Apache Bench
sudo apt install apache2-utils

# Run load test
ab -n 1000 -c 10 http://localhost:8069/
```

---

## 🔧 **TROUBLESHOOTING**

### **Common Issues**

#### **Database Connection Error**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Check database connectivity
psql -h localhost -U erp_user -d kids_clothing_erp
```

#### **Port Already in Use**
```bash
# Check port usage
sudo netstat -tlnp | grep 8069

# Kill process using port
sudo kill -9 $(sudo lsof -t -i:8069)
```

#### **Permission Issues**
```bash
# Fix file permissions
sudo chown -R erp:erp /opt/kids-clothing-erp
sudo chmod -R 755 /opt/kids-clothing-erp
```

### **Log Analysis**
```bash
# Check error logs
grep -i error /var/log/kids-clothing-erp.log

# Check warning logs
grep -i warning /var/log/kids-clothing-erp.log
```

---

## 📞 **SUPPORT**

### **Getting Help**
- **Documentation**: Check the project documentation
- **Issues**: Report issues on GitHub
- **Community**: Join our community forum
- **Email**: support@kidsclothingerp.com

### **Professional Support**
- **Consulting**: Custom implementation services
- **Training**: User and administrator training
- **Maintenance**: Ongoing support and maintenance
- **Customization**: Business-specific customizations

---

## 🎉 **SUCCESS!**

Your Kids Clothing ERP system is now installed and ready to use!

**Access your ERP system:**
- **URL**: http://your-domain.com or http://localhost:8069
- **Username**: admin
- **Password**: admin (change immediately!)

**Next Steps:**
1. Change default passwords
2. Configure company settings
3. Import your business data
4. Set up user accounts
5. Customize dashboards and reports
6. Train your team

Welcome to your new Kids Clothing ERP system! 🎉