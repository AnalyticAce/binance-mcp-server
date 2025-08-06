"""
Binance account balance retrieval tool implementation.

This module provides functionality to fetch current account balance information
for all assets in a user's Binance account, including available and locked amounts.
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
def get_balance() -> Dict[str, Any]:
    """
    Get the current account balance for all assets on Binance.
    
    This function retrieves the balances of all assets in the user's Binance account,
    including available (free) and locked amounts for each asset. Only assets with
    non-zero balances are returned to reduce response size.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (dict): Mapping of asset symbols to balance information
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        Balance data structure for each asset:
        - free (float): Available balance for trading/withdrawal
        - locked (float): Balance locked in open orders or other operations
        
    Examples:
        result = get_balance()
        if result["success"]:
            balances = result["data"]
            print(f"Available USDT: {balances['USDT']['free']}")
            print(f"Locked BTC: {balances['BTC']['locked']}")
            
        # Check if specific asset exists
        if "ETH" in result["data"]:
            eth_balance = result["data"]["ETH"]
            total_eth = eth_balance["free"] + eth_balance["locked"]
    """
    logger.info("Fetching account balance")
    
    try:
        client = get_binance_client()
        
        account_info = client.get_account()
        
        balances = {
            asset["asset"]: {
                "free": float(asset["free"]),
                "locked": float(asset["locked"])
            }
            for asset in account_info["balances"]
            if float(asset["free"]) > 0 or float(asset["locked"]) > 0
        }
        
        logger.info("Successfully fetched account balances")
        
        return create_success_response(
            data=balances
        )

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching account assets: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching account assets: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_account_assets tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")