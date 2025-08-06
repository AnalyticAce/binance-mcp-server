"""
Binance universal transfer history retrieval tool implementation.

This module provides functionality to fetch universal transfer history between different
account types on Binance, enabling comprehensive transfer tracking and analysis.
"""

import logging
from typing import Dict, Any, Optional
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance_mcp_server.utils import (
    get_binance_client, 
    create_error_response, 
    create_success_response,
    rate_limited,
    binance_rate_limiter,
)


logger = logging.getLogger(__name__)