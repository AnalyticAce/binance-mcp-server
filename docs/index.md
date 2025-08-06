# Binance MCP Server Documentation

Welcome to the comprehensive documentation for the **Binance MCP Server** - a powerful Model Context Protocol server that enables AI agents to interact seamlessly with the Binance cryptocurrency exchange.

## Overview

The Binance MCP Server provides a standardized interface for AI agents to access Binance's trading and market data APIs through the Model Context Protocol (MCP). Built with [FastMCP](https://fastmcp.io/), it offers 17 robust tools for cryptocurrency trading, portfolio management, and market analysis.

## Key Features

🔐 **Secure API Integration**
- Robust authentication with Binance API keys
- Support for both production and testnet environments
- Built-in rate limiting to respect Binance API limits

📊 **Comprehensive Market Data**
- Real-time price feeds and ticker information
- Order book data with customizable depth
- 24-hour trading statistics

💼 **Portfolio Management**
- Account balance tracking across all assets
- Position monitoring for futures trading
- Profit and loss (P&L) analysis

⚡ **Trading Operations**
- Create and manage orders (market, limit, stop orders)
- Order history and status tracking
- Fee information and calculations

🏦 **Account Management**
- Deposit and withdrawal history
- Account snapshots and reporting
- Liquidation history tracking

## Quick Navigation

- **[Setup Guide](setup.md)** - Get started with installation and configuration
- **[API Reference](api-reference.md)** - Complete documentation of all 17 tools
- **[Architecture](architecture.md)** - Technical overview of the server design
- **[Examples](examples.md)** - Practical usage examples
- **[Configuration](configuration.md)** - Environment setup and configuration options
- **[Contributing](contributing.md)** - Guidelines for contributors

## Getting Started

### Quick Installation

```bash
# Install from PyPI (recommended)
pip install binance-mcp-server
```

### Basic Usage

1. **Install the package**: `pip install binance-mcp-server`
2. **Configure your API keys**: Set `BINANCE_API_KEY` and `BINANCE_API_SECRET`
3. **Run the server**: `binance-mcp-server`
4. **Connect your MCP client**: Use STDIO transport to connect

### Why Choose the PyPI Package?

- 🎯 **Always Latest**: Automatically get the latest stable releases
- 🛡️ **Reliable**: Thoroughly tested releases with version management  
- ⚡ **Simple**: One command installation and updates
- 🔧 **Maintained**: Regular updates and security patches

## Support

- 📖 [Full Documentation](https://analyticace.github.io/BinanceMCPServer/)
- 🐛 [Issues & Bug Reports](https://github.com/AnalyticAce/BinanceMCPServer/issues)
- 💬 [Discussions](https://github.com/AnalyticAce/BinanceMCPServer/discussions)

---

*Built with ❤️ using [FastMCP](https://fastmcp.io/) and the [python-binance](https://python-binance.readthedocs.io/) library.*