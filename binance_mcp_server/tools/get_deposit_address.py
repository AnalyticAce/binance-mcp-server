"""
Binance deposit address retrieval tool implementation.

This module provides functionality to fetch deposit addresses for specific cryptocurrencies
on a user's Binance account, enabling external transfers to the exchange.
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
def get_deposit_address(coin: str) -> Dict[str, Any]:
    """
    Get the deposit address for a specific cryptocurrency on the user's Binance account.
    
    This function retrieves the deposit address for a specified coin, which can be used
    to transfer funds from external wallets or exchanges to the user's Binance account.
    
    Args:
        coin (str): The cryptocurrency symbol for which to fetch the deposit address.
                   Examples: 'BTC', 'ETH', 'USDT', 'BNB', etc.
                   Must be a valid coin supported by Binance.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (dict): Deposit address information including address and network details
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        Deposit address data typically includes:
        - address (str): The deposit address
        - coin (str): The coin symbol
        - tag (str, optional): Memo/tag for certain coins (e.g., XRP, BNB)
        - url (str, optional): QR code URL for the address
        
    Examples:
        # Get Bitcoin deposit address
        result = get_deposit_address("BTC")
        if result["success"]:
            address = result["data"]["address"]
            print(f"BTC deposit address: {address}")
        
        # Get address for coin with memo/tag
        result = get_deposit_address("XRP")
        if result["success"]:
            address = result["data"]["address"]
            tag = result["data"].get("tag")
            print(f"XRP address: {address}, Tag: {tag}")
    """
    logger.info(f"Fetching deposit address for {coin}")

    try:
        client = get_binance_client()
        deposit_address = client.get_deposit_address(coin=coin)

        return create_success_response(deposit_address)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching deposit address: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching deposit address: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_deposit_address tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")