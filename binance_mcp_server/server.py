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
from binance_mcp_server.security import SecurityConfig, validate_api_credentials, security_audit_log


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)


logger = logging.getLogger(__name__)


mcp = FastMCP(
    name="binance-mcp-server",
    version="1.2.7",  # Updated to match pyproject.toml
    instructions="""
    This server provides secure access to Binance cryptocurrency exchange functionality following MCP best practices.
    
    SECURITY FEATURES:
    - Rate limiting to prevent abuse
    - Input validation and sanitization
    - Secure error handling without information leakage
    - Comprehensive audit logging
    - Credential protection
    
    AVAILABLE TOOLS:
    
    Market Data:
    - get_ticker_price: Get current price for a trading symbol
    - get_ticker: Get 24-hour price statistics for a symbol  
    - get_order_book: Get current order book (bids/asks) for a trading symbol
    - get_available_assets: Get exchange trading rules and symbol information
    - get_fee_info: Get trading fee rates (maker/taker commissions) for symbols
    
    Account Management:
    - get_balance: Get account balances for all assets
    - get_account_snapshot: Get account snapshot data
    
    Trading Operations:
    - create_order: Create new trading orders (with enhanced validation)
    - get_orders: Get order history for a specific symbol
    
    Portfolio & Analytics:
    - get_position_info: Get current futures position information
    - get_pnl: Get profit and loss information
    
    Wallet Operations:
    - get_deposit_address: Get deposit address for a specific coin
    - get_deposit_history: Get deposit history for a specific coin
    - get_withdraw_history: Get withdrawal history for a specific coin
    
    Risk Management:
    - get_liquidation_history: Get liquidation history for futures trading
    
    All operations implement:
    - Comprehensive input validation
    - Rate limiting to respect Binance API limits
    - Secure error handling
    - Audit logging for security monitoring
    - Proper configuration management
    
    Tools are implemented in dedicated modules following security best practices.
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
    side: str,
    order_type: str,
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


@mcp.tool()
def get_liquidation_history() -> Dict[str, Any]:
    """
    Get the liquidation history on Binance account.
    
    This tool retrieves the user's liquidation orders in futures trading.
    
    Returns:
        Dictionary containing success status and liquidation history data.
    """
    logger.info("Tool called: get_liquidation_history")
    
    try:
        from binance_mcp_server.tools.get_liquidation_history import get_liquidation_history as _get_liquidation_history
        result = _get_liquidation_history()
        
        if result.get("success"):
            logger.info("Successfully fetched liquidation history")
        else:
            logger.warning(f"Failed to fetch liquidation history: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_liquidation_history tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }

@mcp.tool()
def get_deposit_address(coin: str) -> Dict[str, Any]:
    """
    Get the deposit address for a specific coin on the user's Binance account.
    
    Args:
        coin (str): The coin for which to fetch the deposit address.
        
    Returns:
        Dictionary containing success status and deposit address data.
    """
    logger.info(f"Tool called: get_deposit_address with coin={coin}")
    
    try:
        from binance_mcp_server.tools.get_deposit_address import get_deposit_address as _get_deposit_address
        result = _get_deposit_address(coin)
        
        if result.get("success"):
            logger.info(f"Successfully fetched deposit address for {coin}")
        else:
            logger.warning(f"Failed to fetch deposit address for {coin}: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_deposit_address tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_deposit_history(coin: str) -> Dict[str, Any]:
    """
    Get the deposit history for a specific coin on the user's Binance account.
    
    Args:
        coin (str): The coin for which to fetch the deposit history.
        
    Returns:
        Dictionary containing success status and deposit history data.
    """
    logger.info(f"Tool called: get_deposit_history with coin={coin}")
    
    try:
        from binance_mcp_server.tools.get_deposit_history import get_deposit_history as _get_deposit_history
        result = _get_deposit_history(coin)
        
        if result.get("success"):
            logger.info(f"Successfully fetched deposit history for {coin}")
        else:
            logger.warning(f"Failed to fetch deposit history for {coin}: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_deposit_history tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_withdraw_history(coin: str) -> Dict[str, Any]:
    """
    Get the withdrawal history for the user's Binance account.
    
    Args:
        coin (Optional[str]): The coin for which to fetch the withdrawal history. Defaults to 'BTC'.
        
    Returns:
        Dictionary containing success status and withdrawal history data.
    """
    logger.info(f"Tool called: get_withdraw_history with coin={coin}")
    
    try:
        from binance_mcp_server.tools.get_withdraw_history import get_withdraw_history as _get_withdraw_history
        result = _get_withdraw_history(coin)
        
        if result.get("success"):
            logger.info(f"Successfully fetched withdrawal history for {coin}")
        else:
            logger.warning(f"Failed to fetch withdrawal history for {coin}: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_withdraw_history tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_account_snapshot(account_type: str = "SPOT") -> Dict[str, Any]:
    """
    Get the account snapshot for the user's Binance account.
    
    Args:
        account_type (str): The account type to filter the snapshot. Defaults to "SPOT".
        
    Returns:
        Dictionary containing success status and account snapshot data.
    """
    logger.info(f"Tool called: get_account_snapshot with account_type={account_type}")
    
    try:
        from binance_mcp_server.tools.get_account_snapshot import get_account_snapshot as _get_account_snapshot
        result = _get_account_snapshot(account_type)
        
        if result.get("success"):
            logger.info(f"Successfully fetched account snapshot for {account_type} account")
        else:
            logger.warning(f"Failed to fetch account snapshot for {account_type}: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_account_snapshot tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_fee_info(symbol: Optional[str] = None) -> Dict[str, Any]:
    """
    Get trading fee information for symbols on Binance.
    
    This tool retrieves trading fee rates including maker and taker commissions
    for spot trading. Fee information is essential for calculating trading costs
    and optimizing trading strategies.
    
    Args:
        symbol (Optional[str]): Specific trading pair symbol to get fees for.
                               If not provided, returns fees for all symbols.
                               Format: 'BTCUSDT', 'ETHUSDT', etc.
        
    Returns:
        Dictionary containing success status, fee data, and metadata.
    """
    logger.info(f"Tool called: get_fee_info with symbol={symbol}")
    
    try:
        from binance_mcp_server.tools.get_fee_info import get_fee_info as _get_fee_info
        result = _get_fee_info(symbol)
        
        if result.get("success"):
            fee_count = len(result.get("data", []))
            logger.info(f"Successfully fetched fee information for {fee_count} symbol(s)")
        else:
            logger.warning(f"Failed to fetch fee information: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_fee_info tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }


@mcp.tool()
def get_order_book(symbol: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Get the current order book (bids/asks) for a trading symbol on Binance.
    
    This tool fetches real-time order book data for any valid trading pair available
    on Binance. The order book contains arrays of bid and ask orders with their prices
    and quantities, essential for trading/finance operations.
    
    Args:
        symbol: Trading pair symbol in format BASEQUOTE (e.g., 'BTCUSDT', 'ETHBTC')
        limit: Optional limit for number of orders per side (default: 100, max: 5000)
        
    Returns:
        Dictionary containing success status, order book data, and metadata.
    """
    logger.info(f"Tool called: get_order_book with symbol={symbol}, limit={limit}")
    
    try:
        from binance_mcp_server.tools.get_order_book import get_order_book as _get_order_book
        result = _get_order_book(symbol, limit)
        
        if result.get("success"):
            data = result.get("data", {})
            bid_count = data.get("bidCount", 0)
            ask_count = data.get("askCount", 0)
            logger.info(f"Successfully fetched order book for {symbol}: {bid_count} bids, {ask_count} asks")
        else:
            logger.warning(f"Failed to fetch order book for {symbol}: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_order_book tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }



def validate_configuration() -> bool:
    """
    Validate server configuration and dependencies with security checks.
    
    Returns:
        bool: True if configuration is valid and secure, False otherwise
    """
    try:
        from binance_mcp_server.config import BinanceConfig
        from binance_mcp_server.security import SecurityConfig, validate_api_credentials
        
        # Validate basic configuration
        config = BinanceConfig()
        if not config.is_valid():
            logger.error("Invalid Binance configuration:")
            for error in config.get_validation_errors():
                logger.error(f"  • {error}")
            return False
        
        # Validate API credentials security
        if not validate_api_credentials():
            logger.error("API credentials validation failed")
            return False
        
        # Validate security configuration
        security_config = SecurityConfig()
        if not security_config.is_secure():
            logger.warning("Security configuration warnings:")
            for warning in security_config.get_security_warnings():
                logger.warning(f"  • {warning}")
            # Don't fail on security warnings, just log them
        
        # Log successful validation with security audit
        security_audit_log(
            "configuration_validated",
            {
                "testnet": config.testnet,
                "security_enabled": security_config.is_secure()
            }
        )
        
        logger.info(f"Configuration validated successfully (testnet: {config.testnet})")
        logger.info(f"Security features enabled: {security_config.is_secure()}")
        return True
        
    except ImportError as e:
        logger.error(f"Failed to import configuration module: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Configuration validation failed: {str(e)}")
        security_audit_log(
            "configuration_validation_failed",
            {"error": str(e)},
            level="ERROR"
        )
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