import logging
from typing import Dict, Any, Optional
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance_mcp_server.utils import (
    get_binance_client, 
    create_error_response, 
    create_success_response,
    rate_limited,
    binance_rate_limiter,
    # validate_and_get_account_type
)


logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def get_account_snapshot(account_type: str) -> Dict[str, Any]:
    """
    Get the account snapshot for the user's Binance account.

    Args:
        account_type (AccountType): The account type to filter the snapshot.

    Returns:
        Dictionary containing success status and account snapshot data.
    """
    logger.info("Fetching account snapshot")

    try:
        client = get_binance_client()
        
        # account_type = validate_and_get_account_type(account_type)
        
        snapshot = client.get_account_snapshot(type=account_type)

        return create_success_response(snapshot)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching account snapshot: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching account snapshot: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_account_snapshot tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")