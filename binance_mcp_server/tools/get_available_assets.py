"""
Binance available assets tool implementation.

This module provides the get_available_assets tool for retrieving a list of
all available trading symbols and their information from the Binance API.
"""

from typing import Dict, Any
from binance.exceptions import BinanceAPIException
from binance_mcp_server.utils import get_binance_client


def get_available_assets() -> Dict[str, Any]:
    """
    Get a list of all available assets on Binance.
    
    Returns:
        Dictionary containing asset information.
    """
    try:
        client = get_binance_client()
        exchange_info = client.get_exchange_info()
        
        assets = {symbol["symbol"]: symbol for symbol in exchange_info["symbols"]}
        
        return {
            "assets": assets,
            "count": len(assets)
        }
        
    except BinanceAPIException as e:
        return {
            "error": "Binance API Error",
            "message": str(e),
            "code": getattr(e, 'code', 'UNKNOWN')
        }
    except Exception as e:
        return {
            "error": "Unexpected Error",
            "message": str(e)
        }
