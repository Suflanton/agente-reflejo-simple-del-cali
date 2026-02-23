"""
Tabla de decisión percepción-reacción para el agente de reacción simple.
Percept: [left, up, right, down] donde 0=libre, 1=no libre (pared), 2=queso.
"""
import numpy as np

# Tabla de decisión: (left, up, right, down) -> acción
# 0 = libre, 1 = no libre. Orden de evaluación: primera coincidencia gana.
# Prioridad general: arriba > izquierda > derecha > abajo
DECISION_TABLE = [
    # (left, up, right, down) -> action
    ((0, 0, 0, 0), "up"),   # Todo libre -> ir arriba
    ((0, 0, 0, 1), "up"),   # Abajo bloqueado
    ((0, 0, 1, 0), "up"),   # Derecha bloqueada
    ((0, 0, 1, 1), "up"),   # Derecha y abajo bloqueadas
    ((0, 1, 0, 0), "left"), # Arriba bloqueado, izquierda libre
    ((0, 1, 0, 1), "left"), # Arriba y abajo bloqueadas
    ((0, 1, 1, 0), "left"), # Arriba y derecha bloqueadas
    ((0, 1, 1, 1), "left"), # Solo izquierda libre
    ((1, 0, 0, 0), "up"),   # Izquierda bloqueada, arriba libre
    ((1, 0, 0, 1), "up"),   # Izquierda y abajo bloqueadas
    ((1, 0, 1, 0), "up"),   # Izquierda y derecha bloqueadas
    ((1, 0, 1, 1), "up"),   # Solo arriba libre
    ((1, 1, 0, 0), "right"),# Arriba e izquierda bloqueadas
    ((1, 1, 0, 1), "right"),# Solo derecha libre (entre varias opciones)
    ((1, 1, 1, 0), "down"), # Solo abajo libre
    ((1, 1, 1, 1), "up"),   # Todo bloqueado - default (intentará up)
]


def get_action(percepts: np.ndarray) -> str:
    """
    Dado el array de percepciones [left, up, right, down],
    devuelve la acción a realizar: "up", "left", "right" o "down".

    Valores en percepts: 0=libre, 1=no libre (pared), 2=queso.
    """
    print("--------------------------------")
    print("percepts", percepts)
    print("--------------------------------")
    left, up, right, down = int(percepts[0]), int(percepts[1]), int(percepts[2]), int(percepts[3])

    # Reglas 1-4: Si hay queso (2) en alguna dirección, moverse hacia allí
    if up == 2:
        return "up"
    if left == 2:
        return "left"
    if right == 2:
        return "right"
    if down == 2:
        return "down"

    # Reglas 5-22: Tabla de decisión según paredes (0=libre, 1=bloqueado)
    state = (left, up, right, down)
    for (rule_state, action) in DECISION_TABLE:
        if state == rule_state:
            print("--------------------------------")
            print("state", state)
            print("action", action)
            print("--------------------------------")
            return action
    
    

    if up == 0:
        return "up"
    if left == 0:
        return "left"
    if right == 0:
        return "right"
    if down == 0:
        return "down"

    return "up"  # Todo bloqueado
