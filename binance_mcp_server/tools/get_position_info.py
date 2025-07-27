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
def get_position_info() -> Dict[str, Any]:
    """
    Get the current position information for the user on Binance.

    Returns:
        Dictionary containing success status, position data, and metadata.
    """
    logger.info("Tool called: get_position_info")

    try:
        client = get_binance_client()
        positions = client.futures_position_information()

        return create_success_response(positions)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching position info: {str(e)}")
        return create_error_response(f"Error fetching position info: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_position_info tool: {str(e)}")
        return create_error_response(f"Tool execution failed: {str(e)}")