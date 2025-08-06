"""
Shared utilities for the Binance MCP Server.

This module provides common functionality used across all tools, including
client initialization, rate limiting, and error handling utilities.
"""

import time
import logging
from typing import Dict, Any, Optional
from functools import wraps
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance_mcp_server.config import BinanceConfig
from enum import Enum as PyEnum

logger = logging.getLogger(__name__)


# Global configuration instance
_config: Optional[BinanceConfig] = None


class OrderSide(PyEnum):
    """
    Enum for order side types.
    
    Attributes:
        BUY: Buy order
        SELL: Sell order
    """
    SIDE_BUY = 'BUY'
    SIDE_SELL = 'SELL'


class OrderType(PyEnum):
    """
    Enum for order types.
    
    Attributes:
        ORDER_TYPE_LIMIT: Limit order
        ORDER_TYPE_MARKET: Market order
        ORDER_TYPE_STOP_LOSS: Stop loss order
        ORDER_TYPE_STOP_LOSS_LIMIT: Stop loss limit order
        ORDER_TYPE_TAKE_PROFIT: Take profit order
        ORDER_TYPE_TAKE_PROFIT_LIMIT: Take profit limit order
        ORDER_TYPE_LIMIT_MAKER: Limit maker order
    """
    ORDER_TYPE_LIMIT = 'LIMIT'
    ORDER_TYPE_MARKET = 'MARKET'
    ORDER_TYPE_STOP_LOSS = 'STOP_LOSS'
    ORDER_TYPE_STOP_LOSS_LIMIT = 'STOP_LOSS_LIMIT'
    ORDER_TYPE_TAKE_PROFIT = 'TAKE_PROFIT'
    ORDER_TYPE_TAKE_PROFIT_LIMIT = 'TAKE_PROFIT_LIMIT'
    ORDER_TYPE_LIMIT_MAKER = 'LIMIT_MAKER'


class AccountType(PyEnum):
    """
    Enum for account types.
    
    Attributes:
        SPOT: Spot account
        MARGIN: Margin account
        FUTURES: Futures account
    """
    SPOT = 'SPOT'
    MARGIN = 'MARGIN'
    FUTURES = 'FUTURES'


def get_config() -> BinanceConfig:
    """
    Get the global BinanceConfig instance.
    
    Returns:
        BinanceConfig: The configuration instance
        
    Raises:
        RuntimeError: If configuration is not initialized or invalid
    """
    global _config
    
    if _config is None:
        _config = BinanceConfig()
    
    if not _config.is_valid():
        error_msg = "Invalid Binance configuration: " + ", ".join(_config.get_validation_errors())
        logger.error(error_msg)
        raise RuntimeError(error_msg)
    
    return _config


def get_binance_client() -> Client:
    """
    Create and return a configured Binance client instance.
    
    This function uses the global configuration to create a properly configured
    Binance client with appropriate base URL for testnet/production.
    
    Returns:
        Client: Configured Binance API client
        
    Raises:
        RuntimeError: If configuration is invalid
        BinanceAPIException: If client initialization fails
        
    Examples:
        client = get_binance_client()
        ticker = client.get_symbol_ticker(symbol="BTCUSDT")
    """
    config = get_config()
    
    try:
        # Create client with appropriate configuration
        client = Client(
            api_key=config.api_key,
            api_secret=config.api_secret,
            # testnet=config.testnet
        )
        
        # Test connection
        client.ping()
        
        logger.info(f"Successfully initialized Binance client (testnet: {config.testnet})")
        return client
        
    except BinanceAPIException as e:
        error_msg = f"Binance API error during client initialization: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e
    except BinanceRequestException as e:
        error_msg = f"Binance request error during client initialization: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e
    except Exception as e:
        error_msg = f"Unexpected error during client initialization: {str(e)}"
        logger.error(error_msg)
        raise RuntimeError(error_msg) from e


