# Development Guide

This guide covers development, testing, and contribution workflows for the Binance MCP Server.

## Development Setup

### Prerequisites

- **Python 3.10+** - Required for modern typing and FastMCP support
- **Git** - For version control
- **uv** (recommended) or pip for package management

### Local Development Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/AnalyticAce/BinanceMCPServer.git
cd BinanceMCPServer
```

#### 2. Set Up Virtual Environment
```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Using pip
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
# Development installation
pip install -e .

# Install development dependencies
pip install pytest pytest-cov black isort mypy pre-commit
```

#### 4. Set Up Pre-commit Hooks
```bash
pre-commit install
```

#### 5. Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your credentials
export BINANCE_API_KEY="your_testnet_key"
export BINANCE_API_SECRET="your_testnet_secret"
export BINANCE_TESTNET="true"
```

## Project Structure

```
BinanceMCPServer/
├── binance_mcp_server/          # Main package
│   ├── __init__.py
│   ├── server.py                # FastMCP server with tool registration
│   ├── config.py                # Configuration management
│   ├── utils.py                 # Shared utilities and rate limiting
│   ├── cli.py                   # Command-line interface
│   └── tools/                   # Individual tool implementations
│       ├── __init__.py
│       ├── get_ticker_price.py  # Price data tool
│       ├── get_balance.py       # Account balance tool
│       ├── create_order.py      # Order creation tool
│       └── ...                  # Other tools
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── conftest.py             # Pytest configuration
│   ├── test_server.py          # Server tests
│   └── test_tools/             # Tool-specific tests
├── docs/                       # Documentation
│   ├── index.md
│   ├── api-reference.md
│   └── ...
├── scripts/                    # Utility scripts
├── pyproject.toml             # Package configuration
├── mkdocs.yml                 # Documentation configuration
└── README.md
```

## Development Workflow

### Code Style and Formatting

The project uses standardized code formatting:

#### Black (Code Formatting)
```bash
# Format all Python files
black binance_mcp_server/ tests/

# Check formatting without changes
black --check binance_mcp_server/ tests/
```

#### isort (Import Sorting)
```bash
# Sort imports
isort binance_mcp_server/ tests/

# Check import sorting
isort --check-only binance_mcp_server/ tests/
```

#### Type Checking with mypy
```bash
# Run type checking
mypy binance_mcp_server/
```

### Testing

#### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=binance_mcp_server --cov-report=html

# Run specific test file
pytest tests/test_tools/test_get_ticker_price.py

# Run with verbose output
pytest -v
```

#### Test Categories

**Unit Tests**: Test individual functions and modules
```bash
pytest tests/test_tools/
```

**Integration Tests**: Test tool integration with mocked Binance API
```bash
pytest tests/test_server.py
```

**End-to-End Tests**: Test complete workflows (requires testnet API keys)
```bash
pytest tests/test_e2e.py --run-e2e
```

### Adding New Tools

#### Step 1: Create Tool Module

Create a new file in `binance_mcp_server/tools/`:

```python
# binance_mcp_server/tools/get_new_feature.py
import logging
from typing import Dict, Any
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance_mcp_server.utils import (
    get_binance_client,
    create_error_response,
    create_success_response,
    rate_limited,
    binance_rate_limiter,
)

logger = logging.getLogger(__name__)

@rate_limited(binance_rate_limiter)
def get_new_feature(param1: str, param2: int = None) -> Dict[str, Any]:
    """
    Tool description.
    
    Args:
        param1: Description of parameter 1
        param2: Optional description of parameter 2
        
    Returns:
        Dict containing success status and data
        
    Examples:
        result = get_new_feature("value1", 123)
        if result["success"]:
            data = result["data"]
    """
    logger.info(f"Tool called: get_new_feature with param1={param1}, param2={param2}")
    
    try:
        client = get_binance_client()
        
        # Implement tool logic
        api_result = client.some_api_method(param1, param2)
        
        # Process and format result
        processed_data = {
            "processed_field": api_result["field"],
            "calculated_value": api_result["value"] * 2
        }
        
        logger.info("Successfully executed get_new_feature")
        
        return create_success_response(
            data=processed_data,
            metadata={
                "source": "binance_api",
                "endpoint": "new_feature"
            }
        )
        
    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error in get_new_feature: {str(e)}")
        return create_error_response("binance_api_error", f"Error: {str(e)}")
    
    except Exception as e:
        logger.error(f"Unexpected error in get_new_feature: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")
```

#### Step 2: Register Tool in Server

Add the tool to `binance_mcp_server/server.py`:

```python
@mcp.tool()
def get_new_feature(param1: str, param2: Optional[int] = None) -> Dict[str, Any]:
    """
    Tool description for MCP clients.
    
    Args:
        param1: Description of parameter 1
        param2: Optional description of parameter 2
        
    Returns:
        Dictionary containing success status and data
    """
    logger.info(f"Tool called: get_new_feature with param1={param1}, param2={param2}")
    
    try:
        from binance_mcp_server.tools.get_new_feature import get_new_feature as _get_new_feature
        result = _get_new_feature(param1, param2)
        
        if result.get("success"):
            logger.info("Successfully executed get_new_feature")
        else:
            logger.warning(f"Failed to execute get_new_feature: {result.get('error', {}).get('message')}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in get_new_feature tool: {str(e)}")
        return {
            "success": False,
            "error": {
                "type": "tool_error",
                "message": f"Tool execution failed: {str(e)}"
            }
        }
```

#### Step 3: Create Tests

Create test file in `tests/test_tools/`:

```python
# tests/test_tools/test_get_new_feature.py
import pytest
from unittest.mock import Mock, patch
from binance_mcp_server.tools.get_new_feature import get_new_feature

