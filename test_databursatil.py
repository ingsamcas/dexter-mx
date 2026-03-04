#!/usr/bin/env python3
"""
Quick test script to verify DataBursatil API integration.
Run: uv run python test_databursatil.py
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dotenv import load_dotenv
load_dotenv()

from dexter.tools.databursatil import (
    db_search_company,
    db_get_key_metrics,
    db_get_price_snapshot,
    db_get_historical_prices,
    db_get_income_statements
)

def test_databursatil():
    print("=" * 60)
    print("Testing DataBursatil API Integration")
    print("=" * 60)
    
    # Test 1: Search for LASITE
    print("\n1. Searching for LASITE...")
    result = db_search_company.invoke({"letra": "LASITE"})
    print(f"Result: {result}")
    
    # Test 2: Get company info
    print("\n2. Getting LASITE company info...")
    result = db_get_key_metrics.invoke({"ticker": "LASITE", "serie": "*"})
    print(f"Result: {result}")
    
    # Test 3: Get current price
    print("\n3. Getting LASITE current price...")
    result = db_get_price_snapshot.invoke({"ticker": "LASITE", "serie": "*"})
    print(f"Result: {result}")
    
    # Test 4: Get historical prices
    print("\n4. Getting LASITE historical prices (last 7 days)...")
    from datetime import datetime, timedelta
    final = datetime.now().strftime("%Y-%m-%d")
    inicio = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    result = db_get_historical_prices.invoke({
        "ticker": "LASITE",
        "serie": "*",
        "inicio": inicio,
        "final": final
    })
    print(f"Result: {result}")
    
    # Test 5: Get financials
    print("\n5. Getting LASITE income statements (Q4 2024)...")
    result = db_get_income_statements.invoke({
        "ticker": "LASITE",
        "periodo": "4T_2024"
    })
    print(f"Result: {result}")
    
    print("\n" + "=" * 60)
    print("Test complete!")
    print("=" * 60)

if __name__ == "__main__":
    if not os.getenv("DATABURSATIL_API_KEY"):
        print("ERROR: DATABURSATIL_API_KEY not found in environment")
        print("Please set it in your .env file")
        sys.exit(1)
    
    test_databursatil()
