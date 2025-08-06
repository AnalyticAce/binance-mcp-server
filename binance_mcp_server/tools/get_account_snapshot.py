"""
Binance account snapshot retrieval tool implementation.

This module provides functionality to fetch point-in-time account snapshots
for different account types on Binance, useful for portfolio analysis and reporting.
"""

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
    Get a point-in-time account snapshot for the user's Binance account.
    
    This function retrieves a comprehensive account snapshot for the specified
    account type, providing a historical view of account state including balances
    and positions at a specific point in time.
    
    Args:
        account_type (str): The type of account to capture snapshot for.
                           Supported types:
                           - 'SPOT': Spot trading account balances
                           - 'MARGIN': Cross margin account balances
                           - 'FUTURES': USDⓈ-M futures account balances
                           - 'FAPI': Futures API account (alias for FUTURES)
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (dict): Account snapshot data with balances and metadata
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        Snapshot data structure:
        - snapshotVos (list): List of snapshot records
        - type (str): Account type
        - updateTime (int): Last update timestamp
        
        Each snapshot record contains:
        - data (dict): Account state data (balances, positions)
        - type (str): Record type
        - updateTime (int): Snapshot timestamp
        
    Examples:
        # Get spot account snapshot
        result = get_account_snapshot("SPOT")
        if result["success"]:
            snapshot = result["data"]
            print(f"Snapshot type: {snapshot['type']}")
            for record in snapshot["snapshotVos"]:
                print(f"Update time: {record['updateTime']}")
        
        # Get futures account snapshot
        result = get_account_snapshot("FUTURES")
        if result["success"]:
            futures_data = result["data"]
            print(f"Futures account snapshot captured")
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