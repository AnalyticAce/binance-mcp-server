"""
Binance order history retrieval tool implementation.

This module provides functionality to fetch order history for specific trading symbols
on Binance, enabling analysis of past trading activity and order management.
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
    validate_symbol
)


logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def get_orders(symbol: str, start_time: Optional[int] = None, end_time: Optional[int] = None) -> Dict[str, Any]:
    """
    Get all orders for a specific trading symbol on Binance.
    
    This function retrieves the complete order history for a specified trading pair,
    with optional time filtering to focus on specific periods. Essential for
    analyzing trading patterns and order management.
    
    Args:
        symbol (str): Trading pair symbol in format BASEQUOTE (e.g., 'BTCUSDT', 'ETHBTC').
                     Must be a valid symbol listed on Binance exchange.
        start_time (Optional[int]): Unix timestamp (milliseconds) to start retrieving orders from.
                                   If not provided, retrieves from the beginning of order history.
        end_time (Optional[int]): Unix timestamp (milliseconds) to stop retrieving orders.
                                 If not provided, retrieves up to the current time.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (list): List of order objects with detailed information
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        Each order object includes:
        - orderId (int): Unique order identifier
        - symbol (str): Trading pair symbol
        - status (str): Order status (NEW, FILLED, CANCELED, etc.)
        - side (str): Order side (BUY/SELL)
        - type (str): Order type (MARKET, LIMIT, etc.)
        - origQty (str): Original order quantity
        - executedQty (str): Executed quantity
        - price (str): Order price
        - time (int): Order creation timestamp
        
    Examples:
        # Get all orders for BTCUSDT
        result = get_orders("BTCUSDT")
        if result["success"]:
            orders = result["data"]
            print(f"Found {len(orders)} orders for BTCUSDT")
            
        # Get orders within a specific time range
        import time
        week_ago = int((time.time() - 7*24*3600) * 1000)
        result = get_orders("ETHUSDT", start_time=week_ago)
        if result["success"]:
            recent_orders = result["data"]
            print(f"Found {len(recent_orders)} orders in the last week")
    """
    logger.info("Fetching orders for symbol: %s", symbol)

    try:
        
        normalized_symbol = validate_symbol(symbol)
        
        client = get_binance_client()

        orders = client.get_all_orders(symbol=normalized_symbol, start_time=start_time, end_time=end_time)

        logger.info("Successfully fetched orders for symbol: %s", symbol)

        response_data = {
            "symbol": normalized_symbol,
            "orders": orders
        }

        return create_success_response(
            data=response_data
        )

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching orders: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching orders: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_orders tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")