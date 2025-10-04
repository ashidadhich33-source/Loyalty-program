#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Web Interface
=================================

Web interface for the standalone ERP system.
"""

import logging
from typing import Dict, List, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
from pathlib import Path
from .auth import AuthenticationManager
from .session import SessionManager
from .templates import TemplateEngine, TemplateRenderer

class ERPWebHandler(BaseHTTPRequestHandler):
    """HTTP Request Handler for ERP Web Interface"""
    
    def __init__(self, *args, erp_server=None, **kwargs):
        self.erp_server = erp_server
        self.auth_manager = erp_server.auth_manager if erp_server else None
        self.session_manager = erp_server.session_manager if erp_server else None
        self.template_renderer = erp_server.template_renderer if erp_server else None
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            path = urllib.parse.urlparse(self.path).path
            
            if path == '/':
                self._serve_home_page()
            elif path == '/login':
                self._serve_login_page()
            elif path == '/logout':
                self._serve_logout()
            elif path == '/api/status':
                self._serve_api_status()
            elif path.startswith('/api/'):
                self._serve_api_request(path)
            elif path.startswith('/static/'):
                self._serve_static_file(path)
            else:
                self._serve_404()
                
        except Exception as e:
            self._serve_500(str(e))
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            path = urllib.parse.urlparse(self.path).path
            
            if path == '/api/login':
                self._handle_login()
            elif path == '/api/logout':
                self._handle_logout()
            elif path.startswith('/api/'):
                self._handle_api_post(path)
            else:
                self._serve_404()
                
        except Exception as e:
            self._serve_500(str(e))
    
    def _serve_home_page(self):
        """Serve home page"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Kids Clothing ERP</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }
                .container {
                    max-width: 800px;
                    margin: 0 auto;
                    text-align: center;
                }
                .logo {
                    font-size: 3em;
                    margin-bottom: 20px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .subtitle {
                    font-size: 1.2em;
                    margin-bottom: 40px;
                    opacity: 0.9;
                }
                .features {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-top: 40px;
                }
                .feature {
                    background: rgba(255,255,255,0.1);
                    padding: 20px;
                    border-radius: 10px;
                    backdrop-filter: blur(10px);
                }
                .feature h3 {
                    margin-top: 0;
                    color: #ffd700;
                }
                .status {
                    margin-top: 40px;
                    padding: 20px;
                    background: rgba(0,255,0,0.2);
                    border-radius: 10px;
                    border: 1px solid rgba(0,255,0,0.3);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="logo">👶 Kids Clothing ERP</div>
                <div class="subtitle">Complete ERP Solution for Kids' Clothing Retail</div>
                
                <div class="features">
                    <div class="feature">
                        <h3>🛍️ Sales Management</h3>
                        <p>Quotations, Sales Orders, Invoicing</p>
                    </div>
                    <div class="feature">
                        <h3>🏪 Point of Sale</h3>
                        <p>Fast checkout, exchange/return handling</p>
                    </div>
                    <div class="feature">
                        <h3>📦 Inventory</h3>
                        <p>Stock management, warehouse operations</p>
                    </div>
                    <div class="feature">
                        <h3>👥 CRM</h3>
                        <p>Customer management, loyalty programs</p>
                    </div>
                    <div class="feature">
                        <h3>💰 Accounting</h3>
                        <p>Financial management, GST compliance</p>
                    </div>
                    <div class="feature">
                        <h3>📊 Reports</h3>
                        <p>Analytics, custom dashboards</p>
                    </div>
                </div>
                
                <div class="status">
                    <h3>✅ System Status</h3>
                    <p>ERP System is running successfully!</p>
                    <p>Addons loaded: <span id="addon-count">Loading...</span></p>
                </div>
            </div>
            
            <script>
                // Load system status
                fetch('/api/status')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('addon-count').textContent = data.addons_loaded;
                    })
                    .catch(error => {
                        console.error('Error loading status:', error);
                    });
            </script>
        </body>
        </html>
        """
        
        self._send_response(200, html_content, 'text/html')
    
    def _serve_login_page(self):
        """Serve login page"""
        html_content = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Login - Kids Clothing ERP</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    min-height: 100vh;
                }
                .login-container {
                    background: white;
                    padding: 40px;
                    border-radius: 10px;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
                    width: 400px;
                }
                .login-header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .login-header h1 {
                    color: #333;
                    margin: 0;
                }
                .login-header p {
                    color: #666;
                    margin: 10px 0 0 0;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                .form-group label {
                    display: block;
                    margin-bottom: 5px;
                    color: #333;
                    font-weight: bold;
                }
                .form-group input {
                    width: 100%;
                    padding: 12px;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    font-size: 16px;
                    box-sizing: border-box;
                }
                .form-group input:focus {
                    outline: none;
                    border-color: #667eea;
                }
                .login-button {
                    width: 100%;
                    padding: 12px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: transform 0.2s;
                }
                .login-button:hover {
                    transform: translateY(-2px);
                }
                .error-message {
                    color: #e74c3c;
                    text-align: center;
                    margin-top: 10px;
                    display: none;
                }
            </style>
        </head>
        <body>
            <div class="login-container">
                <div class="login-header">
                    <h1>👶 Kids Clothing ERP</h1>
                    <p>Please login to continue</p>
                </div>
                <form id="loginForm">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <input type="text" id="username" name="username" required>
                    </div>
                    <div class="form-group">
                        <label for="password">Password</label>
                        <input type="password" id="password" name="password" required>
                    </div>
                    <button type="submit" class="login-button">Login</button>
                    <div id="errorMessage" class="error-message"></div>
                </form>
            </div>
            
            <script>
                document.getElementById('loginForm').addEventListener('submit', async function(e) {
                    e.preventDefault();
                    
                    const username = document.getElementById('username').value;
                    const password = document.getElementById('password').value;
                    const errorMessage = document.getElementById('errorMessage');
                    
                    try {
                        const response = await fetch('/api/login', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ username, password })
                        });
                        
                        const result = await response.json();
                        
                        if (result.success) {
                            window.location.href = '/';
                        } else {
                            errorMessage.textContent = result.message;
                            errorMessage.style.display = 'block';
                        }
                    } catch (error) {
                        errorMessage.textContent = 'Login failed. Please try again.';
                        errorMessage.style.display = 'block';
                    }
                });
            </script>
        </body>
        </html>
        """
        
        self._send_response(200, html_content, 'text/html')
    
    def _serve_logout(self):
        """Serve logout page"""
        # Redirect to login page
        self.send_response(302)
        self.send_header('Location', '/login')
        self.end_headers()
    
    def _handle_login(self):
        """Handle login request"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                self._send_json_response(400, {
                    'success': False,
                    'message': 'Username and password are required'
                })
                return
            
            # Authenticate user
            if self.auth_manager:
                result = self.auth_manager.authenticate_user(username, password, self)
                
                if result['success']:
                    # Set session cookie
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Set-Cookie', f"session_id={result['session_id']}; HttpOnly; Secure; SameSite=Strict")
                    self.end_headers()
                    
                    self.wfile.write(json.dumps(result).encode('utf-8'))
                else:
                    self._send_json_response(401, result)
            else:
                self._send_json_response(500, {
                    'success': False,
                    'message': 'Authentication system not available'
                })
                
        except Exception as e:
            self._send_json_response(500, {
                'success': False,
                'message': f'Login error: {str(e)}'
            })
    
    def _handle_logout(self):
        """Handle logout request"""
        try:
            session_id = self._get_session_id()
            
            if self.auth_manager and session_id:
                result = self.auth_manager.logout_user(session_id)
                
                if result['success']:
                    # Clear session cookie
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Set-Cookie', 'session_id=; HttpOnly; Secure; SameSite=Strict; Max-Age=0')
                    self.end_headers()
                    
                    self.wfile.write(json.dumps(result).encode('utf-8'))
                else:
                    self._send_json_response(400, result)
            else:
                self._send_json_response(200, {
                    'success': True,
                    'message': 'Logged out successfully'
                })
                
        except Exception as e:
            self._send_json_response(500, {
                'success': False,
                'message': f'Logout error: {str(e)}'
            })
    
    def _get_session_id(self):
        """Get session ID from request"""
        # Check cookies
        if 'cookie' in self.headers:
            cookies = self.headers['cookie']
            for cookie in cookies.split(';'):
                if 'session_id=' in cookie:
                    return cookie.split('session_id=')[1].strip()
        
        # Check Authorization header
        if 'authorization' in self.headers:
            auth_header = self.headers['authorization']
            if auth_header.startswith('Bearer '):
                return auth_header[7:]
        
        return None
    
    def _serve_api_status(self):
        """Serve API status"""
        try:
            status_data = {
                'status': 'running',
                'addons_loaded': len(self.erp_server.addon_manager.loaded_addons),
                'addons': self.erp_server.addon_manager.list_installed_addons(),
                'database': 'connected',
                'version': '1.0.0'
            }
            
            self._send_json_response(200, status_data)
            
        except Exception as e:
            self._send_json_response(500, {'error': str(e)})
    
    def _serve_api_request(self, path: str):
        """Serve API requests"""
        # Extract API endpoint
        endpoint = path[5:]  # Remove '/api/' prefix
        
        if endpoint == 'models':
            self._serve_models_api()
        elif endpoint == 'addons':
            self._serve_addons_api()
        else:
            self._send_json_response(404, {'error': 'API endpoint not found'})
    
    def _serve_models_api(self):
        """Serve models API"""
        try:
            models = list(self.erp_server.orm_manager.models.keys())
            self._send_json_response(200, {'models': models})
        except Exception as e:
            self._send_json_response(500, {'error': str(e)})
    
    def _serve_addons_api(self):
        """Serve addons API"""
        try:
            addons = self.erp_server.addon_manager.list_addons()
            self._send_json_response(200, {'addons': addons})
        except Exception as e:
            self._send_json_response(500, {'error': str(e)})
    
    def _handle_api_post(self, path: str):
        """Handle API POST requests"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            endpoint = path[5:]  # Remove '/api/' prefix
            
            if endpoint == 'addons/install':
                self._handle_install_addon(data)
            elif endpoint == 'addons/uninstall':
                self._handle_uninstall_addon(data)
            else:
                self._send_json_response(404, {'error': 'API endpoint not found'})
                
        except Exception as e:
            self._send_json_response(500, {'error': str(e)})
    
    def _handle_install_addon(self, data: Dict):
        """Handle addon installation"""
        try:
            addon_name = data.get('addon_name')
            if not addon_name:
                self._send_json_response(400, {'error': 'addon_name required'})
                return
            
            success = self.erp_server.addon_manager.install_addon(addon_name)
            if success:
                self._send_json_response(200, {'message': f'Addon {addon_name} installed successfully'})
            else:
                self._send_json_response(500, {'error': f'Failed to install addon {addon_name}'})
                
        except Exception as e:
            self._send_json_response(500, {'error': str(e)})
    
    def _handle_uninstall_addon(self, data: Dict):
        """Handle addon uninstallation"""
        try:
            addon_name = data.get('addon_name')
            if not addon_name:
                self._send_json_response(400, {'error': 'addon_name required'})
                return
            
            success = self.erp_server.addon_manager.uninstall_addon(addon_name)
            if success:
                self._send_json_response(200, {'message': f'Addon {addon_name} uninstalled successfully'})
            else:
                self._send_json_response(500, {'error': f'Failed to uninstall addon {addon_name}'})
                
        except Exception as e:
            self._send_json_response(500, {'error': str(e)})
    
    def _serve_static_file(self, path: str):
        """Serve static files"""
        try:
            # Remove '/static/' prefix
            file_path = path[8:]
            
            # Security check - prevent directory traversal
            if '..' in file_path or file_path.startswith('/'):
                self._serve_404()
                return
            
            # Get static files directory
            static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
            full_path = os.path.join(static_dir, file_path)
            
            if os.path.exists(full_path) and os.path.isfile(full_path):
                with open(full_path, 'rb') as f:
                    content = f.read()
                
                # Determine content type
                content_type = 'text/plain'
                if file_path.endswith('.css'):
                    content_type = 'text/css'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript'
                elif file_path.endswith('.html'):
                    content_type = 'text/html'
                elif file_path.endswith('.png'):
                    content_type = 'image/png'
                elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                    content_type = 'image/jpeg'
                
                self._send_response(200, content, content_type)
            else:
                self._serve_404()
                
        except Exception as e:
            self._serve_500(str(e))
    
    def _serve_404(self):
        """Serve 404 error"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>404 Not Found</title></head>
        <body><h1>404 - Page Not Found</h1></body>
        </html>
        """
        self._send_response(404, html_content, 'text/html')
    
    def _serve_500(self, error_message: str):
        """Serve 500 error"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head><title>500 Internal Server Error</title></head>
        <body><h1>500 - Internal Server Error</h1><p>{error_message}</p></body>
        </html>
        """
        self._send_response(500, html_content, 'text/html')
    
    def _send_response(self, status_code: int, content: bytes, content_type: str = 'text/html'):
        """Send HTTP response"""
        self.send_response(status_code)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    
    def _send_json_response(self, status_code: int, data: Dict):
        """Send JSON response"""
        json_content = json.dumps(data, indent=2).encode('utf-8')
        self._send_response(status_code, json_content, 'application/json')
    
    def log_message(self, format, *args):
        """Override to use our logger"""
        self.erp_server.logger.info(f"{self.address_string()} - {format % args}")

