"""
Agente de Chat - Lógica del chatbot IA (ratón hincha del Deportivo Cali).
"""
from core.prompts import SYSTEM_PROMPT
from api.llm_client import chat

MAX_HISTORY = 20

# Respuestas exactas para preguntas específicas (sin llamar a la API)
CANNED_RESPONSES = [
    (["jupiter", "lunas", "cuantas lunas"], "No tengo ni idea mi papacho, que seguro tendrán muchas pero nunca serán más grandes que las 10 estrellas del glorioso. !SOLO VERDEEEEEEEEEEE¡"),
    (["mil y una noches", "quien escribió", "escribió las mil"], "Eso está entre Gabriel García Márquez, Rafael Dudamel y Harold Preciado, parce. !SOLO VERDEEEEEEEEEEE¡"),
    (["tron", "es tron bueno", "tron es buena"], "No sé qué es peor, si tron o el América. !SOLO VERDEEEEEEEEEEE¡"),
]


def _get_canned_response(message: str):
    """Si el mensaje coincide con una pregunta conocida, devuelve la respuesta exacta."""
    msg = message.lower().strip()
    for keywords, response in CANNED_RESPONSES:
        if any(kw in msg for kw in keywords):
            return response
    return None


class ChatAgent:
    """Maneja la conversación con la IA usando prompts y historial."""

    def __init__(self):
        self.history: list[dict] = []  # [{"role": "user"|"assistant", "content": "..."}]

    def get_response(self, user_message: str) -> str:
        """Envía el mensaje del usuario, obtiene la respuesta y actualiza el historial."""
        canned = _get_canned_response(user_message)
        if canned:
            self.history.append({"role": "user", "content": user_message})
            self.history.append({"role": "assistant", "content": canned})
            return canned

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            *self._get_recent_history(),
            {"role": "user", "content": user_message},
        ]

        response = chat(messages)

        # Guardar en historial
        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": response})

        return response

    def _get_recent_history(self) -> list[dict]:
        """Devuelve los últimos N intercambios para no exceder tokens."""
        if len(self.history) <= MAX_HISTORY * 2:
            return self.history
        return self.history[-(MAX_HISTORY * 2):]

    def clear_history(self):
        """Limpia el historial de la conversación."""
        self.history.clear()
