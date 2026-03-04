# Dexter MX - Agente de Investigación Financiera para Mercado Mexicano 🇲🇽

Dexter MX es un agente autónomo de investigación financiera adaptado específicamente para el mercado mexicano. Integra múltiples fuentes de datos (DataBursatil, Yahoo Finance), soporte multi-modelo con OpenRouter, y memoria conversacional para análisis profundos de la Bolsa Mexicana de Valores (BMV) y BIVA.

*Fork de [dexter-free](https://github.com/michaelh03/dexter-free), optimizado para el mercado mexicano*

## 🎯 Diferencias vs. dexter-free original

### Proveedores de Datos
- **Sistema Multi-Fuente**: Fuentes primaria y secundaria con fallback automático
  - **DataBursatil**: Datos premium del mercado mexicano (BMV, BIVA)
  - **Yahoo Finance**: Datos globales gratuitos (incluye tickers .MX)
  - **Financial Datasets**: Mercado estadounidense (opcional)
- **Comando `/source`**: Cambiar fuentes dinámicamente durante el análisis

### Web Search (Nuevo)
- **Exa Search**: Búsqueda neural optimizada para IA
  - Búsqueda de noticias financieras recientes
  - Contexto sobre eventos del mercado
  - Información cualitativa sobre emisoras
- **Comandos**: `web_search`, `web_search_news`

### LLM y Modelos
- **OpenRouter**: Múltiples modelos con una sola API key
- **Comando `/model`**: Cambiar modelos en tiempo real
- **Comparador de Modelos**: Herramienta interactiva para comparar análisis
- **Modelos soportados**: GPT-5.x, Claude 4.x, Gemini 3.x, DeepSeek, Grok, y más

### Optimizaciones para México
- **Memoria Conversacional**: Contexto entre queries para análisis profundos
- **Límites Extendidos**: `max_steps=300` para análisis complejos (múltiples FIBRAs)
- **Validación Optimizada**: Manejo inteligente de datos parciales en Yahoo Finance
- **Soporte FIBRAs**: Manejo especial para FIBRAs mexicanas con datos limitados

## 📋 Requisitos

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (opcional pero recomendado)

## 🚀 Instalación

### Setup Local

```bash
git clone https://github.com/ingsamcas/dexter-mx.git
cd dexter-mx

# Instalar dependencias
uv sync

# Configurar variables de entorno
cp env.example .env
# Editar .env con tus API keys
```

### Setup con Docker (Recomendado)

```bash
# Build
docker build -t dexter-mx .

# Run con modo interactivo
./dexter.sh compare
```

## 💡 Uso

### Modo Comparador Interactivo (Recomendado)

```bash
./dexter.sh compare
```

**Comandos disponibles:**
- `/model <nombre>` - Cambiar modelo LLM
- `/models` - Ver modelos disponibles
- `/source primary <fuente>` - Cambiar fuente primaria
- `/source secondary <fuente>` - Cambiar fuente secundaria
- `/sources` - Ver fuentes de datos disponibles
- `/history` - Ver historial de conversación
- `/clear` - Limpiar historial
- `/quit` - Salir

### Modo Agente Directo

```bash
./dexter.sh agent
```

### Ejemplo de Uso Completo

```bash
🚀 DEXTER - Comparador con Memoria Conversacional

[gpt-5.2] >>> /source primary databursatil
✓ Primary source: yfinance → databursatil

[gpt-5.2] >>> /source secondary yahoo
✓ Secondary source: yfinance → yahoo

[gpt-5.2] >>> Analyze the fundamentals of AMXL, WALMEX and BIMBOA

[Agent ejecuta análisis con DataBursatil como fuente primaria...]

[gpt-5.2] >>> /model claude-sonnet-46
✓ Modelo cambiado: gpt-5.2 → claude-sonnet-4.6

[claude-sonnet-4.6] >>> Compare the ROE of the 3 companies

[Agent continúa con contexto previo usando Claude...]

[claude-sonnet-4.6] >>> continue with debt analysis

[Agent usa memoria conversacional para entender "continue"...]
```

## ⚙️ Variables de Entorno

### Requeridas

```bash
# LLM Provider
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_MODEL=openai/gpt-5.2

# Data Source (al menos una)
DATABURSATIL_API_KEY=db_...
# o usar Yahoo Finance (gratis, no requiere key)
```

### Opcionales

```bash
# Configuración de fuentes
PRIMARY_DATA_SOURCE=databursatil
SECONDARY_DATA_SOURCE=yfinance

# Financial Datasets (datos US, requiere pago)
FINANCIAL_DATASETS_API_KEY=fd_...
```

## 📊 Fuentes de Datos Disponibles

| Fuente | Mercados | Costo | API Key | Cobertura |
|--------|----------|-------|---------|-----------|
| **DataBursatil** | México (BMV, BIVA) | Pago | ✓ | Excelente para tickers MX |
| **Yahoo Finance** | Global (incluye .MX) | Gratis | ✗ | Buena, puede tener gaps |
| **Financial Datasets** | USA | Pago | ✓ | Excelente para tickers US |

### Cobertura por Ticker

**Tickers Mexicanos**: `AMXL.MX`, `WALMEX.MX`, `BIMBOA.MX`, `FCFE18.MX` (FIBRAs)
- **Mejor con**: DataBursatil (datos más completos)
- **Alternativa**: Yahoo Finance (puede tener gaps en FIBRAs)

**Tickers US**: `AAPL`, `TSLA`, `MSFT`
- **Mejor con**: Financial Datasets o Yahoo Finance
- **DataBursatil**: Cobertura limitada

## 🏗️ Arquitectura

```
dexter-mx/
├── src/
│   └── dexter/
│       ├── agent.py              # Agent core con multi-source
│       ├── model.py              # OpenRouter integration
│       ├── prompts.py            # Optimized prompts
│       ├── data_sources.py       # Multi-source manager
│       └── tools/
│           ├── yf_*.py           # Yahoo Finance tools
│           ├── databursatil/     # DataBursatil integration
│           │   ├── api.py
│           │   ├── db_prices.py
│           │   ├── db_financials.py
│           │   └── db_metrics.py
│           └── web_search/       # Exa Search integration
│               └── exa_search.py
├── interactive_compare_with_memory.py  # Interactive CLI
├── dexter.sh                     # Docker wrapper
└── Dockerfile
```

## 🛠️ Desarrollo

### Agregar nueva fuente de datos

1. Crear módulo en `src/dexter/tools/nuevafuente/`
2. Implementar herramientas siguiendo patrón `@tool`
3. Registrar en `src/dexter/tools/__init__.py`
4. Agregar a `DataSource` enum en `data_sources.py`

### Testing

```bash
uv run pytest
```

## 🗺️ Roadmap

- [x] Integración DataBursatil
- [x] Sistema multi-source con fallback
- [x] Comandos interactivos `/model` y `/source`
- [x] Memoria conversacional
- [x] Exa Search para noticias y contexto
- [ ] Integración Lápiz API
- [ ] Export de reportes PDF
- [ ] Bot de WhatsApp
- [ ] API REST service
- [ ] Migración a Kotlin

## 📝 Queries de Ejemplo

Prueba preguntas como:

**Mercado Mexicano:**
- "What was AMXL's revenue growth over the last 4 quarters?"
- "Compare WALMEX and BIMBOA's operating margins for 2023"
- "Analyze FCFE18 cash flow trends over the past year"

**Análisis Comparativo:**
- "Compare the top 3 FIBRAs in Mexico by market cap"
- "What are the key differences between AMXL and TELMEX?"

**Con Memoria Conversacional:**
1. "Analyze WALMEX fundamentals"
2. "continue with profitability analysis"
3. "compare with its main competitor"

## 🤝 Contribuir

1. Fork el repositorio
2. Crea una rama: `git checkout -b feat/amazing-feature`
3. Commit cambios: `git commit -m "feat: add amazing feature"`
4. Push a tu branch: `git push origin feat/amazing-feature`
5. Abre un Pull Request

**Importante**: PRs pequeños y enfocados para facilitar review.

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 🙏 Créditos

Basado en:
- [dexter](https://github.com/virattt/dexter) por @virattt
- [dexter-free](https://github.com/michaelh03/dexter-free) por @michaelh03

Adaptado para el mercado mexicano por [@ingsamcas](https://github.com/ingsamcas).

## 📞 Soporte

¿Preguntas? Abre un [Issue](https://github.com/ingsamcas/dexter-mx/issues) o contáctame en Twitter.

---

**⚠️ Aviso**: Este software es para fines informativos. No constituye asesoría financiera. Siempre consulta con un profesional certificado antes de tomar decisiones de inversión.
