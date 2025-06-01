"""
Command Line Interface for the Binance MCP Server.

This module provides a CLI for starting the Binance MCP server with various
configuration options including API credentials and testnet mode.
"""

import os
import typer
from dotenv import load_dotenv
from binance_mcp_server import mcp

app = typer.Typer(
    add_completion=True,
    help="Binance MCP Server - Model Context Protocol server for Binance API"
)


@app.command()
def binance_mcp_server(
    api_key: str = typer.Option(
        "", 
        "--api-key", 
        "-k", 
        help="Binance API key", 
        prompt=True, 
        envvar="BINANCE_API_KEY"
    ),
    api_secret: str = typer.Option(
        "", 
        "--api-secret", 
        "-s", 
        help="Binance API secret", 
        prompt=True, 
        envvar="BINANCE_API_SECRET"
    ),
    binance_testnet: bool = typer.Option(
        False, 
        "--binance-testnet", 
        "-t", 
        help="Use Binance testnet", 
        envvar="BINANCE_TESTNET"
    )
) -> None:
    """
    Start the Binance MCP server with the specified configuration.
    
    Args:
        api_key: Binance API key for authentication
        api_secret: Binance API secret for authentication  
        binance_testnet: Whether to use Binance testnet instead of production
    """
    load_dotenv()

    os.environ["BINANCE_API_KEY"] = api_key
    os.environ["BINANCE_API_SECRET"] = api_secret
    os.environ["BINANCE_TESTNET"] = str(binance_testnet).lower()
    
    typer.echo(f"Starting Binance MCP Server...")
    typer.echo(f"Testnet mode: {binance_testnet}")

    mcp.run(transport="stdio")


if __name__ == "__main__":
    app()