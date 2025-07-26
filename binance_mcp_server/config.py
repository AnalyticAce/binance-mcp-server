import os
from typing import Optional


class BinanceConfig:
    """Configuration management for Binance MCP Server."""
    
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.api_secret = os.getenv("BINANCE_API_SECRET")
        self.testnet = os.getenv("BINANCE_TESTNET", "false").lower() == "true"
        self.base_url = self._get_base_url()
    
    
    def _get_base_url(self) -> str:
        """Get appropriate base URL based on testnet setting."""
        if self.testnet:
            return "https://testnet.binance.vision"
        return "https://api.binance.com"
    
    
    def is_valid(self) -> bool:
        """Check if configuration is valid."""
        return bool(self.api_key and self.api_secret)
    
    
    def get_validation_errors(self) -> list[str]:
        """Get list of configuration validation errors."""
        errors = []
        if not self.api_key:
            errors.append("BINANCE_API_KEY environment variable is required")
        if not self.api_secret:
            errors.append("BINANCE_API_SECRET environment variable is required")
        return errors