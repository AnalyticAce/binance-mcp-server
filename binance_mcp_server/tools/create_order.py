"""
Binance order creation tool implementation.

This module provides functionality to create trading orders on the Binance exchange,
supporting various order types including market and limit orders for spot trading.
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
    validate_and_get_order_side,
    validate_and_get_order_type
)


logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def create_order(symbol: str, side: str, order_type: str, quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
    """
    Create a new trading order on Binance.
    
    This function places a new trading order on the Binance exchange. Supports
    various order types including market and limit orders for spot trading.
    
    Args:
        symbol (str): Trading pair symbol in format BASEQUOTE (e.g., 'BTCUSDT', 'ETHBTC').
                     Must be a valid symbol listed on Binance exchange.
        side (str): Order side - 'BUY' to purchase or 'SELL' to dispose of the base asset.
        order_type (str): Type of order to place. Supported types:
                         - 'MARKET': Execute immediately at current market price
                         - 'LIMIT': Execute only at specified price or better
        quantity (float): Quantity of the base asset to buy/sell. Must be greater than 0
                         and respect the symbol's minimum quantity requirements.
        price (Optional[float]): Price per unit for limit orders. Required for LIMIT orders,
                               ignored for MARKET orders. Must be greater than 0.
    
    Returns:
        Dict containing:
        - success (bool): Whether the order was successfully created
        - data (dict): Order details including order ID, status, and execution info
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if order creation failed
        
    Examples:
        # Create a limit buy order
        result = create_order(
            symbol="BTCUSDT",
            side="BUY",
            order_type="LIMIT", 
            quantity=0.001,
            price=50000.00
        )
        if result["success"]:
            order_id = result["data"]["orderId"]
            print(f"Order created with ID: {order_id}")
        
        # Create a market sell order
        result = create_order(
            symbol="ETHUSDT",
            side="SELL",
            order_type="MARKET",
            quantity=0.1
        )
    """
    logger.info(f"Creating order: {symbol}, Side: {side}, Type: {order_type}, Quantity: {quantity}, Price: {price}")

    try:
        client = get_binance_client()
        
        normalized_symbol = validate_symbol(symbol)
        side = validate_and_get_order_side(side)
        order_type = validate_and_get_order_type(order_type)
        
        if quantity <= 0:
            return create_error_response("validation_error", "Invalid quantity. Must be greater than zero.")
        
        order = client.create_order(
            symbol=normalized_symbol,
            side=side,
            type=order_type,
            quantity=quantity,
            price=price
        )

        return create_success_response(order)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error creating order: {str(e)}")
        return create_error_response("binance_api_error", f"Error creating order: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in create_order tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")