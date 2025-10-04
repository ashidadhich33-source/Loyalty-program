#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Authentication System
======================================

Authentication and session management for the ERP system.
"""

import hashlib
import secrets
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
import logging

logger = logging.getLogger(__name__)

class AuthenticationManager:
    """Authentication Manager for ERP System"""
    
    def __init__(self, config):
        """Initialize authentication manager"""
        self.config = config
        self.sessions = {}  # In production, this would be stored in database
        self.session_timeout = config.get('security.session_timeout', 3600)
        self.max_login_attempts = config.get('security.max_login_attempts', 5)
        self.lockout_duration = config.get('security.lockout_duration', 300)
        self.login_attempts = {}  # Track failed login attempts
        
    def authenticate_user(self, username: str, password: str, request=None) -> Dict[str, Any]:
        """Authenticate user with username and password"""
        try:
            # Check if user is locked out
            if self._is_user_locked_out(username):
                return {
                    'success': False,
                    'message': 'Account is temporarily locked due to too many failed attempts',
                    'locked_until': self.login_attempts.get(username, {}).get('locked_until')
                }
            
            # Get user from database
            user = self._get_user_by_username(username)
            if not user:
                self._record_failed_attempt(username)
                return {
                    'success': False,
                    'message': 'Invalid username or password'
                }
            
            # Check if user is active
            if not user.get('active', True):
                return {
                    'success': False,
                    'message': 'Account is deactivated'
                }
            
            # Verify password
            if not self._verify_password(password, user.get('password_hash')):
                self._record_failed_attempt(username)
                return {
                    'success': False,
                    'message': 'Invalid username or password'
                }
            
            # Clear failed attempts on successful login
            self._clear_failed_attempts(username)
            
            # Create session
            session_data = self._create_session(user, request)
            
            return {
                'success': True,
                'message': 'Login successful',
                'session_id': session_data['session_id'],
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'name': user.get('name', ''),
                    'email': user.get('email', ''),
                    'groups': user.get('groups', []),
                    'roles': user.get('roles', [])
                }
            }
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return {
                'success': False,
                'message': 'Authentication failed'
            }
    
    def _get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username from database"""
        # This would query the database for user
        # For now, return a mock user
        return {
            'id': 1,
            'username': username,
            'name': 'Admin User',
            'email': 'admin@example.com',
            'password_hash': self._hash_password('admin'),
            'active': True,
            'groups': ['base.group_user', 'base.group_system'],
            'roles': ['admin']
        }
    
    def _hash_password(self, password: str) -> str:
        """Hash password using secure method"""
        # Use bcrypt or similar in production
        salt = secrets.token_hex(16)
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        # In production, use proper password verification
        # For now, simple check
        return password == 'admin'  # This is just for demo
    
    def _is_user_locked_out(self, username: str) -> bool:
        """Check if user is locked out"""
        if username not in self.login_attempts:
            return False
        
        attempt_data = self.login_attempts[username]
        if attempt_data['count'] < self.max_login_attempts:
            return False
        
        # Check if lockout period has expired
        locked_until = attempt_data.get('locked_until')
        if locked_until and datetime.now() < locked_until:
            return True
        
        # Clear expired lockout
        self._clear_failed_attempts(username)
        return False
    
    def _record_failed_attempt(self, username: str):
        """Record failed login attempt"""
        if username not in self.login_attempts:
            self.login_attempts[username] = {'count': 0, 'last_attempt': None}
        
        attempt_data = self.login_attempts[username]
        attempt_data['count'] += 1
        attempt_data['last_attempt'] = datetime.now()
        
        # Lock account if max attempts reached
        if attempt_data['count'] >= self.max_login_attempts:
            attempt_data['locked_until'] = datetime.now() + timedelta(seconds=self.lockout_duration)
    
    def _clear_failed_attempts(self, username: str):
        """Clear failed login attempts"""
        if username in self.login_attempts:
            del self.login_attempts[username]
    
    def _create_session(self, user: Dict, request=None) -> Dict[str, Any]:
        """Create user session"""
        session_id = secrets.token_urlsafe(32)
        session_data = {
            'session_id': session_id,
            'user_id': user['id'],
            'username': user['username'],
            'created_at': datetime.now(),
            'last_activity': datetime.now(),
            'ip_address': self._get_client_ip(request),
            'user_agent': self._get_user_agent(request),
            'expires_at': datetime.now() + timedelta(seconds=self.session_timeout)
        }
        
        self.sessions[session_id] = session_data
        return session_data
    
    def _get_client_ip(self, request) -> str:
        """Get client IP address"""
        if request:
            # Implementation would get IP from request headers
            return '127.0.0.1'
        return '127.0.0.1'
    
    def _get_user_agent(self, request) -> str:
        """Get user agent"""
        if request:
            # Implementation would get user agent from request headers
            return 'ERP Client'
        return 'ERP Client'
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Validate session and return user data"""
        try:
            if session_id not in self.sessions:
                return None
            
            session_data = self.sessions[session_id]
            
            # Check if session is expired
            if datetime.now() > session_data['expires_at']:
                self._destroy_session(session_id)
                return None
            
            # Update last activity
            session_data['last_activity'] = datetime.now()
            
            # Extend session if needed
            if self._should_extend_session(session_data):
                session_data['expires_at'] = datetime.now() + timedelta(seconds=self.session_timeout)
            
            return session_data
            
        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return None
    
    def _should_extend_session(self, session_data: Dict) -> bool:
        """Check if session should be extended"""
        # Extend session if user is active within last 30 minutes
        last_activity = session_data['last_activity']
        if datetime.now() - last_activity < timedelta(minutes=30):
            return True
        return False
    
    def destroy_session(self, session_id: str) -> bool:
        """Destroy user session"""
        try:
            self._destroy_session(session_id)
            return True
        except Exception as e:
            logger.error(f"Session destruction error: {e}")
            return False
    
    def _destroy_session(self, session_id: str):
        """Internal method to destroy session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def logout_user(self, session_id: str) -> Dict[str, Any]:
        """Logout user and destroy session"""
        try:
            session_data = self.validate_session(session_id)
            if not session_data:
                return {
                    'success': False,
                    'message': 'Invalid session'
                }
            
            self._destroy_session(session_id)
            
            return {
                'success': True,
                'message': 'Logout successful'
            }
            
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return {
                'success': False,
                'message': 'Logout failed'
            }
    
    def get_user_permissions(self, user_id: int) -> Dict[str, Any]:
        """Get user permissions"""
        try:
            # This would query the database for user permissions
            # For now, return mock permissions
            return {
                'groups': ['base.group_user', 'base.group_system'],
                'roles': ['admin'],
                'permissions': {
                    'read': True,
                    'write': True,
                    'create': True,
                    'delete': True
                }
            }
        except Exception as e:
            logger.error(f"Permission retrieval error: {e}")
            return {}
    
    def check_permission(self, user_id: int, model: str, operation: str) -> bool:
        """Check if user has permission for model operation"""
        try:
            permissions = self.get_user_permissions(user_id)
            return permissions.get('permissions', {}).get(operation, False)
        except Exception as e:
            logger.error(f"Permission check error: {e}")
            return False
    
    def get_active_sessions(self) -> list:
        """Get all active sessions"""
        active_sessions = []
        current_time = datetime.now()
        
        for session_id, session_data in self.sessions.items():
            if current_time <= session_data['expires_at']:
                active_sessions.append({
                    'session_id': session_id,
                    'user_id': session_data['user_id'],
                    'username': session_data['username'],
                    'created_at': session_data['created_at'],
                    'last_activity': session_data['last_activity'],
                    'ip_address': session_data['ip_address'],
                    'expires_at': session_data['expires_at']
                })
        
        return active_sessions
    
    def cleanup_expired_sessions(self):
        """Clean up expired sessions"""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session_data in self.sessions.items():
            if current_time > session_data['expires_at']:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self._destroy_session(session_id)
        
        logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")


