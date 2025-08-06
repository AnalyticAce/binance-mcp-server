"""
Binance withdrawal history retrieval tool implementation.

This module provides functionality to fetch withdrawal transaction history for specific
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
def get_withdraw_history(coin: str) -> Dict[str, Any]:
    """
    Get the withdrawal transaction history for a specific cryptocurrency on the user's Binance account.
    
    This function retrieves the complete history of withdrawals for a specified coin,
    providing detailed information about each withdrawal transaction including status,
    amounts, fees, and destination addresses.
    
    Args:
        coin (str): The cryptocurrency symbol for which to fetch withdrawal history.
                   Examples: 'BTC', 'ETH', 'USDT', 'BNB', etc.
                   Must be a valid coin supported by Binance.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (list): List of withdrawal transaction records
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        Each withdrawal record includes:
        - amount (str): Withdrawal amount
        - transactionFee (str): Network transaction fee
        - coin (str): Cryptocurrency symbol
        - status (int): Withdrawal status (0=Email Sent, 1=Cancelled, 2=Awaiting Approval, 3=Rejected, 4=Processing, 5=Failure, 6=Completed)
        - address (str): Destination address
        - addressTag (str): Address tag/memo if applicable
        - txId (str): Blockchain transaction hash (when available)
        - applyTime (str): Withdrawal request timestamp
        - network (str): Blockchain network used
        - info (str): Additional information
        
    Examples:
        # Get Bitcoin withdrawal history
        result = get_withdraw_history("BTC")
        if result["success"]:
            withdrawals = result["data"]
            for withdrawal in withdrawals:
                print(f"Amount: {withdrawal['amount']} BTC")
                print(f"Fee: {withdrawal['transactionFee']} BTC")
                print(f"Status: {withdrawal['status']}")
                print(f"Address: {withdrawal['address']}")
        
        # Check for recent withdrawals
        result = get_withdraw_history("USDT")
        if result["success"]:
            usdt_withdrawals = result["data"]
            completed = [w for w in usdt_withdrawals if w['status'] == 6]
            print(f"Completed USDT withdrawals: {len(completed)}")
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