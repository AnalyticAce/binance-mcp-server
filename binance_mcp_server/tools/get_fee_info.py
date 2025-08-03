"""
Tool for retrieving trading, withdrawal, and funding fee rates from Binance.

This module provides functionality to fetch comprehensive fee information including
trading commissions for spot trading, which is essential for trading/finance operations.
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
    validate_symbol,
)

logger = logging.getLogger(__name__)


@rate_limited(binance_rate_limiter)
def get_fee_info(symbol: Optional[str] = None) -> Dict[str, Any]:
    """
    Get trading fee information for symbols on Binance.
    
    This function retrieves trading fee rates including maker and taker commissions
    for spot trading. Fee information is essential for calculating trading costs
    and optimizing trading strategies.
    
    Args:
        symbol (Optional[str]): Specific trading pair symbol to get fees for.
                               If not provided, returns fees for all symbols.
                               Format: 'BTCUSDT', 'ETHUSDT', etc.
    
    Returns:
        Dict containing:
        - success (bool): Whether the request was successful
        - data (list): List of fee information for symbols
        - timestamp (int): Unix timestamp of the response
        - error (dict, optional): Error details if request failed
        
    Examples:
        # Get fees for all symbols
        result = get_fee_info()
        if result["success"]:
            fees = result["data"]
            for fee in fees:
                print(f"{fee['symbol']}: maker={fee['makerCommission']}, taker={fee['takerCommission']}")
        
        # Get fees for specific symbol
        result = get_fee_info(symbol="BTCUSDT")
        if result["success"]:
            fee_data = result["data"][0]
            print(f"BTCUSDT maker fee: {fee_data['makerCommission']}")
    """
    logger.info(f"Fetching fee information for symbol: {symbol if symbol else 'all symbols'}")
    
    try:
        client = get_binance_client()
        
        # Prepare parameters for API call
        params = {}
        if symbol and symbol.strip():  # Check for non-empty symbol after stripping
            # Validate and normalize symbol if provided
            validated_symbol = validate_symbol(symbol)
            params['symbol'] = validated_symbol
            logger.info(f"Requesting fees for specific symbol: {validated_symbol}")
        else:
            logger.info("Requesting fees for all symbols")
        
        # Get trade fee information from Binance API
        fee_data = client.get_trade_fee(**params)
        
        # Process and structure the response data
        if not isinstance(fee_data, list):
            fee_data = [fee_data]
        
        # Convert string values to float for easier calculation
        processed_fees = []
        for fee_item in fee_data:
            processed_fee = {
                "symbol": fee_item["symbol"],
                "makerCommission": float(fee_item["makerCommission"]),
                "takerCommission": float(fee_item["takerCommission"]),
                "makerCommissionPercent": f"{float(fee_item['makerCommission']) * 100:.4f}%",
                "takerCommissionPercent": f"{float(fee_item['takerCommission']) * 100:.4f}%"
            }
            processed_fees.append(processed_fee)
        
        # Sort by symbol for consistent ordering
        processed_fees.sort(key=lambda x: x["symbol"])
        
        metadata = {
            "count": len(processed_fees),
            "fee_type": "trading_fees",
            "description": "Spot trading maker and taker commission rates"
        }
        
        if symbol and symbol.strip():
            metadata["requested_symbol"] = symbol
        
        logger.info(f"Successfully fetched fee information for {len(processed_fees)} symbol(s)")
        
        return create_success_response(
            data=processed_fees,
            metadata=metadata
        )

    except ValueError as e:
        logger.error(f"Validation error in get_fee_info: {str(e)}")
        return create_error_response("validation_error", f"Invalid input: {str(e)}")

    except (BinanceAPIException, BinanceRequestException) as e:
        logger.error(f"Binance API error fetching fee information: {str(e)}")
        return create_error_response("binance_api_error", f"Error fetching fee information: {str(e)}")

    except Exception as e:
        logger.error(f"Unexpected error in get_fee_info tool: {str(e)}")
        return create_error_response("tool_error", f"Tool execution failed: {str(e)}")