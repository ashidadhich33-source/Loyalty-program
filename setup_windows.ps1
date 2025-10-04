# Ocean ERP - Windows PowerShell Setup Script
# ==========================================

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Ocean ERP - Windows Setup Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "WARNING: Not running as Administrator" -ForegroundColor Yellow
    Write-Host "Some operations may fail. Please run as Administrator for best results." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to continue anyway"
}

Write-Host ""
Write-Host "Step 1: Checking system requirements..." -ForegroundColor Green
Write-Host ""

# Check Python
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Python is installed: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ from https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH' during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check pip
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ pip is available: $pipVersion" -ForegroundColor Green
    } else {
        throw "pip not found"
    }
} catch {
    Write-Host "✗ pip is not available" -ForegroundColor Red
    Write-Host "Please reinstall Python with pip included" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check PostgreSQL
try {
    $psqlVersion = psql --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ PostgreSQL is installed: $psqlVersion" -ForegroundColor Green
    } else {
        throw "PostgreSQL not found"
    }
} catch {
    Write-Host "✗ PostgreSQL is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install PostgreSQL from https://www.postgresql.org/download/windows/" -ForegroundColor Yellow
    Write-Host "Make sure to add PostgreSQL to PATH during installation" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 2: Installing Python dependencies..." -ForegroundColor Green
Write-Host ""

# Install requirements
try {
    Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
    } else {
        throw "Installation failed"
    }
} catch {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    Write-Host "Please check your internet connection and try again" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 3: Creating necessary directories..." -ForegroundColor Green
Write-Host ""

# Create directories
$directories = @(
    "static\images\logo",
    "static\css",
    "static\js",
    "templates",
    "uploads",
    "logs",
    "backups",
    "data",
    "config"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "✓ Created directory: $dir" -ForegroundColor Green
    } else {
        Write-Host "✓ Directory already exists: $dir" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "Step 4: Setting up PostgreSQL database..." -ForegroundColor Green
Write-Host ""

# Check PostgreSQL service
$postgresService = Get-Service -Name "postgresql-x64-15" -ErrorAction SilentlyContinue
if ($postgresService -and $postgresService.Status -eq "Running") {
    Write-Host "✓ PostgreSQL service is running" -ForegroundColor Green
} else {
    Write-Host "Starting PostgreSQL service..." -ForegroundColor Yellow
    try {
        Start-Service -Name "postgresql-x64-15" -ErrorAction Stop
        Write-Host "✓ PostgreSQL service started" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to start PostgreSQL service" -ForegroundColor Red
        Write-Host "Please start PostgreSQL service manually" -ForegroundColor Yellow
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Create database and user
Write-Host "Creating database and user..." -ForegroundColor Yellow

try {
    # Create database
    $createDbResult = psql -U postgres -c "CREATE DATABASE ocean_erp;" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Database 'ocean_erp' created" -ForegroundColor Green
    } else {
        Write-Host "Database 'ocean_erp' may already exist" -ForegroundColor Yellow
    }

    # Create user
    $createUserResult = psql -U postgres -c "CREATE USER erp_user WITH PASSWORD 'erp_password';" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ User 'erp_user' created" -ForegroundColor Green
    } else {
        Write-Host "User 'erp_user' may already exist" -ForegroundColor Yellow
    }

    # Grant permissions
    psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;" 2>&1 | Out-Null
    psql -U postgres -c "ALTER USER erp_user CREATEDB;" 2>&1 | Out-Null
    Write-Host "✓ Permissions granted to erp_user" -ForegroundColor Green

} catch {
    Write-Host "✗ Database setup failed" -ForegroundColor Red
    Write-Host "Please check PostgreSQL configuration" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 5: Configuring Windows Firewall..." -ForegroundColor Green
Write-Host ""

# Configure Windows Firewall
try {
    New-NetFirewallRule -DisplayName "Ocean ERP" -Direction Inbound -Protocol TCP -LocalPort 8069 -Action Allow -ErrorAction SilentlyContinue | Out-Null
    New-NetFirewallRule -DisplayName "PostgreSQL" -Direction Inbound -Protocol TCP -LocalPort 5432 -Action Allow -ErrorAction SilentlyContinue | Out-Null
    Write-Host "✓ Firewall rules added" -ForegroundColor Green
} catch {
    Write-Host "⚠ Could not configure firewall automatically" -ForegroundColor Yellow
    Write-Host "Please manually allow ports 8069 and 5432 in Windows Firewall" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 6: Setting up file permissions..." -ForegroundColor Green
Write-Host ""

# Set permissions
try {
    $directories = @("static", "uploads", "logs", "backups")
    foreach ($dir in $directories) {
        if (Test-Path $dir) {
            icacls $dir /grant Everyone:F /T 2>&1 | Out-Null
        }
    }
    Write-Host "✓ File permissions set" -ForegroundColor Green
} catch {
    Write-Host "⚠ Could not set all permissions automatically" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Green
Write-Host "1. Start Ocean ERP server:" -ForegroundColor White
Write-Host "   python run_erp.py" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Open your browser and go to:" -ForegroundColor White
Write-Host "   http://localhost:8069" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Complete the setup wizard" -ForegroundColor White
Write-Host ""
Write-Host "4. Login with your admin credentials" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to start the server
$startServer = Read-Host "Do you want to start Ocean ERP server now? (y/n)"
if ($startServer -eq "y" -or $startServer -eq "Y") {
    Write-Host ""
    Write-Host "Starting Ocean ERP server..." -ForegroundColor Green
    Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
    Write-Host ""
    python run_erp.py
} else {
    Write-Host ""
    Write-Host "You can start Ocean ERP later by running:" -ForegroundColor Green
    Write-Host "python run_erp.py" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Thank you for using Ocean ERP!" -ForegroundColor Cyan
Read-Host "Press Enter to exit"