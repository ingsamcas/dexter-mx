from langchain_core.tools import tool
from typing import Optional, Literal
from .api import call_api

@tool
def db_get_income_statements(
    ticker: str,
    periodo: str = "4T_2025",
    incluir: str = "resultado_trimestre,resultado_acumulado"
) -> dict:
    """
    Get income statements from DataBursatil (Mexican market).
    
    Uses DataBursatil /v2/financieros endpoint.
    
    Args:
        ticker: Stock ticker symbol WITHOUT .MX and WITHOUT series (e.g., 'LASITE', not 'LASITE*')
        periodo: Period in format 'QTR_YEAR' (e.g., '1T_2025', '4T_2024')
        incluir: Which financials to include: 'resultado_trimestre', 'resultado_acumulado'
    
    Returns:
        Income statement data (Estado de Resultados)
    """
    params = {
        "emisora": ticker,
        "periodo": periodo,
        "financieros": incluir
    }
    
    data = call_api("/financieros", params)
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    if not data or (isinstance(data, dict) and not any(k in data for k in ["resultado_trimestre", "resultado_acumulado"])):
        return {"error": "No financial data found", "ticker": ticker, "periodo": periodo}
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "periodo": periodo,
        "resultado_trimestre": data.get("resultado_trimestre", {}),
        "resultado_acumulado": data.get("resultado_acumulado", {})
    }

@tool
def db_get_balance_sheets(
    ticker: str,
    periodo: str = "4T_2025"
) -> dict:
    """
    Get balance sheet from DataBursatil (Mexican market).
    
    Uses DataBursatil /v2/financieros endpoint for Estado de Situación Financiera.
    
    Args:
        ticker: Stock ticker symbol WITHOUT .MX and WITHOUT series (e.g., 'LASITE')
        periodo: Period in format 'QTR_YEAR' (e.g., '1T_2025')
    
    Returns:
        Balance sheet data (Estado de Situación Financiera)
    """
    params = {
        "emisora": ticker,
        "periodo": periodo,
        "financieros": "posicion"
    }
    
    data = call_api("/financieros", params)
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    if not data or not data.get("posicion"):
        return {"error": "No balance sheet data found", "ticker": ticker, "periodo": periodo}
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "periodo": periodo,
        "posicion": data.get("posicion", {})
    }

@tool
def db_get_cash_flow(
    ticker: str,
    periodo: str = "4T_2025"
) -> dict:
    """
    Get cash flow statement from DataBursatil (Mexican market).
    
    Uses DataBursatil /v2/financieros endpoint for Estado de Flujo de Efectivo.
    
    Args:
        ticker: Stock ticker symbol WITHOUT .MX and WITHOUT series (e.g., 'LASITE')
        periodo: Period in format 'QTR_YEAR' (e.g., '1T_2025')
    
    Returns:
        Cash flow statement data (Estado de Flujo de Efectivo)
    """
    params = {
        "emisora": ticker,
        "periodo": periodo,
        "financieros": "flujos"
    }
    
    data = call_api("/financieros", params)
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    if not data or not data.get("flujos"):
        return {"error": "No cash flow data found", "ticker": ticker, "periodo": periodo}
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "periodo": periodo,
        "flujos": data.get("flujos", {})
    }
