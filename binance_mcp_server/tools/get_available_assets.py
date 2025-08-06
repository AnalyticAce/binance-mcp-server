"""
Binance available assets tool implementation.

This module provides the get_available_assets tool for retrieving a list of
all available trading symbols and their information from the Binance API.
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
def get_available_assets() -> Dict[str, Any]:
    """
    Get a comprehensive list of all available trading assets and symbols on Binance.
    
    This function retrieves complete exchange information including all tradable symbols,
    their configurations, and trading rules. Essential for discovering available trading
    pairs and understanding their specifications.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (dict): Exchange information with assets and trading rules
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
        Data structure includes:
        - assets (dict): Mapping of symbol names to detailed symbol information
        - count (int): Total number of available trading symbols
        
        Each symbol entry contains:
        - symbol (str): Trading pair symbol (e.g., "BTCUSDT")
        - status (str): Symbol status (TRADING, HALT, etc.)
        - baseAsset (str): Base asset symbol (e.g., "BTC")
        - quoteAsset (str): Quote asset symbol (e.g., "USDT")
        - baseAssetPrecision (int): Precision for base asset
        - quotePrecision (int): Precision for quote asset
        - filters (list): Trading filters (price, quantity, etc.)
        - permissions (list): Allowed order types and permissions
        - orderTypes (list): Supported order types
        - icebergAllowed (bool): Iceberg orders allowed
        - ocoAllowed (bool): OCO orders allowed
        - quoteOrderQtyMarketAllowed (bool): Market orders by quote quantity allowed
        - allowTrailingStop (bool): Trailing stop orders allowed
        - cancelReplaceAllowed (bool): Cancel and replace allowed
        - isSpotTradingAllowed (bool): Spot trading allowed
        - isMarginTradingAllowed (bool): Margin trading allowed
        
    Examples:
        result = get_available_assets()
        if result["success"]:
            exchange_data = result["data"]
            assets = exchange_data["assets"]
            
            print(f"Total available symbols: {exchange_data['count']}")
            
            # Find USDT pairs
            usdt_pairs = [symbol for symbol in assets.keys() if symbol.endswith("USDT")]
            print(f"USDT trading pairs: {len(usdt_pairs)}")
            
            # Check specific symbol details
            if "BTCUSDT" in assets:
                btc_info = assets["BTCUSDT"]
                print(f"BTC/USDT Status: {btc_info['status']}")
                print(f"Order types: {btc_info['orderTypes']}")
    """
    logger.info("Fetching available assets from Binance")

    try:
        client = get_binance_client()
        exchange_info = client.get_exchange_info()

        assets = {symbol["symbol"]: symbol for symbol in exchange_info["symbols"]}

        return create_success_response({
            "assets": assets,
            "count": len(assets)
        })

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching available assets: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching available assets: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_available_assets tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")