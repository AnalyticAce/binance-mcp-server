"""
Binance MCP Server implementation using FastMCP.

This module provides a Model Context Protocol (MCP) server for interacting with 
the Binance cryptocurrency exchange API. It exposes Binance functionality as 
tools that can be called by LLM clients.
"""

import sys
import logging
from typing import Dict, Any
from fastmcp import FastMCP


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr  # Essential: Use stderr for STDIO servers
)


logger = logging.getLogger(__name__)


mcp = FastMCP(
    name="binance-mcp-server",
    version="1.1.0",
    description="MCP server for Binance cryptocurrency exchange API",
    instructions="""
    This server provides access to Binance cryptocurrency exchange functionality.
    Available tools include:
    - get_ticker_price: Get current price for a trading symbol
    - get_ticker: Get 24-hour price statistics for a symbol
    - get_available_assets: Get exchange trading rules and symbol information
    
    All operations respect Binance API rate limits and use proper configuration management.
    Tools are implemented in dedicated modules for better maintainability.
    """
)


@mcp.tool()
def get_ticker_price(symbol: str) -> Dict[str, Any]:
    """
    Get the current price for a trading symbol on Binance.
    
    This tool fetches real-time price data for any valid trading pair available
    on Binance using the configured environment (production or testnet).
    
    Args:
        symbol: Trading pair symbol in format BASEQUOTE (e.g., 'BTCUSDT', 'ETHBTC')
        
    Returns:
        Dictionary containing success status, price data, and metadata
    """
    logger.info(f"Tool called: get_ticker_price with symbol={symbol}")
    
    try:
        from binance_mcp_server.tools.get_ticker_price import get_ticker_price as _get_ticker_price
        result = _get_ticker_price(symbol)
        
        if result.get("success"):
            logger.info(f"Successfully fetched price for {symbol}")
        else:
            logger.warning(f"Failed to fetch price for {symbol}: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_ticker_price tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_ticker(symbol: str) -> Dict[str, Any]:
    """
    Get 24-hour ticker price change statistics for a symbol.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')
        
    Returns:
        Dictionary containing 24-hour price statistics and metadata.
    """
    logger.info(f"Tool called: get_ticker with symbol={symbol}")
    
    try:
        from binance_mcp_server.tools.get_ticker import get_ticker as _get_ticker
        result = _get_ticker(symbol)
        
        if result.get("success"):
            logger.info(f"Successfully fetched ticker stats for {symbol}")
        else:
            logger.warning(f"Failed to fetch ticker stats for {symbol}: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_ticker tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_available_assets() -> Dict[str, Any]:
    """
    Get a list of all available assets and trading pairs on Binance.
    
    Returns:
        Dictionary containing comprehensive exchange information and available assets.
    """
    logger.info("Tool called: get_available_assets")
    
    try:
        from binance_mcp_server.tools.get_available_assets import get_available_assets as _get_available_assets
        result = _get_available_assets()
        
        if result.get("success"):
            logger.info("Successfully fetched available assets")
        else:
            logger.warning(f"Failed to fetch available assets: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_available_assets tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


if __name__ == "__main__":
    import argparse
    from dotenv import load_dotenv
    
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Binance MCP Server")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio",
                    help="Transport method to use")
    parser.add_argument("--port", type=int, default=8000,
                    help="Port for HTTP transport")
    parser.add_argument("--host", type=str, default="localhost",
                    help="Host for HTTP transport")
    
    args = parser.parse_args()
    
    logger.info(f"Starting Binance MCP Server with {args.transport} transport")
    
    try:
        if args.transport == "stdio":
            mcp.run(transport="stdio")
        else:
            logger.info(f"HTTP server starting on {args.host}:{args.port}")
            mcp.run(transport="http", port=args.port, host=args.host)
    except Exception as e:
        logger.error(f"Server startup failed: {str(e)}")
        sys.exit(1)