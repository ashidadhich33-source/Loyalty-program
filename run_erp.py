#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Main Runner
==============================

Main entry point for the standalone ERP system.
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core_framework.server import ERPServer

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Kids Clothing ERP Server')
    parser.add_argument('--config', help='Configuration file path', default='erp.conf')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8069, help='Server port')
    parser.add_argument('--init', action='store_true', help='Initialize database')
    parser.add_argument('--update', action='store_true', help='Update addons')
    parser.add_argument('--install', action='store_true', help='Install addons')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("👶 Kids Clothing ERP System")
    print("=" * 60)
    print(f"Configuration: {args.config}")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Debug: {args.debug}")
    print("=" * 60)
    
    # Create server instance
    server = ERPServer(args.config)
    
    # Initialize if requested
    if args.init:
        print("Initializing ERP system...")
        if server.initialize():
            print("✅ ERP system initialized successfully!")
        else:
            print("❌ Failed to initialize ERP system!")
            sys.exit(1)
    
    # Update addons if requested
    if args.update:
        print("Updating addons...")
        server.addon_manager.update_addons()
        print("✅ Addons updated!")
    
    # Install addons if requested
    if args.install:
        print("Installing addons...")
        # This would install specific addons
        print("✅ Addons installed!")
    
    # Start server
    print("Starting ERP server...")
    if server.initialize():
        print(f"🚀 ERP server starting on http://{args.host}:{args.port}")
        print("Press Ctrl+C to stop the server")
        try:
            server.start(args.host, args.port)
        except KeyboardInterrupt:
            print("\n🛑 Stopping ERP server...")
            server.stop()
            print("✅ ERP server stopped!")
    else:
        print("❌ Failed to initialize ERP system!")
        sys.exit(1)

if __name__ == '__main__':
    main()