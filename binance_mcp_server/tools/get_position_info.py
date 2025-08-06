"""
Binance position information retrieval tool implementation.

This module provides functionality to fetch current position information for futures trading
on Binance, essential for monitoring open positions and risk management.
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
def get_position_info() -> Dict[str, Any]:
    """
    Get the current position information for the user's Binance futures account.
    
    This function retrieves detailed information about all current futures positions,
    including position sizes, entry prices, unrealized P&L, and margin requirements.
    Essential for position monitoring and risk management.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (list): List of position information for all symbols
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        Each position object includes:
        - symbol (str): Trading pair symbol
        - positionAmt (str): Position size (positive for long, negative for short)
        - entryPrice (str): Average entry price
        - markPrice (str): Current mark price
        - unRealizedProfit (str): Unrealized profit/loss
        - liquidationPrice (str): Liquidation price
        - leverage (str): Current leverage
        - maxNotionalValue (str): Maximum notional value
        - marginType (str): Margin type (isolated/cross)
        - isolatedMargin (str): Isolated margin amount
        - isAutoAddMargin (str): Auto-add margin flag
        - positionSide (str): Position side (BOTH/LONG/SHORT)
        - notional (str): Notional value
        - isolatedWallet (str): Isolated wallet amount
        - updateTime (int): Last update timestamp
        
    Examples:
        result = get_position_info()
        if result["success"]:
            positions = result["data"]
            
            # Filter for active positions (non-zero size)
            active_positions = [p for p in positions if float(p["positionAmt"]) != 0]
            
            print(f"Active positions: {len(active_positions)}")
            for position in active_positions:
                symbol = position["symbol"]
                size = float(position["positionAmt"])
                pnl = float(position["unRealizedProfit"])
                entry_price = float(position["entryPrice"])
                
                side = "LONG" if size > 0 else "SHORT"
                print(f"{symbol}: {side} {abs(size):.4f} @ ${entry_price:.2f}")
                print(f"  Unrealized P&L: ${pnl:.2f}")
                print(f"  Liquidation: ${float(position['liquidationPrice']):.2f}")
    """
    logger.info("Fetching position information from Binance")

    try:
        client = get_binance_client()
        positions = client.futures_position_information()

        return create_success_response(positions)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching position info: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching position info: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_position_info tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")