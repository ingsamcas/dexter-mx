from langchain_core.tools import tool
from typing import Optional
from datetime import datetime, timedelta
from .api import call_api

@tool
def db_get_price_snapshot(ticker: str, serie: str = "*") -> dict:
    """
    Get current stock price and market data from DataBursatil (Mexican market).
    
    Uses DataBursatil /v2/cotizaciones endpoint.
    
    Args:
        ticker: Stock ticker symbol WITHOUT .MX suffix (e.g., 'LASITE', 'WALMEX', 'BIMBOA')
        serie: Stock series (default '*', common values: '*', 'A', 'B', 'CPO', etc.)
    
    Returns:
        Current price, volume, and other snapshot data
    """
    emisora_serie = f"{ticker}{serie}"
    
    params = {
        "emisora_serie": emisora_serie,
        "concepto": "u,p,a,x,n,c,m,v,o,i",
        "bolsa": "BMV,BIVA"
    }
    
    data = call_api("/cotizaciones", params)
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    ticker_data = data.get(emisora_serie, {})
    if not ticker_data:
        return {"error": "No data found for ticker", "ticker": ticker, "serie": serie}
    
    bmv_data = ticker_data.get("bmv", {})
    biva_data = ticker_data.get("biva", {})
    
    merged = bmv_data if bmv_data else biva_data
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "serie": serie,
        "emisora_serie": emisora_serie,
        "ultimo": merged.get("u"),
        "ppp": merged.get("p"),
        "anterior": merged.get("a"),
        "maximo": merged.get("x"),
        "minimo": merged.get("n"),
        "cambio_porciento": merged.get("c"),
        "cambio_pesos": merged.get("m"),
        "volumen": merged.get("v"),
        "operaciones": merged.get("o"),
        "importe": merged.get("i"),
        "fecha": merged.get("f"),
        "bolsa": "BMV" if bmv_data else "BIVA"
    }

@tool
def db_get_historical_prices(
    ticker: str,
    serie: str = "*",
    inicio: Optional[str] = None,
    final: Optional[str] = None
) -> dict:
    """
    Get historical stock prices from DataBursatil (Mexican market).
    
    Uses DataBursatil /v2/historicos endpoint.
    
    Args:
        ticker: Stock ticker symbol WITHOUT .MX suffix (e.g., 'LASITE')
        serie: Stock series (default '*')
        inicio: Start date in YYYY-MM-DD format (default: 30 days ago)
        final: End date in YYYY-MM-DD format (default: today)
    
    Returns:
        Historical price data
    """
    if not final:
        final = datetime.now().strftime("%Y-%m-%d")
    if not inicio:
        inicio = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    emisora_serie = f"{ticker}{serie}"
    
    params = {
        "emisora_serie": emisora_serie,
        "inicio": inicio,
        "final": final
    }
    
    data = call_api("/historicos", params)
    
    if "error" in data:
        return {"error": data["error"], "ticker": ticker}
    
    ticker_data = data.get(emisora_serie, {})
    if not ticker_data:
        return {"error": "No historical data found", "ticker": ticker}
    
    prices = []
    for fecha, valores in ticker_data.items():
        if isinstance(valores, dict):
            prices.append({
                "fecha": fecha,
                "precio": valores.get("precio"),
                "importe": valores.get("importe")
            })
    
    return {
        "data_source": "databursatil",
        "ticker": ticker,
        "serie": serie,
        "inicio": inicio,
        "final": final,
        "prices": prices
    }
