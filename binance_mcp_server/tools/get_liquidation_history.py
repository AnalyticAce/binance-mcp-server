"""
Binance liquidation history retrieval tool implementation.

This module provides functionality to fetch liquidation history for futures trading
on Binance, essential for risk management and performance analysis.
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
def get_liquidation_history() -> Dict[str, Any]:
    """
    Get the liquidation history for the user's Binance futures account.
    
    This function retrieves past liquidation events from futures trading,
    which is crucial for risk management analysis and understanding account
    performance during volatile market conditions.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (list): List of liquidation events with details
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        Each liquidation event typically includes:
        - symbol (str): Trading pair that was liquidated
        - side (str): Position side (BUY/SELL)
        - orderType (str): Type of liquidation order
        - timeInForce (str): Time in force for the order
        - origQty (str): Original quantity
        - price (str): Liquidation price
        - executedQty (str): Executed quantity
        - status (str): Order status
        - time (int): Liquidation timestamp
        
    Examples:
        result = get_liquidation_history()
        if result["success"]:
            liquidations = result["data"]
            for liq in liquidations:
                print(f"Liquidated {liq['symbol']} at {liq['price']}")
                print(f"Quantity: {liq['executedQty']}, Time: {liq['time']}")
            
            if not liquidations:
                print("No liquidation history found")
    """
    logger.info("Fetching liquidation history")

    try:
        client = get_binance_client()
        liquidation_history = client.futures_liquidation_orders()

        return create_success_response(liquidation_history)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching liquidation history: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching liquidation history: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_liquidation_history tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")