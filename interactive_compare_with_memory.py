#!/usr/bin/env python3
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from dexter.agent import Agent
from dexter.data_sources import DataSourceManager, DataSource

SESSIONS_DIR = "/app/sessions" if os.path.exists("/app/sessions") else "./sessions"
os.makedirs(SESSIONS_DIR, exist_ok=True)

# Inicializar manager de fuentes de datos
# Si DATABURSATIL_API_KEY existe, usar databursatil como primaria
try:
    if os.getenv("DATABURSATIL_API_KEY"):
        data_source_manager = DataSourceManager(
            primary=DataSource.DATABURSATIL,
            secondary=DataSource.YAHOO_FINANCE
        )
        print("🇲🇽 DataBursatil detectado - configurado como fuente primaria")
    else:
        data_source_manager = DataSourceManager.from_env()
        print("📊 Yahoo Finance configurado como fuente primaria (gratis)")
except ValueError as e:
    # Si falla (ej. falta API key), usar Yahoo Finance
    data_source_manager = DataSourceManager(
        primary=DataSource.YAHOO_FINANCE,
        secondary=DataSource.YAHOO_FINANCE
    )
    print(f"⚠️  {str(e)} - usando Yahoo Finance")

# MODELOS COMPLETOS
MODELS = {
    # OpenAI (mejor compatibilidad con tools)
    "gpt5": "openai/gpt-5",
    "gpt52": "openai/gpt-5.2",
    "gpt52-pro": "openai/gpt-5.2-pro",
    "gpt5-mini": "openai/gpt-5-mini",
    "gpt5-nano": "openai/gpt-5-nano",
    
    # Anthropic Claude (puede tener problemas con algunos parámetros)
    "claude-sonnet-46": "anthropic/claude-sonnet-4.6",
    "claude-opus-46": "anthropic/claude-opus-4.6",
    "claude-sonnet-45": "anthropic/claude-sonnet-4.5",
    "claude-haiku-45": "anthropic/claude-haiku-4.5",
    
    # Google Gemini (buena compatibilidad)
    "gemini-3-flash": "google/gemini-3-flash-preview",
    "gemini-3-pro": "google/gemini-3-pro-preview",
    "gemini-31-pro": "google/gemini-3.1-pro-preview",
    "gemini-25-flash": "google/gemini-2.5-flash-lite",
    
    # DeepSeek (excelente precio/calidad)
    "deepseek": "deepseek/deepseek-r1",
    
    # xAI Grok
    "grok4": "x-ai/grok-4",
    "grok3": "x-ai/grok-3",
    "grok3-mini": "x-ai/grok-3-mini",
    
    # Otros modelos
    "llama-33": "meta-llama/llama-3.3-70b-instruct",
    "mistral-large": "mistralai/mistral-large",
    "qwen3": "qwen/qwen3-235b-a22b",
    "perplexity": "perplexity/sonar",
    
    # Auto Router
    "auto": "openrouter/auto",
}

current_model = "openai/gpt-5.2"
session_log = []
session_file = None
conversation_history = []

