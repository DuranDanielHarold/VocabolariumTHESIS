"""
Authentication utilities for Vocabolarioum
Handles user authentication, session management, and password hashing
"""

import hashlib
import secrets
import hmac
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
import streamlit as st


class AuthManager:
    """Comprehensive authentication manager for admin access"""
    
    def __init__(self):
        """Initialize authentication manager"""
        self.sessions = {}
        self.failed_attempts = {}
        self.max_attempts = 5
        self.lockout_duration = timedelta(minutes=15)
    
    @staticmethod
    def hash_password(password: str, salt: Optional[str] = None) -> Tuple[str, str]:
        """
        Hash password using SHA256 with salt
        
        Args:
            password: Plain text password
            salt: Optional salt, generates new if not provided
            
        Returns:
            Tuple of (hashed_password, salt)
        """
        if salt is None:
            salt = secrets.token_hex(32)
        
        # Combine password and salt
        salted_password = f"{password}{salt}".encode('utf-8')
        
        # Hash using SHA256
        hashed = hashlib.sha256(salted_password).hexdigest()
        
        return hashed, salt
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """
        Verify password against hash with salt
        
        Args:
            password: Plain text password to verify
            hashed: Stored hash
            salt: Salt used in hashing
            
        Returns:
            True if password matches, False otherwise
        """
        test_hash, _ = AuthManager.hash_password(password, salt)
        return hmac.compare_digest(test_hash, hashed)
    
    @staticmethod
    def simple_hash_password(password: str) -> str:
        """
        Simple password hashing (for backward compatibility)
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def simple_verify_password(password: str, hashed: str) -> bool:
        """
        Simple password verification
        
        Args:
            password: Plain text password
            hashed: Stored hash
            
        Returns:
            True if password matches
        """
        return AuthManager.simple_hash_password(password) == hashed
    
    def create_session(self, username: str, duration_hours: int = 8) -> str:
        """
        Create a new session for user
        
        Args:
            username: Username for the session
            duration_hours: Session duration in hours
            
        Returns:
            Session token
        """
        session_token = secrets.token_urlsafe(32)
        
        self.sessions[session_token] = {
            'username': username,
            'created_at': datetime.now(),
            'expires_at': datetime.now() + timedelta(hours=duration_hours),
            'last_activity': datetime.now(),
            'ip_address': None,  # Can be extended to track IP
        }
        
        return session_token
    
    def validate_session(self, session_token: str, extend_session: bool = True) -> bool:
        """
        Validate if session is still active
        
        Args:
            session_token: Token to validate
            extend_session: Whether to extend session on activity
            
        Returns:
            True if session is valid, False otherwise
        """
        if session_token not in self.sessions:
            return False
        
        session = self.sessions[session_token]
        current_time = datetime.now()
        
        # Check if session expired
        if current_time > session['expires_at']:
            del self.sessions[session_token]
            return False
        
        # Update last activity and extend session if needed
        if extend_session:
            session['last_activity'] = current_time
            # Extend expiration by 1 hour on activity
            session['expires_at'] = current_time + timedelta(hours=1)
        
        return True
    
    def get_session_info(self, session_token: str) -> Optional[Dict]:
        """
        Get session information
        
        Args:
            session_token: Session token
            
        Returns:
            Session info dict or None
        """
        if session_token in self.sessions and self.validate_session(session_token):
            return self.sessions[session_token].copy()
        return None
    
    def destroy_session(self, session_token: str) -> bool:
        """
        Destroy a session (logout)
        
        Args:
            session_token: Token to destroy
            
        Returns:
            True if session was destroyed
        """
        if session_token in self.sessions:
            del self.sessions[session_token]
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """
        Remove all expired sessions
        
        Returns:
            Number of sessions cleaned up
        """
        current_time = datetime.now()
        expired_tokens = [
            token for token, session in self.sessions.items()
            if current_time > session['expires_at']
        ]
        
        for token in expired_tokens:
            del self.sessions[token]
        
        return len(expired_tokens)
    
    def record_failed_attempt(self, username: str) -> None:
        """
        Record a failed login attempt
        
        Args:
            username: Username that failed
        """
        current_time = datetime.now()
        
        if username not in self.failed_attempts:
            self.failed_attempts[username] = {
                'count': 0,
                'first_attempt': current_time,
                'locked_until': None
            }
        
        attempt_info = self.failed_attempts[username]
        attempt_info['count'] += 1
        
        # Lock account if max attempts reached
        if attempt_info['count'] >= self.max_attempts:
            attempt_info['locked_until'] = current_time + self.lockout_duration
    
    def is_account_locked(self, username: str) -> Tuple[bool, Optional[datetime]]:
        """
        Check if account is locked
        
        Args:
            username: Username to check
            
        Returns:
            Tuple of (is_locked, locked_until)
        """
        if username not in self.failed_attempts:
            return False, None
        
        attempt_info = self.failed_attempts[username]
        locked_until = attempt_info.get('locked_until')
        
        if locked_until is None:
            return False, None
        
        current_time = datetime.now()
        
        # Check if lockout expired
        if current_time > locked_until:
            # Reset attempts
            del self.failed_attempts[username]
            return False, None
        
        return True, locked_until
    
    def reset_failed_attempts(self, username: str) -> None:
        """
        Reset failed login attempts (on successful login)
        
        Args:
            username: Username to reset
        """
        if username in self.failed_attempts:
            del self.failed_attempts[username]
    
    def get_active_sessions_count(self) -> int:
        """
        Get count of active sessions
        
        Returns:
            Number of active sessions
        """
        self.cleanup_expired_sessions()
        return len(self.sessions)
    
    def get_all_active_sessions(self) -> list:
        """
        Get all active sessions info
        
        Returns:
            List of session info dictionaries
        """
        self.cleanup_expired_sessions()
        return [
            {
                'token': token[:10] + '...',  # Truncated for security
                'username': info['username'],
                'created_at': info['created_at'],
                'expires_at': info['expires_at'],
                'last_activity': info['last_activity']
            }
            for token, info in self.sessions.items()
        ]


class StreamlitAuthManager:
    """
    Streamlit-specific authentication manager using session state
    """
    
    @staticmethod
    def initialize_auth_state():
        """Initialize authentication state in Streamlit session"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        
        if 'username' not in st.session_state:
            st.session_state.username = None
        
        if 'login_time' not in st.session_state:
            st.session_state.login_time = None
        
        if 'session_token' not in st.session_state:
            st.session_state.session_token = None
    
    @staticmethod
    def login(username: str, auth_manager: AuthManager) -> bool:
        """
        Log in user (set Streamlit session state)
        
        Args:
            username: Username to log in
            auth_manager: AuthManager instance
            
        Returns:
            True if login successful
        """
        session_token = auth_manager.create_session(username)
        
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.login_time = datetime.now()
        st.session_state.session_token = session_token
        
        return True
    
    @staticmethod
    def logout(auth_manager: Optional[AuthManager] = None):
        """
        Log out user (clear Streamlit session state)
        
        Args:
            auth_manager: Optional AuthManager to destroy session
        """
        if auth_manager and 'session_token' in st.session_state:
            if st.session_state.session_token:
                auth_manager.destroy_session(st.session_state.session_token)
        
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.login_time = None
        st.session_state.session_token = None
    
    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if user is authenticated
        
        Returns:
            True if authenticated
        """
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def get_username() -> Optional[str]:
        """
        Get current username
        
        Returns:
            Username or None
        """
        return st.session_state.get('username')
    
    @staticmethod
    def get_session_duration() -> Optional[timedelta]:
        """
        Get current session duration
        
        Returns:
            Session duration or None
        """
        login_time = st.session_state.get('login_time')
        if login_time:
            return datetime.now() - login_time
        return None
    
    @staticmethod
    def require_authentication(redirect_page: Optional[str] = None):
        """
        Decorator/function to require authentication
        
        Args:
            redirect_page: Page to redirect to if not authenticated
        """
        if not StreamlitAuthManager.is_authenticated():
            st.error("🔒 Authentication required. Please log in.")
            if redirect_page:
                st.switch_page(redirect_page)
            else:
                st.stop()


# Utility functions for common operations
def generate_secure_token(length: int = 32) -> str:
    """
    Generate a secure random token
    
    Args:
        length: Length of token in bytes
        
    Returns:
        URL-safe token string
    """
    return secrets.token_urlsafe(length)


def verify_credentials(username: str, password: str, stored_username: str, stored_password: str) -> bool:
    """
    Verify login credentials (simple version)
    
    Args:
        username: Provided username
        password: Provided password
        stored_username: Correct username
        stored_password: Correct password (plain text or hashed)
        
    Returns:
        True if credentials match
    """
    # Constant-time comparison to prevent timing attacks
    username_match = hmac.compare_digest(username, stored_username)
    password_match = hmac.compare_digest(password, stored_password)
    
    return username_match and password_match


def hash_api_key(api_key: str) -> str:
    """
    Hash an API key for secure storage
    
    Args:
        api_key: API key to hash
        
    Returns:
        Hashed API key
    """
    return hashlib.sha256(api_key.encode()).hexdigest()


# Example usage
if __name__ == "__main__":
    # Testing authentication manager
    auth = AuthManager()
    
    # Test password hashing
    password = "admin123"
    hashed, salt = auth.hash_password(password)
    print(f"Hashed: {hashed}")
    print(f"Salt: {salt}")
    print(f"Verification: {auth.verify_password(password, hashed, salt)}")
    
    # Test session management
    token = auth.create_session("admin")
    print(f"\nSession Token: {token}")
    print(f"Session Valid: {auth.validate_session(token)}")
    print(f"Session Info: {auth.get_session_info(token)}")
    
    # Test failed attempts
    auth.record_failed_attempt("test_user")
    print(f"\nAccount Locked: {auth.is_account_locked('test_user')}")