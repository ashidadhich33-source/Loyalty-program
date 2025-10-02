#!/usr/bin/env python3
"""
Kids Clothing ERP - Test Runner
This script runs all tests for the Kids Clothing ERP system
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_tests(test_module=None, verbose=False, coverage=False):
    """Run tests for the Kids Clothing ERP system"""
    
    # Get the current directory
    current_dir = Path(__file__).parent
    
    # Build the test command
    cmd = ['python3', '-m', 'pytest']
    
    # Add test directory
    test_dir = current_dir / 'tests'
    if test_dir.exists():
        cmd.append(str(test_dir))
    
    # Add specific test module if provided
    if test_module:
        cmd.append(f'tests/test_{test_module}.py')
    
    # Add verbose flag
    if verbose:
        cmd.append('-v')
    
    # Add coverage flag
    if coverage:
        cmd.extend(['--cov=kids_clothing_erp', '--cov-report=html', '--cov-report=term'])
    
    # Add other useful flags
    cmd.extend([
        '--tb=short',  # Short traceback format
        '--strict-markers',  # Strict marker handling
        '--disable-warnings',  # Disable warnings
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    print("=" * 50)
    
    try:
        result = subprocess.run(cmd, check=True, cwd=current_dir)
        print("=" * 50)
        print("✅ All tests passed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print("=" * 50)
        print(f"❌ Tests failed with exit code: {e.returncode}")
        return False
    except FileNotFoundError:
        print("❌ pytest not found. Please install pytest:")
        print("pip install pytest pytest-cov")
        return False


def run_specific_tests():
    """Run specific test modules"""
    test_modules = [
        'res_partner',
        'product_template', 
        'sale_order',
        'pos_order',
        'pos_config',
        'pos_session',
        'stock_quant',
        'report_analytics',
    ]
    
    print("Available test modules:")
    for i, module in enumerate(test_modules, 1):
        print(f"{i}. {module}")
    
    try:
        choice = input("\nEnter test module number (or 'all' for all tests): ").strip()
        
        if choice.lower() == 'all':
            return run_tests(verbose=True, coverage=True)
        else:
            module_index = int(choice) - 1
            if 0 <= module_index < len(test_modules):
                module = test_modules[module_index]
                return run_tests(test_module=module, verbose=True)
            else:
                print("❌ Invalid choice")
                return False
    except (ValueError, KeyboardInterrupt):
        print("❌ Invalid input or cancelled")
        return False


def main():
    parser = argparse.ArgumentParser(description='Run Kids Clothing ERP Tests')
    parser.add_argument('--module', '-m', help='Specific test module to run')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--coverage', '-c', action='store_true', help='Run with coverage')
    parser.add_argument('--interactive', '-i', action='store_true', help='Interactive test selection')
    
    args = parser.parse_args()
    
    print("🧪 Kids Clothing ERP - Test Runner")
    print("=" * 50)
    
    if args.interactive:
        success = run_specific_tests()
    else:
        success = run_tests(
            test_module=args.module,
            verbose=args.verbose,
            coverage=args.coverage
        )
    
    if success:
        print("\n🎉 All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()