class WebInterface:
    """Web Interface for ERP System"""
    
    def __init__(self, config):
        """Initialize web interface"""
        self.config = config
        self.server = None
        self.logger = logging.getLogger('ERP.WebInterface')
        
    def initialize(self):
        """Initialize web interface"""
        try:
            self.logger.info("Initializing web interface...")
            
            # Create static directory if it doesn't exist
            static_dir = os.path.join(os.path.dirname(__file__), '..', 'static')
            os.makedirs(static_dir, exist_ok=True)
            
            self.logger.info("Web interface initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize web interface: {e}")
            return False
    
    def start_server(self, host: str = 'localhost', port: int = 8069):
        """Start web server"""
        try:
            def handler(*args, **kwargs):
                return ERPWebHandler(*args, erp_server=self.erp_server, **kwargs)
            
            self.server = HTTPServer((host, port), handler)
            self.logger.info(f"Web server started on {host}:{port}")
            self.logger.info(f"Access the ERP system at: http://{host}:{port}")
            
            # Start serving
            self.server.serve_forever()
            
        except Exception as e:
            self.logger.error(f"Failed to start web server: {e}")
            raise
    
    def stop_server(self):
        """Stop web server"""
        if self.server:
            self.server.shutdown()
            self.logger.info("Web server stopped")
    
    def set_erp_server(self, erp_server):
        """Set ERP server reference"""
        self.erp_server = erp_server