"""
Binance order book retrieval tool implementation.

This module provides functionality to fetch current order book data (bids/asks)
for trading symbols from the Binance exchange API.
"""

import logging
from typing import Dict, Any, Optional
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance_mcp_server.utils import (
    get_binance_client,
    create_error_response,
    create_success_response,
    rate_limited,
    binance_rate_limiter,
    validate_symbol,
    validate_limit_parameter,
)

logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def get_order_book(symbol: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Get the current order book (bids/asks) for a trading symbol on Binance.
    
    This function fetches real-time order book data for any valid trading pair available
    on Binance. The order book contains arrays of bid and ask orders with their prices
    and quantities.
    
    Args:
        symbol: Trading pair symbol in format BASEQUOTE (e.g., 'BTCUSDT', 'ETHBTC')
            Must be a valid symbol listed on Binance exchange.
        limit: Optional limit for the number of orders to return per side.
               Default is 100, maximum is 1000. Valid limits: 5, 10, 20, 50, 100, 500, 1000, 5000.
        
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (dict): Response data containing order book information
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
    Examples:
        # Get order book with default limit (100)
        result = get_order_book("BTCUSDT")
        if result["success"]:
            bids = result["data"]["bids"]
            asks = result["data"]["asks"]
            print(f"Best bid: ${bids[0]['price']}")
            print(f"Best ask: ${asks[0]['price']}")
        
        # Get order book with custom limit
        result = get_order_book("ETHUSDT", limit=10)
        if result["success"]:
            print(f"Top 10 bids and asks for ETHUSDT")
    """
    logger.info(f"Fetching order book for symbol: {symbol}, limit: {limit}")
    
    try:
        # Validate and normalize symbol
        normalized_symbol = validate_symbol(symbol)
        
        # Validate limit parameter using enhanced validation
        validated_limit = validate_limit_parameter(limit, max_limit=5000)
        
        client = get_binance_client()
        
        # Prepare API parameters
        params = {"symbol": normalized_symbol}
        if validated_limit is not None:
            params["limit"] = validated_limit
        
        # Get order book data from Binance API
        order_book_data = client.get_order_book(**params)
        
        # Process bids and asks arrays
        def process_orders(orders_array):
            """Convert order arrays to structured format with float values."""
            return [
                {
                    "price": float(order[0]),
                    "quantity": float(order[1])
                }
                for order in orders_array
            ]
        
        # Process and structure the response data
        processed_bids = process_orders(order_book_data["bids"])
        processed_asks = process_orders(order_book_data["asks"])
        
        # Ensure proper sorting (bids descending by price, asks ascending by price)
        processed_bids.sort(key=lambda x: x["price"], reverse=True)
        processed_asks.sort(key=lambda x: x["price"])
        
        response_data = {
            "symbol": normalized_symbol,
            "lastUpdateId": order_book_data["lastUpdateId"],
            "bids": processed_bids,
            "asks": processed_asks,
            "bidCount": len(processed_bids),
            "askCount": len(processed_asks),
            "spread": processed_asks[0]["price"] - processed_bids[0]["price"] if processed_bids and processed_asks else None,
            "spreadPercent": (
                ((processed_asks[0]["price"] - processed_bids[0]["price"]) / processed_bids[0]["price"]) * 100
                if processed_bids and processed_asks and processed_bids[0]["price"] > 0 else None
            )
        }
        
        # Add best bid/ask for quick access
        if processed_bids:
            response_data["bestBid"] = processed_bids[0]
        if processed_asks:
            response_data["bestAsk"] = processed_asks[0]
        
        metadata = {
            "source": "binance_api",
            "endpoint": "order_book",
            "requested_limit": limit or 100,
            "actual_bids": len(processed_bids),
            "actual_asks": len(processed_asks)
        }
        
        logger.info(f"Successfully fetched order book for {normalized_symbol}: {len(processed_bids)} bids, {len(processed_asks)} asks")
        
        return create_success_response(
            data=response_data,
            metadata=metadata
        )
        
    except ValueError as e:
        error_msg = f"Invalid parameter: {str(e)}"
        logger.warning(f"Validation error for symbol '{symbol}', limit '{limit}': {error_msg}")
        return create_error_response("validation_error", error_msg)
        
    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching order book: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching order book: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_order_book tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")