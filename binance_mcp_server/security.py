"""
Security utilities and best practices for the Binance MCP Server.

This module implements security best practices including input validation,
error sanitization, rate limiting, and secure configuration management.
"""

import os
import logging
import hashlib
import secrets
from typing import Dict, Any, Optional, List
from functools import wraps

logger = logging.getLogger(__name__)


class SecurityConfig:
    """
    Security configuration and validation for MCP server.
    """
    
    def __init__(self):
        self.rate_limit_enabled = os.getenv("MCP_RATE_LIMIT_ENABLED", "true").lower() == "true"
        self.max_requests_per_minute = int(os.getenv("MCP_MAX_REQUESTS_PER_MINUTE", "60"))
        self.enable_input_validation = os.getenv("MCP_INPUT_VALIDATION", "true").lower() == "true"
        self.log_security_events = os.getenv("MCP_LOG_SECURITY", "true").lower() == "true"
    
    def is_secure(self) -> bool:
        """Check if current configuration meets security requirements."""
        return all([
            self.rate_limit_enabled,
            self.max_requests_per_minute <= 120,  # Reasonable limit
            self.enable_input_validation
        ])
    
    def get_security_warnings(self) -> List[str]:
        """Get list of security configuration warnings."""
        warnings = []
        
        if not self.rate_limit_enabled:
            warnings.append("Rate limiting is disabled - this may expose the server to abuse")
        
        if self.max_requests_per_minute > 120:
            warnings.append("Rate limit is set too high - recommended maximum is 120 requests/minute")
        
        if not self.enable_input_validation:
            warnings.append("Input validation is disabled - this is a security risk")
        
        return warnings


def validate_api_credentials() -> bool:
    """
    Validate that API credentials are properly configured and secure.
    
    Returns:
        bool: True if credentials are valid and secure
    """
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    
    if not api_key or not api_secret:
        logger.error("Missing API credentials")
        return False
    
    # Validate API key format (basic check)
    if len(api_key) < 32:
        logger.warning("API key appears to be too short")
        return False
    
    if len(api_secret) < 32:
        logger.warning("API secret appears to be too short")
        return False
    
    # Check for common insecure values
    insecure_values = ["test", "demo", "example", "your_key", "your_secret"]
    if api_key.lower() in insecure_values or api_secret.lower() in insecure_values:
        logger.error("API credentials appear to be placeholder values")
        return False
    
    return True


def secure_hash(data: str) -> str:
    """
    Create a secure hash of sensitive data for logging/identification purposes.
    
    Args:
        data: The data to hash
        
    Returns:
        str: SHA-256 hash of the data
    """
    return hashlib.sha256(data.encode('utf-8')).hexdigest()[:16]  # First 16 chars for brevity


def generate_request_id() -> str:
    """
    Generate a secure random request ID for tracking.
    
    Returns:
        str: Cryptographically secure random request ID
    """
    return secrets.token_hex(8)


class SecurityMiddleware:
    """
    Security middleware for request validation and monitoring.
    """
    
    def __init__(self, config: Optional[SecurityConfig] = None):
        self.config = config or SecurityConfig()
        self.request_counts = {}
        
    def validate_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate incoming request for security issues.
        
        Args:
            request_data: The request data to validate
            
        Returns:
            Dict containing validation result and any security warnings
        """
        warnings = []
        is_valid = True
        
        # Check for common injection patterns
        if self._contains_injection_patterns(request_data):
            warnings.append("Potential injection pattern detected")
            is_valid = False
        
        # Check request size
        if self._request_too_large(request_data):
            warnings.append("Request size exceeds limits")
            is_valid = False
        
        return {
            "valid": is_valid,
            "warnings": warnings,
            "request_id": generate_request_id()
        }
    
    def _contains_injection_patterns(self, data: Dict[str, Any]) -> bool:
        """Check for common injection patterns in request data."""
        if not isinstance(data, dict):
            return False
        
        dangerous_patterns = [
            'script', 'javascript:', 'onload=', 'onerror=',
            'eval(', 'exec(', 'system(', 'shell_exec',
            '../', './', '..\\', '.\\',
            'SELECT', 'INSERT', 'UPDATE', 'DELETE', 'DROP'
        ]
        
        data_str = str(data).lower()
        return any(pattern.lower() in data_str for pattern in dangerous_patterns)
    
    def _request_too_large(self, data: Dict[str, Any], max_size: int = 1024*1024) -> bool:
        """Check if request data is too large."""
        try:
            import json
            return len(json.dumps(data).encode('utf-8')) > max_size
        except (TypeError, ValueError):
            return True


def security_audit_log(event_type: str, details: Dict[str, Any], level: str = "INFO") -> None:
    """
    Log security-related events with proper formatting.
    
    Args:
        event_type: Type of security event
        details: Event details (will be sanitized)
        level: Log level (INFO, WARNING, ERROR)
    """
    security_logger = logging.getLogger(f"{__name__}.security")
    
    # Sanitize details to prevent log injection
    sanitized_details = {k: _sanitize_log_value(v) for k, v in details.items()}
    
    log_entry = {
        "event_type": event_type,
        "details": sanitized_details,
        "request_id": generate_request_id()
    }
    
    if level.upper() == "ERROR":
        security_logger.error(f"SECURITY_EVENT: {log_entry}")
    elif level.upper() == "WARNING":
        security_logger.warning(f"SECURITY_EVENT: {log_entry}")
    else:
        security_logger.info(f"SECURITY_EVENT: {log_entry}")


def _sanitize_log_value(value: Any) -> Any:
    """Sanitize values before logging to prevent log injection."""
    if isinstance(value, str):
        # Remove control characters and potential log injection patterns
        return ''.join(c for c in value if c.isprintable())[:500]  # Limit length
    return str(value)[:500] if value is not None else None


def secure_tool_wrapper(func):
    """
    Decorator to add security validation to MCP tools.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        request_id = generate_request_id()
        
        try:
            # Log tool invocation (without sensitive data)
            security_audit_log(
                "tool_invocation",
                {
                    "tool_name": func.__name__,
                    "request_id": request_id,
                    "args_count": len(args),
                    "kwargs_count": len(kwargs)
                }
            )
            
            result = func(*args, **kwargs)
            
            # Log successful completion
            if isinstance(result, dict) and result.get("success"):
                security_audit_log(
                    "tool_success",
                    {"tool_name": func.__name__, "request_id": request_id}
                )
            else:
                security_audit_log(
                    "tool_failure",
                    {"tool_name": func.__name__, "request_id": request_id},
                    level="WARNING"
                )
            
            return result
            
        except Exception as e:
            security_audit_log(
                "tool_exception",
                {
                    "tool_name": func.__name__,
                    "request_id": request_id,
                    "error_type": type(e).__name__
                },
                level="ERROR"
            )
            raise
    
    return wrapper