class SessionMiddleware:
    """Session Middleware for Web Requests"""
    
    def __init__(self, auth_manager):
        """Initialize session middleware"""
        self.auth_manager = auth_manager
    
    def process_request(self, request) -> Optional[Dict[str, Any]]:
        """Process incoming request for session validation"""
        try:
            # Get session ID from request
            session_id = self._extract_session_id(request)
            if not session_id:
                return None
            
            # Validate session
            session_data = self.auth_manager.validate_session(session_id)
            if not session_data:
                return None
            
            # Add user data to request context
            request.user_id = session_data['user_id']
            request.username = session_data['username']
            request.session_id = session_id
            
            return session_data
            
        except Exception as e:
            logger.error(f"Session middleware error: {e}")
            return None
    
    def _extract_session_id(self, request) -> Optional[str]:
        """Extract session ID from request"""
        # Check cookies first
        if hasattr(request, 'cookies') and 'session_id' in request.cookies:
            return request.cookies['session_id']
        
        # Check headers
        if hasattr(request, 'headers'):
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                return auth_header[7:]  # Remove 'Bearer ' prefix
        
        return None
    
    def set_session_cookie(self, response, session_id: str):
        """Set session cookie in response"""
        try:
            # Set HTTP-only cookie for security
            response.set_cookie(
                'session_id',
                session_id,
                httponly=True,
                secure=True,  # Use HTTPS in production
                samesite='Strict',
                max_age=self.auth_manager.session_timeout
            )
        except Exception as e:
            logger.error(f"Cookie setting error: {e}")