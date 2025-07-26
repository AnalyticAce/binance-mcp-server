"""
Binance 24-hour ticker statistics tool implementation.

This module provides the get_ticker tool for retrieving 24-hour price change
statistics for trading symbols from the Binance API.
"""

from typing import Dict, Any
from binance.exceptions import BinanceAPIException
from binance_mcp_server.utils import get_binance_client


def get_ticker(symbol: str) -> Dict[str, Any]:
    """
    Get 24-hour ticker price change statistics for a symbol.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')
        
    Returns:
        Dictionary containing 24-hour price statistics.
    """
    try:
        client = get_binance_client()
        ticker = client.get_ticker(symbol=symbol.upper())
        
        return {
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
