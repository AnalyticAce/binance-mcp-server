"""
Binance MCP Server implementation using FastMCP.

This module provides a Model Context Protocol (MCP) server for interacting with 
the Binance cryptocurrency exchange API. It exposes Binance functionality as 
tools that can be called by LLM clients.
"""

import os
from typing import Optional, Dict, Any
from fastmcp import FastMCP
from binance.client import Client
from binance.exceptions import BinanceAPIException


def get_binance_client() -> Client:
    """
    Get the initialized Binance client.
    
    Returns:
        The global Binance client instance.
    """
    return Client(
        api_key=os.getenv("BINANCE_API_KEY") or os.getenv("api_key"),
        api_secret=os.getenv("BINANCE_API_SECRET") or os.getenv("api_secret"),
        testnet=os.getenv("BINANCE_TESTNET") or os.getenv("binance_testnet")
    )


mcp = FastMCP(
    name="binance-mcp-server",
    version="1.1.0",
    description="MCP server for Binance cryptocurrency exchange API",
    instructions="""
    This server provides access to Binance cryptocurrency exchange functionality.
    Available tools include:
    - get_server_info: Get server status and configuration (helpful for debugging)
    - get_account: Retrieve account information and balances (requires 'Enable Reading' permission)
    - get_ticker_price: Get current price for a trading symbol
    - get_24hr_ticker: Get 24-hour price statistics for a symbol
    - get_exchange_info: Get exchange trading rules and symbol information
    
    All operations respect Binance API rate limits and require valid API credentials.
    If you're getting API errors, try check_api_permissions first to diagnose issues.
    """
)


@mcp.tool()
def get_ticker_price(symbol: str) -> Dict[str, Any]:
    """
    Get the current price for a trading symbol.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')
        
    Returns:
        Dictionary containing current price information.
    """
    try:
        client = get_binance_client()
        ticker = client.get_symbol_ticker(symbol=symbol.upper())
        
        return {
            "symbol": ticker["symbol"],
            "price": float(ticker["price"]),
            "timestamp": ticker.get("timestamp", "N/A")
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


@mcp.tool()
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


@mcp.tool()
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


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    mcp.run(transport="stdio")