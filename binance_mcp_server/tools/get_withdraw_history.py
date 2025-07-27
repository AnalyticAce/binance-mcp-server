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
def get_withdraw_history(coin: str) -> Dict[str, Any]:
    """
    Get the withdrawal history for the user's Binance account.

    Args:
        coin (Optional[str]): The coin for which to fetch the withdrawal history. Defaults to 'BTC'.

    Returns:
        Dictionary containing success status and withdrawal history data.
    """
    logger.info("Fetching withdrawal history")

    try:
        client = get_binance_client()
        withdraw_history = client.get_withdraw_history(coin=coin)

        return create_success_response(withdraw_history)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching withdrawal history: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching withdrawal history: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_withdraw_history tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")