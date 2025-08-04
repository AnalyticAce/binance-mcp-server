# Configuration Guide

## Environment Variables

The Binance MCP Server uses environment variables for configuration. This approach ensures security by keeping sensitive credentials out of source code.

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `BINANCE_API_KEY` | Your Binance API key | `abc123def456...` |
| `BINANCE_API_SECRET` | Your Binance API secret | `xyz789uvw012...` |

### Optional Variables

| Variable | Default | Description | Options |
|----------|---------|-------------|---------|
| `BINANCE_TESTNET` | `false` | Use Binance testnet | `true`, `false` |

## Configuration Methods

### Method 1: Environment Variables (Recommended)

=== "Linux/macOS"
    ```bash
    export BINANCE_API_KEY="your_api_key_here"
    export BINANCE_API_SECRET="your_api_secret_here"
    export BINANCE_TESTNET="true"
    ```

=== "Windows PowerShell"
    ```powershell
    $env:BINANCE_API_KEY="your_api_key_here"
    $env:BINANCE_API_SECRET="your_api_secret_here"
    $env:BINANCE_TESTNET="true"
    ```

=== "Windows Command Prompt"
    ```cmd
    set BINANCE_API_KEY=your_api_key_here
    set BINANCE_API_SECRET=your_api_secret_here
    set BINANCE_TESTNET=true
    ```

### Method 2: .env File

Create a `.env` file in your project directory:

```bash
# .env file
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
BINANCE_TESTNET=true
```

The server will automatically load the `.env` file using `python-dotenv`.

### Method 3: MCP Client Configuration

When configuring MCP clients like Claude Desktop, include environment variables in the configuration:

```json
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

## API Key Management

### Creating API Keys

1. **Login to Binance**: Visit [binance.com](https://binance.com) or [binance.us](https://binance.us)
2. **Navigate to API Management**: Account → API Management
3. **Create New Key**: Click "Create API" → "System generated"
4. **Set Permissions**:
   - ✅ **Enable Reading** (Required for market data)
   - ✅ **Enable Spot Trading** (Required for trading)
   - ✅ **Enable Futures** (Optional, for futures trading)
   - ❌ **Enable Withdrawals** (Not recommended for security)

### API Key Security

#### IP Restrictions (Recommended)
- Add your server's IP address to the allowed list
- Use "Restrict access to trusted IPs only"
- Update IP restrictions when your server IP changes

#### Key Rotation
- Rotate API keys regularly (monthly/quarterly)
- Delete unused API keys
- Monitor API key usage in Binance account

#### Permissions
- Only enable necessary permissions
- Avoid enabling withdrawal permissions unless absolutely required
- Use separate keys for different applications

### Testnet vs Production

#### Testnet Configuration
```bash
export BINANCE_TESTNET="true"
```

- **URL**: `https://testnet.binance.vision`
- **Purpose**: Development and testing with fake money
- **Benefits**: Safe experimentation, no real financial risk
- **Limitations**: Reduced functionality, fake data

#### Production Configuration
```bash
export BINANCE_TESTNET="false"  # or omit entirely
```

- **URL**: `https://api.binance.com`
- **Purpose**: Live trading with real money
- **Benefits**: Full functionality, real market data
- **Requirements**: Extra caution, proper risk management

## Server Configuration

### Command Line Options

```bash
binance-mcp-server [OPTIONS]
```

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--transport` | Transport method | `stdio` | `--transport streamable-http` |
| `--port` | Port for HTTP transport | `8000` | `--port 3000` |
| `--host` | Host for HTTP transport | `localhost` | `--host 0.0.0.0` |
| `--log-level` | Logging level | `INFO` | `--log-level DEBUG` |

### Transport Options

#### STDIO (Default)
```bash
binance-mcp-server
```
- **Best for**: MCP clients (Claude, etc.)
- **Communication**: stdin/stdout
- **Use case**: Production MCP integration

#### HTTP
```bash
binance-mcp-server --transport streamable-http --port 8000
```
- **Best for**: Testing and development
- **Communication**: HTTP POST requests
- **Use case**: API testing, debugging

#### SSE (Server-Sent Events)
```bash
binance-mcp-server --transport sse --port 8080
```
- **Best for**: Real-time applications
- **Communication**: Server-sent events
- **Use case**: Live data streaming

## Logging Configuration

### Log Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| `DEBUG` | Detailed debugging information | Development, troubleshooting |
| `INFO` | General information messages | Production monitoring |
| `WARNING` | Warning messages | Error monitoring |
| `ERROR` | Error messages only | Minimal logging |

### Example Log Output

```bash
# INFO level (default)
2024-01-01 12:00:00 - binance_mcp_server.server - INFO - Starting Binance MCP Server with stdio transport
2024-01-01 12:00:01 - binance_mcp_server.utils - INFO - Successfully initialized Binance client (testnet: True)
2024-01-01 12:00:02 - binance_mcp_server.tools.get_ticker_price - INFO - Tool called: get_ticker_price with symbol=BTCUSDT

