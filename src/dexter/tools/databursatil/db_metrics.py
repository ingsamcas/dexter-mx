from langchain_core.tools import tool
from .api import call_api

@tool
def db_get_key_metrics(ticker: str, serie: str = "*") -> dict:
    """
    Get key company metrics from DataBursatil (Mexican market).
    
    Uses DataBursatil /v2/emisoras endpoint to get basic company info.
    
    Args:
        ticker: Stock ticker symbol WITHOUT .MX suffix (e.g., 'LASITE')
        serie: Stock series (default '*', common: 'A', 'B', 'CPO', etc.)
    
    Returns:
        Company information including shares outstanding, ISIN, status, etc.
    """
    params = {
        "letra": ticker,
        "mercado": "local"
    }
    
    data = call_api("/emisoras", params)
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    ticker_data = data.get(ticker, {})
    if not ticker_data:
        return {"error": "No company data found", "ticker": ticker}
    
    serie_data = ticker_data.get(serie, ticker_data.get("*", {}))
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "serie": serie,
        "razon_social": serie_data.get("razon_social"),
        "isin": serie_data.get("isin"),
        "bolsa": serie_data.get("bolsa"),
        "tipo_valor": serie_data.get("tipo_valor_descripcion"),
        "estatus": serie_data.get("estatus"),
        "acciones_en_circulacion": serie_data.get("acciones_en_circulacion"),
        "rango_historicos": serie_data.get("rango_historicos"),
        "rango_financieros": serie_data.get("rango_financieros"),
        "dividendos": serie_data.get("dividendos")
    }

@tool
def db_search_company(letra: str) -> dict:
    """
    Search for companies in DataBursatil (Mexican market) by ticker prefix or full ticker.
    
    Useful when you're not sure of the exact ticker or want to see available series.
    Uses DataBursatil /v2/emisoras endpoint.
    
    Args:
        letra: Ticker prefix or full ticker to search (e.g., 'LAS' will find LASITE)
    
    Returns:
        List of matching companies with their available series
    """
    params = {
        "letra": letra,
        "mercado": "local"
    }
    
    data = call_api("/emisoras", params)
    
    if "error" in data:
        return {"error": data["error"], "search": letra}
    
    if not data:
        return {"error": "No companies found", "search": letra}
    
    results = []
    for ticker, series_data in data.items():
        company_info = {
            "ticker": ticker,
            "series": []
        }
        
        for serie, details in series_data.items():
            if isinstance(details, dict):
                company_info["series"].append({
                    "serie": serie,
                    "razon_social": details.get("razon_social"),
                    "estatus": details.get("estatus"),
                    "bolsa": details.get("bolsa")
                })
        
        if company_info["series"]:
            results.append(company_info)
    
    return {
        "data_source": "databursatil",
        "search": letra,
        "results": results,
        "count": len(results)
    }