class RateLimiter:
    """
    Rate limiter for API calls to respect Binance limits.

    Binance has strict rate limits (1200 requests per minute for most endpoints).
    This class helps prevent rate limit violations.
    """
    
    def __init__(self, max_calls: int = 1200, window: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            max_calls: Maximum number of calls allowed in the time window
            window: Time window in seconds
        """
        self.max_calls = max_calls
        self.window = window
        self.calls = []
    
    def can_proceed(self) -> bool:
        """
        Check if we can make another API call without violating rate limits.
        
        Returns:
            bool: True if call can proceed, False if rate limited
        """
        now = time.time()
        
        self.calls = [call_time for call_time in self.calls if now - call_time < self.window]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
            
        return False


def create_error_response(error_type: str, message: str, details: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Create a standardized error response structure following MCP best practices.
    
    Args:
        error_type: Type/category of the error (e.g., 'validation_error', 'api_error')
        message: Human-readable error message (sanitized)
        details: Optional additional error details (sanitized)
        
    Returns:
        Dict containing standardized error response
    """
    # Sanitize error message to prevent information leakage
    sanitized_message = _sanitize_error_message(message)
    
    response = {
        "success": False,
        "error": {
            "type": error_type,
            "message": sanitized_message,
            "timestamp": int(time.time() * 1000)
        }
    }
    
    if details:
        # Ensure details don't contain sensitive information
        sanitized_details = _sanitize_error_details(details)
        response["error"]["details"] = sanitized_details
        
    return response


def _sanitize_error_message(message: str) -> str:
    """
    Sanitize error messages to prevent sensitive information leakage.
    
    Args:
        message: Raw error message
        
    Returns:
        str: Sanitized error message
    """
    if not isinstance(message, str):
        return "An error occurred"
    
    # Remove potential sensitive patterns (API keys, secrets, etc.)
    import re
    
    # Pattern to match potential API keys or secrets (more comprehensive)
    sensitive_patterns = [
        r'\b[A-Za-z0-9]{32,}\b',  # Long alphanumeric strings (API keys)
        r'(?i)api[_\s-]*key[:\s=]*[A-Za-z0-9]+',  # API key patterns
        r'(?i)secret[:\s=]*[A-Za-z0-9]+',  # Secret patterns
        r'(?i)token[:\s=]*[A-Za-z0-9]+',  # Token patterns
        r'(?i)password[:\s=]*[A-Za-z0-9]+',  # Password patterns
    ]
    
    sanitized = message
    for pattern in sensitive_patterns:
        sanitized = re.sub(pattern, '[REDACTED]', sanitized)
    
    return sanitized


def _sanitize_error_details(details: Dict) -> Dict:
    """
    Sanitize error details to remove sensitive information.
    
    Args:
        details: Raw error details
        
    Returns:
        Dict: Sanitized error details
    """
    if not isinstance(details, dict):
        return {}
    
    sanitized = {}
    sensitive_keys = {'api_key', 'secret', 'password', 'token', 'key'}
    
    for key, value in details.items():
        if key.lower() in sensitive_keys:
            sanitized[key] = '[REDACTED]'
        elif isinstance(value, str):
            sanitized[key] = _sanitize_error_message(value)
        else:
            sanitized[key] = value
    
    return sanitized


def create_success_response(data: Any, metadata: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Create a standardized success response structure.
    
    Args:
        data: The response data
        metadata: Optional metadata about the response
        
    Returns:
        Dict containing standardized success response
    """
    response = {
        "success": True,
        "data": data,
        "timestamp": int(time.time() * 1000)
    }
    
    if metadata:
        response["metadata"] = metadata
        
    return response


def rate_limited(rate_limiter: Optional[RateLimiter] = None):
    """
    Decorator to apply rate limiting to functions.
    
    Args:
        rate_limiter: Optional custom rate limiter instance
    """
    if rate_limiter is None:
        rate_limiter = RateLimiter(max_calls=1200, window=60)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not rate_limiter.can_proceed():
                return create_error_response(
                    "rate_limit_exceeded",
                    "API rate limit exceeded. Please try again later."
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def validate_symbol(symbol: str) -> str:
    """
    Validate and normalize trading symbol format.
    
    Args:
        symbol: Trading pair symbol to validate
        
    Returns:
        str: Normalized symbol in uppercase
        
    Raises:
        ValueError: If symbol format is invalid
    """
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string")
    
    # First normalize - strip and convert to uppercase
    symbol = symbol.upper().strip()
    
    # Enhanced validation before sanitization
    if len(symbol) < 3:
        raise ValueError("Symbol must be at least 3 characters long")
    
    if len(symbol) > 20:  # Reasonable upper limit for trading symbols
        raise ValueError("Symbol must be less than 20 characters long")
    
    # Sanitize input by removing any non-alphanumeric characters
    sanitized_symbol = ''.join(c for c in symbol if c.isalnum())
    
    # Validate sanitized symbol
    if len(sanitized_symbol) < 3:
        raise ValueError("Symbol must be at least 3 characters long after removing special characters")
        
    if not sanitized_symbol.isalnum():
        raise ValueError("Symbol must contain only alphanumeric characters")
    
    # Check for common invalid patterns on the sanitized symbol
    if sanitized_symbol.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')) or sanitized_symbol.isdigit():
        raise ValueError("Symbol cannot start with a number or be purely numeric")
    
    return sanitized_symbol


def validate_and_get_order_side(side: str) -> Any:
    """
    Validate and normalize order side.
    
    Args:
        side: Order side to validate ('BUY' or 'SELL')

    Returns:
        Any: Normalized order side constant from OrderSide enum
        
    Raises:
        ValueError: If order side is invalid
    """
    if not side or not isinstance(side, str):
        raise ValueError("Order side must be a non-empty string")
    
    # Sanitize and normalize input
    side = side.upper().strip()
    
    if side == "BUY":
        return Client.SIDE_BUY
    elif side == "SELL":
        return Client.SIDE_SELL
    else:
        raise ValueError("Invalid order side. Must be 'BUY' or 'SELL'.")


def validate_and_get_order_type(order_type: str) -> Any:
    """
    Validate and normalize order type.
    
    Args:
        order_type: Order type to validate (e.g., 'LIMIT', 'MARKET')

    Returns:
        Any: Normalized order type constant from OrderType enum
        
    Raises:
        ValueError: If order type is invalid
    """
    if not order_type or not isinstance(order_type, str):
        raise ValueError("Order type must be a non-empty string")
    
    # Sanitize and normalize input
    order_type = order_type.upper().strip()
    
    # Define valid order types with their corresponding client constants
    valid_order_types = {
        "LIMIT": Client.ORDER_TYPE_LIMIT,
        "MARKET": Client.ORDER_TYPE_MARKET,
        "STOP_LOSS": Client.ORDER_TYPE_STOP_LOSS,
        "STOP_LOSS_LIMIT": Client.ORDER_TYPE_STOP_LOSS_LIMIT,
        "TAKE_PROFIT": Client.ORDER_TYPE_TAKE_PROFIT,
        "TAKE_PROFIT_LIMIT": Client.ORDER_TYPE_TAKE_PROFIT_LIMIT,
        "LIMIT_MAKER": Client.ORDER_TYPE_LIMIT_MAKER
    }
    
    if order_type not in valid_order_types:
        valid_types = ", ".join(valid_order_types.keys())
        raise ValueError(f"Invalid order type. Must be one of: {valid_types}")
    
    return valid_order_types[order_type]


def validate_positive_number(value: float, field_name: str, min_value: float = 0.0, max_value: Optional[float] = None) -> float:
    """
    Validate that a numeric value is positive and within acceptable bounds.
    
    Args:
        value: The numeric value to validate
        field_name: Name of the field for error messages
        min_value: Minimum acceptable value (default: 0.0)
        max_value: Maximum acceptable value (optional)
        
    Returns:
        float: The validated value
        
    Raises:
        ValueError: If value is invalid
    """
    if not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number")
    
    if value <= min_value:
        raise ValueError(f"{field_name} must be greater than {min_value}")
    
    if max_value is not None and value > max_value:
        raise ValueError(f"{field_name} must be less than or equal to {max_value}")
    
    # Check for reasonable bounds to prevent extremely large values
    if value > 1e15:  # Prevent extremely large numbers
        raise ValueError(f"{field_name} value is too large")
    
    return float(value)


def validate_limit_parameter(limit: Optional[int], max_limit: int = 5000) -> Optional[int]:
    """
    Validate limit parameter for API calls.
    
    Args:
        limit: The limit value to validate
        max_limit: Maximum allowed limit
        
    Returns:
        Optional[int]: The validated limit or None
        
    Raises:
        ValueError: If limit is invalid
    """
    if limit is None:
        return None
    
    if not isinstance(limit, int):
        raise ValueError("Limit must be an integer")
    
    if limit <= 0:
        raise ValueError("Limit must be greater than 0")
    
    if limit > max_limit:
        raise ValueError(f"Limit must be less than or equal to {max_limit}")
    
    return limit


# def validate_and_get_account_type(account_type: str) -> Any:
#     """
#     Validate and normalize account type.
    
#     Args:
#         account_type: Account type to validate (e.g., 'SPOT', 'MARGIN', 'FUTURES')
#     Returns:
#         Any: Normalized account type constant from AccountType enum
#     """
#     if account_type == "SPOT":
#         return AccountType.SPOT
#     elif account_type == "MARGIN":
#         return AccountType.MARGIN
#     elif account_type == "FUTURES":
#         return AccountType.FUTURES
#     elif any(account for account in AccountType if account.value != account_type):
#         raise ValueError("Invalid account type. Must be 'SPOT', 'MARGIN', or 'FUTURES'.")



# Global rate limiter instance
binance_rate_limiter = RateLimiter(max_calls=1200, window=60)