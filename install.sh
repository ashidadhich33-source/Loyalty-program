#!/bin/bash
# Kids Clothing ERP - Installation Script
# =======================================

echo "👶 Kids Clothing ERP - Installation Script"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python3 --version

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create necessary directories
echo "Creating directories..."
mkdir -p static
mkdir -p templates
mkdir -p logs

# Set permissions
echo "Setting permissions..."
chmod +x run_erp.py

# Create database user (if needed)
echo "Setting up database..."
echo "Note: Make sure PostgreSQL is installed and running"
echo "Create database user: erp_user"
echo "Create database: kids_clothing_erp"

echo ""
echo "✅ Installation completed!"
echo ""
echo "To start the ERP system:"
echo "  python3 run_erp.py"
echo ""
echo "To initialize the database:"
echo "  python3 run_erp.py --init"
echo ""
echo "Access the system at: http://localhost:8069"
echo ""