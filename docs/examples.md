# Usage Examples

This guide provides practical examples of using the Binance MCP Server tools in various scenarios.

## Getting Started Examples

### Basic Market Data

#### Get Current Bitcoin Price
```json
{
  "tool": "get_ticker_price",
  "arguments": {
    "symbol": "BTCUSDT"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "BTCUSDT",
    "price": 42350.50
  },
  "timestamp": 1704067200000
}
```

#### Get 24-Hour Market Statistics
```json
{
  "tool": "get_ticker",
  "arguments": {
    "symbol": "ETHUSDT"
  }
}
```

**Use case**: Track daily performance, price changes, and trading volume.

## Trading Examples

### Placing Orders

#### Market Buy Order
```json
{
  "tool": "create_order",
  "arguments": {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "order_type": "MARKET",
    "quantity": 0.001
  }
}
```

**Use case**: Buy Bitcoin immediately at current market price.

#### Limit Sell Order
```json
{
  "tool": "create_order",
  "arguments": {
    "symbol": "ETHUSDT",
    "side": "SELL",
    "order_type": "LIMIT",
    "quantity": 0.5,
    "price": 2500.00
  }
}
```

**Use case**: Sell Ethereum when price reaches $2,500.

### Order Management

#### Check Order History
```json
{
  "tool": "get_orders",
  "arguments": {
    "symbol": "BTCUSDT",
    "start_time": 1704000000000,
    "end_time": 1704086400000
  }
}
```

**Use case**: Review all Bitcoin trades from the last 24 hours.

## Portfolio Management Examples

### Account Monitoring

#### Check All Balances
```json
{
  "tool": "get_balance",
  "arguments": {}
}
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "BTC": {"free": 0.12345678, "locked": 0.0},
    "ETH": {"free": 2.5, "locked": 0.5},
    "USDT": {"free": 1234.56, "locked": 100.0}
  }
}
```

**Use case**: Monitor portfolio composition and available funds.

#### Get Account Snapshot
```json
{
  "tool": "get_account_snapshot",
  "arguments": {
    "account_type": "SPOT"
  }
}
```

**Use case**: Generate portfolio reports and track account performance over time.

### Futures Trading

#### Check Positions
```json
{
  "tool": "get_position_info",
  "arguments": {}
}
```

**Use case**: Monitor open futures positions, leverage, and liquidation prices.

#### Check P&L
```json
{
  "tool": "get_pnl",
  "arguments": {}
}
```

**Use case**: Track realized and unrealized profits/losses.

## Market Analysis Examples

### Order Book Analysis

#### Get Market Depth
```json
{
  "tool": "get_order_book",
  "arguments": {
    "symbol": "BTCUSDT",
    "limit": 20
  }
}
```

**Example Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "BTCUSDT",
    "bids": [
      ["42350.00", "1.5"],
      ["42349.50", "2.1"],
      ["42349.00", "0.8"]
    ],
    "asks": [
      ["42350.50", "2.1"],
      ["42351.00", "1.8"],
      ["42351.50", "3.2"]
    ]
  }
}
```

**Use case**: Analyze market liquidity and find optimal entry/exit points.

### Trading Pair Discovery

#### List Available Assets
```json
{
  "tool": "get_available_assets",
  "arguments": {}
}
```

**Use case**: Discover new trading pairs and verify symbol formats.

## Transaction History Examples

### Deposit Tracking

#### Check Bitcoin Deposits
```json
{
  "tool": "get_deposit_history",
  "arguments": {
    "coin": "BTC"
  }
}
```

**Use case**: Verify incoming Bitcoin transfers and deposit confirmations.

#### Get Deposit Address
```json
{
  "tool": "get_deposit_address",
  "arguments": {
    "coin": "ETH"
  }
}
```

**Use case**: Generate deposit address for receiving Ethereum.

### Withdrawal Monitoring

#### Check Withdrawal Status
```json
{
  "tool": "get_withdraw_history",
  "arguments": {
    "coin": "USDT"
  }
}
```

**Use case**: Track outgoing USDT transfers and withdrawal status.

## Fee Analysis Examples

### Trading Cost Calculation

#### Get Trading Fees
```json
{
  "tool": "get_fee_info",
  "arguments": {
    "symbol": "BTCUSDT"
  }
}
```

**Example Response:**
```json
{
  "success": true,
  "data": [
    {
      "symbol": "BTCUSDT",
      "makerCommission": "0.001",
      "takerCommission": "0.001"
    }
  ]
}
```

**Use case**: Calculate trading costs and optimize order types (maker vs taker).

## Advanced Scenarios

### Automated Trading Bot

Here's an example workflow for a simple trading bot:

#### 1. Check Market Conditions
```json
{
  "tool": "get_ticker",
  "arguments": {"symbol": "BTCUSDT"}
}
```

#### 2. Analyze Order Book
```json
{
  "tool": "get_order_book", 
  "arguments": {"symbol": "BTCUSDT", "limit": 10}
}
```

#### 3. Check Available Balance
```json
{
  "tool": "get_balance",
  "arguments": {}
}
```

#### 4. Place Strategic Order
```json
{
  "tool": "create_order",
  "arguments": {
    "symbol": "BTCUSDT",
    "side": "BUY",
    "order_type": "LIMIT",
    "quantity": 0.001,
    "price": 42000.0
  }
}
```

#### 5. Monitor Order Status
```json
{
  "tool": "get_orders",
  "arguments": {"symbol": "BTCUSDT"}
}
```

### Portfolio Rebalancing

#### 1. Get Current Portfolio
```json
{
  "tool": "get_balance",
  "arguments": {}
}
```

#### 2. Check Current Prices
```json
{
  "tool": "get_ticker_price",
  "arguments": {"symbol": "BTCUSDT"}
}
```

```json
{
  "tool": "get_ticker_price", 
  "arguments": {"symbol": "ETHUSDT"}
}
```

#### 3. Calculate Rebalancing Trades
Based on portfolio percentages and current values.

#### 4. Execute Rebalancing Orders
```json
{
  "tool": "create_order",
  "arguments": {
    "symbol": "BTCUSDT",
    "side": "SELL",
    "order_type": "MARKET",
    "quantity": 0.01
  }
}
```

### Risk Management

#### 1. Monitor Futures Positions
```json
{
  "tool": "get_position_info",
  "arguments": {}
}
```

#### 2. Check Liquidation History
```json
{
  "tool": "get_liquidation_history",
  "arguments": {}
}
```

#### 3. Set Stop-Loss Orders
```json
{
  "tool": "create_order",
  "arguments": {
    "symbol": "BTCUSDT",
    "side": "SELL",
    "order_type": "STOP_LOSS_LIMIT",
    "quantity": 0.001,
    "price": 40000.0
  }
}
```

## Error Handling Examples

### Handling API Errors

```python
# Example error response
{
  "success": false,
  "error": {
    "type": "binance_api_error",
    "message": "Insufficient balance",
    "timestamp": 1704067200000
  }
}
```

**Common errors and solutions:**

1. **Insufficient Balance**
   - Check balance before placing orders
   - Adjust order quantity

2. **Invalid Symbol**
   - Verify symbol format (e.g., "BTCUSDT" not "BTC/USDT")
   - Check available assets list

3. **Rate Limit Exceeded**
   - Wait before retrying
   - Implement exponential backoff

### Validation Examples

#### Symbol Validation
```json
// ✅ Correct
{"symbol": "BTCUSDT"}

