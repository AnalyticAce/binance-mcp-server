"""
Tests for the get_order_book tool.

This module contains tests for the order book retrieval functionality,
including success cases, error handling, and edge cases.
"""

import pytest
from unittest.mock import Mock, patch
from binance.exceptions import BinanceAPIException, BinanceRequestException

from binance_mcp_server.tools.get_order_book import get_order_book


class TestGetOrderBook:
    """Test cases for the get_order_book function."""

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_success_default_limit(self, mock_get_client):
        """Test successful retrieval of order book with default limit."""
        # Mock client and response
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_order_book_data = {
            "lastUpdateId": 1027024,
            "bids": [
                ["4.00000000", "431.00000000"],
                ["3.99000000", "200.00000000"],
                ["3.98000000", "100.00000000"]
            ],
            "asks": [
                ["4.00000200", "12.00000000"],
                ["4.01000000", "50.00000000"],
                ["4.02000000", "25.00000000"]
            ]
        }
        mock_client.get_order_book.return_value = mock_order_book_data
        
        # Call function
        result = get_order_book("BTCUSDT")
        
        # Assertions
        assert result["success"] is True
        assert "data" in result
        assert "timestamp" in result
        assert "metadata" in result
        
        # Check data structure
        data = result["data"]
        assert data["symbol"] == "BTCUSDT"
        assert data["lastUpdateId"] == 1027024
        assert len(data["bids"]) == 3
        assert len(data["asks"]) == 3
        assert data["bidCount"] == 3
        assert data["askCount"] == 3
        
        # Check bid/ask structure and sorting
        assert data["bids"][0]["price"] == 4.0  # Highest bid first
        assert data["bids"][0]["quantity"] == 431.0
        assert data["asks"][0]["price"] == 4.000002  # Lowest ask first
        assert data["asks"][0]["quantity"] == 12.0
        
        # Check best bid/ask
        assert data["bestBid"]["price"] == 4.0
        assert data["bestAsk"]["price"] == 4.000002
        
        # Check spread calculation
        assert data["spread"] == pytest.approx(0.000002, rel=1e-6)
        assert data["spreadPercent"] is not None
        
        # Check metadata
        metadata = result["metadata"]
        assert metadata["requested_limit"] == 100  # Default limit
        assert metadata["actual_bids"] == 3
        assert metadata["actual_asks"] == 3
        
        # Verify client was called correctly
        mock_client.get_order_book.assert_called_once_with(symbol="BTCUSDT")

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_success_custom_limit(self, mock_get_client):
        """Test successful retrieval of order book with custom limit."""
        # Mock client and response
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_order_book_data = {
            "lastUpdateId": 1027025,
            "bids": [
                ["4.00000000", "431.00000000"]
            ],
            "asks": [
                ["4.00000200", "12.00000000"]
            ]
        }
        mock_client.get_order_book.return_value = mock_order_book_data
        
        # Call function with custom limit
        result = get_order_book("ETHUSDT", limit=10)
        
        # Assertions
        assert result["success"] is True
        assert result["data"]["symbol"] == "ETHUSDT"
        assert result["metadata"]["requested_limit"] == 10
        
        # Verify client was called with limit parameter
        mock_client.get_order_book.assert_called_once_with(symbol="ETHUSDT", limit=10)

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_empty_order_book(self, mock_get_client):
        """Test handling of empty order book response."""
        # Mock client and response
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_order_book_data = {
            "lastUpdateId": 1027026,
            "bids": [],
            "asks": []
        }
        mock_client.get_order_book.return_value = mock_order_book_data
        
        # Call function
        result = get_order_book("ADAUSDT")
        
        # Assertions
        assert result["success"] is True
        assert result["data"]["bidCount"] == 0
        assert result["data"]["askCount"] == 0
        assert result["data"]["spread"] is None
        assert result["data"]["spreadPercent"] is None
        assert "bestBid" not in result["data"]
        assert "bestAsk" not in result["data"]

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_symbol_validation(self, mock_get_client):
        """Test symbol validation in get_order_book."""
        # Mock client (needed even for validation errors to avoid config issues)
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Test invalid symbol formats
        invalid_symbols = ["BT", "123$%", "", "   "]
        
        for invalid_symbol in invalid_symbols:
            result = get_order_book(invalid_symbol)
            assert result["success"] is False
            assert result["error"]["type"] == "validation_error"

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_limit_validation(self, mock_get_client):
        """Test limit parameter validation."""
        # Mock client (needed even for validation errors to avoid config issues)
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        # Test invalid limit values
        invalid_limits = [-1, 0, 10000, "invalid", 3.14]
        
        for invalid_limit in invalid_limits:
            result = get_order_book("BTCUSDT", limit=invalid_limit)
            assert result["success"] is False
            assert result["error"]["type"] == "validation_error"

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_binance_api_exception(self, mock_get_client):
        """Test handling of Binance API exceptions."""
        # Mock client to raise BinanceAPIException
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_response = Mock()
        mock_response.text = "Invalid symbol"
        mock_client.get_order_book.side_effect = BinanceAPIException(
            response=mock_response, status_code=400, text="Invalid symbol"
        )
        
        # Call function
        result = get_order_book("INVALID")
        
        # Assertions
        assert result["success"] is False
        assert result["error"]["type"] == "binance_api_error"
        assert "Error fetching order book" in result["error"]["message"]

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_binance_request_exception(self, mock_get_client):
        """Test handling of Binance request exceptions."""
        # Mock client to raise BinanceRequestException
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_order_book.side_effect = BinanceRequestException("Network error")
        
        # Call function
        result = get_order_book("BTCUSDT")
        
        # Assertions
        assert result["success"] is False
        assert result["error"]["type"] == "binance_api_error"
        assert "Network error" in result["error"]["message"]

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_unexpected_exception(self, mock_get_client):
        """Test handling of unexpected exceptions."""
        # Mock client to raise unexpected exception
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_order_book.side_effect = Exception("Unexpected error")
        
        # Call function
        result = get_order_book("BTCUSDT")
        
        # Assertions
        assert result["success"] is False
        assert result["error"]["type"] == "tool_error"
        assert "Unexpected error" in result["error"]["message"]

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_sorting(self, mock_get_client):
        """Test that bids and asks are properly sorted."""
        # Mock client and response with unsorted data
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_order_book_data = {
            "lastUpdateId": 1027027,
            "bids": [
                ["3.98000000", "100.00000000"],  # Lower price
                ["4.00000000", "431.00000000"],  # Higher price - should be first
                ["3.99000000", "200.00000000"]   # Middle price
            ],
            "asks": [
                ["4.02000000", "25.00000000"],   # Higher price
                ["4.00000200", "12.00000000"],   # Lower price - should be first
                ["4.01000000", "50.00000000"]    # Middle price
            ]
        }
        mock_client.get_order_book.return_value = mock_order_book_data
        
        # Call function
        result = get_order_book("BTCUSDT")
        
        # Assertions
        assert result["success"] is True
        
        # Check bid sorting (descending by price)
        bids = result["data"]["bids"]
        assert bids[0]["price"] == 4.0      # Highest first
        assert bids[1]["price"] == 3.99     # Middle
        assert bids[2]["price"] == 3.98     # Lowest last
        
        # Check ask sorting (ascending by price)
        asks = result["data"]["asks"]
        assert asks[0]["price"] == 4.000002  # Lowest first
        assert asks[1]["price"] == 4.01      # Middle
        assert asks[2]["price"] == 4.02      # Highest last

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_spread_calculation(self, mock_get_client):
        """Test spread and spread percentage calculations."""
        # Mock client and response
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_order_book_data = {
            "lastUpdateId": 1027028,
            "bids": [
                ["100.00000000", "10.00000000"]  # Best bid: $100
            ],
            "asks": [
                ["101.00000000", "5.00000000"]   # Best ask: $101
            ]
        }
        mock_client.get_order_book.return_value = mock_order_book_data
        
        # Call function
        result = get_order_book("TESTUSDT")
        
        # Assertions
        assert result["success"] is True
        data = result["data"]
        
        # Check spread calculations
        assert data["spread"] == 1.0  # $101 - $100 = $1
        assert data["spreadPercent"] == 1.0  # ($1 / $100) * 100 = 1%

    def test_get_order_book_with_rate_limiting(self):
        """Test that rate limiting decorator is applied."""
        # This test verifies the decorator is in place
        # The actual rate limiting logic is tested in utils tests
        import inspect
        from binance_mcp_server.tools.get_order_book import get_order_book
        
        # Check that the function has been wrapped
        assert hasattr(get_order_book, '__wrapped__')

    @patch('binance_mcp_server.tools.get_order_book.get_binance_client')
    def test_get_order_book_symbol_normalization(self, mock_get_client):
        """Test that symbols are properly normalized."""
        # Mock client and response
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        
        mock_order_book_data = {
            "lastUpdateId": 1027029,
            "bids": [["4.00000000", "431.00000000"]],
            "asks": [["4.00000200", "12.00000000"]]
        }
        mock_client.get_order_book.return_value = mock_order_book_data
        
        # Call function with lowercase symbol
        result = get_order_book("btcusdt")
        
        # Assertions
        assert result["success"] is True
        assert result["data"]["symbol"] == "BTCUSDT"  # Should be normalized to uppercase
        
        # Verify client was called with normalized symbol
        mock_client.get_order_book.assert_called_once_with(symbol="BTCUSDT")