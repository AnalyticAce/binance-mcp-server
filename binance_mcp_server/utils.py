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
    Create a standardized error response structure.
    
    Args:
        error_type: Type/category of the error
        message: Human-readable error message
        details: Optional additional error details
        
    Returns:
        Dict containing standardized error response
    """
    response = {
        "success": False,
        "error": {
            "type": error_type,
            "message": message,
            "timestamp": int(time.time() * 1000)
        }
    }
    
    if details:
        response["error"]["details"] = details
        
    return response


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
    
    # Normalize symbol format
    symbol = symbol.upper().strip()
    
    # Basic validation
    if len(symbol) < 3:
        raise ValueError("Symbol must be at least 3 characters long")
        
    if not symbol.isalnum():
        raise ValueError("Symbol must contain only alphanumeric characters")
    
    return symbol


def validate_and_get_order_side(side: str) -> Any:
    """
    Validate and normalize order side.
    
    Args:
        side: Order side to validate ('BUY' or 'SELL')

    Returns:
        Any: Normalized order side constant from OrderSide enum
    """
    if side == "BUY":
        return Client.SIDE_BUY
    elif side == "SELL":
        return Client.SIDE_SELL
    elif side not in (OrderSide.SIDE_BUY.value, OrderSide.SIDE_SELL.value):
        raise ValueError("Invalid order side. Must be 'BUY' or 'SELL'.")


def validate_and_get_order_type(order_type: str) -> Any:
    """
    Validate and normalize order type.
    
    Args:
        order_type: Order type to validate (e.g., 'LIMIT', 'MARKET')

    Returns:
        Any: Normalized order type constant from OrderType enum
    """
    if order_type == "LIMIT":
        return Client.ORDER_TYPE_LIMIT
    elif order_type == "MARKET":
        return Client.ORDER_TYPE_MARKET
    elif order_type == "STOP_LOSS":
        return Client.ORDER_TYPE_STOP_LOSS
    elif order_type == "STOP_LOSS_LIMIT":
        return Client.ORDER_TYPE_STOP_LOSS_LIMIT
    elif order_type == "TAKE_PROFIT":
        return Client.ORDER_TYPE_TAKE_PROFIT
    elif order_type == "TAKE_PROFIT_LIMIT":
        return Client.ORDER_TYPE_TAKE_PROFIT_LIMIT
    elif order_type == "LIMIT_MAKER":
        return Client.ORDER_TYPE_LIMIT_MAKER
    elif any(order for order in OrderType if order.value != order_type):
        raise ValueError("Invalid order type. Must be 'LIMIT' or 'MARKET', 'STOP_LOSS', 'STOP_LOSS_LIMIT', 'TAKE_PROFIT', 'TAKE_PROFIT_LIMIT', or 'LIMIT_MAKER'.")


# Global rate limiter instance
binance_rate_limiter = RateLimiter(max_calls=1200, window=60)