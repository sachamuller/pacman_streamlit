import numpy as np
from enum import Enum


class Orientations(Enum):
    north = "north"
    south = "south"
    west = "west"
    east = "east"


class Directions(Enum):
    up = "up"
    down = "down"
    left = "left"
    right = "right"


class Action:
    def __init__(self, player, direction: Directions):
        self.player = player
        self.direction = direction

    def __repr__(self) -> str:
        return f"{self.player.name} : {self.direction.name}"


class Game:
    def __init__(self, maze, dots, pacman_position, ghost_position):
        self.maze = maze
        self.dots = dots
        self.pacman = Pacman(pacman_position)
        self.players = [self.pacman, Ghost(0, position=ghost_position)]
        self.update_dots()

    def next_state(self, action):
        for player in self.players:
            if player == action.player:
                player.next(action, self.maze)
            self.update_dots()

    def update_dots(self):
        self.dots[self.pacman.line][self.pacman.column] = 0


class Player:
    def __init__(self, name, position, orientation, alive):
        self.name = name
        self.line = position[0]
        self.column = position[1]
        self.orientation = orientation
        self.alive = alive

    def next(self, action, maze):
        self.next_position(action, maze)
        self.next_orientation(action)

    def next_position(self, action, maze):
        if action.direction == Directions.up and not maze[self.line + 1][self.column]:
            self.line += 1
        if action.direction == Directions.down and not maze[self.line - 1][self.column]:
            self.line -= 1
        if (
            action.direction == Directions.right
            and not maze[self.line][self.column + 1]
        ):
            self.column += 1
        if action.direction == Directions.left and not maze[self.line][self.column - 1]:
            self.column -= 1

    def next_orientation(self, action):
        if action.direction.name == "up":
            self.orientation = Orientations.north
        if action.direction.name == "down":
            self.orientation = Orientations.south
        if action.direction.name == "right":
            self.orientation = Orientations.west
        if action.direction.name == "left":
            self.orientation = Orientations.east


class Pacman(Player):
    def __init__(self, position=(0, 0), orientation=Orientations.west, alive=True):
        super().__init__("Pacman", position, orientation, alive)


class Ghost(Player):
    def __init__(
        self,
        id=0,
        position=(0, 0),
        orientation=Orientations.east,
        alive=True,
        color="red",
    ):
        super().__init__(f"Ghost {id}", position, orientation, alive)
        self.is_zombie = False
        self.zombie_timer = -1
        self.color = color
