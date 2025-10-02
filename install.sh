#!/bin/bash

# Kids Clothing ERP - Installation Script
# This script installs and sets up the Kids Clothing ERP system

set -e

echo "🎯 Kids Clothing ERP - Installation Script"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   print_error "This script should not be run as root"
   exit 1
fi

# Check Python version
print_info "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    print_error "Python 3 is required but not installed"
    exit 1
fi

# Check PostgreSQL
print_info "Checking PostgreSQL..."
if ! command -v psql &> /dev/null; then
    print_warning "PostgreSQL not found. Please install PostgreSQL 12+ first"
    print_info "Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
    print_info "CentOS/RHEL: sudo yum install postgresql-server postgresql-contrib"
    exit 1
fi

# Check if PostgreSQL is running
if ! pg_isready -q; then
    print_error "PostgreSQL is not running. Please start PostgreSQL first"
    print_info "Ubuntu/Debian: sudo systemctl start postgresql"
    print_info "CentOS/RHEL: sudo systemctl start postgresql"
    exit 1
fi

print_status "PostgreSQL is running"

# Create virtual environment
print_info "Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

print_status "Python dependencies installed"

# Create database
print_info "Creating database..."
DB_NAME="kids_clothing_erp"
DB_USER="odoo"
DB_PASSWORD="odoo"

# Check if database exists
if psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    print_warning "Database $DB_NAME already exists"
else
    # Create database
    sudo -u postgres createdb $DB_NAME
    print_status "Database $DB_NAME created"
fi

# Create database user
print_info "Creating database user..."
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || print_warning "User $DB_USER already exists"
sudo -u postgres psql -c "ALTER USER $DB_USER CREATEDB;" 2>/dev/null || true
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;" 2>/dev/null || true

print_status "Database user configured"

# Create logs directory
print_info "Creating logs directory..."
mkdir -p logs
print_status "Logs directory created"

# Create data directory
print_info "Creating data directory..."
mkdir -p data
print_status "Data directory created"

# Set up configuration
print_info "Setting up configuration..."
if [ ! -f "odoo.conf" ]; then
    print_error "Configuration file odoo.conf not found"
    exit 1
fi

# Update configuration with correct paths
sed -i "s|addons_path = .*|addons_path = $(pwd),$(pwd)/odoo/addons|g" odoo.conf
sed -i "s|data_dir = .*|data_dir = $(pwd)/data|g" odoo.conf
sed -i "s|logfile = .*|logfile = $(pwd)/logs/odoo-server.log|g" odoo.conf

print_status "Configuration updated"

# Install Odoo
print_info "Installing Odoo..."
if [ ! -d "odoo" ]; then
    print_info "Downloading Odoo 17.0..."
    wget -q https://nightly.odoo.com/17.0/nightly/src/odoo_17.0.latest.tar.gz
    tar -xzf odoo_17.0.latest.tar.gz
    rm odoo_17.0.latest.tar.gz
    print_status "Odoo downloaded and extracted"
else
    print_warning "Odoo directory already exists"
fi

# Install Odoo dependencies
print_info "Installing Odoo dependencies..."
cd odoo
pip install -r requirements.txt
cd ..

print_status "Odoo dependencies installed"

# Initialize database
print_info "Initializing database..."
python3 odoo/odoo-bin -c odoo.conf -d $DB_NAME --init=base --stop-after-init

print_status "Database initialized"

# Install Kids Clothing ERP module
print_info "Installing Kids Clothing ERP module..."
python3 odoo/odoo-bin -c odoo.conf -d $DB_NAME -i kids_clothing_erp --stop-after-init

print_status "Kids Clothing ERP module installed"

# Create startup script
print_info "Creating startup script..."
cat > start_erp.sh << 'EOF'
#!/bin/bash
# Kids Clothing ERP Startup Script

# Activate virtual environment
source venv/bin/activate

# Start Odoo server
python3 odoo/odoo-bin -c odoo.conf -d kids_clothing_erp
EOF

chmod +x start_erp.sh
print_status "Startup script created"

# Create systemd service (optional)
print_info "Creating systemd service..."
sudo tee /etc/systemd/system/kids-clothing-erp.service > /dev/null << EOF
[Unit]
Description=Kids Clothing ERP
After=network.target postgresql.service

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
ExecStart=$(pwd)/start_erp.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

print_status "Systemd service created"

# Enable service (optional)
read -p "Do you want to enable the systemd service? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    sudo systemctl daemon-reload
    sudo systemctl enable kids-clothing-erp
    print_status "Systemd service enabled"
fi

# Final instructions
echo
echo "🎉 Kids Clothing ERP Installation Complete!"
echo "========================================"
echo
print_info "To start the ERP system:"
echo "  ./start_erp.sh"
echo
print_info "Or using systemd:"
echo "  sudo systemctl start kids-clothing-erp"
echo
print_info "Access the system at:"
echo "  http://localhost:8069"
echo
print_info "Default login credentials:"
echo "  Username: admin"
echo "  Password: admin"
echo
print_info "Configuration file: odoo.conf"
print_info "Logs directory: logs/"
print_info "Data directory: data/"
echo
print_warning "Remember to change the default password after first login!"
echo
print_status "Installation completed successfully! 🚀"