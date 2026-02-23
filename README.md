# Ratoncito buscando la Libertadores

Agente de reacción simple: el ratoncito hincha del Deportivo Cali busca la Copa Libertadores en un laberinto. Incluye chat con IA (Gemini) que responde como hincha caleño.

## Requisitos

- Python 3.9 o superior
- pip

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración de la API (chat)

El chat usa **Google Gemini**. Necesitas una API Key.

### 1. Obtener la API Key

1. Ve a [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Inicia sesión con tu cuenta de Google
3. Haz clic en **Create API Key**
4. Copia la clave (empieza con `AIza...`)

### 2. Crear el archivo `.env`

En la **raíz del proyecto** (donde está `main.py`), crea un archivo `.env`:

```
GEMINI_API_KEY=tu_clave_aqui
```

**Importante:**
- El archivo se llama exactamente `.env` (con punto al inicio)
- Sin comillas, sin espacios alrededor del `=`
- Sustituye `tu_clave_aqui` por tu clave real

**Ejemplo:**
```
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Modelo (opcional)

Por defecto se usa `gemini-2.0-flash`. Para cambiar, añade en `.env`:

```
GEMINI_MODEL=gemini-2.0-flash
```

Otros modelos: `gemini-1.5-flash`, `gemini-2.5-flash`, `gemini-2.5-pro`.

Si ves error **429** (cuota agotada), espera unos minutos o prueba otro modelo.

### 4. Plantilla

Puedes copiar `env.ejemplo` como base:

```bash
# Windows (PowerShell)
copy env.ejemplo .env

# Linux / Mac
cp env.ejemplo .env
```

Luego edita `.env` y pon tu API key. **No subas `.env` a Git.**

## Ejecutar

```bash
python main.py
```

Se abrirá la aplicación en el navegador. Puedes:

- **Cargar**: Abrir modal para crear/cargar laberinto (grid 10×10 o CSV)
- **Random**: Generar laberinto aleatorio
- **Buscar**: Ejecutar la búsqueda automática del ratón
- **Chat**: Hablar con el Ratoncito del Cali (requiere API key configurada)

## Formato del laberinto

Matriz 10×10. Valores: `0`=camino, `1`=pared, `2`=queso (meta), `3`=ratón (inicio).

## Estructura del proyecto

```
├── main.py              # Punto de entrada
├── .env                 # API key (no subir a Git)
├── env.ejemplo          # Plantilla para .env
├── config/settings.py   # Carga GEMINI_API_KEY, GEMINI_MODEL
├── api/llm_client.py    # Cliente Gemini
├── core/
│   ├── prompts.py       # Personalidad del chat
│   └── chat_agent.py    # Lógica del chat
├── agent/               # Laberinto y agente de búsqueda
└── ui_webview/          # Interfaz Eel (HTML)
```
