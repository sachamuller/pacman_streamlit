from enum import Enum
from math import sqrt


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
    stay = "stay"


class Action:
    def __init__(self, player, direction: Directions):
        self.player = player
        self.direction = direction

    def __repr__(self) -> str:
        return f"{self.player.name} : {self.direction.name}"


def manhattan_distance(a, b):
    xa, ya = a
    xb, yb = b
    return abs(xa - xb) + abs(ya - yb)


def manhattan_distance_between_players(player, other_player):
    return manhattan_distance(
        (player.line, player.column), (other_player.line, other_player.column)
    )


def euclidean_distance(a, b):
    xa, ya = a
    xb, yb = b
    return sqrt((xa - xb) ** 2 + (ya - yb) ** 2)


def euclidean_distance_between_players(player, other_player):
    return euclidean_distance(
        (player.line, player.column), (other_player.line, other_player.column)
    )
