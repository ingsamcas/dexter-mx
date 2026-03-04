from langchain_core.tools import tool
from typing import Optional, Literal
from .api import call_api

@tool
def db_get_income_statements(
    ticker: str,
    period: Literal["annual", "quarterly"] = "annual",
    limit: int = 5
) -> dict:
    """
    Get income statements from DataBursatil.
    
    Args:
        ticker: Stock ticker symbol
        period: 'annual' or 'quarterly'
        limit: Number of periods to retrieve
    
    Returns:
        Income statement data
    """
    data = call_api("/stocks/financials/income", {
        "ticker": ticker,
        "period": period,
        "limit": limit
    })
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "period": period,
        "statements": data.get("statements", [])
    }

@tool
def db_get_balance_sheets(
    ticker: str,
    period: Literal["annual", "quarterly"] = "annual",
    limit: int = 5
) -> dict:
    """
    Get balance sheets from DataBursatil.
    """
    data = call_api("/stocks/financials/balance", {
        "ticker": ticker,
        "period": period,
        "limit": limit
    })
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "period": period,
        "balance_sheets": data.get("balance_sheets", [])
    }

@tool
def db_get_cash_flow(
    ticker: str,
    period: Literal["annual", "quarterly"] = "annual",
    limit: int = 5
) -> dict:
    """
    Get cash flow statements from DataBursatil.
    """
    data = call_api("/stocks/financials/cashflow", {
        "ticker": ticker,
        "period": period,
        "limit": limit
    })
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "period": period,
        "cash_flows": data.get("cash_flows", [])
    }
