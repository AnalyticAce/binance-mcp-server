"""
Binance deposit history retrieval tool implementation.

This module provides functionality to fetch deposit transaction history for specific
cryptocurrencies on a user's Binance account, enabling transaction tracking and analysis.
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
)


logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def get_deposit_history(coin: str) -> Dict[str, Any]:
    """
    Get the deposit transaction history for a specific cryptocurrency on the user's Binance account.
    
    This function retrieves the complete history of deposits for a specified coin,
    providing detailed information about each deposit transaction including status,
    amounts, and timestamps.
    
    Args:
        coin (str): The cryptocurrency symbol for which to fetch deposit history.
                   Examples: 'BTC', 'ETH', 'USDT', 'BNB', etc.
                   Must be a valid coin supported by Binance.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (list): List of deposit transaction records
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        Each deposit record includes:
        - amount (str): Deposit amount
        - coin (str): Cryptocurrency symbol
        - network (str): Blockchain network used
        - status (int): Deposit status (0=pending, 6=credited, 1=success)
        - address (str): Deposit address used
        - addressTag (str): Address tag/memo if applicable
        - txId (str): Blockchain transaction hash
        - insertTime (int): Deposit initiation timestamp
        - transferType (int): Transfer type indicator
        - confirmTimes (str): Required confirmation times
        
    Examples:
        # Get Bitcoin deposit history
        result = get_deposit_history("BTC")
        if result["success"]:
            deposits = result["data"]
            for deposit in deposits:
                print(f"Amount: {deposit['amount']} BTC")
                print(f"Status: {deposit['status']}")
                print(f"TxID: {deposit['txId']}")
        
        # Check for recent deposits
        result = get_deposit_history("USDT")
        if result["success"]:
            usdt_deposits = result["data"]
            if usdt_deposits:
                latest = usdt_deposits[0]  # Most recent deposit
                print(f"Latest USDT deposit: {latest['amount']}")
            else:
                print("No USDT deposits found")
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