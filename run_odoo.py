#!/usr/bin/env python3
"""
Kids Clothing ERP - Odoo Server Runner
This script runs the Odoo server with the Kids Clothing ERP module
"""

import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Run Kids Clothing ERP Odoo Server')
    parser.add_argument('--config', '-c', default='odoo.conf', help='Configuration file')
    parser.add_argument('--database', '-d', default='kids_clothing_erp', help='Database name')
    parser.add_argument('--install', '-i', action='store_true', help='Install module')
    parser.add_argument('--update', '-u', action='store_true', help='Update module')
    parser.add_argument('--test', '-t', action='store_true', help='Run tests')
    parser.add_argument('--port', '-p', default='8069', help='Port number')
    parser.add_argument('--host', default='0.0.0.0', help='Host address')
    
    args = parser.parse_args()
    
    # Check if Odoo is installed
    try:
        import odoo
        print(f"✅ Odoo {odoo.release.version} found")
    except ImportError:
        print("❌ Odoo not found. Please install Odoo first.")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Build command
    cmd = [
        'python3', 'odoo-bin',
        '-c', args.config,
        '-d', args.database,
        '--http-port', args.port,
        '--http-interface', args.host,
    ]
    
    if args.install:
        cmd.extend(['-i', 'kids_clothing_erp'])
    elif args.update:
        cmd.extend(['-u', 'kids_clothing_erp'])
    
    if args.test:
        cmd.extend(['--test-enable', '--stop-after-init'])
    
    # Add development options
    cmd.extend([
        '--dev=all',  # Enable development mode
        '--log-level=info',
        '--logfile=odoo.log',
    ])
    
    print(f"🚀 Starting Kids Clothing ERP Server...")
    print(f"📊 Database: {args.database}")
    print(f"🌐 URL: http://{args.host}:{args.port}")
    print(f"⚙️  Config: {args.config}")
    
    if args.install:
        print("📦 Installing Kids Clothing ERP module...")
    elif args.update:
        print("🔄 Updating Kids Clothing ERP module...")
    
    if args.test:
        print("🧪 Running tests...")
    
    print("\n" + "="*50)
    print("🎯 Kids Clothing ERP - Odoo Server")
    print("="*50)
    
    try:
        # Run Odoo server
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Odoo server: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Kids Clothing ERP server...")
        sys.exit(0)

if __name__ == '__main__':
    main()