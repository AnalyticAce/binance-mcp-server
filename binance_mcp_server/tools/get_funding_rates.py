"""
Binance funding rate retrieval tool implementation.

This module provides the get_funding_rates tool for fetching funding rate
data for perpetual futures contracts on Binance.
"""

import logging
from typing import Dict, Any, Optional
from binance.exceptions import BinanceAPIException, BinanceRequestException
from binance_mcp_server.utils import (
    get_binance_client,
    validate_symbol,
    rate_limited,
    binance_rate_limiter,
    create_success_response,
    create_error_response
)


logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def get_funding_rates(symbol: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Get funding rate history for a perpetual futures contract on Binance.

    Funding rates are periodic payments between long and short traders in
    perpetual futures markets. Positive rates mean longs pay shorts (bullish
    crowding), negative rates mean shorts pay longs (bearish crowding).

    Args:
        symbol: Trading pair symbol (e.g., 'BTCUSDT', 'ETHUSDT')
        limit: Number of records to return (default: 100, max: 1000)

    Returns:
        Dictionary containing funding rate data.
        - success (bool): True if request was successful
        - data (dict): Response data with current and historical rates
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed

    Examples:
        result = get_funding_rates("BTCUSDT")
        if result["success"]:
            rates = result["data"]["history"]
            current = rates[0] if rates else None
            if current:
                print(f"Current funding rate: {current['funding_rate']}")
                print(f"Next funding time: {current['funding_time']}")
    """
    logger.info(f"Fetching funding rates for symbol: {symbol}")

    try:
        normalized_symbol = validate_symbol(symbol)

        client = get_binance_client()

        params = {"symbol": normalized_symbol}
        if limit is not None:
            params["limit"] = min(limit, 1000)

        funding_history = client.futures_funding_rate(**params)

        formatted_rates = []
        for entry in funding_history:
            formatted_rates.append({
                "symbol": entry["symbol"],
                "funding_rate": float(entry["fundingRate"]),
                "funding_time": entry["fundingTime"],
            })

        # Sort by time descending (most recent first)
        formatted_rates.sort(key=lambda x: x["funding_time"], reverse=True)

        response = {
            "symbol": normalized_symbol,
            "count": len(formatted_rates),
            "history": formatted_rates,
        }

        logger.info(f"Successfully fetched {len(formatted_rates)} funding rate entries for {symbol}")
        return create_success_response(
            data=response,
            metadata={
                "source": "binance_api",
                "endpoint": "futures_funding_rate"
            }
        )

    except ValueError as e:
        error_msg = f"Invalid symbol format: {str(e)}"
        logger.warning(f"Validation error for symbol '{symbol}': {error_msg}")
        return create_error_response("validation_error", error_msg)

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Error fetching funding rates: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching funding rates: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_funding_rates tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")
