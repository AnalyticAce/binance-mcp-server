"""
Tests for the get_fee_info tool.

This module contains tests for the fee information retrieval functionality,
including success cases, error handling, and edge cases.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from binance.exceptions import BinanceAPIException, BinanceRequestException

from binance_mcp_server.tools.get_fee_info import get_fee_info


class TestGetFeeInfo:
    """Test cases for the get_fee_info function."""

    @patch('binance_mcp_server.tools.get_fee_info.get_binance_client')
    def test_get_fee_info_all_symbols_success(self, mock_get_client):
        """Test successful retrieval of fee information for all symbols."""
        # Mock client and response
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_fee_data = [
            {
                "symbol": "BTCUSDT",
                "makerCommission": "0.001",
                "takerCommission": "0.001"
            },
            {
                "symbol": "ETHUSDT",
                "makerCommission": "0.001",
                "takerCommission": "0.001"
            }
        ]
        mock_client.get_trade_fee.return_value = mock_fee_data
        
        # Call function
        result = get_fee_info()
        
        # Assertions
        assert result["success"] is True
        assert "data" in result
        assert "timestamp" in result
        assert "metadata" in result
        
        # Check data structure
        data = result["data"]
        assert len(data) == 2
        assert data[0]["symbol"] == "BTCUSDT"
        assert data[0]["makerCommission"] == 0.001
        assert data[0]["takerCommission"] == 0.001
        assert data[0]["makerCommissionPercent"] == "0.1000%"
        assert data[0]["takerCommissionPercent"] == "0.1000%"
        
        # Check metadata
        metadata = result["metadata"]
        assert metadata["count"] == 2
        assert metadata["fee_type"] == "trading_fees"
        assert "requested_symbol" not in metadata
        
        # Verify client was called correctly
        mock_client.get_trade_fee.assert_called_once_with()

    @patch('binance_mcp_server.tools.get_fee_info.get_binance_client')
    def test_get_fee_info_specific_symbol_success(self, mock_get_client):
        """Test successful retrieval of fee information for a specific symbol."""
        # Mock client and response
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_fee_data = [
            {
                "symbol": "BTCUSDT",
                "makerCommission": "0.001",
                "takerCommission": "0.001"
            }
        ]
        mock_client.get_trade_fee.return_value = mock_fee_data
        
        # Call function with specific symbol
        result = get_fee_info(symbol="BTCUSDT")
        
        # Assertions
        assert result["success"] is True
        assert len(result["data"]) == 1
        assert result["data"][0]["symbol"] == "BTCUSDT"
        assert result["metadata"]["requested_symbol"] == "BTCUSDT"
        
        # Verify client was called with symbol parameter
        mock_client.get_trade_fee.assert_called_once_with(symbol="BTCUSDT")

    @patch('binance_mcp_server.tools.get_fee_info.get_binance_client')
    def test_get_fee_info_empty_string_symbol(self, mock_get_client):
        """Test that empty string symbol is treated as all symbols."""
        # Mock client and response
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_fee_data = [
            {
                "symbol": "BTCUSDT",
                "makerCommission": "0.001",
                "takerCommission": "0.001"
            }
        ]
        mock_client.get_trade_fee.return_value = mock_fee_data
        
        # Call function with empty string (should behave like no symbol)
        result = get_fee_info(symbol="")
        
        # Assertions
        assert result["success"] is True
        assert "requested_symbol" not in result["metadata"]
        
        # Verify client was called without symbol parameter
        mock_client.get_trade_fee.assert_called_once_with()

    @patch('binance_mcp_server.tools.get_fee_info.get_binance_client')
    def test_get_fee_info_symbol_validation(self, mock_get_client):
        """Test symbol validation in get_fee_info."""
        # Mock client (needed even for validation errors to avoid config issues)
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Test invalid symbol formats that should trigger validation errors
        invalid_symbols = ["BT", "123$%"]  # Only test clearly invalid symbols
        
        for invalid_symbol in invalid_symbols:
            result = get_fee_info(symbol=invalid_symbol)
            assert result["success"] is False
            assert result["error"]["type"] == "validation_error"

    @patch('binance_mcp_server.tools.get_fee_info.get_binance_client')
    def test_get_fee_info_binance_api_exception(self, mock_get_client):
        """Test handling of Binance API exceptions."""
        # Mock client to raise BinanceAPIException
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        # Fix BinanceAPIException constructor call
        mock_response = Mock()
        mock_response.text = "API Error"
        mock_client.get_trade_fee.side_effect = BinanceAPIException(
            response=mock_response, status_code=400, text="API Error"
        )
        
        # Call function
        result = get_fee_info()
        
        # Assertions
        assert result["success"] is False
        assert result["error"]["type"] == "binance_api_error"
        assert "Error fetching fee information" in result["error"]["message"]

    @patch('binance_mcp_server.tools.get_fee_info.get_binance_client')
    def test_get_fee_info_binance_request_exception(self, mock_get_client):
        """Test handling of Binance request exceptions."""
        # Mock client to raise BinanceRequestException
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_trade_fee.side_effect = BinanceRequestException("Request Error")
        
        # Call function
        result = get_fee_info()
        
        # Assertions
        assert result["success"] is False
        assert result["error"]["type"] == "binance_api_error"
        assert "Request Error" in result["error"]["message"]

    @patch('binance_mcp_server.tools.get_fee_info.get_binance_client')
    def test_get_fee_info_unexpected_exception(self, mock_get_client):
        """Test handling of unexpected exceptions."""
        # Mock client to raise unexpected exception
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_trade_fee.side_effect = Exception("Unexpected error")
        
        # Call function
        result = get_fee_info()
        
        # Assertions
        assert result["success"] is False
        assert result["error"]["type"] == "tool_error"
        assert "Unexpected error" in result["error"]["message"]

    @patch('binance_mcp_server.tools.get_fee_info.get_binance_client')
    def test_get_fee_info_single_item_response(self, mock_get_client):
        """Test handling when API returns a single item instead of list."""
        # Mock client and response (single dict instead of list)
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_fee_data = {
            "symbol": "BTCUSDT",
            "makerCommission": "0.001",
            "takerCommission": "0.001"
        }
        mock_client.get_trade_fee.return_value = mock_fee_data
        
        # Call function
        result = get_fee_info(symbol="BTCUSDT")
        
        # Assertions
        assert result["success"] is True
        assert len(result["data"]) == 1
        assert result["data"][0]["symbol"] == "BTCUSDT"

    @patch('binance_mcp_server.tools.get_fee_info.get_binance_client')
    def test_get_fee_info_sorting(self, mock_get_client):
        """Test that results are sorted by symbol."""
        # Mock client and response with unsorted data
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_fee_data = [
            {
                "symbol": "ETHUSDT",
                "makerCommission": "0.001",
                "takerCommission": "0.001"
            },
            {
                "symbol": "BTCUSDT",
                "makerCommission": "0.001",
                "takerCommission": "0.001"
            },
            {
                "symbol": "ADAUSDT",
                "makerCommission": "0.001",
                "takerCommission": "0.001"
            }
        ]
        mock_client.get_trade_fee.return_value = mock_fee_data
        
        # Call function
        result = get_fee_info()
        
        # Assertions
        assert result["success"] is True
        symbols = [item["symbol"] for item in result["data"]]
        assert symbols == ["ADAUSDT", "BTCUSDT", "ETHUSDT"]  # Should be sorted

    def test_get_fee_info_with_rate_limiting(self):
        """Test that rate limiting decorator is applied."""
        # This test verifies the decorator is in place
        # The actual rate limiting logic is tested in utils tests
        import inspect
        from binance_mcp_server.tools.get_fee_info import get_fee_info
        
        # Check that the function has been wrapped
        assert hasattr(get_fee_info, '__wrapped__')