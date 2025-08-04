# Setup Guide

## Installation

### Prerequisites
- **Python 3.10+** - Required for modern typing and async support
- **Binance Account** - With API access enabled
- **API Credentials** - API Key and Secret from Binance

### Step 1: Install the Package

Choose your preferred package manager:

=== "uv (Recommended)"
    ```bash
    # Install using uv for fast, reliable package management
    uv add binance-mcp-server
    ```

=== "pip"
    ```bash
    # Install using pip
    pip install binance-mcp-server
    ```

=== "Development Installation"
    ```bash
    # Clone and install for development
    git clone https://github.com/AnalyticAce/BinanceMCPServer.git
    cd BinanceMCPServer
    pip install -e .
    ```

## Configuration

### Step 2: Binance API Setup

1. **Login to Binance**: Go to [binance.com](https://binance.com) or [binance.us](https://binance.us)

2. **Create API Key**: 
   - Navigate to Account → API Management
   - Click "Create API" 
   - Choose "System generated" API key

3. **Configure Permissions**:
   ```
   ✅ Enable Reading      (Required for market data)
   ✅ Enable Spot Trading (Required for trading operations)  
   ✅ Enable Futures      (Optional, for futures trading)
   ❌ Enable Withdrawals  (Not recommended for security)
   ```

4. **IP Restrictions** (Recommended):
   - Add your server's IP address
   - Use "Restrict access to trusted IPs only"

### Step 3: Environment Variables

Set up your API credentials as environment variables:

=== "Linux/macOS"
    ```bash
    # Required: Your Binance API credentials
    export BINANCE_API_KEY="your_api_key_here"
    export BINANCE_API_SECRET="your_api_secret_here"
    
    # Recommended: Use testnet for development
    export BINANCE_TESTNET="true"
    ```

=== "Windows (PowerShell)"
    ```powershell
    # Required: Your Binance API credentials  
    $env:BINANCE_API_KEY="your_api_key_here"
    $env:BINANCE_API_SECRET="your_api_secret_here"
    
    # Recommended: Use testnet for development
    $env:BINANCE_TESTNET="true"
    ```

=== ".env File"
    ```bash
    # Create a .env file in your project directory
    BINANCE_API_KEY=your_api_key_here
    BINANCE_API_SECRET=your_api_secret_here
    BINANCE_TESTNET=true
    ```

### Configuration Options

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `BINANCE_API_KEY` | ✅ Yes | None | Your Binance API key |
| `BINANCE_API_SECRET` | ✅ Yes | None | Your Binance API secret |
| `BINANCE_TESTNET` | ❌ No | `false` | Use testnet environment |

## Running the Server

### Step 4: Start the Server

=== "STDIO (MCP Clients)"
    ```bash
    # Default mode for MCP clients (Claude, etc.)
    binance-mcp-server
    
    # With custom log level
    binance-mcp-server --log-level DEBUG
    ```

=== "HTTP (Testing)"
    ```bash
    # For testing and development
    binance-mcp-server --transport streamable-http --port 8000
    
    # Custom host and port
    binance-mcp-server --transport streamable-http --host 0.0.0.0 --port 3000
    ```

=== "SSE (Server-Sent Events)"
    ```bash
    # Server-sent events transport
    binance-mcp-server --transport sse --port 8080
    ```

### Command Line Options

```bash
binance-mcp-server [OPTIONS]

Options:
  --transport [stdio|streamable-http|sse]  Transport method (default: stdio)
  --port INTEGER                           Port for HTTP transport (default: 8000)
  --host TEXT                             Host for HTTP transport (default: localhost)
  --log-level [DEBUG|INFO|WARNING|ERROR]  Set logging level (default: INFO)
  --help                                  Show help message
```

## MCP Client Configuration

### Claude Desktop Configuration

Add to your Claude Desktop configuration file:

=== "macOS"
    ```json
    // ~/Library/Application Support/Claude/claude_desktop_config.json
    {
      "mcpServers": {
        "binance": {
          "command": "binance-mcp-server",
          "args": [],
          "env": {
            "BINANCE_API_KEY": "your_api_key_here",
            "BINANCE_API_SECRET": "your_api_secret_here",
            "BINANCE_TESTNET": "true"
          }
        }
      }
    }
    ```

=== "Windows"
    ```json
    // %APPDATA%\Claude\claude_desktop_config.json
    {
      "mcpServers": {
        "binance": {
          "command": "binance-mcp-server",
          "args": [],
          "env": {
            "BINANCE_API_KEY": "your_api_key_here", 
            "BINANCE_API_SECRET": "your_api_secret_here",
            "BINANCE_TESTNET": "true"
          }
        }
      }
    }
    ```

### Other MCP Clients

For other MCP clients, use the STDIO transport:

```bash
# Start server in STDIO mode
binance-mcp-server
```

The server will communicate via stdin/stdout for MCP protocol messages.

## Verification

### Step 5: Test Your Setup

Test the server connection:

=== "HTTP Testing"
    ```bash
    # Start server in HTTP mode
    binance-mcp-server --transport streamable-http --port 8000
    
    # Test with curl (in another terminal)
    curl -X POST http://localhost:8000/call \
      -H "Content-Type: application/json" \
      -d '{"tool": "get_ticker_price", "arguments": {"symbol": "BTCUSDT"}}'
    ```

=== "Python Testing"
    ```python
    import os
    from binance_mcp_server.tools.get_ticker_price import get_ticker_price
    
    # Set environment variables
    os.environ["BINANCE_API_KEY"] = "your_key"
    os.environ["BINANCE_API_SECRET"] = "your_secret"
    os.environ["BINANCE_TESTNET"] = "true"
    
    # Test a simple API call
    result = get_ticker_price("BTCUSDT")
    print(f"BTC Price: ${result['data']['price']}")
    ```

## Troubleshooting

### Common Issues

#### ❌ Configuration Errors
```
Error: Invalid Binance configuration: BINANCE_API_KEY environment variable is required
```
**Solution**: Ensure environment variables are set correctly

#### ❌ API Authentication Errors  
```
Error: API-key format invalid
```
**Solutions**:
- Verify API key and secret are correct
- Check API key permissions in Binance account
- Ensure IP restrictions allow your server IP

#### ❌ Rate Limit Errors
```
Error: API rate limit exceeded
```
**Solutions**:
- Wait a few minutes before retrying
- Reduce request frequency
- Contact Binance support for higher limits

#### ❌ Network Errors
```
Error: Connection timeout
```
**Solutions**:
- Check internet connectivity
- Verify firewall settings
- Try using testnet first

### Testnet vs Production

| Environment | API Base URL | Purpose |
|------------|--------------|---------|
| **Testnet** | `https://testnet.binance.vision` | Development & Testing |
| **Production** | `https://api.binance.com` | Live Trading |

!!! warning "Important"
    Always start with testnet (`BINANCE_TESTNET=true`) for development and testing. Testnet uses fake money and allows safe experimentation.

### Logging

Enable debug logging for troubleshooting:

```bash
binance-mcp-server --log-level DEBUG
```

Log output includes:
- API requests and responses
- Rate limiting status
- Error details and stack traces
- Configuration validation results

## Next Steps

- 📖 **[API Reference](api-reference.md)** - Learn about all available tools
- 💡 **[Examples](examples.md)** - See practical usage examples
- 🏗️ **[Architecture](architecture.md)** - Understand the system design
- 🤝 **[Contributing](contributing.md)** - Help improve the server