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
def get_pnl() -> Dict[str, Any]:
    """
    Get the current profit and loss (PnL) information for the user on Binance.

    Returns:
        Dictionary containing success status, PnL data, and metadata.
    """
    logger.info("Fetching PnL information from Binance")

    try:
        client = get_binance_client()
        pnl_info = client.futures_account()

        response_data = {}

        for asset in pnl_info['assets']:
            response_data[asset['asset']] = {
                "walletBalance": float(asset['walletBalance']),
                "unrealizedProfit": float(asset['unrealizedProfit']),
                "marginBalance": float(asset['marginBalance']),
                "availableBalance": float(asset['availableBalance'])
            }
        
        return create_success_response(response_data)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching PnL info: {str(e)}")
        return create_error_response(f"Error fetching PnL info: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_pnl tool: {str(e)}")
        return create_error_response(f"Tool execution failed: {str(e)}")