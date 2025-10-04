#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kids Clothing ERP - Session Management
=====================================

Session management system for user sessions and state.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    """Session Manager for ERP System"""
    
    def __init__(self, config):
        """Initialize session manager"""
        self.config = config
        self.sessions = {}  # In production, this would be stored in database/Redis
        self.session_timeout = config.get('security.session_timeout', 3600)
        self.max_sessions_per_user = config.get('security.max_sessions_per_user', 5)
        
    def create_session(self, user_id: int, session_data: Dict[str, Any]) -> str:
        """Create new session for user"""
        try:
            session_id = self._generate_session_id()
            
            # Check session limit for user
            self._enforce_session_limit(user_id)
            
            # Create session
            session = {
                'session_id': session_id,
                'user_id': user_id,
                'created_at': datetime.now(),
                'last_activity': datetime.now(),
                'expires_at': datetime.now() + timedelta(seconds=self.session_timeout),
                'data': session_data,
                'active': True
            }
            
            self.sessions[session_id] = session
            
            logger.info(f"Created session {session_id} for user {user_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Session creation error: {e}")
            raise e
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        import secrets
        return secrets.token_urlsafe(32)
    
    def _enforce_session_limit(self, user_id: int):
        """Enforce maximum sessions per user"""
        user_sessions = [s for s in self.sessions.values() if s['user_id'] == user_id and s['active']]
        
        if len(user_sessions) >= self.max_sessions_per_user:
            # Remove oldest session
            oldest_session = min(user_sessions, key=lambda s: s['created_at'])
            self.destroy_session(oldest_session['session_id'])
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session by ID"""
        try:
            if session_id not in self.sessions:
                return None
            
            session = self.sessions[session_id]
            
            # Check if session is expired
            if datetime.now() > session['expires_at']:
                self.destroy_session(session_id)
                return None
            
            # Update last activity
            session['last_activity'] = datetime.now()
            
            return session
            
        except Exception as e:
            logger.error(f"Session retrieval error: {e}")
            return None
    
    def update_session(self, session_id: str, data: Dict[str, Any]) -> bool:
        """Update session data"""
        try:
            session = self.get_session(session_id)
            if not session:
                return False
            
            # Update session data
            session['data'].update(data)
            session['last_activity'] = datetime.now()
            
            return True
            
        except Exception as e:
            logger.error(f"Session update error: {e}")
            return False
    
    def destroy_session(self, session_id: str) -> bool:
        """Destroy session"""
        try:
            if session_id in self.sessions:
                self.sessions[session_id]['active'] = False
                del self.sessions[session_id]
                logger.info(f"Destroyed session {session_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Session destruction error: {e}")
            return False
    
    def destroy_user_sessions(self, user_id: int) -> int:
        """Destroy all sessions for a user"""
        try:
            destroyed_count = 0
            sessions_to_destroy = []
            
            for session_id, session in self.sessions.items():
                if session['user_id'] == user_id and session['active']:
                    sessions_to_destroy.append(session_id)
            
            for session_id in sessions_to_destroy:
                if self.destroy_session(session_id):
                    destroyed_count += 1
            
            logger.info(f"Destroyed {destroyed_count} sessions for user {user_id}")
            return destroyed_count
            
        except Exception as e:
            logger.error(f"User session destruction error: {e}")
            return 0
    
    def extend_session(self, session_id: str, duration: int = None) -> bool:
        """Extend session expiration"""
        try:
            session = self.get_session(session_id)
            if not session:
                return False
            
            if duration is None:
                duration = self.session_timeout
            
            session['expires_at'] = datetime.now() + timedelta(seconds=duration)
            return True
            
        except Exception as e:
            logger.error(f"Session extension error: {e}")
            return False
    
    def get_user_sessions(self, user_id: int) -> list:
        """Get all active sessions for a user"""
        try:
            user_sessions = []
            
            for session_id, session in self.sessions.items():
                if session['user_id'] == user_id and session['active']:
                    user_sessions.append({
                        'session_id': session_id,
                        'created_at': session['created_at'],
                        'last_activity': session['last_activity'],
                        'expires_at': session['expires_at'],
                        'ip_address': session['data'].get('ip_address'),
                        'user_agent': session['data'].get('user_agent')
                    })
            
            return user_sessions
            
        except Exception as e:
            logger.error(f"User sessions retrieval error: {e}")
            return []
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions"""
        try:
            current_time = datetime.now()
            expired_sessions = []
            
            for session_id, session in self.sessions.items():
                if current_time > session['expires_at']:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                self.destroy_session(session_id)
            
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
            return len(expired_sessions)
            
        except Exception as e:
            logger.error(f"Session cleanup error: {e}")
            return 0
    
    def get_session_statistics(self) -> Dict[str, Any]:
        """Get session statistics"""
        try:
            total_sessions = len(self.sessions)
            active_sessions = len([s for s in self.sessions.values() if s['active']])
            
            # Count sessions by user
            user_session_count = {}
            for session in self.sessions.values():
                if session['active']:
                    user_id = session['user_id']
                    user_session_count[user_id] = user_session_count.get(user_id, 0) + 1
            
            return {
                'total_sessions': total_sessions,
                'active_sessions': active_sessions,
                'unique_users': len(user_session_count),
                'user_session_counts': user_session_count
            }
            
        except Exception as e:
            logger.error(f"Session statistics error: {e}")
            return {}


