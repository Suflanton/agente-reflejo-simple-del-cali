from .maze.labyrinth import Labyrinth
from .perception import get_action
import numpy as np
class Mouse:
    def __init__(self, labyrinth: Labyrinth):
        self.labyrinth = labyrinth
        self.position = labyrinth.get_mouse_position()
        self.history = []
        self.movement_history = []
        self.history.append(self.position)
        self.max_iterations = 3

    def move(self):
        percepts = self.labyrinth.percepts()
        action = get_action(percepts)
        self.labyrinth.move_mouse(action)
        self.position = self.labyrinth.get_mouse_position()
        self.history.append(self.position)
        self.movement_history.append(action)
        return action
    
    def action(self):
        if self.eat_cheese():
            return "win"
        else:
            self.move()
            if self.is_in_loop():
                return "loop"
            return "continue"

    def run(self):
        while True:
            result = self.action()
            if result == "win":
                return ["win", self.history, self.movement_history]
            elif result == "loop":
                return ["loop", self.history, self.movement_history]
            elif result == "continue":
                continue

    def reset(self):
        self.position = self.labyrinth.get_mouse_position()
        self.history = []
        self.history.append(self.position)

    def is_in_loop(self):
        if any(np.array_equal(self.position, pos) for pos in self.history[:-1]):
            self.max_iterations -= 1

        if self.max_iterations == 0:
            return True
        else:
            return False

    def eat_cheese(self):
        return self.labyrinth.smells_cheese()

    def get_position(self):
        return self.position

    def get_labyrinth(self):
        return self.labyrinth



labyrinth = Labyrinth()
labyrinth.generate_random_maze()
mouse = Mouse(labyrinth)
result = mouse.run()
labyrinth.print_maze()
print(result)

