# Testing DataBursatil Integration

## Overview
This update fixes the DataBursatil API integration by implementing the correct endpoints and parameters according to the official API documentation.

## Key Changes

### API Implementation
- **Base URL**: Changed from `/v1` to `/v2`
- **Authentication**: Changed from Bearer token to URL parameter `token`
- **Endpoints**: Implemented correct DataBursatil v2 endpoints:
  - `/v2/cotizaciones` - Current prices
  - `/v2/historicos` - Historical prices
  - `/v2/financieros` - Financial statements
  - `/v2/emisoras` - Company information

### Tool Updates

#### Price Tools
- `db_get_price_snapshot(ticker, serie)`: Get current price
  - Example: `ticker="LASITE", serie="*"`
  - NO `.MX` suffix needed
  
- `db_get_historical_prices(ticker, serie, inicio, final)`: Historical data
  - Dates in `YYYY-MM-DD` format
  - Example: `inicio="2026-02-01", final="2026-03-03"`

#### Financial Tools
- `db_get_income_statements(ticker, periodo)`: Income statements
  - **Important**: Use ticker WITHOUT serie (e.g., `"LASITE"` not `"LASITE*"`)
  - Period format: `"QTR_YEAR"` (e.g., `"4T_2024"`, `"1T_2025"`)
  
- `db_get_balance_sheets(ticker, periodo)`: Balance sheet
- `db_get_cash_flow(ticker, periodo)`: Cash flow statement

#### New Tool
- `db_search_company(letra)`: Search for company by ticker prefix
  - Example: `letra="LAS"` will find LASITE
  - Returns all matching companies with available series

### Prompt Updates

The agent now understands two different ticker formats:

**Yahoo Finance (yf_* tools):**
```
LASITE → LASITE.MX  (requires .MX suffix)
```

**DataBursatil (db_* tools):**
```
LASITE → LASITE (NO .MX suffix)
LASITE* → ticker with serie for prices
LASITE → ticker without serie for financials
```

## Testing in VM

### Step 1: Pull Latest Changes

```bash
cd ~/dexter-free
git fetch origin
git checkout develop
git pull origin develop
```

### Step 2: Rebuild Docker Image

```bash
docker build --no-cache -t dexter-mx .
```

### Step 3: Run Quick Test

First, test the API client directly:

```bash
./dexter.sh
# Inside container:
uv run python test_databursatil.py
```

This will test:
1. Search for LASITE company
2. Get company metrics
3. Get current price
4. Get historical prices
5. Get income statements

### Step 4: Run Full Agent Test

```bash
./dexter.sh compare
```

Then test with LASITE:

```
[gpt52] >>> I own 250 shares of LASITE at $4.27 cost basis. Should I sell, buy more, or maintain?
```

Expected behavior:
- Agent should use `db_search_company` first to validate ticker
- Then use `db_get_price_snapshot` to get current price
- Use `db_get_historical_prices` for trend analysis
- Use `db_get_income_statements`, `db_get_balance_sheets`, `db_get_cash_flow` for fundamentals
- NO "Data not found" errors
- Should receive actual LASITE data from DataBursatil

### Step 5: Verify Data Source

After running a query, verify the data source is showing correctly:

```bash
# At startup, you should see:
============================================================
📊 FUENTES DE DATOS CONFIGURADAS
============================================================
  🎯 Primaria:   DATABURSATIL
  🔄 Secundaria: YFINANCE
```

## Common Issues & Solutions

### Issue: "Data not found"
**Solution**: Check the logs for the exact tool call. DataBursatil requires:
- Prices: `ticker="LASITE", serie="*"`
- Financials: `ticker="LASITE"` (no serie), `periodo="4T_2024"`

### Issue: "Invalid or missing token"
**Solution**: Verify `DATABURSATIL_API_KEY` is set in `.env` file

### Issue: Agent still using .MX suffix
**Solution**: Check that prompts.py was updated correctly. The agent should know:
- Yahoo Finance = needs .MX
- DataBursatil = NO .MX

### Issue: Pydantic validation errors
**Solution**: This should be fixed now. The tools now have correct parameter definitions matching the API spec.

## Validation Checklist

- [ ] `test_databursatil.py` runs without errors
- [ ] Search finds LASITE company
- [ ] Current price retrieved successfully
- [ ] Historical prices returned (at least last 7 days)
- [ ] Financial statements available for recent quarters
- [ ] Agent query completes without "Data not found"
- [ ] Data source shows as DATABURSATIL in tool results
- [ ] No Pydantic validation errors

## API Documentation Reference

Full DataBursatil API docs: https://databursatil.com/docs.html

Key sections:
- Cotizaciones: https://databursatil.com/docs.html#cotizaciones-v2
- Históricos: https://databursatil.com/docs.html#historicos-v2
- Financieros: https://databursatil.com/docs.html#estados-financieros-v2
- Emisoras: https://databursatil.com/docs.html#emisoras-v2
