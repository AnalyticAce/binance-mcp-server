# API Reference

This document provides comprehensive documentation for all 17 tools available in the Binance MCP Server.

## Response Format

All tools return a standardized response format:

### Success Response
```json
{
  "success": true,
  "data": { /* Tool-specific data */ },
  "timestamp": 1704067200000,
  "metadata": {
    "source": "binance_api",
    "endpoint": "tool_name"
  }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "type": "error_type",
    "message": "Human-readable error message",
    "timestamp": 1704067200000
  }
}
```

## Market Data Tools

### get_ticker_price

Get the current price for a trading symbol.

**Parameters:**
- `symbol` (string, required): Trading pair symbol (e.g., 'BTCUSDT', 'ETHBTC')

**Example:**
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
  "timestamp": 1704067200000,
  "metadata": {
    "source": "binance_api",
    "endpoint": "ticker_price"
  }
}
```

---

### get_ticker

Get 24-hour ticker price change statistics for a symbol.

**Parameters:**
- `symbol` (string, required): Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')

**Example:**
```json
{
  "tool": "get_ticker",
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
    "priceChange": "125.50",
    "priceChangePercent": "0.297",
    "weightedAvgPrice": "42280.15",
    "prevClosePrice": "42225.00",
    "lastPrice": "42350.50",
    "lastQty": "0.001",
    "bidPrice": "42350.00",
    "bidQty": "1.5",
    "askPrice": "42350.50",
    "askQty": "2.1",
    "openPrice": "42225.00",
    "highPrice": "42450.00",
    "lowPrice": "41800.00",
    "volume": "1234.567",
    "quoteVolume": "52234567.89",
    "openTime": 1704067200000,
    "closeTime": 1704153600000,
    "count": 123456
  },
  "timestamp": 1704067200000
}
```

---

### get_order_book

Get the current order book (bids/asks) for a trading symbol.

**Parameters:**
- `symbol` (string, required): Trading pair symbol (e.g., 'BTCUSDT', 'ETHBTC')
- `limit` (integer, optional): Number of orders per side (default: 100, max: 5000)

**Example:**
```json
{
  "tool": "get_order_book",
  "arguments": {
    "symbol": "BTCUSDT",
    "limit": 10
  }
}
```

**Response:**
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
    ],
    "bidCount": 3,
    "askCount": 3,
    "lastUpdateId": 123456789
  },
  "timestamp": 1704067200000
}
```

---

### get_available_assets

Get a list of all available trading symbols and their information.

**Parameters:**
None

**Example:**
```json
{
  "tool": "get_available_assets",
  "arguments": {}
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "assets": {
      "BTCUSDT": {
        "symbol": "BTCUSDT",
        "status": "TRADING",
        "baseAsset": "BTC",
        "baseAssetPrecision": 8,
        "quoteAsset": "USDT",
        "quotePrecision": 8,
        "quoteAssetPrecision": 8,
        "orderTypes": ["LIMIT", "LIMIT_MAKER", "MARKET", "STOP_LOSS_LIMIT", "TAKE_PROFIT_LIMIT"],
        "icebergAllowed": true,
        "ocoAllowed": true,
        "isSpotTradingAllowed": true,
        "isMarginTradingAllowed": true,
        "filters": [...]
      }
    },
    "count": 2000
  },
  "timestamp": 1704067200000
}
```

## Account Management Tools

### get_balance

Get the current account balance for all assets.

**Parameters:**
None

**Example:**
```json
{
  "tool": "get_balance",
  "arguments": {}
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "BTC": {
      "free": 0.12345678,
      "locked": 0.0
    },
    "USDT": {
      "free": 1234.56,
      "locked": 100.0
    },
    "ETH": {
      "free": 2.5,
      "locked": 0.5
    }
  },
  "timestamp": 1704067200000
}
```

---

### get_account_snapshot

Get a point-in-time snapshot of account state.

**Parameters:**
- `account_type` (string, optional): Account type (default: "SPOT", options: "SPOT", "MARGIN", "FUTURES")