def init_session():
    global session_file
    session_file = os.path.join(
        SESSIONS_DIR, 
        f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    print(f"📝 Sesión: {session_file}\n")

def save_session():
    if not session_file or not session_log:
        return
    
    with open(session_file, 'w') as f:
        json.dump({
            "created": datetime.now().isoformat(),
            "model": current_model,
            "queries": session_log,
            "conversation": conversation_history
        }, f, indent=2)

def build_contextual_query(query: str) -> str:
    """Construye query con contexto de conversación previa"""
    if not conversation_history:
        return query
    
    recent = conversation_history[-3:]
    context = "\n".join([
        f"Previous Q: {h['query']}\nPrevious A: {h['answer'][:200]}..."
        for h in recent
    ])
    
    return f"""Context from previous questions:
{context}

Current question: {query}

If the current question refers to "continue", "more details", "elaborate", or similar, 
use the context above to understand what the user wants to continue with."""

def run_query(query: str):
    print(f"\n{'='*60}")
    print(f"🤖 Modelo: {current_model}")
    print(f"📊 Query: {query}")
    print(f"🔍 Fuente: {data_source_manager.get_primary_provider()} (fallback: {data_source_manager.get_secondary_provider()})")
    print(f"{'='*60}\n")
    
    os.environ["OPENROUTER_MODEL"] = current_model
    
    import importlib
    from dexter import model
    importlib.reload(model)
    
    try:
        contextual_query = build_contextual_query(query)
        
        agent = Agent(
            data_provider=data_source_manager.get_primary_provider(),
            max_steps=300,             # 3x de 100
            max_steps_per_task=60      # 3x de 20
        )
        
        result = agent.run(contextual_query)
        
        if isinstance(result, dict):
            answer = result.get("answer", str(result))
            tasks = result.get("tasks", [])
        else:
            answer = str(result)
            tasks = []
        
        conversation_history.append({
            "query": query,
            "answer": answer,
            "model": current_model,
            "timestamp": datetime.now().isoformat()
        })
        
        session_log.append({
            "timestamp": datetime.now().isoformat(),
            "model": current_model,
            "query": query,
            "contextual_query": contextual_query if len(conversation_history) > 1 else query,
            "answer": answer,
            "tasks": tasks,
            "success": True
        })
        
        save_session()
        print(f"\n✅ Guardado (conversación: {len(conversation_history)} mensajes)\n")
        
    except Exception as e:
        session_log.append({
            "timestamp": datetime.now().isoformat(),
            "model": current_model,
            "query": query,
            "error": str(e),
            "success": False
        })
        save_session()
        print(f"\n❌ Error: {str(e)}\n")

def set_model(model_name: str):
    global current_model
    if model_name.lower() in MODELS:
        current_model = MODELS[model_name.lower()]
        print(f"\n✅ Modelo: {current_model}\n")
    else:
        print(f"\n❌ Use /models\n")

def show_models():
    print("\n" + "="*60)
    print("📋 MODELOS DISPONIBLES")
    print("="*60)
    
    categories = {
        "OpenAI": ["gpt5", "gpt52", "gpt52-pro", "gpt5-mini", "gpt5-nano"],
        "Anthropic Claude": ["claude-sonnet-46", "claude-opus-46", "claude-sonnet-45", "claude-haiku-45"],
        "Google Gemini": ["gemini-3-flash", "gemini-3-pro", "gemini-31-pro", "gemini-25-flash"],
        "DeepSeek": ["deepseek"],
        "xAI Grok": ["grok4", "grok3", "grok3-mini"],
        "Otros": ["llama-33", "mistral-large", "qwen3", "perplexity", "auto"],
    }
    
    for category, models in categories.items():
        print(f"\n{category}:")
        for alias in models:
            mark = "👉" if MODELS[alias] == current_model else "  "
            print(f"{mark} {alias:<18} → {MODELS[alias]}")
    
    print("\n⚠️  Nota: Claude puede tener errores con tools (problema conocido)")
    print("="*60 + "\n")

def show_history():
    if not conversation_history:
        print("\n📭 No hay historial aún\n")
        return
    
    print(f"\n{'='*60}")
    print(f"📜 HISTORIAL ({len(conversation_history)} mensajes)")
    print(f"{'='*60}")
    
    for i, entry in enumerate(conversation_history[-5:], 1):
        print(f"\n{i}. Q: {entry['query']}")
        print(f"   A: {entry['answer'][:150]}...")
        print(f"   [{entry['model'].split('/')[-1]}]")
    
    print(f"{'='*60}\n")

def clear_history():
    global conversation_history
    conversation_history = []
    print("\n🗑️  Historial limpiado\n")

def show_sources():
    print("\n" + "="*60)
    print("📊 FUENTES DE DATOS")
    print("="*60)
    print(f"\n  Primary:   {data_source_manager.get_primary_provider()} 👉")
    print(f"  Secondary: {data_source_manager.get_secondary_provider()}")
    print("\nDisponibles:")
    print("  yahoo        → Yahoo Finance (gratis)")
    print("  databursatil → DataBursatil (premium MX)")
    print("  financialdatasets → Financial Datasets (premium US)")
    print("\nUso:")
    print("  /source primary yahoo")
    print("  /source secondary databursatil")
    print("="*60 + "\n")

def switch_source(level: str, source_name: str):
    try:
        new_source = DataSource(source_name)
        if level == "primary":
            msg = data_source_manager.switch_primary(new_source)
        elif level == "secondary":
            msg = data_source_manager.switch_secondary(new_source)
        else:
            print("❌ Level must be 'primary' or 'secondary'")
            return
        print(f"\n✓ {msg}\n")
    except ValueError as e:
        print(f"\n❌ Error: {str(e)}")
        print("   Valid sources: yahoo, databursatil, financialdatasets\n")

def main():
    init_session()
    
    print("🚀 DEXTER - Comparador con Memoria Conversacional")
    print("\nComandos:")
    print("  /model <nombre>  - Cambiar modelo")
    print("  /models          - Ver todos los modelos")
    print("  /source primary <fuente>   - Cambiar fuente primaria")
    print("  /source secondary <fuente> - Cambiar fuente secundaria")
    print("  /sources         - Ver fuentes disponibles")
    print("  /history         - Ver historial")
    print("  /clear           - Limpiar historial")
    print("  /quit            - Salir")
    print("\n⚠️  IMPORTANTE: Preguntas en INGLÉS")
    print("✨ NUEVO: Memoria conversacional - usa 'continue', 'more details', etc.\n")
    
    show_models()
    show_sources()
    
    while True:
        try:
            inp = input(f"[{current_model.split('/')[-1]}] >>> ").strip()
            
            if inp.startswith("/model "):
                set_model(inp.split("/model ")[1])
            elif inp == "/models":
                show_models()
            elif inp.startswith("/source "):
                parts = inp.split()
                if len(parts) == 3:
                    switch_source(parts[1], parts[2])
                else:
                    print("\n❌ Uso: /source [primary|secondary] [yahoo|databursatil|financialdatasets]\n")
            elif inp == "/sources":
                show_sources()
            elif inp == "/history":
                show_history()
            elif inp == "/clear":
                clear_history()
            elif inp in ["/quit", "/q"]:
                save_session()
                print(f"\n💾 Sesión guardada: {session_file}")
                print("👋 ¡Hasta luego!\n")
                break
            elif inp:
                run_query(inp)
        
        except (KeyboardInterrupt, EOFError):
            save_session()
            print(f"\n\n💾 Guardado: {session_file}\n")
            break

if __name__ == "__main__":
    main()
