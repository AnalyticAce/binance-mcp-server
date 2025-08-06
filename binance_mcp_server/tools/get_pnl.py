"""
Binance profit and loss (P&L) calculation tool implementation.

This module provides functionality to calculate and retrieve profit and loss information
for futures trading on Binance, essential for performance analysis and risk management.
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
    validate_symbol
)


logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def get_pnl() -> Dict[str, Any]:
    """
    Get the current profit and loss (P&L) information for the user's Binance futures account.
    
    This function retrieves comprehensive P&L data from the futures account, including
    unrealized and realized profits/losses, essential for portfolio performance analysis
    and risk management in futures trading.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (dict): Complete futures account P&L information
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        P&L data includes:
        - totalUnrealizedProfit (str): Total unrealized profit across all positions
        - totalWalletBalance (str): Total wallet balance
        - totalMarginBalance (str): Total margin balance
        - totalPositionInitialMargin (str): Initial margin for positions
        - totalOpenOrderInitialMargin (str): Initial margin for open orders
        - totalCrossWalletBalance (str): Cross wallet balance
        - totalCrossUnPnl (str): Cross margin unrealized P&L
        - availableBalance (str): Available balance for new positions
        - maxWithdrawAmount (str): Maximum withdrawable amount
        - assets (list): Asset-specific balance information
        - positions (list): Current position details with individual P&L
        
    Examples:
        result = get_pnl()
        if result["success"]:
            pnl_data = result["data"]
            total_pnl = float(pnl_data["totalUnrealizedProfit"])
            wallet_balance = float(pnl_data["totalWalletBalance"])
            
            print(f"Total Unrealized P&L: ${total_pnl:.2f}")
            print(f"Wallet Balance: ${wallet_balance:.2f}")
            
            # Check individual positions
            for position in pnl_data.get("positions", []):
                if float(position["positionAmt"]) != 0:
                    symbol = position["symbol"]
                    pnl = float(position["unrealizedProfit"])
                    print(f"{symbol} P&L: ${pnl:.2f}")
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
        return create_error_response("binance_api_error", f"Error fetching PnL info: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_pnl tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")