**Example:**
```json
{
  "tool": "get_account_snapshot",
  "arguments": {
    "account_type": "SPOT"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "code": 200,
    "msg": "",
    "snapshotVos": [
      {
        "data": {
          "balances": [
            {
              "asset": "BTC",
              "free": "0.12345678",
              "locked": "0.00000000"
            }
          ],
          "totalAssetOfBtc": "0.12345678"
        },
        "type": "spot",
        "updateTime": 1704067200000
      }
    ]
  },
  "timestamp": 1704067200000
}
```

---

### get_position_info

Get current position information for futures trading.

**Parameters:**
None

**Example:**
```json
{
  "tool": "get_position_info",
  "arguments": {}
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "symbol": "BTCUSDT",
      "positionAmt": "0.001",
      "entryPrice": "42000.0",
      "markPrice": "42350.50",
      "unRealizedProfit": "0.3505",
      "liquidationPrice": "0",
      "leverage": "10",
      "maxNotionalValue": "25000",
      "marginType": "isolated",
      "isolatedMargin": "42.00000000",
      "isAutoAddMargin": "false",
      "positionSide": "BOTH",
      "notional": "42.3505",
      "isolatedWallet": "42.00000000",
      "updateTime": 1704067200000
    }
  ],
  "timestamp": 1704067200000
}
```

---

### get_pnl

Get profit and loss (PnL) information for futures trading.

**Parameters:**
None

**Example:**
```json
{
  "tool": "get_pnl",
  "arguments": {}
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "symbol": "BTCUSDT",
      "income": "12.34567890",
      "incomeType": "REALIZED_PNL",
      "asset": "USDT",
      "time": 1704067200000,
      "info": "BTCUSDT",
      "tranId": 9876543210,
      "tradeId": "123456789"
    }
  ],
  "timestamp": 1704067200000
}
```

## Trading Tools

### create_order

Create a new trading order.

**Parameters:**
- `symbol` (string, required): Trading pair symbol (e.g., 'BTCUSDT')
- `side` (string, required): Order side ('BUY' or 'SELL')
- `order_type` (string, required): Order type ('LIMIT', 'MARKET', 'STOP_LOSS', etc.)
- `quantity` (float, required): Quantity of the asset to buy/sell
- `price` (float, optional): Price for limit orders

**Example:**
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

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "BTCUSDT",
    "orderId": 123456789,
    "orderListId": -1,
    "clientOrderId": "abc123",
    "transactTime": 1704067200000,
    "price": "42000.00000000",
    "origQty": "0.00100000",
    "executedQty": "0.00000000",
    "cummulativeQuoteQty": "0.00000000",
    "status": "NEW",
    "timeInForce": "GTC",
    "type": "LIMIT",
    "side": "BUY",
    "fills": []
  },
  "timestamp": 1704067200000
}
```

---

### get_orders

Get order history for a specific symbol.

**Parameters:**
- `symbol` (string, required): Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')
- `start_time` (integer, optional): Start time for filtering orders (Unix timestamp in ms)
- `end_time` (integer, optional): End time for filtering orders (Unix timestamp in ms)

**Example:**
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

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "symbol": "BTCUSDT",
      "orderId": 123456789,
      "orderListId": -1,
      "clientOrderId": "abc123",
      "price": "42000.00000000",
      "origQty": "0.00100000",
      "executedQty": "0.00100000",
      "cummulativeQuoteQty": "42.00000000",
      "status": "FILLED",
      "timeInForce": "GTC",
      "type": "LIMIT",
      "side": "BUY",
      "stopPrice": "0.00000000",
      "icebergQty": "0.00000000",
      "time": 1704067200000,
      "updateTime": 1704067250000,
      "isWorking": true,
      "origQuoteOrderQty": "0.00000000"
    }
  ],
  "timestamp": 1704067200000
}
```

## Transaction History Tools

### get_deposit_history

Get deposit history for a specific coin.

**Parameters:**
- `coin` (string, required): The coin for which to fetch deposit history (e.g., 'BTC', 'ETH')

