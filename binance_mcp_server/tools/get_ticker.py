"""
Binance 24-hour ticker statistics tool implementation.

This module provides the get_ticker tool for retrieving 24-hour price change
statistics for trading symbols from the Binance API.
"""

import logging
from typing import Dict, Any
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance_mcp_server.utils import  (
    get_binance_client, 
    validate_symbol, 
    rate_limited, 
    binance_rate_limiter,
    create_success_response,
    create_error_response
)


logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def get_ticker(symbol: str) -> Dict[str, Any]:
    """
    Get 24-hour ticker price change statistics for a symbol.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')
        
    Returns:
        Dictionary containing 24-hour price statistics.
        - success (bool): True if request was successful
        - data (dict): Response data with price statistics
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed

    Examples:
        result = get_ticker("BTCUSDT")
        if result["success"]:
            stats = result["data"]
            print(f"24h price change for BTC: {stats['price_change']} ({stats['price_change_percent']}%)")
    """

    logger.info(f"Fetching 24-hour ticker stats for symbol: {symbol}")

    try:
        
        normalized_symbol = validate_symbol(symbol)
        
        client = get_binance_client()
        ticker = client.get_ticker(symbol=normalized_symbol)

        response = {
            "symbol": ticker["symbol"],
            "price_change": float(ticker["priceChange"]),
            "price_change_percent": float(ticker["priceChangePercent"]),
            "weighted_avg_price": float(ticker["weightedAvgPrice"]),
            "prev_close_price": float(ticker["prevClosePrice"]),
            "last_price": float(ticker["lastPrice"]),
            "bid_price": float(ticker["bidPrice"]),
            "ask_price": float(ticker["askPrice"]),
            "open_price": float(ticker["openPrice"]),
            "high_price": float(ticker["highPrice"]),
            "low_price": float(ticker["lowPrice"]),
            "volume": float(ticker["volume"]),
            "quote_volume": float(ticker["quoteVolume"]),
            "open_time": ticker["openTime"],
            "close_time": ticker["closeTime"],
            "count": ticker["count"]
        }
        
        logger.info(f"Successfully fetched ticker stats for {symbol}")
        return create_success_response(
            data=response,
            metadata={
                "source": "binance_api",
                "endpoint": "24h_ticker"
            }
        )
        
        
    except ValueError as e:
        error_msg = f"Invalid symbol format: {str(e)}"
        logger.warning(f"Validation error for symbol '{symbol}': {error_msg}")
        return create_error_response("validation_error", error_msg)
        
    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching ticker stats: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching ticker stats: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_ticker tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")