from langchain_core.tools import tool
from typing import Optional
from .api import call_api

@tool
def db_get_price_snapshot(ticker: str) -> dict:
    """
    Get current stock price and market data from DataBursatil.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AMXL', 'WALMEX', 'BIMBOA')
    
    Returns:
        Current price, volume, market cap, and other snapshot data
    """
    data = call_api("/stocks/quote", {"ticker": ticker})
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "price": data.get("price"),
        "change": data.get("change"),
        "change_percent": data.get("change_percent"),
        "volume": data.get("volume"),
        "market_cap": data.get("market_cap"),
        "timestamp": data.get("timestamp")
    }

@tool
def db_get_historical_prices(
    ticker: str,
    period: str = "1mo",
    interval: str = "1d"
) -> dict:
    """
    Get historical stock prices from DataBursatil.
    
    Args:
        ticker: Stock ticker symbol
        period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, max)
        interval: Data interval (1d, 1wk, 1mo)
    
    Returns:
        Historical price data
    """
    data = call_api("/stocks/history", {
        "ticker": ticker,
        "period": period,
        "interval": interval
    })
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "period": period,
        "prices": data.get("prices", [])
    }