**Example:**
```json
{
  "tool": "get_deposit_history",
  "arguments": {
    "coin": "BTC"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "amount": "0.12345678",
      "coin": "BTC",
      "network": "BTC",
      "status": 1,
      "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
      "addressTag": "",
      "txId": "abc123def456",
      "insertTime": 1704067200000,
      "transferType": 0,
      "confirmTimes": "1/1"
    }
  ],
  "timestamp": 1704067200000
}
```

---

### get_withdraw_history

Get withdrawal history for a specific coin.

**Parameters:**
- `coin` (string, required): The coin for which to fetch withdrawal history (e.g., 'BTC', 'ETH')

**Example:**
```json
{
  "tool": "get_withdraw_history",
  "arguments": {
    "coin": "BTC"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
      "amount": "0.05000000",
      "applyTime": "2024-01-01 12:00:00",
      "coin": "BTC",
      "id": "abc123def456",
      "withdrawOrderId": "def456ghi789",
      "network": "BTC",
      "transferType": 0,
      "status": 6,
      "transactionFee": "0.0005",
      "confirmNo": 3,
      "info": "Withdrawal completed",
      "txId": "ghi789jkl012"
    }
  ],
  "timestamp": 1704067200000
}
```

---

### get_deposit_address

Get deposit address for a specific coin.

**Parameters:**
- `coin` (string, required): The coin for which to fetch the deposit address (e.g., 'BTC', 'ETH')

**Example:**
```json
{
  "tool": "get_deposit_address",
  "arguments": {
    "coin": "BTC"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "address": "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa",
    "coin": "BTC",
    "tag": "",
    "url": "https://btc.com/1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
  },
  "timestamp": 1704067200000
}
```

---

### get_liquidation_history

Get liquidation history for futures trading.

**Parameters:**
None

**Example:**
```json
{
  "tool": "get_liquidation_history",
  "arguments": {}
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "symbol": "BTCUSDT",
      "price": "40000.00",
      "origQty": "0.001",
      "executedQty": "0.001",
      "avrPrice": "40000.00",
      "status": "FILLED",
      "timeInForce": "IOC",
      "type": "LIMIT",
      "side": "SELL",
      "time": 1704067200000
    }
  ],
  "timestamp": 1704067200000
}
```

---

### get_universal_transfer_history

Get universal transfer history (transfers between different account types).

**Parameters:**
None

**Example:**
```json
{
  "tool": "get_universal_transfer_history",
  "arguments": {}
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "This feature is currently under development"
  },
  "timestamp": 1704067200000
}
```

## Fee Information Tools

### get_fee_info

Get trading fee information for symbols.

**Parameters:**
- `symbol` (string, optional): Specific trading pair symbol. If not provided, returns fees for all symbols

**Example:**
```json
{
  "tool": "get_fee_info",
  "arguments": {
    "symbol": "BTCUSDT"
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "symbol": "BTCUSDT",
      "makerCommission": "0.001",
      "takerCommission": "0.001"
    }
  ],
  "timestamp": 1704067200000,
  "metadata": {
    "source": "binance_api",
    "endpoint": "trade_fee"
  }
}
```

## Error Types

The API can return the following error types:

### validation_error
Parameter validation failed (invalid symbol format, missing required parameters, etc.)

### binance_api_error  
Error from Binance API (invalid API key, insufficient balance, rate limits, etc.)

### rate_limit_exceeded
API rate limit has been exceeded, retry after waiting

### tool_error
Unexpected error during tool execution

### network_error
Network connectivity issues or timeouts

## Rate Limiting

All tools are subject to Binance API rate limits:
- **1200 requests per minute** for most endpoints
- **10 requests per second** burst limit
- Rate limiting is handled automatically by the server

When rate limits are exceeded, you'll receive a `rate_limit_exceeded` error. Wait a few seconds before retrying.

## Best Practices

1. **Always check the `success` field** before processing data
2. **Handle errors gracefully** with appropriate fallback logic  
3. **Use testnet** (`BINANCE_TESTNET=true`) for development
4. **Respect rate limits** - avoid making too many requests too quickly
5. **Validate symbols** before making requests to avoid API errors
6. **Log responses** for debugging and monitoring