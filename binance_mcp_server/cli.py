"""
Command Line Interface for the Binance MCP Server.

This module provides a CLI for starting the Binance MCP server with various
configuration options including API credentials, testnet mode, and transport methods.
"""

import os
import typer
from typing import Optional
from enum import Enum
from dotenv import load_dotenv
from binance_mcp_server import mcp
from binance_mcp_server.config import BinanceConfig


class TransportType(str, Enum):
    """Available transport types for the MCP server."""
    stdio = "stdio"
    streamable_http = "streamable-http"
    sse = "sse"


app = typer.Typer(
    add_completion=True,
    help="Binance MCP Server - Model Context Protocol server for Binance API"
)


@app.command()
def binance_mcp_server(
    api_key: Optional[str] = typer.Option(
        None, 
        "--api-key", 
        "-k", 
        help="Binance API key (can also be set via BINANCE_API_KEY env var)", 
        envvar="BINANCE_API_KEY"
    ),
    api_secret: Optional[str] = typer.Option(
        None, 
        "--api-secret", 
        "-s", 
        help="Binance API secret (can also be set via BINANCE_API_SECRET env var)", 
        envvar="BINANCE_API_SECRET"
    ),
    binance_testnet: bool = typer.Option(
        False, 
        "--binance-testnet", 
        "-t", 
        help="Use Binance testnet environment", 
        envvar="BINANCE_TESTNET"
    ),
    transport: TransportType = typer.Option(
        TransportType.stdio,
        "--transport",
        help="Transport method to use (stdio, streamable-http, or sse)"
    ),
    port: int = typer.Option(
        8000,
        "--port",
        "-p",
        help="Port for HTTP transport (only used with --transport streamable-http or sse)"
    ),
    host: str = typer.Option(
        "localhost",
        "--host",
        "-h", 
        help="Host for HTTP transport (only used with --transport streamable-http or sse)"
    )
) -> None:
    """
    Start the Binance MCP server with the specified configuration.
    This command initializes and runs the Binance MCP server using the Model Context
    Protocol. It supports STDIO, streamable-http, and SSE transports for maximum 
    compatibility with different MCP clients.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    if api_key:
        os.environ["BINANCE_API_KEY"] = api_key
    if api_secret:
        os.environ["BINANCE_API_SECRET"] = api_secret
    if binance_testnet:
        os.environ["BINANCE_TESTNET"] = str(binance_testnet).lower()
    
    # Initialize and validate configuration
    config = BinanceConfig()
    
    # Validate configuration
    if not config.is_valid():
        typer.echo("Configuration Error:", err=True)
        for error in config.get_validation_errors():
            typer.echo(f"  • {error}", err=True)
        typer.echo("\nPlease provide API credentials via:", err=True)
        typer.echo("  • Command line options: --api-key and --api-secret", err=True)
        typer.echo("  • Environment variables: BINANCE_API_KEY and BINANCE_API_SECRET", err=True)
        typer.echo("  • .env file in the current directory", err=True)
        raise typer.Exit(1)
    
    # Display configuration summary
    typer.echo("🚀 Starting Binance MCP Server...")
    typer.echo(f"📡 Transport: {transport.value.upper()}")
    typer.echo(f"🌐 Environment: {'Testnet' if config.testnet else 'Production'}")
    typer.echo(f"🔗 Base URL: {config.base_url}")
    
    if transport in [TransportType.streamable_http, TransportType.sse]:
        typer.echo(f"Server: http://{host}:{port}")
    else:
        typer.echo("STDIO mode: Ready for MCP client connections")
    
    try:
        if transport == TransportType.stdio:
            mcp.run(transport="stdio")
        else:
            mcp.run(transport=transport.value, port=port, host=host)
            
    except KeyboardInterrupt:
        typer.echo("\nServer stopped by user", err=True)
        raise typer.Exit(0)
    except Exception as e:
        typer.echo(f"\nServer error: {str(e)}", err=True)
        raise typer.Exit(1)


if __name__ == "__main__":
    app()