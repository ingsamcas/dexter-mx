from langchain_core.tools import tool
from .api import call_api

@tool
def db_get_key_metrics(ticker: str) -> dict:
    """
    Get key financial metrics from DataBursatil.
    
    Args:
        ticker: Stock ticker symbol
    
    Returns:
        P/E ratio, EPS, dividend yield, ROE, etc.
    """
    data = call_api("/stocks/metrics", {"ticker": ticker})
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "pe_ratio": data.get("pe_ratio"),
        "eps": data.get("eps"),
        "dividend_yield": data.get("dividend_yield"),
        "roe": data.get("roe"),
        "roa": data.get("roa"),
        "debt_to_equity": data.get("debt_to_equity")
    }
