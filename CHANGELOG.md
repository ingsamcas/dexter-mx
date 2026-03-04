# Changelog

Todos los cambios notables a este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

## [1.0.0] - 2026-03-03

### Added

#### Core Features
- **OpenRouter Integration**: Soporte para múltiples modelos LLM con una sola API key
  - GPT-5.x series (nano, mini, 5.2, pro)
  - Claude 4.x series (Opus, Sonnet, Haiku)
  - Gemini 3.x series (Pro, Flash)
  - DeepSeek R1
  - xAI Grok (3, 4, mini)
  - Y más modelos disponibles
- **DataBursatil API Integration**: Cliente completo para el mercado mexicano
  - Precios en tiempo real (`db_get_price_snapshot`)
  - Precios históricos (`db_get_historical_prices`)
  - Estados financieros (`db_get_income_statements`, `db_get_balance_sheets`, `db_get_cash_flow`)
  - Métricas clave (`db_get_key_metrics`)
- **Multi-Source Data System**: Sistema de fuentes primaria/secundaria con fallback automático
  - Soporte para Yahoo Finance, DataBursatil y Financial Datasets
  - Cambio dinámico de fuentes vía comando `/source`
  - Validación automática de API keys

#### Interactive Features
- **Memoria Conversacional**: Contexto entre queries para análisis profundos
  - Historial de últimas 3 conversaciones
  - Soporte para comandos como "continue", "more details", "elaborate"
- **Comandos Interactivos**:
  - `/model <nombre>` - Cambiar modelo LLM en tiempo real
  - `/models` - Ver todos los modelos disponibles
  - `/source primary <fuente>` - Cambiar fuente primaria
  - `/source secondary <fuente>` - Cambiar fuente secundaria
  - `/sources` - Ver fuentes de datos disponibles
  - `/history` - Ver historial de conversación
  - `/clear` - Limpiar historial
  - `/quit` - Salir guardando sesión
- **Session Persistence**: Auto-guardado de sesiones en JSON
  - Timestamp, modelo usado, queries y respuestas
  - Directorio configurable (`./sessions` o `/app/sessions`)

#### Infrastructure
- **Docker Support**: Dockerfile completo con Python 3.11
  - Soporte para `uv` package manager
  - Volúmenes para persistencia de sesiones
- **Docker Wrapper Script** (`dexter.sh`):
  - Modo `compare`: Interactive CLI con memoria
  - Modo `compare-simple`: CLI sin memoria
  - Modo `agent`: CLI original de dexter
- **Scripts de Comparación**:
  - `interactive_compare_with_memory.py`: Full-featured
  - `interactive_compare_fixed.py`: Versión simplificada

### Changed

#### Optimizations for Mexican Market
- **Validation Prompts**: Optimizados para manejar datos parciales
  - Lógica mejorada para detección de tareas completadas
  - Manejo especial cuando herramientas retornan datos parciales
  - Prevención de loops infinitos con datos limitados de FIBRAs
- **Agent Limits**: Extendidos para análisis complejos
  - `max_steps`: 20 → 300 (15x aumento)
  - `max_steps_per_task`: 5 → 60 (12x aumento)
  - Ideal para análisis multi-ticker de FIBRAs mexicanas
- **Environment Variables**: Actualizadas para reflejar nueva arquitectura
  - `OPENROUTER_API_KEY` y `OPENROUTER_MODEL`
  - `PRIMARY_DATA_SOURCE` y `SECONDARY_DATA_SOURCE`
  - `DATABURSATIL_API_KEY`

#### Improved UX
- Interfaz CLI más informativa con emojis y separadores
- Mensajes de error más claros y accionables
- Feedback en tiempo real de cambios de modelo/fuente
- Contador de mensajes en historial conversacional

### Fixed
- Manejo robusto de errores de API (rate limiting, timeouts, 404s)
- Validación de API keys al inicio para prevenir errores tardíos
- Recargar dinámico del módulo `model` al cambiar `OPENROUTER_MODEL`

### Technical Details

#### Dependencies
- `langchain>=0.3.27`
- `langchain-openai>=0.3.35`
- `openai>=2.2.0`
- `prompt-toolkit>=3.0.0`
- `pydantic>=2.11.10`
- `python-dotenv>=1.1.1`
- `requests>=2.32.5`
- `yfinance>=0.2.66`

#### Architecture
- Python 3.11+ requerido
- Modular tool-based architecture
- Enum-based data source management
- Type-safe with Pydantic models

### Based On

Este release está basado en:
- [dexter](https://github.com/virattt/dexter) - Agent framework original
- [dexter-free](https://github.com/michaelh03/dexter-free) - Yahoo Finance integration

### Contributors

- [@ingsamcas](https://github.com/ingsamcas) - Adaptación para mercado mexicano
- Basado en trabajo de [@virattt](https://github.com/virattt) y [@michaelh03](https://github.com/michaelh03)

---

## [Unreleased]

### Planned Features
- Integración con Lápiz API
- Export de reportes en PDF
- Bot de WhatsApp
- API REST service
- Migración gradual a Kotlin

---

**Formato de versiones**: `MAJOR.MINOR.PATCH`
- **MAJOR**: Cambios incompatibles en la API
- **MINOR**: Nueva funcionalidad compatible con versiones anteriores
- **PATCH**: Correcciones de bugs compatibles con versiones anteriores
