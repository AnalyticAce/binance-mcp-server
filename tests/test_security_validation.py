"""
Test suite for enhanced security and validation functions.

Tests the security improvements and enhanced input validation added
to the Binance MCP Server.
"""

import pytest
from unittest.mock import patch, MagicMock
from binance_mcp_server.utils import (
    validate_symbol,
    validate_positive_number,
    validate_limit_parameter,
    validate_and_get_order_side,
    validate_and_get_order_type,
    create_error_response,
    _sanitize_error_message
)
from binance_mcp_server.security import (
    SecurityConfig,
    validate_api_credentials,
    SecurityMiddleware,
    secure_hash
)


class TestEnhancedValidation:
    """Test enhanced input validation functions."""
    
    def test_validate_symbol_enhanced(self):
        """Test enhanced symbol validation."""
        # Valid symbols
        assert validate_symbol("BTCUSDT") == "BTCUSDT"
        assert validate_symbol("ethbtc") == "ETHBTC"
        assert validate_symbol("  BNBusdt  ") == "BNBUSDT"
        
        # Invalid symbols
        with pytest.raises(ValueError, match="must be a non-empty string"):
            validate_symbol("")
        
        with pytest.raises(ValueError, match="must be a non-empty string"):
            validate_symbol(None)
        
        with pytest.raises(ValueError, match="must be at least 3 characters"):
            validate_symbol("BT")
        
        with pytest.raises(ValueError, match="must be less than 20 characters"):
            validate_symbol("A" * 25)
        
        with pytest.raises(ValueError, match="cannot start with a number"):
            validate_symbol("1BTCUSDT")
        
        with pytest.raises(ValueError, match="cannot start with a number"):
            validate_symbol("123456")
    
    def test_validate_symbol_sanitization(self):
        """Test symbol sanitization removes non-alphanumeric characters."""
        # Symbols with special characters should be sanitized
        assert validate_symbol("BTC-USDT") == "BTCUSDT"
        assert validate_symbol("BTC_USDT") == "BTCUSDT"
        assert validate_symbol("BTC/USDT") == "BTCUSDT"
        assert validate_symbol("BTC@USDT") == "BTCUSDT"
    
    def test_validate_positive_number(self):
        """Test positive number validation."""
        # Valid numbers
        assert validate_positive_number(1.0, "test") == 1.0
        assert validate_positive_number(100, "test") == 100.0
        assert validate_positive_number(0.001, "test") == 0.001
        
        # Invalid numbers
        with pytest.raises(ValueError, match="must be a number"):
            validate_positive_number("not_a_number", "test")
        
        with pytest.raises(ValueError, match="must be greater than 0.0"):
            validate_positive_number(0, "test")
        
        with pytest.raises(ValueError, match="must be greater than 0.0"):
            validate_positive_number(-1, "test")
        
        with pytest.raises(ValueError, match="value is too large"):
            validate_positive_number(1e16, "test")
    
    def test_validate_positive_number_with_bounds(self):
        """Test positive number validation with custom bounds."""
        # Valid within bounds
        assert validate_positive_number(5.0, "test", min_value=1.0, max_value=10.0) == 5.0
        
        # Invalid - below minimum
        with pytest.raises(ValueError, match="must be greater than 1.0"):
            validate_positive_number(0.5, "test", min_value=1.0)
        
        # Invalid - above maximum
        with pytest.raises(ValueError, match="must be less than or equal to 10.0"):
            validate_positive_number(15.0, "test", max_value=10.0)
    
    def test_validate_limit_parameter(self):
        """Test limit parameter validation."""
        # Valid limits
        assert validate_limit_parameter(10) == 10
        assert validate_limit_parameter(100) == 100
        assert validate_limit_parameter(None) is None
        
        # Invalid limits
        with pytest.raises(ValueError, match="must be an integer"):
            validate_limit_parameter(10.5)
        
        with pytest.raises(ValueError, match="must be greater than 0"):
            validate_limit_parameter(0)
        
        with pytest.raises(ValueError, match="must be greater than 0"):
            validate_limit_parameter(-1)
        
        with pytest.raises(ValueError, match="must be less than or equal to 5000"):
            validate_limit_parameter(6000)
    
    def test_validate_and_get_order_side_enhanced(self):
        """Test enhanced order side validation."""
        from binance.client import Client
        
        # Valid sides
        assert validate_and_get_order_side("BUY") == Client.SIDE_BUY
        assert validate_and_get_order_side("SELL") == Client.SIDE_SELL
        assert validate_and_get_order_side("buy") == Client.SIDE_BUY  # Case insensitive
        assert validate_and_get_order_side("  SELL  ") == Client.SIDE_SELL  # Whitespace trimmed
        
        # Invalid sides
        with pytest.raises(ValueError, match="must be a non-empty string"):
            validate_and_get_order_side("")
        
        with pytest.raises(ValueError, match="must be a non-empty string"):
            validate_and_get_order_side(None)
        
        with pytest.raises(ValueError, match="Invalid order side"):
            validate_and_get_order_side("INVALID")
    
    def test_validate_and_get_order_type_enhanced(self):
        """Test enhanced order type validation."""
        from binance.client import Client
        
        # Valid order types
        assert validate_and_get_order_type("LIMIT") == Client.ORDER_TYPE_LIMIT
        assert validate_and_get_order_type("MARKET") == Client.ORDER_TYPE_MARKET
        assert validate_and_get_order_type("limit") == Client.ORDER_TYPE_LIMIT  # Case insensitive
        
        # Invalid order types
        with pytest.raises(ValueError, match="must be a non-empty string"):
            validate_and_get_order_type("")
        
        with pytest.raises(ValueError, match="Invalid order type"):
            validate_and_get_order_type("INVALID_TYPE")


