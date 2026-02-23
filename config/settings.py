"""
Configuración centralizada del proyecto.
Carga variables desde .env (nunca subas .env a Git).
"""
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    # Cargar .env desde la raíz del proyecto
    env_path = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_path)
    # Por si se ejecuta desde otro directorio
    if not os.getenv("GEMINI_API_KEY"):
        load_dotenv(Path.cwd() / ".env")
except ImportError:
    pass

# API de Google Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# Modelo que funciona: gemini-2.0-flash (verifica en ai.google.dev)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
