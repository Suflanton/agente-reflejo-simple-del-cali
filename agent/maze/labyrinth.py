import csv
from pathlib import Path

import numpy as np
class Labyrinth:

    def __init__(self):
        self.grid = np.empty((10,10))
        self.cheese_position = np.array([0,0])

    def reset_grid(self):
        """Resetea la matriz del laberinto para generar uno nuevo."""
        self.grid = np.empty((10, 10))

    def generate_random_maze(self):
        """Genera un laberinto aleatorio: 0=camino, 1=pared, 2=queso, 3=ratón."""
        self.reset_grid()
        # Llenar con caminos (0) y paredes (1)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                self.grid[i, j] = np.random.choice([0, 1], p=[0.85, 0.15])

        # Queso en celda libre de la mitad superior (filas 0-4)
        half = self.grid.shape[0] // 2
        empty_upper = [(i, j) for i in range(half) for j in range(self.grid.shape[1])
                       if self.grid[i, j] == 0]
        if not empty_upper:
            empty_upper = [(i, j) for i in range(self.grid.shape[0]) for j in range(self.grid.shape[1])
                          if self.grid[i, j] == 0]
        if empty_upper:
            idx = np.random.randint(0, len(empty_upper))
            r, c = empty_upper[idx]
            self.grid[r, c] = 2
            self.cheese_position = np.array([r, c])

        # Ratón en celda libre de la mitad inferior (filas 5-9)
        empty_lower = [(i, j) for i in range(half, self.grid.shape[0])
                      for j in range(self.grid.shape[1])
                      if self.grid[i, j] == 0]
        if not empty_lower:
            empty_lower = [(i, j) for i in range(self.grid.shape[0]) for j in range(self.grid.shape[1])
                          if self.grid[i, j] == 0]
        if empty_lower:
            idx = np.random.randint(0, len(empty_lower))
            r, c = empty_lower[idx]
            self.grid[r, c] = 3
        

    def generate_input_maze(self, input_file: str):
        base_dir = Path(__file__).resolve().parent.parent.parent
        default_path = base_dir / "media" / "default_labyrinth" / "laberinto.csv"
        try:
            with open(input_file, 'r') as file:
                data = np.loadtxt(file, delimiter=",")
            self.grid = data.reshape(10, 10)
        except Exception:
            data = np.loadtxt(default_path, delimiter=",")
            self.grid = data.reshape(10, 10)
        pos = np.where(self.grid == 2)
        i = pos[0][0]
        j = pos[1][0]
        self.cheese_position = np.array([i, j])

    def load_from_grid(self, grid_data):
        """Carga el laberinto desde una lista 10x10. 0=camino, 1=pared, 2=queso, 3=ratón."""
        data = np.array(grid_data, dtype=float).reshape(10, 10)
        self.grid = data
        pos = np.where(self.grid == 2)
        if len(pos[0]) > 0 and len(pos[1]) > 0:
            self.cheese_position = np.array([pos[0][0], pos[1][0]])
        else:
            self.cheese_position = np.array([0, 0])
        # Si no hay ratón (3), ponerlo en la primera celda libre
        if 3 not in self.grid:
            for i in range(10):
                for j in range(10):
                    if self.grid[i, j] == 0:
                        self.grid[i, j] = 3
                        return
            self.grid[9, 9] = 3 
    
    def get_cheese_position(self):
        return self.cheese_position

    def get_mouse_position(self):
        pos = np.where(self.grid == 3)
        i = pos[0][0]
        j = pos[1][0]
        return np.array([i,j])

    def get_square_value(self, position):
        row, col = int(position[0]), int(position[1])
        if row < 0 or col < 0 or row >= self.grid.shape[0] or col >= self.grid.shape[1]:
            return 1  # Fuera del grid = pared
        return self.grid[row, col]
            
    def percepts(self):
        mouse_position = self.get_mouse_position()
        up = self.get_square_value(mouse_position + np.array([-1, 0]))
        down = self.get_square_value(mouse_position + np.array([1, 0]))
        left = self.get_square_value(mouse_position + np.array([0, -1]))
        right = self.get_square_value(mouse_position + np.array([0, 1]))
        return np.array([left, up, right, down])

    def get_maze(self):
        return self.grid

    def move_mouse(self, direction: str):
        current_position = self.get_mouse_position()
        if direction == "up":
            new_position = current_position + np.array([-1, 0])
        elif direction == "down":
            new_position = current_position + np.array([1, 0])
        elif direction == "left":
            new_position = current_position + np.array([0, -1])
        elif direction == "right":
            new_position = current_position + np.array([0, 1])
        if self.grid[new_position[0], new_position[1]] == 0:
            self.grid[current_position[0], current_position[1]] = 0
            self.grid[new_position[0], new_position[1]] = 3
        elif self.grid[new_position[0], new_position[1]] == 2:
            self.grid[current_position[0], current_position[1]] = 0
            self.grid[new_position[0], new_position[1]] = 3
        return new_position

    def smells_cheese(self):
        return np.array_equal(self.get_mouse_position(), self.get_cheese_position())

    def print_maze(self):
        print(self.grid)

""" Ejemplo de uso
labyrinth = Labyrinth()
labyrinth.generate_input_maze("media/default_labyrinth/laberinto.csv")
#labyrinth.generate_random_maze()
labyrinth.move_mouse("right")
labyrinth.move_mouse("down")
labyrinth.move_mouse("down")
labyrinth.move_mouse("right")
labyrinth.move_mouse("right")
labyrinth.move_mouse("down")
labyrinth.move_mouse("down")
labyrinth.move_mouse("right")
labyrinth.move_mouse("right")
labyrinth.move_mouse("right")
labyrinth.move_mouse("right")
labyrinth.move_mouse("down")
labyrinth.move_mouse("down")
labyrinth.move_mouse("right")
labyrinth.move_mouse("right")
labyrinth.move_mouse("down")
labyrinth.move_mouse("down")
labyrinth.move_mouse("down")
labyrinth.print_maze()
print(labyrinth.percepts())
print(labyrinth.is_cheese_eaten())
"""
