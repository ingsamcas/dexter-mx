# Testing Exa Search Integration

## Overview

Exa Search has been integrated into Dexter MX to provide web research capabilities. This enables the agent to search for recent news, market context, and qualitative information about companies.

## Prerequisites

1. **Exa API Key**: Get yours at https://exa.ai
2. **Updated Code**: Pull latest `develop` branch
3. **Install exa-py**: Required Python package

## Setup Instructions

### Step 1: Get Exa API Key

1. Visit https://exa.ai
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier includes generous limits for testing

### Step 2: Update VM Code

```bash
cd ~/dexter-free
git checkout develop
git pull origin develop
```

You should see:
```
From https://github.com/ingsamcas/dexter-mx
 * branch            develop       -> FETCH_HEAD
Updating 46a70f5..9db7e8e
Fast-forward
 README.md                                     |  16 ++-
 env.example                                   |   3 +
 pyproject.toml                                |   1 +
 src/dexter/tools/__init__.py                  |  13 ++-
 src/dexter/tools/web_search/__init__.py       |  19 +++-
 src/dexter/tools/web_search/exa_search.py     | 222 ++++++++++++++++++++++
 test_exa_search.py                            | 165 ++++++++++++++++
 7 files changed, 390 insertions(+), 117 deletions(-)
```

### Step 3: Add API Key to .env

```bash
nano .env
```

Add this line:
```
EXASEARCH_API_KEY=your-actual-exa-api-key-here
```

Save and exit (Ctrl+X, Y, Enter)

### Step 4: Rebuild Docker with exa-py

```bash
docker build --no-cache -t dexter-mx .
```

The build will automatically install `exa-py` from pyproject.toml.

## Testing

### Quick Test (Standalone)

```bash
./dexter.sh
# Inside container:
uv run python test_exa_search.py
```

**Expected output**:
```
==========================================================
Testing Exa Search Integration
==========================================================

✓ API key found: exa_xxxxx...

1. Testing imports...
   ✓ Web search tools imported
   ✓ HAS_WEB_SEARCH: True
   ✓ Available tools: 2

2. Testing web_search (general search)...
   ✓ Search successful
   ✓ Query: LASITE Sitios Latinoamerica Mexico stock
   ✓ Results found: 3
   
   First result:
   - Title: Sitios Latinoamérica (LASITE) - Análisis Bursátil...
   - URL: https://...
   - Published: 2026-02-15

3. Testing web_search_news (recent news)...
   ✓ News search successful
   ✓ Query: Mexican stock market BMV recent trends
   ✓ Articles found: 3
   ✓ Date range: last 30 days

4. Testing with Mexican financial domains...
   ✓ Domain-filtered search successful
   ✓ Results from Mexican sites: 3

==========================================================
✅ All tests passed! Exa Search is ready to use.
==========================================================
```

### Agent Test (Full Integration)

```bash
./dexter.sh compare
```

**Test queries**:

1. **Recent news about a company**:
```
What recent news or events could explain LASITE's stock price movement?
```

Expected: Agent uses `web_search_news` to find recent articles about LASITE.

2. **Market context**:
```
What are current trends in the Mexican FIBRA market?
```

Expected: Agent uses `web_search` to find analysis and commentary.

3. **Qualitative research**:
```
Find information about WALMEX management strategy and expansion plans
```

Expected: Agent searches for strategic information not in financial statements.

4. **News + fundamentals combined**:
```
Analyze BIMBOA combining recent news with financial fundamentals
```

Expected: Agent uses both DataBursatil (for financials) and Exa (for news).

## Tool Usage in Agent Logs

When the agent uses Exa Search, you'll see:

```
⠋ Executing web_search ✓
  ⚡ web_search ({'query': 'LASITE recent news', 'num_results': 5...})
  
⠋ Executing web_search_news ✓
  ⚡ web_search_news ({'query': 'Mexican inflation', 'days_back': 30...})
```

## Available Tools

### 1. web_search

**Purpose**: General web search with neural ranking

**Parameters**:
- `query` (required): Search query string
- `num_results` (optional): Number of results (default 5, max 10)
- `search_type` (optional): "auto" (default), "neural", or "keyword"
- `include_domains` (optional): List of domains to search
- `exclude_domains` (optional): List of domains to exclude

