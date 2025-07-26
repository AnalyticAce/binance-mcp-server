# Binance MCP Server 🚀

[![PyPI version](https://img.shields.io/pypi/v/binance-mcp-server.svg?style=flat&color=blue)](https://pypi.org/project/binance-mcp-server/) 
[![Documentation Status](https://github.com/AnalyticAce/binance-mcp-server/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/AnalyticAce/binance-mcp-server/actions/workflows/deploy-docs.yml)
[![PyPI Deployement Status](https://github.com/AnalyticAce/binance-mcp-server/actions/workflows/publish-package.yml/badge.svg)](https://github.com/AnalyticAce/binance-mcp-server/actions/workflows/publish-package.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful **Model Context Protocol (MCP) server** that enables AI agents to interact seamlessly with the **Binance cryptocurrency exchange**. This server provides a comprehensive suite of trading tools, market data access, and account management capabilities through the standardized MCP interface.

## 🎯 Key Features

- **Secure Authentication**: API key-based authentication with Binance
- **Real-time Market Data**: Live price feeds, order book data, and market statistics
- **Trading Operations**: Place, modify, and cancel orders across spot and futures markets
- **Portfolio Management**: Account balance tracking, position monitoring, and P&L analysis
- **Smart Notifications**: Real-time alerts for price movements, order fills, and market events
- **Risk Management**: Built-in safeguards and validation for trading operations

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** installed on your system
- **Binance account** with API access enabled
- **API credentials** (API Key & Secret) from your Binance account

### 1️⃣ Installation

```bash
# Install using uv (recommended for Python package management)
uv add binance-mcp-server

# Alternative: Install using pip
pip install binance-mcp-server
```

### 2️⃣ Configuration

Set up your Binance API credentials as environment variables:

```bash
# Required: Your Binance API credentials
export BINANCE_API_KEY="your_api_key_here"
export BINANCE_API_SECRET="your_api_secret_here"

# Recommended: Use testnet for development and testing
export BINANCE_TESTNET="true"
```

### 3️⃣ Launch Server

```bash
# Start the MCP server
binance_mcp_server --api-key $BINANCE_API_KEY --api-secret $BINANCE_API_SECRET --binance-testnet $BINANCE_TESTNET
```

### 4️⃣ Connect Your AI Agent

Configure your AI agent (Claude, GPT-4, or custom bot) to connect to the MCP server:

```json
{
  "mcpServers": {
    "binance": {
      "command": "binance_mcp_server",
      "args": [
        "--api-key": "your_api_key",
        "--api-secret": "your_secret",
        "--binance-testnet": "false" # Set to true for testnet
      ]
    }
  }
}
```
## 📚 Available Tools

Our MCP server provides **26 comprehensive trading tools** that enable AI agents to perform advanced cryptocurrency trading operations. Each tool follows the Model Context Protocol standard for seamless integration.

### 🏦 Account & Portfolio Management
| Tool | Purpose | Alternatives |
|------|---------|-------------|
| `get_balance` | Retrieve account balances (spot, margin, futures) | `fetch_account_balance`, `account_balance_info` |
| `get_portfolio` | Fetch holdings, positions, and asset allocation | `fetch_portfolio`, `portfolio_info` |
| `get_account_snapshot` | Point-in-time account state snapshot | `fetch_account_snapshot`, `account_state` |
| `get_fee_info` | Trading, withdrawal, and funding fee rates | `fetch_fee_info`, `fee_rates` |
| `get_available_assets` | List all tradable cryptocurrencies | `fetch_available_assets`, `asset_list` |

### 📊 Market Data & Analysis  
| Tool | Purpose | Alternatives |
|------|---------|-------------|
| `get_market_data` | Real-time and historical price/volume data | `fetch_market_data`, `market_data_feed` |
| `get_ticker` | Latest price and 24h statistics | `fetch_ticker`, `ticker_info` |
| `get_order_book` | Current order book (bids/asks) | `fetch_order_book`, `orderbook_info` |
| `get_asset_price` | Current or historical asset pricing | `fetch_asset_price`, `asset_price_info` |

### 💱 Trading Operations
| Tool | Purpose | Alternatives |
|------|---------|-------------|
| `place_order` | Submit buy/sell orders (market, limit, stop) | `create_order`, `submit_order` |
| `cancel_order` | Cancel open orders by ID or symbol | `remove_order`, `revoke_order` |
| `get_order_status` | Retrieve order status and details | `fetch_order_status`, `order_info` |
| `list_orders` | List open, filled, or cancelled orders | `get_orders`, `fetch_order_list` |
| `get_trade_history` | Historical trades executed by user | `fetch_trade_history`, `trade_log` |

### 📈 Performance & Analytics
| Tool | Purpose | Alternatives |
|------|---------|-------------|
| `get_pnl` | Calculate realized/unrealized profit and loss | `fetch_pnl`, `profit_and_loss` |
| `get_position_info` | Open positions details (size, entry, liquidation) | `fetch_position_info`, `position_details` |
| `get_transaction_history` | Deposits, withdrawals, and transfers log | `fetch_transaction_history`, `transaction_log` |
| `get_dividends` | Dividend payments and history | `fetch_dividends`, `dividend_history` |

### 🛡️ Risk Management & Margins
| Tool | Purpose | Alternatives |
|------|---------|-------------|
| `get_risk_metrics` | Margin level, liquidation risk, leverage info | `fetch_risk_metrics`, `risk_info` |
| `get_funding_rates` | Futures/perpetual contract funding rates | `fetch_funding_rates`, `funding_info` |
| `get_leverage_brackets` | Allowed leverage and margin requirements | `fetch_leverage_brackets`, `leverage_info` |
| `get_margin_interest` | Interest rates and accrued interest | `fetch_margin_interest`, `margin_interest_info` |
| `get_liquidation_history` | Past liquidation events | `fetch_liquidation_history`, `liquidation_log` |
| `get_borrow_history` | Borrowed funds and repayment history | `fetch_borrow_history`, `borrow_log` |

### 🔄 Advanced Operations
| Tool | Purpose | Alternatives |
|------|---------|-------------|
| `get_asset_transfer` | Transfer assets between accounts | `fetch_asset_transfer`, `transfer_funds` |
| `get_withdrawal_status` | Check withdrawal request status | `fetch_withdrawal_status`, `withdrawal_info` |


## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BINANCE_API_KEY` | Your Binance API key | ✅ | - |
| `BINANCE_API_SECRET` | Your Binance API secret | ✅ | - |
| `BINANCE_TESTNET` | Use testnet environment | ❌ | `false` |


## 🛠️ Development

### Development Environment Setup

```bash
# 1. Clone the repository
git clone https://github.com/AnalyticAce/binance-mcp-server.git
cd binance-mcp-server

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install development dependencies
uv install --dev

# 4. Set up pre-commit hooks (required for development)
pre-commit install --hook-type commit-msg

# 5. Run tests to verify setup
pytest

# 6. Start development server with hot-reload
python -m binance_mcp_server.cli --dev --reload
```

### Testing Strategy

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=binance_mcp_server --cov-report=html

# Run specific test category
pytest tests/test_tools/test_account.py -v
```

## 🤝 Contributing

We welcome contributions from the crypto and AI development community! Here's how you can help:

### 🎯 Current Priorities

Check our [GitHub Issues](https://github.com/AnalyticAce/binance-mcp-server/issues) for the latest development priorities:

- [ ] **Account Management Tools** (#6-8) - `get_balance`, `get_portfolio`, `get_fee_info`
- [ ] **Market Data Integration** (#9-13) - Real-time data feeds and historical analysis
- [ ] **Trading Operations** (#14-18) - Order management and execution
- [ ] **Portfolio Analytics** (#19-22) - Performance tracking and risk metrics
- [ ] **Alert System** (#23-24) - Price and position monitoring
- [ ] **Risk Management** (#25-26) - Margin and liquidation safeguards

### 📋 Contribution Guidelines

1. **Fork & Branch**: Create a feature branch from `main`
2. **Code**: Follow our [coding standards](docs/contributing.md)
3. **Pre-commit Hooks**: Install and configure pre-commit hooks for commit message validation
4. **Test**: Add tests for new features (aim for >80% coverage)
5. **Document**: Update documentation for user-facing changes
6. **Review**: Submit a pull request for review

### 🔧 Development Setup for Contributors

```bash
# Clone your fork
git clone https://github.com/your-username/binance-mcp-server.git
cd binance-mcp-server

# Install dependencies and set up environment
uv install --dev

# Install pre-commit hooks (enforces commit message conventions)
pre-commit install --hook-type commit-msg

# Make your changes and commit using conventional format
git commit -m "feat(tools): add new market data tool"
```

### 🏷️ Issue Labels

- `good first issue` - Perfect for newcomers
- `enhancement` - New features and improvements  
- `bug` - Something isn't working correctly
- `documentation` - Documentation updates needed
- `help wanted` - Community assistance requested

### 📝 Development Standards

- **Pre-commit Hooks**: Required for all contributors to ensure commit message consistency
- **Type Hints**: Full type annotations required
- **Testing**: pytest with >80% coverage target
- **Commits**: Conventional commit format (`feat:`, `fix:`, etc.) enforced by pre-commit hooks
- **Documentation**: Google-style docstrings

## 🔒 Security & Best Practices

### 🛡️ API Security
- **Credential Management**: Never commit API keys to version control
- **Testnet First**: Always test with Binance testnet before live trading  
- **Rate Limiting**: Built-in respect for Binance API rate limits
- **Input Validation**: Comprehensive validation of all trading parameters
- **Audit Logging**: Complete audit trail of all operations

### 🔐 Environment Security
```bash
# Use environment variables for sensitive data
export BINANCE_API_KEY="your_key_here"
export BINANCE_API_SECRET="your_secret_here"

# Enable testnet for development
export BINANCE_TESTNET="true"
```

## 💡 Usage Examples

### 📊 Market Data Queries

```python
# Get real-time Bitcoin price and market data
{
    "name": "get_market_data",
    "arguments": {
        "symbol": "BTCUSDT",
        "interval": "1h"
    }
}

# Check current order book for Ethereum
{
    "name": "get_order_book", 
    "arguments": {
        "symbol": "ETHUSDT",
        "limit": 10
    }
}
```

### 💰 Account Management

```python
# Check account balances
{
    "name": "get_balance",
    "arguments": {
        "account_type": "spot"
    }
}

# Get portfolio overview
{
    "name": "get_portfolio",
    "arguments": {
        "include_positions": true
    }
}
```

### 🛒 Trading Operations

```python
# Place a limit buy order for Ethereum
{
    "name": "place_order",
    "arguments": {
        "symbol": "ETHUSDT",
        "side": "BUY", 
        "type": "LIMIT",
        "quantity": "0.1",
        "price": "2000.00",
        "timeInForce": "GTC"
    }
}

# Cancel an open order
{
    "name": "cancel_order",
    "arguments": {
        "symbol": "ETHUSDT", 
        "orderId": "12345678"
    }
}
```

### 📈 Performance Analysis

```python
# Calculate profit and loss
{
    "name": "get_pnl",
    "arguments": {
        "symbol": "BTCUSDT",
        "timeframe": "24h"
    }
}

# Get trading history
{
    "name": "get_trade_history",
    "arguments": {
        "symbol": "ETHUSDT",
        "limit": 50
    }
}
```

## 🎯 Roadmap

### 🚀 Phase 1: Core Foundation
- [x] **MCP Server Framework** - FastMCP integration and basic structure
- [x] **Documentation & Planning** - Comprehensive tool specifications
- [ ] **Authentication System** - Secure Binance API integration
- [ ] **Basic Tools Implementation** - Essential trading and account tools

### 📊 Phase 2: Trading Operations
- [ ] **Order Management** - Complete buy/sell order lifecycle
- [ ] **Market Data Integration** - Real-time feeds and historical data
- [ ] **Portfolio Analytics** - P&L tracking and performance metrics
- [ ] **Risk Management** - Margin monitoring and position limits

### 🔥 Phase 3: Advanced Features
- [ ] **Advanced Analytics** - Technical indicators and market insights
- [ ] **Alert System** - Price notifications and position monitoring
- [ ] **Strategy Tools** - DCA, grid trading, and automation helpers


### 📈 Success Metrics
- **Tool Coverage**: 26/26 core tools implemented ✅
- **Test Coverage**: >90% code coverage target
- **Performance**: <100ms average API response time
- **Community**: 1000+ GitHub stars, 100+ contributors
- **Production Usage**: 10,000+ monthly active installations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support & Community

### 📚 Documentation & Resources
- **[Complete Documentation](https://analyticace.github.io/binance-mcp-server/)** - Comprehensive guides and tutorials

### 💬 Get Help
- **[Report Issues](https://github.com/AnalyticAce/binance-mcp-server/issues)** - Bug reports and feature requests
- **[Discussions](https://github.com/AnalyticAce/binance-mcp-server/discussions)** - Community Q&A and ideas
- **[Email Support](mailto:dossehdosseh14@gmail.com)** - Technical questions and partnership inquiries

### 🏷️ Quick Help Tags
When creating issues, please use these labels to help us respond faster:
- `bug` - Something isn't working
- `enhancement` - Feature requests  
- `question` - General questions
- `documentation` - Docs improvements
- `good first issue` - Perfect for newcomers

---

## ⚠️ Legal Disclaimer

**Important Notice**: This software is provided for educational and development purposes only. Cryptocurrency trading involves substantial risk of financial loss. 

### 📋 Risk Acknowledgment
- **Testing Environment**: Always use Binance testnet for development and testing
- **Financial Risk**: Only trade with funds you can afford to lose
- **Due Diligence**: Conduct thorough testing before deploying to live trading
- **No Liability**: Developers assume no responsibility for financial losses

### 📄 License & Attribution

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**Built with ❤️ by the crypto development community**

---

<div align="center">

**⚡ Powered by [Model Context Protocol](https://modelcontextprotocol.io/) ⚡**

[![GitHub Stars](https://img.shields.io/github/stars/AnalyticAce/binance-mcp-server?style=social)](https://github.com/AnalyticAce/binance-mcp-server)
[![GitHub Forks](https://img.shields.io/github/forks/AnalyticAce/binance-mcp-server?style=social)](https://github.com/AnalyticAce/binance-mcp-server/fork)
[![GitHub Issues](https://img.shields.io/github/issues/AnalyticAce/binance-mcp-server)](https://github.com/AnalyticAce/binance-mcp-server/issues)

[⭐ Star this project](https://github.com/AnalyticAce/binance-mcp-server) | [🍴 Fork & Contribute](https://github.com/AnalyticAce/binance-mcp-server/fork) | [📖 Read the Docs](https://github.com/AnalyticAce/binance-mcp-server/wiki)

</div>
