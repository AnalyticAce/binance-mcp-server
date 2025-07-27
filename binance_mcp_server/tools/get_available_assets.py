"""
Binance available assets tool implementation.

This module provides the get_available_assets tool for retrieving a list of
all available trading symbols and their information from the Binance API.
"""
import logging
from typing import Dict, Any
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance_mcp_server.utils import (
    get_binance_client, 
    create_error_response, 
    create_success_response,
    rate_limited,
    binance_rate_limiter,
)


logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def get_available_assets() -> Dict[str, Any]:
    """
    Get a list of all available assets on Binance.

    Returns:
        Dictionary containing asset information.
    """
    logger.info("Tool called: get_available_assets")

    try:
        client = get_binance_client()
        exchange_info = client.get_exchange_info()

        assets = {symbol["symbol"]: symbol for symbol in exchange_info["symbols"]}

        return create_success_response({
            "assets": assets,
            "count": len(assets)
        })

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching available assets: {str(e)}")
        return create_error_response(f"Error fetching available assets: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_available_assets tool: {str(e)}")
        return create_error_response(f"Tool execution failed: {str(e)}")