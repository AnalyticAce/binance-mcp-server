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
    validate_and_get_order_type,
    OrderSide,
    OrderType
)


logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def create_order(symbol: str, side: OrderSide, order_type: OrderType, quantity: float, price: Optional[float] = None) -> Dict[str, Any]:
    """
    Create a new order on Binance.

    Args:
        symbol (str): Trading pair symbol (e.g., 'BTCUSDT').
        side (str): Order side ('BUY' or 'SELL').
        order_type (str): Type of order ('LIMIT', 'MARKET', etc.).
        quantity (float): Quantity of the asset to buy/sell.
        price (float, optional): Price for limit orders.

    Returns:
        Dictionary containing success status and order data.
    """
    logger.info(f"Tool called: create_order with symbol={symbol}, side={side}, type={order_type}, quantity={quantity}, price={price}")

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