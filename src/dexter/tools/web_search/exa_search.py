"""
Exa Search integration for web search functionality.

Exa is a search API designed for AI applications, providing neural search
capabilities optimized for research and information retrieval.

Official docs: https://docs.exa.ai
"""

import os
from typing import Optional, Literal
from langchain_core.tools import tool

def get_exa_client():
    """Get Exa client instance with lazy initialization."""
    try:
        from exa_py import Exa
    except ImportError:
        raise ImportError(
            "exa-py package not installed. Install with: uv add exa-py"
        )
    
    api_key = os.getenv("EXASEARCH_API_KEY")
    if not api_key:
        raise ValueError("EXASEARCH_API_KEY not found in environment")
    
    return Exa(api_key=api_key)


@tool
def web_search(
    query: str,
    num_results: int = 5,
    search_type: Literal["auto", "neural", "keyword"] = "auto",
    include_domains: Optional[list[str]] = None,
    exclude_domains: Optional[list[str]] = None
) -> dict:
    """
    Search the web for current information using Exa neural search.
    
    Best for: Financial news, company research, market trends, recent events.
    
    Args:
        query: The search query (e.g., "LASITE recent news", "Mexican FIBRA market trends")
        num_results: Number of results to return (default 5, max 10)
        search_type: Type of search - "auto" (default), "neural", or "keyword"
        include_domains: Optional list of domains to search (e.g., ["eleconomista.com.mx"])
        exclude_domains: Optional list of domains to exclude
    
    Returns:
        dict with 'results' containing title, url, published_date, and text snippet
    
    Examples:
        - "LASITE Sitios Latinoamerica recent news"
        - "Mexican stock market outlook 2026"
        - "FIBRA real estate investment trends Mexico"
    """
    try:
        client = get_exa_client()
        
        # Prepare search parameters
        search_params = {
            "num_results": min(num_results, 10),  # Cap at 10
            "type": search_type,
            "use_autoprompt": True,  # Let Exa optimize the query
        }
        
        if include_domains:
            search_params["include_domains"] = include_domains
        if exclude_domains:
            search_params["exclude_domains"] = exclude_domains
        
        # Perform search with content extraction
        response = client.search_and_contents(
            query,
            **search_params,
            text={"max_characters": 500},  # Get snippet
            highlights=True
        )
        
        # Format results
        results = []
        for item in response.results:
            result = {
                "title": item.title,
                "url": item.url,
                "published_date": item.published_date if hasattr(item, 'published_date') else None,
                "text": item.text[:500] if hasattr(item, 'text') and item.text else "",
                "highlights": item.highlights if hasattr(item, 'highlights') and item.highlights else [],
                "score": item.score if hasattr(item, 'score') else None
            }
            results.append(result)
        
        return {
            "query": query,
            "num_results": len(results),
            "results": results,
            "search_engine": "exa"
        }
    
    except ImportError as e:
        return {
            "error": "Exa Search not available",
            "message": str(e),
            "query": query
        }
    except ValueError as e:
        return {
            "error": "API key not configured",
            "message": str(e),
            "query": query
        }
    except Exception as e:
        return {
            "error": "Search failed",
            "message": str(e),
            "query": query
        }


@tool
def web_search_news(
    query: str,
    num_results: int = 5,
    days_back: int = 30
) -> dict:
    """
    Search for recent news articles using Exa.
    
    Optimized for financial news and recent events about companies and markets.
    
    Args:
        query: News query (e.g., "LASITE financial results", "Mexican inflation")
        num_results: Number of articles to return (default 5)
        days_back: How many days back to search (default 30)
    
    Returns:
        dict with recent news articles including title, url, date, and snippet
    
    Examples:
        - "LASITE quarterly earnings"
        - "Banco de Mexico interest rate decision"
        - "Mexican peso exchange rate news"
    """
    try:
        client = get_exa_client()
        
        # Calculate start date
        from datetime import datetime, timedelta
        start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
        
        # Search for news with date filter
        response = client.search_and_contents(
            query,
            num_results=min(num_results, 10),
            type="auto",
            use_autoprompt=True,
            start_published_date=start_date,
            text={"max_characters": 500},
            highlights=True
        )
        
        # Format results
        results = []
        for item in response.results:
            result = {
                "title": item.title,
                "url": item.url,
                "published_date": item.published_date if hasattr(item, 'published_date') else None,
                "text": item.text[:500] if hasattr(item, 'text') and item.text else "",
                "highlights": item.highlights if hasattr(item, 'highlights') and item.highlights else []
            }
            results.append(result)
        
        return {
            "query": query,
            "days_back": days_back,
            "start_date": start_date,
            "num_results": len(results),
            "results": results,
            "search_engine": "exa"
        }
    
    except Exception as e:
        return {
            "error": "News search failed",
            "message": str(e),
            "query": query
        }


# Export tools
__all__ = ["web_search", "web_search_news"]
