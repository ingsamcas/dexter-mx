import os
import requests
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

BASE_URL = "https://api.databursatil.com/v1"

def get_api_key() -> str:
    """Get DataBursatil API key from environment."""
    api_key = os.getenv("DATABURSATIL_API_KEY")
    if not api_key:
        raise ValueError("DATABURSATIL_API_KEY not found in environment")
    return api_key

def call_api(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    method: str = "GET"
) -> Dict[str, Any]:
    """
    Make API call to DataBursatil.
    
    Args:
        endpoint: API endpoint (e.g., "/stocks/price")
        params: Query parameters
        method: HTTP method
    
    Returns:
        JSON response as dictionary
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Authorization": f"Bearer {get_api_key()}",
        "Content-Type": "application/json"
    }
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, params=params, timeout=30)
        else:
            response = requests.post(url, headers=headers, json=params, timeout=30)
        
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Data not found", "ticker": params.get("ticker", "unknown")}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded"}
        else:
            return {"error": f"HTTP {response.status_code}: {str(e)}"}
    
    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}