class TestGetNewFeature:
    
    @patch('binance_mcp_server.tools.get_new_feature.get_binance_client')
    def test_get_new_feature_success(self, mock_get_client):
        # Arrange
        mock_client = Mock()
        mock_client.some_api_method.return_value = {
            "field": "test_value",
            "value": 50
        }
        mock_get_client.return_value = mock_client
        
        # Act
        result = get_new_feature("test_param", 123)
        
        # Assert
        assert result["success"] is True
        assert result["data"]["processed_field"] == "test_value"
        assert result["data"]["calculated_value"] == 100
        mock_client.some_api_method.assert_called_once_with("test_param", 123)
    
    @patch('binance_mcp_server.tools.get_new_feature.get_binance_client')
    def test_get_new_feature_api_error(self, mock_get_client):
        # Arrange
        from binance.exceptions import BinanceAPIException
        mock_client = Mock()
        mock_client.some_api_method.side_effect = BinanceAPIException("API Error")
        mock_get_client.return_value = mock_client
        
        # Act
        result = get_new_feature("test_param")
        
        # Assert
        assert result["success"] is False
        assert result["error"]["type"] == "binance_api_error"
        assert "API Error" in result["error"]["message"]
```

#### Step 4: Update Documentation

Add tool documentation to `docs/api-reference.md`:

```markdown
### get_new_feature

Description of the new tool.

**Parameters:**
- `param1` (string, required): Description
- `param2` (integer, optional): Description

**Example:**
```json
{
  "tool": "get_new_feature",
  "arguments": {
    "param1": "value",
    "param2": 123
  }
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "processed_field": "value",
    "calculated_value": 246
  }
}
```
```

### Running the Development Server

#### STDIO Mode (for MCP testing)
```bash
python -m binance_mcp_server.server
```

#### HTTP Mode (for development)
```bash
python -m binance_mcp_server.server --transport streamable-http --port 8000 --log-level DEBUG
```

#### Testing HTTP Endpoints
```bash
curl -X POST http://localhost:8000/call \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_ticker_price", "arguments": {"symbol": "BTCUSDT"}}'
```

## Debugging

### Logging Configuration

Enable debug logging for detailed output:

```bash
python -m binance_mcp_server.server --log-level DEBUG
```

### Common Debug Scenarios

#### API Connection Issues
```python
# Test client connection
from binance_mcp_server.utils import get_binance_client

try:
    client = get_binance_client()
    result = client.ping()
    print("Connection successful:", result)
except Exception as e:
    print("Connection failed:", e)
```

#### Rate Limiting
```python
# Check rate limiter status
from binance_mcp_server.utils import binance_rate_limiter

print(f"Current calls: {len(binance_rate_limiter.calls)}")
print(f"Can proceed: {binance_rate_limiter.can_proceed()}")
```

#### Configuration Validation
```python
# Validate configuration
from binance_mcp_server.config import BinanceConfig

config = BinanceConfig()
print(f"Valid: {config.is_valid()}")
print(f"Errors: {config.get_validation_errors()}")
print(f"Testnet: {config.testnet}")
```

## Contributing Guidelines

### Submitting Pull Requests

1. **Fork the repository** on GitHub
2. **Create a feature branch** from `main`
3. **Make your changes** following the development workflow
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Run the full test suite** and ensure all tests pass
7. **Submit a pull request** with a clear description

### Code Review Process

1. **Automated checks** must pass (tests, linting, type checking)
2. **Code review** by maintainers
3. **Documentation review** for completeness and accuracy
4. **Testing** on testnet environment
5. **Merge** after approval

### Issue Reporting

When reporting issues, include:

- **Environment details** (Python version, OS, package version)
- **Configuration** (testnet vs production, anonymized)
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Error messages** and stack traces
- **Minimal code example** demonstrating the issue

### Feature Requests

For new features:

- **Describe the use case** and business value
- **Provide examples** of how the feature would be used
- **Consider implementation complexity** and maintenance burden
- **Check existing issues** to avoid duplicates

## Release Process

### Version Management

The project uses semantic versioning (SemVer):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

### Creating a Release

1. **Update version** in `pyproject.toml`
2. **Update CHANGELOG.md** with release notes
3. **Run full test suite** on testnet and production
4. **Create git tag** with version number
5. **Build and publish** to PyPI
6. **Deploy documentation** to GitHub Pages

### Testing Checklist

Before release:

- [ ] All tests pass locally
- [ ] All tests pass in CI/CD
- [ ] Documentation builds successfully
- [ ] Manual testing on testnet
- [ ] Manual testing on production (read-only operations)
- [ ] Performance testing under load
- [ ] Security review of changes

## Troubleshooting Development Issues

### Common Development Problems

#### 1. Import Errors
```bash
# Ensure package is installed in development mode
pip install -e .
```

#### 2. Test Failures
```bash
# Run tests with verbose output
pytest -v -s

# Run specific failing test
pytest tests/test_tools/test_specific.py::test_method -v
```

#### 3. Type Checking Errors
```bash
# Run mypy with verbose output
mypy binance_mcp_server/ --show-error-codes
```

#### 4. API Rate Limiting During Testing
```bash
# Use longer delays between test API calls
pytest --timeout=60 -s
```

### Development Tools

#### Useful Scripts
```bash
# Format and check code
scripts/format.sh

# Run all quality checks
scripts/check.sh

# Build documentation
scripts/build-docs.sh
```

#### IDE Configuration

**VS Code** - Recommended extensions:
- Python
- Pylance
- Black Formatter
- isort
- Better TOML

**PyCharm** - Recommended settings:
- Enable type checking
- Configure Black as external tool
- Set up pytest as test runner

This development guide provides everything needed to contribute effectively to the Binance MCP Server project.