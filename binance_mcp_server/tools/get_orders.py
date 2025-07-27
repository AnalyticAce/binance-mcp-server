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