@echo off
REM Ocean ERP - Windows Setup Script
REM =================================

echo.
echo ========================================
echo    Ocean ERP - Windows Setup Script
echo ========================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator - Good!
) else (
    echo WARNING: Not running as Administrator
    echo Some operations may fail. Please run as Administrator for best results.
    echo.
    pause
)

echo.
echo Step 1: Checking system requirements...
echo.

REM Check Python
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ Python is installed
    python --version
) else (
    echo ✗ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

REM Check pip
pip --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ pip is available
) else (
    echo ✗ pip is not available
    echo Please reinstall Python with pip included
    pause
    exit /b 1
)

REM Check PostgreSQL
psql --version >nul 2>&1
if %errorLevel% == 0 (
    echo ✓ PostgreSQL is installed
    psql --version
) else (
    echo ✗ PostgreSQL is not installed or not in PATH
    echo Please install PostgreSQL from https://www.postgresql.org/download/windows/
    echo Make sure to add PostgreSQL to PATH during installation
    pause
    exit /b 1
)

echo.
echo Step 2: Installing Python dependencies...
echo.

REM Install requirements
pip install -r requirements.txt
if %errorLevel% == 0 (
    echo ✓ Dependencies installed successfully
) else (
    echo ✗ Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo Step 3: Creating necessary directories...
echo.

REM Create directories
if not exist "static\images\logo" mkdir "static\images\logo"
if not exist "static\css" mkdir "static\css"
if not exist "static\js" mkdir "static\js"
if not exist "templates" mkdir "templates"
if not exist "uploads" mkdir "uploads"
if not exist "logs" mkdir "logs"
if not exist "backups" mkdir "backups"
if not exist "data" mkdir "data"
if not exist "config" mkdir "config"

echo ✓ Directories created successfully

echo.
echo Step 4: Setting up PostgreSQL database...
echo.

REM Check if PostgreSQL service is running
sc query postgresql-x64-15 | find "RUNNING" >nul
if %errorLevel% == 0 (
    echo ✓ PostgreSQL service is running
) else (
    echo Starting PostgreSQL service...
    net start postgresql-x64-15
    if %errorLevel% == 0 (
        echo ✓ PostgreSQL service started
    ) else (
        echo ✗ Failed to start PostgreSQL service
        echo Please start PostgreSQL service manually
        pause
        exit /b 1
    )
)

REM Create database and user
echo Creating database and user...
psql -U postgres -c "CREATE DATABASE ocean_erp;" 2>nul
if %errorLevel% == 0 (
    echo ✓ Database 'ocean_erp' created
) else (
    echo Database 'ocean_erp' may already exist
)

psql -U postgres -c "CREATE USER erp_user WITH PASSWORD 'erp_password';" 2>nul
if %errorLevel% == 0 (
    echo ✓ User 'erp_user' created
) else (
    echo User 'erp_user' may already exist
)

psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE ocean_erp TO erp_user;" 2>nul
psql -U postgres -c "ALTER USER erp_user CREATEDB;" 2>nul
echo ✓ Permissions granted to erp_user

echo.
echo Step 5: Configuring Windows Firewall...
echo.

REM Configure Windows Firewall
netsh advfirewall firewall add rule name="Ocean ERP" dir=in action=allow protocol=TCP localport=8069 2>nul
netsh advfirewall firewall add rule name="PostgreSQL" dir=in action=allow protocol=TCP localport=5432 2>nul
echo ✓ Firewall rules added

echo.
echo Step 6: Setting up file permissions...
echo.

REM Set permissions
icacls "static" /grant Everyone:F /T >nul 2>&1
icacls "uploads" /grant Everyone:F /T >nul 2>&1
icacls "logs" /grant Everyone:F /T >nul 2>&1
icacls "backups" /grant Everyone:F /T >nul 2>&1
echo ✓ File permissions set

echo.
echo ========================================
echo    Setup Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Start Ocean ERP server:
echo    python run_erp.py
echo.
echo 2. Open your browser and go to:
echo    http://localhost:8069
echo.
echo 3. Complete the setup wizard
echo.
echo 4. Login with your admin credentials
echo.
echo ========================================
echo.

REM Ask if user wants to start the server
set /p start_server="Do you want to start Ocean ERP server now? (y/n): "
if /i "%start_server%"=="y" (
    echo.
    echo Starting Ocean ERP server...
    echo Press Ctrl+C to stop the server
    echo.
    python run_erp.py
) else (
    echo.
    echo You can start Ocean ERP later by running:
    echo python run_erp.py
)

echo.
echo Thank you for using Ocean ERP!
pause