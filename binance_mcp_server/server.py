"""
Binance MCP Server implementation using FastMCP.

This module provides a Model Context Protocol (MCP) server for interacting with 
the Binance cryptocurrency exchange API. It exposes Binance functionality as 
tools that can be called by LLM clients.
"""

import sys
import logging
import argparse
from typing import Dict, Any, Optional
from fastmcp import FastMCP
from dotenv import load_dotenv

from binance_mcp_server.utils import OrderSide, OrderType


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)


logger = logging.getLogger(__name__)


mcp = FastMCP(
    name="binance-mcp-server",
    version="1.2.4",
    description="MCP server for Binance cryptocurrency exchange API",
    instructions="""
    This server provides access to Binance cryptocurrency exchange functionality.
    Available tools include:
    - get_ticker_price: Get current price for a trading symbol
    - get_ticker: Get 24-hour price statistics for a symbol
    - get_available_assets: Get exchange trading rules and symbol information
    
    All operations respect Binance API rate limits and use proper configuration management.
    Tools are implemented in dedicated modules for better maintainability.
    """,
    capabilities={
        "tools": {"listChanged": True},
        "resources": {},
        "prompts": {}
    }
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


@mcp.tool()
def get_balance() -> Dict[str, Any]:
    """
    Get the current account balance for all assets on Binance.
    
    This tool retrieves the balances of all assets in the user's Binance account,
    including available and locked amounts.
    
    Returns:
        Dictionary containing success status, asset balances, and metadata.
    """
    logger.info("Tool called: get_balance")
    
    try:
        from binance_mcp_server.tools.get_balance import get_balance as _get_balance
        result = _get_balance()
        
        if result.get("success"):
            logger.info("Successfully fetched account balances")
        else:
            logger.warning(f"Failed to fetch account balances: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_balance tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_orders(symbol: str, start_time: Optional[int] = None, end_time: Optional[int] = None) -> Dict[str, Any]:
    """
    Get all orders for a specific trading symbol on Binance.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')
        start_time: Optional start time for filtering orders (Unix timestamp)
        end_time: Optional end time for filtering orders (Unix timestamp)
        
    Returns:
        Dictionary containing success status, order data, and metadata.
    """
    logger.info(f"Tool called: get_orders with symbol={symbol}, start_time={start_time}, end_time={end_time}")
    
    try:
        from binance_mcp_server.tools.get_orders import get_orders as _get_orders
        result = _get_orders(symbol, start_time=start_time, end_time=end_time)

        if result.get("success"):
            logger.info(f"Successfully fetched orders for {symbol}")
        else:
            logger.warning(f"Failed to fetch orders for {symbol}: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_orders tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_position_info() -> Dict[str, Any]:
    """
    Get the current position information for the user on Binance.
    
    This tool retrieves the user's current positions in futures trading.
    
    Returns:
        Dictionary containing success status, position data, and metadata.
    """
    logger.info("Tool called: get_position_info")
    
    try:
        from binance_mcp_server.tools.get_position_info import get_position_info as _get_position_info
        result = _get_position_info()
        
        if result.get("success"):
            logger.info("Successfully fetched position info")
        else:
            logger.warning(f"Failed to fetch position info: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_position_info tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_pnl() -> Dict[str, Any]:
    """
    Get the current profit and loss (PnL) information for the user on Binance.
    
    This tool retrieves the user's PnL data for futures trading.
    
    Returns:
        Dictionary containing success status, PnL data, and metadata.
    """
    logger.info("Tool called: get_pnl")
    
    try:
        from binance_mcp_server.tools.get_pnl import get_pnl as _get_pnl
        result = _get_pnl()
        
        if result.get("success"):
            logger.info("Successfully fetched PnL info")
        else:
            logger.warning(f"Failed to fetch PnL info: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_pnl tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def create_order(
    symbol: str,
    side: OrderSide,
    order_type: OrderType,
    quantity: float,
    price: Optional[float] = None,
) -> Dict[str, Any]:
    """
    Create a new order on Binance.
    
    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT').
        side: Order side ('BUY' or 'SELL').
        order_type: Type of order ('LIMIT', 'MARKET', etc.).
        quantity: Quantity of the asset to buy/sell.
        price: Price for limit orders (optional).
        
    Returns:
        Dictionary containing success status and order data.
    """
    logger.info(f"Tool called: create_order with symbol={symbol}, side={side}, type={order_type}, quantity={quantity}, price={price}")
    
    try:
        from binance_mcp_server.tools.create_order import create_order as _create_order
        result = _create_order(symbol, side, order_type, quantity, price)
        
        if result.get("success"):
            logger.info(f"Successfully created order for {symbol}")
        else:
            logger.warning(f"Failed to create order for {symbol}: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in create_order tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


def validate_configuration() -> bool:
    """
    Validate server configuration and dependencies.
    
    Returns:
        bool: True if configuration is valid, False otherwise
    """
    try:
        from binance_mcp_server.config import BinanceConfig
        
        config = BinanceConfig()
        if not config.is_valid():
            logger.error("Invalid Binance configuration:")
            for error in config.get_validation_errors():
                logger.error(f"  • {error}")
            return False
            
        logger.info(f"Configuration validated successfully (testnet: {config.testnet})")
        return True
        
    except ImportError as e:
        logger.error(f"Failed to import configuration module: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Configuration validation failed: {str(e)}")
        return False


def main() -> None:
    """
    Main entry point for the Binance MCP Server.
    
    Handles argument parsing, configuration validation, and server startup
    with proper error handling and exit codes.
    
    Exit Codes:
        0: Successful execution or user interruption
        1: Configuration error or validation failure
        84: Server startup or runtime error
    """
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Binance MCP Server - Model Context Protocol server for Binance API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
            %(prog)s                           # Start with STDIO transport (default)
            %(prog)s --transport streamable-http          # Start with streamable-http transport for testing
            %(prog)s --transport sse --port 8080 --host 0.0.0.0  # Custom SSE configuration
        """
    )
    
    parser.add_argument(
        "--transport", 
        choices=["stdio", "streamable-http", "sse"], 
        default="stdio",
        help="Transport method to use (stdio for MCP clients, streamable-http/sse for testing)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port for HTTP transport (default: 8000)"
    )
    parser.add_argument(
        "--host", 
        type=str, 
        default="localhost",
        help="Host for HTTP transport (default: localhost)"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    # Configure logging level based on argument
    logging.getLogger().setLevel(getattr(logging, args.log_level))
    
    
    logger.info(f"Starting Binance MCP Server with {args.transport} transport")
    logger.info(f"Log level set to: {args.log_level}")
    
    
    # Validate configuration before starting server
    if not validate_configuration():
        logger.error("Configuration validation failed. Please check your environment variables.")
        logger.error("Required: BINANCE_API_KEY, BINANCE_API_SECRET")
        logger.error("Optional: BINANCE_TESTNET (true/false)")
        sys.exit(84)
    
    
    if args.transport in ["streamable-http", "sse"]:
        logger.info(f"HTTP server will start on {args.host}:{args.port}")
        logger.info("HTTP mode is primarily for testing. Use STDIO for MCP clients.")
    else:
        logger.info("STDIO mode: Ready for MCP client connections")
    
    try:
        if args.transport == "stdio":
            logger.info("Initializing STDIO transport...")
            mcp.run(transport="stdio")
        else:
            logger.info(f"Initializing {args.transport} transport on {args.host}:{args.port}")
            mcp.run(transport=args.transport, port=args.port, host=args.host)

    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user (Ctrl+C)")
        sys.exit(0)

    except ImportError as e:
        logger.error(f"Missing required dependencies: {str(e)}")
        logger.error("Please ensure all required packages are installed")
        sys.exit(84)

    except OSError as e:
        if "Address already in use" in str(e):
            logger.error(f"Port {args.port} is already in use. Please choose a different port.")
            sys.exit(84)
        else:
            logger.error(f"Network error during server startup: {str(e)}")
            sys.exit(84)

    except Exception as e:
        logger.error(f"Server startup failed with unexpected error: {str(e)}")
        logger.error("This is likely a configuration or environment issue")
        sys.exit(84)


if __name__ == "__main__":
    main()