import logging
from typing import Dict, Any, Optional
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
def get_deposit_history(coin: str) -> Dict[str, Any]:
    """
    Get the deposit history for the user's Binance account.
    
    Args:
        coin (str): The coin for which to fetch the deposit history.

    Returns:
        Dictionary containing success status and deposit history data.
    """
    logger.info("Fetching deposit history")

    try:
        client = get_binance_client()
        deposit_history = client.get_deposit_history(coin=coin)

        return create_success_response(deposit_history)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching deposit history: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching deposit history: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_deposit_history tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")