**Examples**:
```python
# Basic search
web_search("LASITE financial performance")

# Search Mexican sites only
web_search(
    "análisis mercado valores",
    include_domains=["eleconomista.com.mx", "expansion.mx"]
)

# Exclude irrelevant domains
web_search(
    "WALMEX stock",
    exclude_domains=["reddit.com", "stocktwits.com"]
)
```

### 2. web_search_news

**Purpose**: Time-filtered news search for recent articles

**Parameters**:
- `query` (required): News query string
- `num_results` (optional): Number of articles (default 5)
- `days_back` (optional): How many days to look back (default 30)

**Examples**:
```python
# Recent news (last 30 days)
web_search_news("LASITE quarterly results")

# Last 7 days only
web_search_news("Mexican peso exchange rate", days_back=7)

# More results
web_search_news("BMV market trends", num_results=10)
```

## Common Use Cases

### 1. News-Driven Analysis
```
Query: "Why did LASITE stock drop 5% today?"

Agent workflow:
1. web_search_news("LASITE stock news", days_back=7)
2. db_get_price_snapshot("LASITE")
3. Correlate news with price movement
```

### 2. Market Research
```
Query: "What are analysts saying about Mexican FIBRAs?"

Agent workflow:
1. web_search("Mexican FIBRA analysis outlook 2026")
2. web_search_news("FIBRA market", days_back=90)
3. Synthesize market sentiment
```

### 3. Company Deep Dive
```
Query: "Comprehensive analysis of WALMEX including strategy and news"

Agent workflow:
1. db_get_key_metrics("WALMEX")
2. db_get_income_statements("WALMEX", "4T_2025")
3. web_search("WALMEX expansion strategy Mexico")
4. web_search_news("WALMEX", days_back=30)
5. Combine quantitative + qualitative
```

## Troubleshooting

### Issue: "exa-py package not installed"
**Solution**: 
```bash
# In VM
docker build --no-cache -t dexter-mx .
# This reinstalls all dependencies including exa-py
```

### Issue: "EXASEARCH_API_KEY not found"
**Solution**: 
```bash
# Check .env file
cat .env | grep EXASEARCH

# If missing, add it
nano .env
# Add: EXASEARCH_API_KEY=your-key-here
```

### Issue: "Rate limit exceeded"
**Solution**: 
- Free tier has daily limits
- Wait or upgrade Exa plan
- Reduce num_results in queries

### Issue: No results returned
**Solution**:
- Try different query phrasing
- Use `search_type="keyword"` for exact matches
- Check if include_domains are too restrictive

### Issue: Search results not in Spanish
**Solution**:
- Add Mexican domains: `include_domains=["eleconomista.com.mx", ...]`
- Use Spanish query terms
- Exa auto-detects language from query

## Mexican Financial Domains

Recommended domains for Mexican market research:

```python
MEXICAN_FINANCE_DOMAINS = [
    "eleconomista.com.mx",
    "expansion.mx",
    "elfinanciero.com.mx",
    "forbes.com.mx",
    "bmv.com.mx",
    "banxico.org.mx"
]

# Use in searches
web_search(
    "análisis bursátil México",
    include_domains=MEXICAN_FINANCE_DOMAINS
)
```

## API Usage Monitoring

Check your Exa usage at: https://exa.ai/dashboard

Monitor:
- Daily API calls
- Credits remaining
- Rate limit status

## Performance Tips

1. **Start broad, then narrow**: Use general search first, then refine with domains
2. **Cache results**: Agent automatically caches within session
3. **Combine tools**: Use DataBursatil for hard data, Exa for soft context
4. **Date relevance**: Use `web_search_news` for time-sensitive queries

## Next Steps

After validating Exa Search works:
1. Test with 5+ different Mexican tickers
2. Try various query types (news, analysis, strategy)
3. Monitor API usage for cost estimation
4. Consider merging to `main` if satisfied

## Support

- Exa Documentation: https://docs.exa.ai
- Exa Discord: https://discord.gg/exa
- Exa GitHub: https://github.com/exa-labs/exa-py

---

**Created**: March 4, 2026  
**Branch**: develop  
**Commit**: 9db7e8e