class TestSecurityFeatures:
    """Test security features and error handling."""
    
    def test_error_message_sanitization(self):
        """Test error message sanitization."""
        # Test API key sanitization
        message_with_key = "Error with API key abc123def456ghi789jkl012mno345pqr678stu901vwx234yzab567cde890fgh123"
        sanitized = _sanitize_error_message(message_with_key)
        assert "[REDACTED]" in sanitized
        assert "abc123def456" not in sanitized
        
        # Test secret sanitization
        message_with_secret = "API secret xyz789 failed"
        sanitized = _sanitize_error_message(message_with_secret)
        assert "[REDACTED]" in sanitized
        
        # Test normal message unchanged
        normal_message = "Invalid symbol format"
        assert _sanitize_error_message(normal_message) == normal_message
    
    def test_create_error_response_security(self):
        """Test error response creation with security."""
        # Test error response with sensitive data
        response = create_error_response(
            "test_error",
            "Error with API key abc123def456ghi789jkl012mno345pqr678stu901vwx234yzab567cde890fgh123",
            {"api_key": "secret_key", "normal_field": "normal_value"}
        )
        
        assert response["success"] is False
        assert response["error"]["type"] == "test_error"
        assert "[REDACTED]" in response["error"]["message"]
        assert response["error"]["details"]["api_key"] == "[REDACTED]"
        assert response["error"]["details"]["normal_field"] == "normal_value"
    
    @patch.dict('os.environ', {
        'BINANCE_API_KEY': 'valid_api_key_with_sufficient_length',
        'BINANCE_API_SECRET': 'valid_api_secret_with_sufficient_length'
    })
    def test_validate_api_credentials_valid(self):
        """Test API credentials validation with valid credentials."""
        assert validate_api_credentials() is True
    
    @patch.dict('os.environ', {}, clear=True)
    def test_validate_api_credentials_missing(self):
        """Test API credentials validation with missing credentials."""
        assert validate_api_credentials() is False
    
    @patch.dict('os.environ', {
        'BINANCE_API_KEY': 'short',
        'BINANCE_API_SECRET': 'also_short'
    })
    def test_validate_api_credentials_too_short(self):
        """Test API credentials validation with too short credentials."""
        assert validate_api_credentials() is False
    
    @patch.dict('os.environ', {
        'BINANCE_API_KEY': 'test',
        'BINANCE_API_SECRET': 'demo'
    })
    def test_validate_api_credentials_insecure_values(self):
        """Test API credentials validation with insecure placeholder values."""
        assert validate_api_credentials() is False
    
    def test_security_config(self):
        """Test security configuration."""
        config = SecurityConfig()
        
        # Test default values
        assert config.rate_limit_enabled is True
        assert config.enable_input_validation is True
        
        # Test security validation
        warnings = config.get_security_warnings()
        # Default config should be secure, so no warnings
        assert len([w for w in warnings if "disabled" in w]) == 0
    
    def test_security_middleware(self):
        """Test security middleware."""
        middleware = SecurityMiddleware()
        
        # Test normal request
        normal_request = {"symbol": "BTCUSDT", "side": "BUY"}
        result = middleware.validate_request(normal_request)
        assert result["valid"] is True
        assert len(result["warnings"]) == 0
        
        # Test request with potential injection
        malicious_request = {"symbol": "BTCUSDT'; DROP TABLE users; --"}
        result = middleware.validate_request(malicious_request)
        assert result["valid"] is False
        assert any("injection" in warning.lower() for warning in result["warnings"])
    
    def test_secure_hash(self):
        """Test secure hash function."""
        test_data = "sensitive_data_12345"
        hash_result = secure_hash(test_data)
        
        assert len(hash_result) == 16  # First 16 chars of SHA-256
        assert hash_result == secure_hash(test_data)  # Consistent
        assert hash_result != secure_hash("different_data")  # Different for different input