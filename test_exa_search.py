#!/usr/bin/env python3
"""
Quick test script to verify Exa Search integration.
Run: uv run python test_exa_search.py
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
load_dotenv()

def test_exa_search():
    print("=" * 60)
    print("Testing Exa Search Integration")
    print("=" * 60)
    
    # Check if API key is present
    api_key = os.getenv("EXASEARCH_API_KEY")
    if not api_key:
        print("\n❌ ERROR: EXASEARCH_API_KEY not found in environment")
        print("Please set it in your .env file")
        print("\nGet your API key at: https://exa.ai")
        return False
    
    print(f"\n✓ API key found: {api_key[:10]}...")
    
    # Test imports
    print("\n1. Testing imports...")
    try:
        from dexter.tools.web_search import WEB_SEARCH_TOOLS, HAS_WEB_SEARCH
        print(f"   ✓ Web search tools imported")
        print(f"   ✓ HAS_WEB_SEARCH: {HAS_WEB_SEARCH}")
        print(f"   ✓ Available tools: {len(WEB_SEARCH_TOOLS)}")
        
        if not HAS_WEB_SEARCH:
            print("\n   ⚠️ Web search not available (exa-py not installed)")
            print("   Install with: uv add exa-py")
            return False
            
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False
    
    # Test web_search
    print("\n2. Testing web_search (general search)...")
    try:
        from dexter.tools.web_search.exa_search import web_search
        
        result = web_search.invoke({
            "query": "LASITE Sitios Latinoamerica Mexico stock",
            "num_results": 3
        })
        
        if "error" in result:
            print(f"   ❌ Search failed: {result['error']}")
            print(f"   Message: {result.get('message', 'N/A')}")
            return False
        
        print(f"   ✓ Search successful")
        print(f"   ✓ Query: {result['query']}")
        print(f"   ✓ Results found: {result['num_results']}")
        
        if result['num_results'] > 0:
            first = result['results'][0]
            print(f"\n   First result:")
            print(f"   - Title: {first['title'][:80]}...")
            print(f"   - URL: {first['url']}")
            print(f"   - Published: {first.get('published_date', 'N/A')}")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test web_search_news
    print("\n3. Testing web_search_news (recent news)...")
    try:
        from dexter.tools.web_search.exa_search import web_search_news
        
        result = web_search_news.invoke({
            "query": "Mexican stock market BMV recent trends",
            "num_results": 3,
            "days_back": 30
        })
        
        if "error" in result:
            print(f"   ❌ News search failed: {result['error']}")
            return False
        
        print(f"   ✓ News search successful")
        print(f"   ✓ Query: {result['query']}")
        print(f"   ✓ Articles found: {result['num_results']}")
        print(f"   ✓ Date range: last {result['days_back']} days")
        
        if result['num_results'] > 0:
            first = result['results'][0]
            print(f"\n   First article:")
            print(f"   - Title: {first['title'][:80]}...")
            print(f"   - URL: {first['url']}")
            print(f"   - Published: {first.get('published_date', 'N/A')}")
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test with Mexican domains
    print("\n4. Testing with Mexican financial domains...")
    try:
        from dexter.tools.web_search.exa_search import web_search
        
        result = web_search.invoke({
            "query": "análisis mercado bursátil México",
            "num_results": 3,
            "include_domains": ["eleconomista.com.mx", "expansion.mx", "elfinanciero.com.mx"]
        })
        
        if "error" in result:
            print(f"   ⚠️ Domain-filtered search returned error: {result['error']}")
        else:
            print(f"   ✓ Domain-filtered search successful")
            print(f"   ✓ Results from Mexican sites: {result['num_results']}")
        
    except Exception as e:
        print(f"   ⚠️ Domain test failed (non-critical): {e}")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed! Exa Search is ready to use.")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Rebuild Docker: docker build --no-cache -t dexter-mx .")
    print("2. Run agent: ./dexter.sh compare")
    print("3. Try queries like:")
    print("   - 'What recent news affects LASITE stock?'")
    print("   - 'Search for WALMEX earnings reports'")
    print("   - 'Find analysis of Mexican FIBRA market trends'")
    
    return True

if __name__ == "__main__":
    success = test_exa_search()
    sys.exit(0 if success else 1)
