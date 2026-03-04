#!/usr/bin/env python3
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

from dexter.agent import Agent

# Modelos categorizados por proveedor y capacidad
MODELS = {
    # OpenAI (mejor compatibilidad con tools)
    "gpt5": "openai/gpt-5",
    "gpt52": "openai/gpt-5.2",
    "gpt52-pro": "openai/gpt-5.2-pro",
    "gpt5-mini": "openai/gpt-5-mini",
    "gpt5-nano": "openai/gpt-5-nano",
    
    # Anthropic Claude (puede tener problemas con tools via Bedrock)
    "claude-sonnet-46": "anthropic/claude-sonnet-4.6",
    "claude-opus-46": "anthropic/claude-opus-4.6",
    "claude-sonnet-45": "anthropic/claude-sonnet-4.5",
    "claude-haiku-45": "anthropic/claude-haiku-4.5",
    
    # Google Gemini (buena compatibilidad)
    "gemini-3-flash": "google/gemini-3-flash-preview",
    "gemini-3-pro": "google/gemini-3-pro-preview",
    "gemini-31-pro": "google/gemini-3.1-pro-preview",
    "gemini-25-flash": "google/gemini-2.5-flash-lite",
    
    # DeepSeek (excelente relación calidad/precio)
    "deepseek": "deepseek/deepseek-r1",
    
    # xAI Grok
    "grok4": "x-ai/grok-4",
    "grok3": "x-ai/grok-3",
    "grok3-mini": "x-ai/grok-3-mini",
    
    # Otros modelos populares
    "llama-33": "meta-llama/llama-3.3-70b-instruct",
    "mistral-large": "mistralai/mistral-large",
    "qwen3": "qwen/qwen3-235b-a22b",
    "perplexity": "perplexity/sonar",
    
    # Auto Router (deja que OpenRouter elija)
    "auto": "openrouter/auto",
}

current_model = "openai/gpt-5.2"
session_log = []

def run_query(query: str):
    """Ejecuta query con el Agent completo (con tools)"""
    print(f"\n{'='*60}")
    print(f"🤖 Modelo: {current_model}")
    print(f"📊 Query: {query}")
    print(f"{'='*60}\n")
    
    os.environ["OPENROUTER_MODEL"] = current_model
    
    import importlib
    from dexter import model
    importlib.reload(model)
    
    try:
        agent = Agent(data_provider="yfinance")
        result = agent.run(query)
        
        if isinstance(result, dict):
            answer = result.get("answer", str(result))
            tasks = result.get("tasks", [])
        else:
            answer = str(result)
            tasks = []
        
        session_log.append({
            "timestamp": datetime.now().isoformat(),
            "model": current_model,
            "query": query,
            "answer": answer,
            "tasks": tasks,
            "success": True
        })
        
        print(f"\n✅ Respuesta registrada\n")
        
    except Exception as e:
        session_log.append({
            "timestamp": datetime.now().isoformat(),
            "model": current_model,
            "query": query,
            "error": str(e),
            "success": False
        })
        print(f"\n❌ Error: {str(e)}\n")

def save_session():
    filename = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(session_log, f, indent=2)
    print(f"\n💾 Guardado: {filename}\n")
    return filename

def set_model(model_name: str):
    global current_model
    if model_name.lower() in MODELS:
        current_model = MODELS[model_name.lower()]
        print(f"\n✅ Modelo: {current_model}\n")
    else:
        print(f"\n❌ Modelo no encontrado. Use /models para ver opciones.\n")

def show_models():
    print("\n" + "="*60)
    print("📋 MODELOS DISPONIBLES")
    print("="*60)
    
    categories = {
        "OpenAI": ["gpt5", "gpt52", "gpt52-pro", "gpt5-mini", "gpt5-nano"],
        "Anthropic": ["claude-sonnet-46", "claude-opus-46", "claude-sonnet-45", "claude-haiku-45"],
        "Google": ["gemini-3-flash", "gemini-3-pro", "gemini-31-pro", "gemini-25-flash"],
        "DeepSeek": ["deepseek"],
        "xAI": ["grok4", "grok3", "grok3-mini"],
        "Otros": ["llama-33", "mistral-large", "qwen3", "perplexity", "auto"],
    }
    
    for category, models in categories.items():
        print(f"\n{category}:")
        for alias in models:
            mark = "👉" if MODELS[alias] == current_model else "  "
            print(f"{mark} {alias:<18} → {MODELS[alias]}")
    
    print("\n" + "="*60 + "\n")

def main():
    print("\n" + "="*60)
    print("🚀 DEXTER - Comparador de Modelos Financieros")
    print("="*60)
    print("\nComandos:")
    print("  /model <nombre>   - Cambiar modelo")
    print("  /models           - Ver todos los modelos")
    print("  /save             - Guardar sesión")
    print("  /quit             - Salir y guardar")
    print("\n⚠️  IMPORTANTE: Haz preguntas en INGLÉS")
    print("\nEjemplos:")
    print("  - What is TSLA's current stock price?")
    print("  - Get AMXL.MX revenue for last quarter")
    print("  - Compare WALMEX.MX and OXXO.MX margins")
    print("="*60 + "\n")
    
    show_models()
    
    while True:
        try:
            inp = input(f"[{current_model.split('/')[-1]}] >>> ").strip()
            
            if inp.startswith("/model "):
                set_model(inp.split("/model ")[1])
            elif inp == "/models":
                show_models()
            elif inp == "/save":
                filename = save_session()
                print(f"Sesión guardada en: {filename}")
            elif inp in ["/quit", "/q", "/exit"]:
                filename = save_session()
                print(f"Sesión guardada en: {filename}")
                print("👋 ¡Hasta luego!\n")
                break
            elif inp:
                run_query(inp)
        
        except (KeyboardInterrupt, EOFError):
            filename = save_session()
            print(f"\n\nSesión guardada en: {filename}")
            print("👋 ¡Hasta luego!\n")
            break

if __name__ == "__main__":
    main()
