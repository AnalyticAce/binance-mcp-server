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

Install the official package from [PyPI](https://pypi.org/project/binance-mcp-server/):

```bash
# Recommended: Install using pip
pip install binance-mcp-server

# Alternative: Using uv for faster package management
uv add binance-mcp-server
```

> 💡 **Why use the PyPI package?**
> - ✅ Always up-to-date with latest releases
> - ✅ Automatic dependency management
> - ✅ Simple installation and updates
> - ✅ No need to clone repositories or manage source code

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
# Start the MCP server (after installing from PyPI)
# By default the server runs in READ-ONLY mode (trading disabled)
binance-mcp-server --api-key $BINANCE_API_KEY --api-secret $BINANCE_API_SECRET --binance-testnet --read-only

# To enable trading tools explicitly, pass --enable-trading (recommended only on testnet)
# binance-mcp-server --api-key $BINANCE_API_KEY --api-secret $BINANCE_API_SECRET --binance-testnet --enable-trading

## Capabilities & Environment

- Trading (state-changing):
  - Default: disabled
  - Enable via CLI `--enable-trading` or env `BINANCE_MCP_ENABLE_TRADING=true`
  - `BINANCE_MCP_READ_ONLY=true` will always disable trading

- Wallet (sensitive account info like deposit/withdraw endpoints):
  - Default: disabled
  - Enable via env `BINANCE_MCP_ENABLE_WALLET=true`

- Account (balances, positions, PnL):
  - Default: enabled
  - Can be disabled via env `BINANCE_MCP_ENABLE_ACCOUNT=false`

## Rate Limiting

- Weighted token-bucket aligned with Binance weights (approximate).
- Depth endpoint cost scales with `limit` (2..50).
- Configure capacity via env: `BINANCE_WEIGHT_LIMIT_PER_MINUTE` (future), current default ~1200/min.

## Symbol Validation (optional)

- Enable existence checks with `BINANCE_MCP_VALIDATE_SYMBOL_EXISTS=true` (uses cached exchange info, TTL 15m).
```

### 4️⃣ Connect Your AI Agent

Configure your AI agent (Claude, GPT-4, or custom bot) to connect to the MCP server:

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
## 📚 Available Tools

Our MCP server provides **15 comprehensive trading tools** that enable AI agents to perform cryptocurrency trading operations. Each tool follows the Model Context Protocol standard for seamless integration.

### 🏦 Account & Portfolio Management
| Tool | Purpose |
|------|---------|
| `get_balance` | Retrieve account balances for all assets |
| `get_account_snapshot` | Point-in-time account state snapshot |
| `get_fee_info` | Trading fee rates (maker/taker commissions) for symbols |
| `get_available_assets` | List all tradable cryptocurrencies and exchange info |

### 📊 Market Data & Analysis  
| Tool | Purpose |
|------|---------|
| `get_ticker_price` | Current price for a trading symbol |
| `get_ticker` | 24-hour ticker price change statistics |
| `get_order_book` | Current order book (bids/asks) for a symbol |

### 💱 Trading Operations
| Tool | Purpose |
|------|---------|
| `create_order` | Create buy/sell orders (market, limit, etc.) |
| `get_orders` | List order history for a specific symbol |

### 📈 Performance & Analytics
| Tool | Purpose |
|------|---------|
| `get_pnl` | Calculate profit and loss for futures trading |
| `get_position_info` | Open futures positions details |

### 🏪 Wallet & Transfers
| Tool | Purpose |
|------|---------|
| `get_deposit_address` | Get deposit address for a specific coin |
| `get_deposit_history` | Deposit history for a specific coin |
| `get_withdraw_history` | Withdrawal history for a specific coin |

### 🛡️ Risk Management
| Tool | Purpose |
|------|---------|
| `get_liquidation_history` | Past liquidation events for futures trading |


## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `BINANCE_API_KEY` | Your Binance API key | ✅ | - |
| `BINANCE_API_SECRET` | Your Binance API secret | ✅ | - |
| `BINANCE_TESTNET` | Use testnet environment | ❌ | `false` |


## 🛠️ Development

> 📝 **Note**: This section is for contributors and developers who want to modify the source code. Regular users should install from PyPI using the instructions above.

### Development Environment Setup

```bash
# 1. Clone the repository
git clone https://github.com/AnalyticAce/binance-mcp-server.git
cd binance-mcp-server

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install development dependencies (choose one)
# Option A: Using uv (if available)
uv install --dev

# Option B: Using pip
pip install -e .
pip install pytest  # for testing

# 4. Set up pre-commit hooks (optional)
pip install pre-commit
pre-commit install --hook-type commit-msg

# 5. Run tests to verify setup
pytest

# 6. Start development server
python -m binance_mcp_server.cli
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

- [ ] **Enhanced Trading Tools** - Order cancellation, modification, and advanced order types
- [ ] **Portfolio Management** - Advanced portfolio analytics and asset allocation tools  
- [ ] **Risk Management Extensions** - Margin monitoring, leverage management, and liquidation alerts
- [ ] **Market Data Enhancements** - Historical data, technical indicators, and market analysis
- [ ] **Alert System** - Price notifications and position monitoring
- [ ] **Documentation & Examples** - Comprehensive guides and use case examples

### 📋 Contribution Guidelines

1. **Fork & Branch**: Create a feature branch from `main`
2. **Code**: Follow our [coding standards](docs/contributing.md)
3. **Pre-commit Hooks**: Install and configure pre-commit hooks for commit message validation
4. **Test**: Add tests for new features (aim for >80% coverage)
5. **Document**: Update documentation for user-facing changes
6. **Review**: Submit a pull request for review

### 🔧 Development Setup for Contributors

> 💡 **For Regular Use**: Most users should install via `pip install binance-mcp-server` instead of cloning this repository.

```bash
# Clone your fork
git clone https://github.com/your-username/binance-mcp-server.git
cd binance-mcp-server

# Install dependencies and set up environment (choose one)
# Option A: Using uv (if available)
uv install --dev

# Option B: Using pip
pip install -e .
pip install pytest pre-commit

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

### 📋 Development Standards

- **MCP Protocol Compliance**: Full adherence to Model Context Protocol standards
- **Pre-commit Hooks**: Required for all contributors to ensure commit message consistency
- **Type Hints**: Full type annotations required
- **Testing**: pytest with >80% coverage target
- **Commits**: Conventional commit format (`feat:`, `fix:`, etc.) enforced by pre-commit hooks
- **Documentation**: Google-style docstrings
- **Security**: Comprehensive input validation and secure error handling

## 🔒 Security & Best Practices

### 🛡️ MCP Protocol Compliance

This server implements comprehensive security measures following Model Context Protocol best practices:

- **Enhanced Input Validation**: All inputs are validated and sanitized
- **Secure Error Handling**: Error messages are sanitized to prevent information leakage  
- **Rate Limiting**: Built-in protection against API abuse
- **Credential Protection**: No sensitive data logged or exposed
- **Audit Logging**: Comprehensive security event tracking

### 🔐 API Security

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

# Optional: Configure security features
export MCP_RATE_LIMIT_ENABLED="true"
export MCP_MAX_REQUESTS_PER_MINUTE="60"
```

📖 **[Read Full Security Documentation](docs/security.md)** - Comprehensive security guidelines and best practices.

## 💡 Usage Examples

### 📊 Market Data Queries

```python
# Get real-time Bitcoin price
{
    "name": "get_ticker_price",
    "arguments": {
        "symbol": "BTCUSDT"
    }
}

# Get 24-hour ticker statistics for Ethereum
{
    "name": "get_ticker", 
    "arguments": {
        "symbol": "ETHUSDT"
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
    "arguments": {}
}

# Get account snapshot
{
    "name": "get_account_snapshot",
    "arguments": {
        "account_type": "SPOT"
    }
}
```

### 🛒 Trading Operations

```python
# Create a limit buy order for Ethereum
{
    "name": "create_order",
    "arguments": {
        "symbol": "ETHUSDT",
        "side": "BUY", 
        "order_type": "LIMIT",
        "quantity": 0.1,
        "price": 2000.00
    }
}

# Get order history for a symbol
{
    "name": "get_orders",
    "arguments": {
        "symbol": "ETHUSDT"
    }
}
```

### 📈 Performance Analysis

```python
# Calculate profit and loss
{
    "name": "get_pnl",
    "arguments": {}
}

# Get position information
{
    "name": "get_position_info",
    "arguments": {}
}
```

## 🎯 Roadmap

### 🚀 Phase 1: Core Foundation ✅
- [x] **MCP Server Framework** - FastMCP integration and basic structure
- [x] **MCP Protocol Compliance** - Enhanced security and best practices implementation
- [x] **Documentation & Planning** - Comprehensive tool specifications
- [x] **Authentication System** - Secure Binance API integration
- [x] **Basic Tools Implementation** - Essential trading and account tools (15 tools)
- [x] **Security Features** - Input validation, error sanitization, rate limiting

### 📊 Phase 2: Trading Operations 🚧
- [x] **Order Management** - Basic order creation and history
- [x] **Market Data Integration** - Real-time price feeds and order books
- [x] **Portfolio Analytics** - Basic P&L tracking and position info
- [ ] **Advanced Order Types** - Stop-loss, take-profit, OCO orders
- [ ] **Order Cancellation** - Cancel and modify existing orders
- [ ] **Enhanced Risk Management** - Advanced margin monitoring

### 🔥 Phase 3: Advanced Features 📋
- [ ] **Advanced Analytics** - Technical indicators and market insights
- [ ] **Alert System** - Price notifications and position monitoring
- [ ] **Strategy Tools** - DCA, grid trading, and automation helpers
- [ ] **Multi-account Support** - Cross-margin, isolated margin accounts


### 📈 Success Metrics
- **Tool Coverage**: 15/15 core tools implemented ✅
- **Test Coverage**: >90% code coverage target (currently 38 tests passing)
- **Security Compliance**: MCP best practices implemented ✅
- **Performance**: <100ms average API response time
- **Community**: Growing GitHub engagement and contributions
- **Production Usage**: Stable package releases on PyPI

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
