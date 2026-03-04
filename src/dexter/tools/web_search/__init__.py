"""
Web search tools for Dexter agent.

Provides web search capabilities via Exa neural search API.
"""

# Import Exa search tools
try:
    from .exa_search import web_search, web_search_news
    
    WEB_SEARCH_TOOLS = [web_search, web_search_news]
    HAS_WEB_SEARCH = True
except ImportError:
    WEB_SEARCH_TOOLS = []
    HAS_WEB_SEARCH = False

__all__ = ["WEB_SEARCH_TOOLS", "HAS_WEB_SEARCH"]

# Note: base.py contains abstract classes for future extensibility
# (e.g., adding Tavily, Perplexity, or other search providers)