// ❌ Incorrect 
{"symbol": "BTC/USDT"}
{"symbol": "btcusdt"}
```

#### Order Side Validation
```json
// ✅ Correct
{"side": "BUY"}
{"side": "SELL"}

// ❌ Incorrect
{"side": "buy"}
{"side": "Buy"}
```

## Integration Examples

### Claude Desktop Integration

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "binance": {
      "command": "binance-mcp-server",
      "args": [],
      "env": {
        "BINANCE_API_KEY": "your_key",
        "BINANCE_API_SECRET": "your_secret",
        "BINANCE_TESTNET": "true"
      }
    }
  }
}
```

### Python Integration

```python
import requests
import json

# Start server in HTTP mode for testing
# binance-mcp-server --transport streamable-http

def call_tool(tool_name, arguments):
    url = "http://localhost:8000/call"
    payload = {
        "tool": tool_name,
        "arguments": arguments
    }
    response = requests.post(url, json=payload)
    return response.json()

# Get Bitcoin price
result = call_tool("get_ticker_price", {"symbol": "BTCUSDT"})
if result["success"]:
    print(f"BTC Price: ${result['data']['price']}")
```

### cURL Examples

```bash
# Get current price
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_ticker_price", "arguments": {"symbol": "BTCUSDT"}}'

# Check balance
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_balance", "arguments": {}}'

# Place order
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "create_order",
    "arguments": {
      "symbol": "BTCUSDT",
      "side": "BUY", 
      "order_type": "LIMIT",
      "quantity": 0.001,
      "price": 42000.0
    }
  }'
```

## Best Practices

### 1. Always Use Testnet First
```bash
export BINANCE_TESTNET="true"
```

### 2. Check Success Before Processing
```python
if result["success"]:
    data = result["data"]
    # Process data
else:
    error = result["error"]
    # Handle error
```

### 3. Implement Retry Logic
```python
import time

def retry_tool_call(tool_name, arguments, max_retries=3):
    for attempt in range(max_retries):
        result = call_tool(tool_name, arguments)
        
        if result["success"]:
            return result
            
        if result["error"]["type"] == "rate_limit_exceeded":
            time.sleep(2 ** attempt)  # Exponential backoff
            continue
            
        return result  # Non-retryable error
```

### 4. Validate Inputs
```python
def validate_symbol(symbol):
    if not symbol or len(symbol) < 3:
        raise ValueError("Invalid symbol")
    return symbol.upper()
```

### 5. Monitor Rate Limits
- Don't exceed 1200 requests per minute
- Implement request queuing for high-frequency applications
- Use rate limit headers if available

These examples provide a comprehensive foundation for building cryptocurrency trading applications, portfolio management tools, and market analysis systems using the Binance MCP Server.