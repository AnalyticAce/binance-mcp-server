import logging
from typing import Dict, Any
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
def get_oders(symbol: str) -> Dict[str, Any]:
    """

    """
    logger.info("Fetching orders for symbol: %s", symbol)

    try:
        normalized_symbol = validate_symbol(symbol)
        
        client = get_binance_client()

        orders = client.get_all_orders(symbol=normalized_symbol)

        logger.info("Successfully fetched orders for symbol: %s", symbol)

        response_data = {
            "symbol": normalized_symbol,
            "orders": orders
        }

        return create_success_response(
            data=response_data
        )

    except BinanceAPIException as e:
        error_msg = f"Binance API Error: {e.message}"
        logger.error(f"Binance API error: {e}")
        return create_error_response(
            "api_error",
            error_msg, {"code": e.code}
        )

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return create_error_response("internal_error", str(e))