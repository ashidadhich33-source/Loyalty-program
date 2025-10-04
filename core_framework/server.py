#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Core Server
==============================

Standalone ERP system built with custom technology stack.
This is the main server file that initializes and runs the ERP system.
"""

import os
import sys
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core_framework.config import Config
from core_framework.database import DatabaseManager
from core_framework.addon_manager import AddonManager
from core_framework.web_interface import WebInterface
from core_framework.orm import ORMManager
from core_framework.auth import AuthenticationManager
from core_framework.session import SessionManager
from core_framework.templates import TemplateEngine, TemplateRenderer

class ERPServer:
    """Main ERP Server Class"""
    
    def __init__(self, config_path=None):
        """Initialize the ERP Server"""
        self.config = Config(config_path)
        self.db_manager = DatabaseManager(self.config)
        self.orm_manager = ORMManager(self.config)
        self.addon_manager = AddonManager(self.config)
        self.web_interface = WebInterface(self.config)
        
        # Initialize new components
        self.auth_manager = AuthenticationManager(self.config)
        self.session_manager = SessionManager(self.config)
        self.template_engine = TemplateEngine(self.config)
        self.template_renderer = TemplateRenderer(self.template_engine)
        
        # Initialize logging
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('erp.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('ERP')
        
    def initialize(self):
        """Initialize the ERP system"""
        try:
            self.logger.info("Initializing Kids Clothing ERP System...")
            
            # Initialize database
            self.logger.info("Setting up database...")
            self.db_manager.initialize()
            
            # Initialize ORM
            self.logger.info("Setting up ORM...")
            self.orm_manager.initialize()
            
            # Load addons
            self.logger.info("Loading addons...")
            self.addon_manager.load_addons()
            
            # Initialize web interface
            self.logger.info("Setting up web interface...")
            self.web_interface.initialize()
            
            # Initialize authentication
            self.logger.info("Setting up authentication...")
            # Authentication is ready to use
            
            # Initialize session management
            self.logger.info("Setting up session management...")
            # Session management is ready to use
            
            # Initialize template engine
            self.logger.info("Setting up template engine...")
            # Template engine is ready to use
            
            self.logger.info("ERP System initialized successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize ERP system: {e}")
            return False
    
    def start(self, host='localhost', port=8069):
        """Start the ERP server"""
        try:
            self.logger.info(f"Starting ERP server on {host}:{port}")
            self.web_interface.start_server(host, port)
        except Exception as e:
            self.logger.error(f"Failed to start server: {e}")
            return False
    
    def stop(self):
        """Stop the ERP server"""
        self.logger.info("Stopping ERP server...")
        self.web_interface.stop_server()
        self.db_manager.close()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Kids Clothing ERP Server')
    parser.add_argument('--config', help='Configuration file path')
    parser.add_argument('--host', default='localhost', help='Server host')
    parser.add_argument('--port', type=int, default=8069, help='Server port')
    parser.add_argument('--init', action='store_true', help='Initialize database')
    parser.add_argument('--update', action='store_true', help='Update addons')
    parser.add_argument('--install', action='store_true', help='Install addons')
    
    args = parser.parse_args()
    
    # Create server instance
    server = ERPServer(args.config)
    
    # Initialize if requested
    if args.init:
        if server.initialize():
            print("ERP system initialized successfully!")
        else:
            print("Failed to initialize ERP system!")
            sys.exit(1)
    
    # Update addons if requested
    if args.update:
        server.addon_manager.update_addons()
    
    # Install addons if requested
    if args.install:
        server.addon_manager.install_addons()
    
    # Start server
    if server.initialize():
        server.start(args.host, args.port)
    else:
        print("Failed to initialize ERP system!")
        sys.exit(1)

if __name__ == '__main__':
    main()