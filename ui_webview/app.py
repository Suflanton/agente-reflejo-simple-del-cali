"""
Aplicación principal Eel - Ratoncito buscando la Libertadores
Usa Eel para mostrar HTML en Chrome/Edge y exponer la API Python.
No requiere pythonnet (evita problemas de instalación en Windows).
"""
import eel
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / "media"
DEFAULT_MAZE_PATH = MEDIA_DIR / "default_labyrinth" / "laberinto.csv"
BACKGROUND_IMAGE = MEDIA_DIR / "estadio.jpg"
MOUSE_IMG = MEDIA_DIR / "ratoncito_regordete_del_cali_frente.png"
WALL_IMG = MEDIA_DIR / "boo.jpg"
CHEESE_IMG = MEDIA_DIR / "copa.png"  # Añade copa.png en media/ para el queso


# API expuesta a JavaScript
@eel.expose
def getMazeState():
    """Devuelve el estado actual del laberinto para el frontend."""
    lab = _get_labyrinth()
    if lab is None:
        return None
    grid = lab.get_maze()
    maze_data = []
    for row in grid:
        maze_data.append([int(v) if v != 2 and v != 3 else 0 for v in row])
    mouse = lab.get_mouse_position()
    cheese = lab.get_cheese_position()
    return {
        "mazeData": maze_data,
        "mousePos": {"x": int(mouse[1]), "y": int(mouse[0])},
        "cheesePos": {"x": int(cheese[1]), "y": int(cheese[0])},
        "gameWon": lab.smells_cheese(),
    }


@eel.expose
def moveMouse(direction):
    """Mueve el ratón ('up','down','left','right')."""
    lab = _get_labyrinth()
    if lab is None:
        return None
    try:
        lab.move_mouse(direction)
    except Exception:
        pass
    return getMazeState()


@eel.expose
def sendChatMessage(message):
    """Envía un mensaje al chat IA y devuelve la respuesta."""
    from core.chat_agent import ChatAgent
    agent = _get_chat_agent()
    return agent.get_response(message)


@eel.expose
def getBackgroundUrl():
    """Devuelve la URL de la imagen de fondo o None."""
    if BACKGROUND_IMAGE.exists():
        return "/media/estadio.jpg"
    return None


@eel.expose
def getMediaUrls():
    """Devuelve las URLs de las imágenes del laberinto."""
    return {
        "mouse": "/media/ratoncito_regordete_del_cali_frente.png" if (MEDIA_DIR / "ratoncito_regordete_del_cali_frente.png").exists() else None,
        "mouseFrente": "/media/ratoncito_regordete_del_cali_frente.png" if (MEDIA_DIR / "ratoncito_regordete_del_cali_frente.png").exists() else None,
        "mouseAtras": "/media/ratoncito_regordete_del_cali_atras.png" if (MEDIA_DIR / "ratoncito_regordete_del_cali_atras.png").exists() else None,
        "mouseIzq": "/media/ratoncito_regordete_del_cali_izq.png" if (MEDIA_DIR / "ratoncito_regordete_del_cali_izq.png").exists() else None,
        "mouseDer": "/media/ratoncito_regordete_del_cali_der.png" if (MEDIA_DIR / "ratoncito_regordete_del_cali_der.png").exists() else None,
        "wall": "/media/boo.jpg" if WALL_IMG.exists() else None,
        "cheese": "/media/copa.png" if CHEESE_IMG.exists() else None,
        "soloVerde": "/media/solo_verde.jpg" if (MEDIA_DIR / "solo_verde.jpg").exists() else None,
    }


@eel.expose
def loadMaze():
    """Recarga el laberinto por defecto (laberinto.csv)."""
    from agent.maze.labyrinth import Labyrinth
    _get_labyrinth._inst = Labyrinth()
    _get_labyrinth._inst.generate_input_maze(str(DEFAULT_MAZE_PATH))
    return getMazeState()


@eel.expose
def loadMazeFromGrid(grid_data):
    """Carga el laberinto desde matriz 10x10 [[row0], [row1], ...]."""
    from agent.maze.labyrinth import Labyrinth
    _get_labyrinth._inst = Labyrinth()
    _get_labyrinth._inst.load_from_grid(grid_data)
    return getMazeState()


@eel.expose
def getDefaultMazeCsv():
    """Devuelve el contenido CSV del laberinto por defecto."""
    if DEFAULT_MAZE_PATH.exists():
        return DEFAULT_MAZE_PATH.read_text(encoding="utf-8").strip()
    return ""


def _get_labyrinth():
    from agent.maze.labyrinth import Labyrinth
    if not hasattr(_get_labyrinth, "_inst"):
        _get_labyrinth._inst = None
    return _get_labyrinth._inst


@eel.expose
def loadRandomMaze():
    """Genera un laberinto aleatorio."""
    from agent.maze.labyrinth import Labyrinth
    _get_labyrinth._inst = Labyrinth()
    _get_labyrinth._inst.generate_random_maze()
    return getMazeState()


@eel.expose
def runMouseSearch():
    """
    Ejecuta la clase Mouse con run() en el laberinto actual.
    Devuelve {result: "win"|"loop", history: [{x,y},...], movement_history: ["up",...]}
    o None si no hay laberinto cargado.
    """
    lab = _get_labyrinth()
    if lab is None:
        return None
    from agent.simple_reflex_agent import Mouse
    mouse = Mouse(lab)
    result_type, history, movement_history = mouse.run()
    # history: list of [row,col] = [y,x] -> convertir a [{x,col, y:row}, ...]
    history_xy = [{"x": int(pos[1]), "y": int(pos[0])} for pos in history]
    return {
        "result": result_type,
        "history": history_xy,
        "movement_history": movement_history,
    }


@eel.expose
def hasMazeLoaded():
    """Indica si hay un laberinto cargado."""
    return _get_labyrinth() is not None


def _get_chat_agent():
    from core.chat_agent import ChatAgent
    if not hasattr(_get_chat_agent, "_inst"):
        _get_chat_agent._inst = ChatAgent()
    return _get_chat_agent._inst


def run():
    """Inicia la aplicación Eel."""
    eel.init(str(BASE_DIR), allowed_extensions=[".js", ".html", ".css", ".jpg", ".jpeg", ".png"])
    eel.start("ui_webview/arena_maze.html", size=(1400, 900), port=0)
