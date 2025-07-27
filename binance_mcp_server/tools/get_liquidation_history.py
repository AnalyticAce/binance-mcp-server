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
def get_liquidation_history() -> Dict[str, Any]:
    """
    Get the liquidation history on Binance account.

    Returns:
        Dictionary containing success status and liquidation history data.
    """
    logger.info("Fetching liquidation history")

    try:
        client = get_binance_client()
        liquidation_history = client.futures_liquidation_orders()

        return create_success_response(liquidation_history)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching liquidation history: {str(e)}")
        return create_error_response(f"Error fetching liquidation history: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_liquidation_history tool: {str(e)}")
        return create_error_response(f"Tool execution failed: {str(e)}")