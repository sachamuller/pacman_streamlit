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
    stay = "stay"


class Action:
    def __init__(self, player, direction: Directions):
        self.player = player
        self.direction = direction

    def __repr__(self) -> str:
        return f"{self.player.name} : {self.direction.name}"


def manhattan_distance(player, other_player):
    return abs(player.line - other_player.line) + abs(
        player.column - other_player.column
    )
