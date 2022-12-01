import numpy as np
import traceback

from utils import (
    euclidean_distance,
    euclidean_distance_between_players,
    manhattan_distance,
    manhattan_distance_between_players,
)

my_heuristic_definition = "def my_heuristic(maze, dots, power_pellets, pacman, ghost):"


def get_heuristic_from_streamlit(heuristic_text):
    # first return is whether there was an error or not

    heuristic_text = add_tab_to_beginning_of_each_line(heuristic_text)
    heuristic_text = (
        f"global my_heuristic\n{my_heuristic_definition}\n" + heuristic_text
    )

    exec(heuristic_text)

    # my_heuristic is marked as undefined in VS code but it is not as we retrieve its value
    # when we exec the test containing its definition !
    heuristic_streamlit = lambda game: my_heuristic(
        game.maze,
        game.dots,
        game.power_pellets,
        game.pacman,
        game.ghosts[0],
    )
    return heuristic_streamlit


def add_tab_to_beginning_of_each_line(text, tabs_quantity=1):
    lines = text.split("\n")
    tabbed_lines = ["    " * tabs_quantity + line for line in lines]
    tabbed_text = "\n".join(tabbed_lines)
    return tabbed_text
