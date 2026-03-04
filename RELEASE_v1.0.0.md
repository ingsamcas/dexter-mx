# Release Notes for v1.0.0

Create this release manually on GitHub: https://github.com/ingsamcas/dexter-mx/releases/new?tag=v1.0.0

---

## Title
v1.0.0 - DataBursatil Integration

## Description

# Dexter MX v1.0.0 - Mexican Market Edition

## 🎉 First Public Release

This is the first production release of **Dexter MX**, a fork of Dexter optimized for the Mexican financial market.

## ✨ Key Features

### DataBursatil API Integration
- Complete integration with DataBursatil API v2
- Access to real-time and historical data from BMV and BIVA
- 7 specialized tools for Mexican stock analysis

### Supported Data
- **Current Prices**: Real-time quotes from BMV/BIVA
- **Historical Prices**: Daily historical data
- **Financial Statements**: 
  - Estado de Resultados (Income Statement)
  - Estado de Situación Financiera (Balance Sheet)
  - Estado de Flujo de Efectivo (Cash Flow)
- **Company Information**: ISIN, shares outstanding, status, etc.

### Multi-Source Architecture
- **Primary**: DataBursatil (when API key configured)
- **Fallback**: Yahoo Finance
- Automatic provider selection and failover

## 🚀 Getting Started

### Prerequisites
- Docker (recommended) or Python 3.11+
- DataBursatil API key (get from https://databursatil.com)
- OpenRouter API key (for LLM access)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/ingsamcas/dexter-mx.git
cd dexter-mx

# Create .env file
cp env.example .env
# Edit .env and add your API keys

# Run with Docker
docker build -t dexter-mx .
docker run -it --env-file .env dexter-mx

# Or run directly
uv sync
uv run python interactive_compare_with_memory.py
```

## 📊 Supported Mexican Tickers

Works with all BMV/BIVA listed companies:
- LASITE, WALMEX, BIMBOA, AMXL, GFNORTEO, CEMEXCPO
- FIBRAs: FCFE18, FIHO12, FINN13, etc.
- And many more...

## 🧪 Testing

```bash
# Test DataBursatil integration
uv run python test_databursatil.py

# Full agent test
./dexter.sh compare
```

## 📚 Documentation

- [Testing Guide](TESTING_DATABURSATIL.md)
- [Git Flow Strategy](.github/GIT_FLOW.md)
- [DataBursatil API Docs](https://databursatil.com/docs.html)

## 🐛 Known Issues

- Some Pydantic validation warnings (cosmetic, doesn't affect functionality)
- Historical data may fail for very old date ranges
- HTTP 400 errors for future quarters (expected behavior)

## 🙏 Credits

- Original Dexter: https://github.com/virattt/dexter
- Based on: Dexter-Free (Python fork)
- DataBursatil: https://databursatil.com
- OpenRouter: https://openrouter.ai

## 📝 License

MIT License (same as original Dexter)

---

**Made with ❤️ for the Mexican financial community**