class SessionData:
    """Session Data Handler"""
    
    def __init__(self, session_manager):
        """Initialize session data handler"""
        self.session_manager = session_manager
    
    def set_data(self, session_id: str, key: str, value: Any) -> bool:
        """Set data in session"""
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return False
            
            session['data'][key] = value
            return True
            
        except Exception as e:
            logger.error(f"Session data set error: {e}")
            return False
    
    def get_data(self, session_id: str, key: str, default: Any = None) -> Any:
        """Get data from session"""
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return default
            
            return session['data'].get(key, default)
            
        except Exception as e:
            logger.error(f"Session data get error: {e}")
            return default
    
    def remove_data(self, session_id: str, key: str) -> bool:
        """Remove data from session"""
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return False
            
            if key in session['data']:
                del session['data'][key]
                return True
            
            return False
            
        except Exception as e:
            logger.error(f"Session data remove error: {e}")
            return False
    
    def clear_data(self, session_id: str) -> bool:
        """Clear all data from session"""
        try:
            session = self.session_manager.get_session(session_id)
            if not session:
                return False
            
            session['data'].clear()
            return True
            
        except Exception as e:
            logger.error(f"Session data clear error: {e}")
            return False


class SessionMiddleware:
    """Session Middleware for Web Framework"""
    
    def __init__(self, session_manager):
        """Initialize session middleware"""
        self.session_manager = session_manager
    
    def process_request(self, request) -> Optional[Dict[str, Any]]:
        """Process incoming request"""
        try:
            # Extract session ID from request
            session_id = self._extract_session_id(request)
            if not session_id:
                return None
            
            # Get session
            session = self.session_manager.get_session(session_id)
            if not session:
                return None
            
            # Add session to request context
            request.session = session
            request.session_id = session_id
            request.user_id = session['user_id']
            
            return session
            
        except Exception as e:
            logger.error(f"Session middleware error: {e}")
            return None
    
    def _extract_session_id(self, request) -> Optional[str]:
        """Extract session ID from request"""
        # Check cookies
        if hasattr(request, 'cookies') and 'session_id' in request.cookies:
            return request.cookies['session_id']
        
        # Check headers
        if hasattr(request, 'headers'):
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                return auth_header[7:]
        
        return None
    
    def set_session_cookie(self, response, session_id: str):
        """Set session cookie in response"""
        try:
            response.set_cookie(
                'session_id',
                session_id,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=self.session_manager.session_timeout
            )
        except Exception as e:
            logger.error(f"Session cookie error: {e}")