"""
Cliente para API de Google Gemini (google-genai SDK).

Usa GEMINI_API_KEY desde .env o variable de entorno.
"""
import sys
import time
import traceback

from config.settings import GEMINI_API_KEY, GEMINI_MODEL

MSG_ERROR = "Lo siento manito estoy en el estadio, más tarde te respondo"


def _log_error(e: Exception, context: str = ""):
    """Muestra el error real por consola."""
    print("\n[GEMINI API ERROR]", context, file=sys.stderr)
    print(str(e), file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    print(file=sys.stderr)


def chat(messages: list[dict]) -> str:
    """Envía mensajes a Gemini y devuelve la respuesta."""
    if not GEMINI_API_KEY:
        print("\n[GEMINI] No hay GEMINI_API_KEY configurada en .env", file=sys.stderr)
        return MSG_ERROR

    try:
        from google import genai

        client = genai.Client(api_key=GEMINI_API_KEY)

        system = _get_system_from_messages(messages)
        turns = _get_user_turns(messages)
        if not turns:
            return ""

        prompt = _build_prompt(system, turns)

        return _generate_with_retry(client, prompt)
    except Exception as e:
        _log_error(e, "Al conectar/enviar:")
        return MSG_ERROR


def _generate_with_retry(client, prompt: str, max_retries: int = 2) -> str:
    """Reintenta si hay 429 (cuota agotada)."""
    for attempt in range(max_retries + 1):
        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )
            return (response.text or "").strip()
        except Exception as e:
            err = str(e).lower()
            if ("429" in err or "resource_exhausted" in err) and attempt < max_retries:
                time.sleep(35)
                continue
            _log_error(e, "Al generar contenido:")
            return MSG_ERROR


def _get_system_from_messages(messages):
    for m in messages:
        if m.get("role") == "system":
            return m["content"]
    return ""


def _get_user_turns(messages):
    turns = []
    for m in messages:
        role, content = m.get("role"), m.get("content", "")
        if role in ("user", "assistant"):
            turns.append((role, content))
    return turns


def _build_prompt(system: str, turns: list) -> str:
    """Construye el prompt con contexto y historial."""
    parts = []
    if system:
        parts.append(f"[Contexto del asistente: {system}]\n")
    for role, content in turns:
        label = "Usuario" if role == "user" else "Asistente"
        parts.append(f"{label}: {content}")
    return "\n\n".join(parts)
