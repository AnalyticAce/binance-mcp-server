"""
Shared utilities for the Binance MCP Server.

This module provides common functionality used across all tools, including
client initialization, rate limiting, and error handling utilities.
"""

import time
import os
import logging
from typing import Dict, Any, Optional, Callable, Iterable
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
        # Create client
        client = Client(
            api_key=config.api_key,
            api_secret=config.api_secret,
        )

        # Explicitly route to testnet endpoints when requested
        if config.testnet:
            try:
                # Spot testnet base URL
                if hasattr(client, "API_URL"):
                    client.API_URL = "https://testnet.binance.vision/api"
                # USD‑M Futures testnet base URL
                if hasattr(client, "FUTURES_URL"):
                    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
            except Exception as e:
                logger.warning(f"Failed to set testnet endpoints on client: {e}")

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


class WeightedRateLimiter:
    """
    Token-bucket weighted rate limiter.

    Defaults to Binance spot limit ~1200 weight/min.
    """

    def __init__(self, capacity: int = 1200, refill_per_minute: int = 1200):
        self.capacity = max(1, capacity)
        self.refill_rate = max(1, refill_per_minute) / 60.0  # tokens per second
        self.tokens = float(self.capacity)
        self.last_refill = time.time()

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill
        if elapsed <= 0:
            return
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

    def try_consume(self, cost: int = 1) -> bool:
        self._refill()
        c = max(1, int(cost))
        if self.tokens >= c:
            self.tokens -= c
            return True
        return False

    def refund(self, cost: int = 1) -> None:
        """Return tokens back into the bucket (best-effort)."""
        c = max(1, int(cost))
        self.tokens = min(self.capacity, self.tokens + c)


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


def rate_limited(rate_limiter: Optional[object] = None, *, cost: Optional[Callable[..., int] | int] = None):
    """
    Decorator to apply rate limiting to functions.
    
    Args:
        rate_limiter: Optional custom rate limiter instance
        cost: Optional constant int cost or callable(*args, **kwargs) -> int
    """
    if rate_limiter is None:
        rate_limiter = WeightedRateLimiter(capacity=1200, refill_per_minute=1200)
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Determine weight cost
            if callable(cost):
                try:
                    weight = int(cost(*args, **kwargs))
                except Exception:
                    weight = 1
            elif isinstance(cost, int):
                weight = max(1, cost)
            else:
                weight = 1

            # Support both old and new limiter interfaces
            allowed = False
            if hasattr(rate_limiter, "try_consume"):
                allowed = rate_limiter.try_consume(weight)
            elif hasattr(rate_limiter, "can_proceed"):
                allowed = rate_limiter.can_proceed()

            if not allowed:
                return create_error_response(
                    "rate_limit_exceeded",
                    "API rate limit exceeded. Please try again later.",
                    details={"weight": weight}
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


# Optional: symbol existence cache (opt-in)
_SYMBOL_CACHE = {"ts": 0.0, "symbols": set()}


def _cache_ttl_seconds() -> int:
    try:
        return int(os.getenv("BINANCE_SYMBOL_CACHE_TTL_SECONDS", "900"))
    except Exception:
        return 900


def _ensure_symbol_cache(client: Client) -> None:
    now = time.time()
    if now - _SYMBOL_CACHE["ts"] < _cache_ttl_seconds():
        return
    info = client.get_exchange_info()
    listed = {s["symbol"].upper() for s in info.get("symbols", []) if s.get("status") == "TRADING" or s.get("isSpotTradingAllowed")}
    _SYMBOL_CACHE["symbols"] = listed
    _SYMBOL_CACHE["ts"] = now


def validate_symbol_exists(symbol: str) -> str:
    """
    Validate format and (optionally) that symbol is listed on the exchange.

    Controlled by env BINANCE_MCP_VALIDATE_SYMBOL_EXISTS (default: false).
    """
    sym = validate_symbol(symbol)
    if os.getenv("BINANCE_MCP_VALIDATE_SYMBOL_EXISTS", "false").lower() != "true":
        return sym
    client = get_binance_client()
    _ensure_symbol_cache(client)
    if sym not in _SYMBOL_CACHE["symbols"]:
        raise ValueError(f"Symbol '{sym}' is not listed on Binance")
    return sym


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



def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except Exception:
        return default


# Separate spot vs. futures limiters (approximate defaults)
_SPOT_PER_MIN = _env_int("BINANCE_SPOT_WEIGHT_LIMIT_PER_MINUTE", 1200)
_FUT_PER_MIN = _env_int("BINANCE_FUTURES_WEIGHT_LIMIT_PER_MINUTE", 1200)
_SAPI_PER_MIN = _env_int("BINANCE_SAPI_WEIGHT_LIMIT_PER_MINUTE", 1200)

_SPOT_PER_SEC = _env_int("BINANCE_SPOT_WEIGHT_LIMIT_PER_SECOND", _SPOT_PER_MIN)
_FUT_PER_SEC = _env_int("BINANCE_FUTURES_WEIGHT_LIMIT_PER_SECOND", _FUT_PER_MIN)
_SAPI_PER_SEC = _env_int("BINANCE_SAPI_WEIGHT_LIMIT_PER_SECOND", _SAPI_PER_MIN)


class MultiWindowRateLimiter:
    """Combine per-second and per-minute weighted buckets."""

    def __init__(self, per_minute: int, per_second: int):
        self.minute = WeightedRateLimiter(capacity=per_minute, refill_per_minute=per_minute)
        # per-second bucket: refill_per_minute = per_second * 60
        self.second = WeightedRateLimiter(capacity=per_second, refill_per_minute=per_second * 60)

    def try_consume(self, cost: int = 1) -> bool:
        # Consume from second first; if minute fails, refund second
        if not self.second.try_consume(cost):
            return False
        if not self.minute.try_consume(cost):
            self.second.refund(cost)
            return False
        return True


binance_spot_rate_limiter = MultiWindowRateLimiter(_SPOT_PER_MIN, _SPOT_PER_SEC)
binance_futures_rate_limiter = MultiWindowRateLimiter(_FUT_PER_MIN, _FUT_PER_SEC)
binance_sapi_rate_limiter = MultiWindowRateLimiter(_SAPI_PER_MIN, _SAPI_PER_SEC)

# Backward compatibility alias (spot)
binance_rate_limiter = binance_spot_rate_limiter


def estimate_weight_for_depth(limit: Optional[int]) -> int:
    """Approximate Binance weight for GET /depth by limit."""
    if limit is None:
        return 5
    try:
        l = int(limit)
    except Exception:
        return 5
    # Based on common Binance guidance; conservative
    if l <= 50:
        return 2
    if l <= 100:
        return 5
    if l <= 500:
        return 10
    if l <= 1000:
        return 20
    return 50


def estimate_weight_for_ticker() -> int:
    return 1


def estimate_weight_for_24hr_ticker() -> int:
    return 1


def estimate_weight_for_exchange_info() -> int:
    return 10


def estimate_weight_for_account() -> int:
    return 10


def estimate_weight_for_all_orders() -> int:
    return 10


def estimate_weight_for_create_order() -> int:
    return 1


def estimate_weight_for_trade_fee() -> int:
    return 1


def estimate_weight_for_futures_account() -> int:
    return 5


def estimate_weight_for_position_info() -> int:
    return 5
