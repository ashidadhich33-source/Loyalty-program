#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ocean ERP - Addon CLI Tool
=========================

Command-line tool for addon management operations.
"""

import argparse
import sys
import json
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core_framework.addon_manager import AddonManager
from core_framework.config import Config

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description='Ocean ERP Addon CLI Tool')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List addons')
    list_parser.add_argument('--installed', '-i', action='store_true', help='Show only installed addons')
    list_parser.add_argument('--available', '-a', action='store_true', help='Show only available addons')
    list_parser.add_argument('--format', '-f', choices=['table', 'json'], default='table', 
                            help='Output format')
    
    # Install command
    install_parser = subparsers.add_parser('install', help='Install addon')
    install_parser.add_argument('addon_name', help='Addon name to install')
    install_parser.add_argument('--force', action='store_true', help='Force installation')
    
    # Uninstall command
    uninstall_parser = subparsers.add_parser('uninstall', help='Uninstall addon')
    uninstall_parser.add_argument('addon_name', help='Addon name to uninstall')
    uninstall_parser.add_argument('--force', action='store_true', help='Force uninstallation')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update addon')
    update_parser.add_argument('addon_name', help='Addon name to update')
    update_parser.add_argument('--all', action='store_true', help='Update all addons')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show addon information')
    info_parser.add_argument('addon_name', help='Addon name')
    
    # Dependencies command
    deps_parser = subparsers.add_parser('deps', help='Show addon dependencies')
    deps_parser.add_argument('addon_name', help='Addon name')
    deps_parser.add_argument('--reverse', '-r', action='store_true', help='Show reverse dependencies')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check addon compatibility')
    check_parser.add_argument('addon_name', help='Addon name')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create new addon')
    create_parser.add_argument('addon_name', help='Addon name')
    create_parser.add_argument('--template', '-t', choices=['basic', 'model', 'view', 'wizard'], 
                              default='basic', help='Template type')
    create_parser.add_argument('--author', help='Author name')
    create_parser.add_argument('--description', help='Addon description')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan for new addons')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        # Load configuration
        config = Config()
        addon_manager = AddonManager(config)
        
        # Load addons
        addon_manager.load_addons()
        
        if args.command == 'list':
            return handle_list(addon_manager, args)
        elif args.command == 'install':
            return handle_install(addon_manager, args)
        elif args.command == 'uninstall':
            return handle_uninstall(addon_manager, args)
        elif args.command == 'update':
            return handle_update(addon_manager, args)
        elif args.command == 'info':
            return handle_info(addon_manager, args)
        elif args.command == 'deps':
            return handle_deps(addon_manager, args)
        elif args.command == 'check':
            return handle_check(addon_manager, args)
        elif args.command == 'create':
            return handle_create(addon_manager, args)
        elif args.command == 'scan':
            return handle_scan(addon_manager, args)
        
    except Exception as e:
        print(f"Error: {e}")
        return 1

def handle_list(addon_manager, args):
    """Handle list command"""
    addons = addon_manager.list_addons()
    
    if args.installed:
        addons = [a for a in addons if a['installed']]
    elif args.available:
        addons = [a for a in addons if not a['installed']]
    
    if args.format == 'json':
        print(json.dumps(addons, indent=2, default=str))
    else:
        if not addons:
            print("No addons found.")
            return 0
        
        print(f"{'Name':<30} {'Version':<15} {'Status':<15} {'Category':<20}")
        print("-" * 80)
        
        for addon in addons:
            status = "Installed" if addon['installed'] else "Available"
            manifest = addon['manifest']
            print(f"{addon['name']:<30} {manifest.get('version', 'N/A'):<15} "
                  f"{status:<15} {manifest.get('category', 'N/A'):<20}")
    
    return 0

def handle_install(addon_manager, args):
    """Handle install command"""
    print(f"Installing addon: {args.addon_name}")
    
    # Check compatibility first
    compatibility = addon_manager.check_addon_compatibility(args.addon_name)
    if not compatibility['compatible'] and not args.force:
        print(f"✗ Addon not compatible: {compatibility.get('error')}")
        if compatibility.get('missing_dependencies'):
            print(f"Missing dependencies: {', '.join(compatibility['missing_dependencies'])}")
        return 1
    
    # Install addon
    success = addon_manager.install_addon(args.addon_name)
    
    if success:
        print(f"✓ Addon {args.addon_name} installed successfully!")
        return 0
    else:
        print(f"✗ Failed to install addon {args.addon_name}")
        return 1

def handle_uninstall(addon_manager, args):
    """Handle uninstall command"""
    print(f"Uninstalling addon: {args.addon_name}")
    
    # Check reverse dependencies
    reverse_deps = addon_manager.get_addon_reverse_dependencies(args.addon_name)
    if reverse_deps and not args.force:
        print(f"✗ Cannot uninstall {args.addon_name}: other addons depend on it")
        print(f"Dependent addons: {', '.join(reverse_deps)}")
        return 1
    
    # Uninstall addon
    success = addon_manager.uninstall_addon(args.addon_name)
    
    if success:
        print(f"✓ Addon {args.addon_name} uninstalled successfully!")
        return 0
    else:
        print(f"✗ Failed to uninstall addon {args.addon_name}")
        return 1

def handle_update(addon_manager, args):
    """Handle update command"""
    if args.all:
        print("Updating all addons...")
        success = addon_manager.update_addons()
        if success:
            print("✓ All addons updated successfully!")
            return 0
        else:
            print("✗ Failed to update addons")
            return 1
    else:
        print(f"Updating addon: {args.addon_name}")
        addon_manager._update_addon(args.addon_name)
        print(f"✓ Addon {args.addon_name} updated successfully!")
        return 0

def handle_info(addon_manager, args):
    """Handle info command"""
    addon_info = addon_manager.get_addon_info(args.addon_name)
    
    if not addon_info:
        print(f"✗ Addon {args.addon_name} not found")
        return 1
    
    manifest = addon_info['manifest']
    
    print(f"Addon Information: {args.addon_name}")
    print("=" * 50)
    print(f"Name: {manifest.get('name', 'N/A')}")
    print(f"Version: {manifest.get('version', 'N/A')}")
    print(f"Category: {manifest.get('category', 'N/A')}")
    print(f"Author: {manifest.get('author', 'N/A')}")
    print(f"Website: {manifest.get('website', 'N/A')}")
    print(f"License: {manifest.get('license', 'N/A')}")
    print(f"Installed: {addon_info['installed']}")
    print(f"Path: {addon_info['path']}")
    
    if manifest.get('depends'):
        print(f"Dependencies: {', '.join(manifest['depends'])}")
    
    if manifest.get('description'):
        print(f"\nDescription:")
        print(manifest['description'])
    
    return 0

def handle_deps(addon_manager, args):
    """Handle dependencies command"""
    if args.reverse:
        deps = addon_manager.get_addon_reverse_dependencies(args.addon_name)
        print(f"Addons that depend on {args.addon_name}:")
    else:
        deps = addon_manager.get_addon_dependencies(args.addon_name)
        print(f"Dependencies of {args.addon_name}:")
    
    if deps:
        for dep in deps:
            print(f"  - {dep}")
    else:
        print("  None")
    
    return 0

def handle_check(addon_manager, args):
    """Handle check command"""
    compatibility = addon_manager.check_addon_compatibility(args.addon_name)
    
    print(f"Compatibility check for {args.addon_name}:")
    print("=" * 50)
    
    if compatibility['compatible']:
        print("✓ Addon is compatible")
    else:
        print("✗ Addon is not compatible")
        print(f"Error: {compatibility.get('error')}")
    
    if compatibility.get('missing_dependencies'):
        print(f"Missing dependencies: {', '.join(compatibility['missing_dependencies'])}")
    
    if compatibility.get('external_dependencies'):
        print(f"External dependencies: {', '.join(compatibility['external_dependencies'])}")
    
    return 0

def handle_create(addon_manager, args):
    """Handle create command"""
    print(f"Creating addon: {args.addon_name}")
    
    template_data = {
        'name': args.addon_name,
        'technical_name': args.addon_name.lower().replace(' ', '_'),
        'template_type': args.template,
        'author': args.author or 'Your Name',
        'description': args.description or f'Custom addon: {args.addon_name}',
    }
    
    success = addon_manager.create_addon_template(template_data)
    
    if success:
        print(f"✓ Addon {args.addon_name} created successfully!")
        print(f"Location: addons/{template_data['technical_name']}")
        return 0
    else:
        print(f"✗ Failed to create addon {args.addon_name}")
        return 1

def handle_scan(addon_manager, args):
    """Handle scan command"""
    print("Scanning for addons...")
    
    # Reload addons
    addon_manager.load_addons()
    
    addons = addon_manager.list_addons()
    print(f"✓ Found {len(addons)} addons")
    
    installed_count = sum(1 for a in addons if a['installed'])
    available_count = len(addons) - installed_count
    
    print(f"  - Installed: {installed_count}")
    print(f"  - Available: {available_count}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())