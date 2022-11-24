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
    def __init__(self, maze, dots, pacman_position, ghost_positions):
        self.maze = maze
        self.dots = dots
        self.pacman = Pacman(pacman_position)
        self.ghosts = [
            Ghost(i, ghost_positions[i]) for i in range(len(ghost_positions))
        ]
        self.players = [self.pacman] + self.ghosts
        self.game_over = False
        self.check_players_names_are_unique()
        self.update_dots()
        self.update_aliveness()
        self.is_game_over()

    def next_state(self, action):
        if not self.game_over:
            for player in self.players:
                if player == action.player:
                    player.next(action, self.maze)
            self.update_dots()
            self.update_aliveness()
            self.is_game_over()

    def check_players_names_are_unique(self):
        for i, player in enumerate(self.players):
            if player.name in [p.name for j, p in enumerate(self.players) if j != i]:
                raise ValueError(
                    f"All players should have unique names but {player.name} is used at least twice."
                )

    def update_dots(self):
        self.dots[self.pacman.line][self.pacman.column] = 0

    def update_aliveness(self):
        self.pacman.is_still_alive(self.ghosts)
        for ghost in self.ghosts:
            ghost.is_still_alive(self.pacman)

    def is_game_over(self):
        if not self.pacman.alive:
            self.game_over = True


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

    def is_still_alive(self, ghosts, pacman):
        NotImplemented


class Pacman(Player):
    def __init__(self, position=(0, 0), orientation=Orientations.west, alive=True):
        super().__init__("Pacman", position, orientation, alive)

    def is_still_alive(self, ghosts):
        for ghost in ghosts:
            if self.line == ghost.line and self.column == ghost.column:
                self.alive = False


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

    def is_still_alive(self, pacman):
        if self.is_zombie:
            if self.line == pacman.line and self.column == pacman.column:
                self.alive = False
