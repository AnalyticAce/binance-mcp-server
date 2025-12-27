# Binance MCP Server 🚀

[![PyPI version](https://img.shields.io/pypi/v/binance-mcp-server.svg?style=flat&color=blue)](https://pypi.org/project/binance-mcp-server/)
[![Cursor Store](https://img.shields.io/badge/Cursor%20Store-Available-blueviolet.svg)](https://www.cursor.store/mcp/AnalyticAce/BinanceMCPServer)
[![Documentation Status](https://github.com/AnalyticAce/binance-mcp-server/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/AnalyticAce/binance-mcp-server/actions/workflows/deploy-docs.yml)
[![PyPI Deployement Status](https://github.com/AnalyticAce/binance-mcp-server/actions/workflows/publish-package.yml/badge.svg)](https://github.com/AnalyticAce/binance-mcp-server/actions/workflows/publish-package.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful **Model Context Protocol (MCP) server** that enables AI agents to interact seamlessly with the **Binance cryptocurrency exchange**. This server provides a comprehensive suite of trading tools, market data access, and account management capabilities through the standardized MCP interface.

## 🌟 What is this?

This tool acts as a bridge between **AI Assistants** (like Claude, Cursor AI, or ChatGPT) and your **Binance Account**.

Instead of manually navigating the Binance website or app, you can ask your AI to:

* "Check the current price of Bitcoin"
* "Show me my account balance"
* "Buy 0.1 ETH at the current market price"

The AI sends the request to this server, which securely executes it on Binance and returns the result to your AI.

## 🚀 Quick Start

### 1️⃣ Installation

The easiest way to install is using `pip`:

```bash
pip install binance-mcp-server
```

### 2️⃣ Configuration

You need your **Binance API Keys** to allow this tool to access your account.

1. Log in to your Binance account and go to **API Management**.
2. Create a new API Key.
3. Set the keys as environment variables in your terminal:

```bash
# Required: Your Binance API credentials
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"

# Recommended: Use testnet for development and safe testing
export BINANCE_TESTNET="true"
```

### 3️⃣ Running with your AI

#### Configure for Claude Desktop / VSCode / Cursor

Add the following to your MCP settings configuration file (e.g., `claude_desktop_config.json` or `mcp_config.json`):

```json
{
  "mcpServers": {
    "binance": {
      "command": "binance-mcp-server",
      "args": [
        "--api-key", "your_api_key",
        "--api-secret", "your_secret",
        "--binance-testnet"
      ]
    }
  }
}
```

## 🎯 Key Capabilities

* **Real-time Market Data**: Get live prices, order books, and ticker stats.
* **Account Management**: specific Check balances and account status.
* **Trading Operations**: Place buy/sell orders (Market, Limit, etc.).
* **Portfolio Tracking**: Monitor open positions and Profit/Loss (PnL).

## 📚 Technical Reference

### Available Tools

<details>
<summary><strong>Click to expand full list of tools</strong></summary>

#### 🏦 Account & Portfolio Management

| Tool | Purpose |
|------|---------|
| `get_balance` | Retrieve account balances for all assets |
| `get_account_snapshot` | Point-in-time account state snapshot |
| `get_fee_info` | Trading fee rates (maker/taker commissions) |
| `get_available_assets` | List all tradable cryptocurrencies |

#### 📊 Market Data & Analysis

| Tool | Purpose |
|------|---------|
| `get_ticker_price` | Current price for a trading symbol |
| `get_ticker` | 24-hour ticker price change statistics |
| `get_order_book` | Current order book (bids/asks) |

#### 💱 Trading Operations

| Tool | Purpose |
|------|---------|
| `create_order` | Create buy/sell orders (market, limit, etc.) |
| `get_orders` | List order history for a specific symbol |

#### 📈 Performance & Analytics

| Tool | Purpose |
|------|---------|
| `get_pnl` | Calculate profit and loss for futures trading |
| `get_position_info` | Open futures positions details |

#### 🏪 Wallet & Transfers

| Tool | Purpose |
|------|---------|
| `get_deposit_address` | Get deposit address for a specific coin |
| `get_deposit_history` | Deposit history for a specific coin |
| `get_withdraw_history` | Withdrawal history for a specific coin |

#### 🛡️ Risk Management

| Tool | Purpose |
|------|---------|
| `get_liquidation_history` | Past liquidation events for futures |

</details>

### Configuration Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BINANCE_API_KEY` | Your Binance API key | ✅ | - |
| `BINANCE_API_SECRET` | Your Binance API secret | ✅ | - |
| `BINANCE_TESTNET` | Use testnet environment | ❌ | `false` |

## 🛠️ Development & Contributing

We welcome contributions! If you are a developer looking to improve this project:

1. **Clone the repo**: `git clone https://github.com/AnalyticAce/binance-mcp-server.git`
2. **Install dev dependencies**: `uv install --dev` or `pip install -e .[dev]`
3. **Run tests**: `pytest`

See [CONTRIBUTING.md](docs/contributing.md) for detailed guidelines.

## 📄 License & Disclaimer

**License**: MIT

**Disclaimer**: This software is for educational purposes. Cryptocurrency trading involves financial risk. **Always use the Binance Testnet** for testing and development. The developers are not responsible for any financial losses.
