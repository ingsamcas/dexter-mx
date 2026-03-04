import os
import requests
from typing import Dict, Any, Optional

BASE_URL = "https://api.databursatil.com/v2"

def get_api_key() -> str:
    """Get DataBursatil API key (token) from environment."""
    api_key = os.getenv("DATABURSATIL_API_KEY")
    if not api_key:
        raise ValueError("DATABURSATIL_API_KEY not found in environment")
    return api_key

def call_api(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Make API call to DataBursatil API v2.
    
    DataBursatil uses URL params with 'token' for authentication.
    All requests use GET method per API docs.
    
    Args:
        endpoint: API endpoint (e.g., "/cotizaciones")
        params: Query parameters (token will be auto-added)
    
    Returns:
        JSON response as dictionary
    """
    url = f"{BASE_URL}{endpoint}"
    
    if params is None:
        params = {}
    
    params["token"] = get_api_key()
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            return {"error": "Data not found"}
        elif response.status_code == 429:
            return {"error": "Rate limit exceeded"}
        elif response.status_code == 403:
            return {"error": "Invalid or missing token"}
        else:
            return {"error": f"HTTP {response.status_code}: {str(e)}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {str(e)}"}
    
    except Exception as e:
        return {"error": f"Unexpected error: {str(e)}"}