# DEBUG level
2024-01-01 12:00:00 - binance_mcp_server.config - DEBUG - Loading configuration from environment
2024-01-01 12:00:00 - binance_mcp_server.config - DEBUG - API key loaded: abc123***
2024-01-01 12:00:00 - binance_mcp_server.config - DEBUG - Testnet mode: True
```

## Configuration Validation

The server validates configuration on startup and provides helpful error messages:

### Missing API Key
```
Error: Invalid Binance configuration: BINANCE_API_KEY environment variable is required
```

### Missing API Secret
```
Error: Invalid Binance configuration: BINANCE_API_SECRET environment variable is required
```

### Invalid API Credentials
```
Error: Binance API error during client initialization: API-key format invalid
```

### Network Issues
```
Error: Binance request error during client initialization: Connection timeout
```

## Production Deployment

### Docker Configuration

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install the package
RUN pip install binance-mcp-server

# Set environment variables
ENV BINANCE_TESTNET=false

# Command to run the server
CMD ["binance-mcp-server"]
```

```bash
# Run with environment variables
docker run -e BINANCE_API_KEY="your_key" \
           -e BINANCE_API_SECRET="your_secret" \
           -e BINANCE_TESTNET="false" \
           your-binance-mcp-server
```

### Environment-Specific Configuration

#### Development
```bash
# Development environment
export BINANCE_TESTNET="true"
export LOG_LEVEL="DEBUG"
binance-mcp-server --log-level DEBUG
```

#### Staging  
```bash
# Staging environment
export BINANCE_TESTNET="true"
export LOG_LEVEL="INFO"
binance-mcp-server --log-level INFO
```

#### Production
```bash
# Production environment
export BINANCE_TESTNET="false"
export LOG_LEVEL="WARNING"
binance-mcp-server --log-level WARNING
```

### Health Checks

The server provides basic health checking through configuration validation:

```python
from binance_mcp_server.config import BinanceConfig

def health_check():
    try:
        config = BinanceConfig()
        if config.is_valid():
            return {"status": "healthy", "testnet": config.testnet}
        else:
            return {"status": "unhealthy", "errors": config.get_validation_errors()}
    except Exception as e:
        return {"status": "error", "message": str(e)}
```

## Troubleshooting Configuration

### Common Issues

#### 1. Environment Variables Not Set
**Problem**: Variables set in terminal but not visible to the process

**Solutions**:
- Use `.env` file instead
- Check if variables are exported: `export VARIABLE=value`
- Restart terminal/IDE after setting variables

#### 2. Wrong Testnet Setting
**Problem**: Using production keys with testnet or vice versa

**Solutions**:
- Verify `BINANCE_TESTNET` matches your API key type
- Testnet keys only work with testnet endpoints
- Production keys only work with production endpoints

#### 3. API Key Permissions
**Problem**: API operations failing due to insufficient permissions

**Solutions**:
- Check API key permissions in Binance account
- Enable "Reading" and "Spot Trading" permissions
- Avoid enabling "Withdrawals" unless necessary

#### 4. IP Restrictions
**Problem**: API calls failing due to IP restrictions

**Solutions**:
- Add your server IP to allowed list in Binance
- Remove IP restrictions for testing
- Use VPN if server IP changes frequently

### Configuration Testing

Test your configuration before deployment:

```bash
# Test with ticker price (read-only operation)
binance-mcp-server --transport streamable-http &
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_ticker_price", "arguments": {"symbol": "BTCUSDT"}}'
```

Expected successful response:
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