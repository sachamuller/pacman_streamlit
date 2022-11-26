import numpy as np
import traceback

from utils import (
    euclidean_distance,
    euclidean_distance_between_players,
    manhattan_distance,
    manhattan_distance_between_players,
)

my_heuristic_definition = "def my_heuristic(maze, dots, pacman_line, pacman_column, ghost_line, ghost_column):"


def get_heuristic_from_streamlit(heuristic_text):
    # first return is whether there was an error or not

    heuristic_text = add_tab_to_beginning_of_each_line(heuristic_text)
    heuristic_text = (
        f"global my_heuristic\n{my_heuristic_definition}\n" + heuristic_text
    )
    try:
        exec(heuristic_text)
    except Exception as e:
        return True, e

    # my_heuristic is marked as undefined in VS code but it is not as we retrieve its value
    # when we exec the test containing its definition !
    heuristic_streamlit = lambda game: my_heuristic(
        game.maze,
        game.dots,
        game.pacman.line,
        game.pacman.column,
        game.ghosts[0].line,
        game.ghosts[0].column,
    )
    return False, heuristic_streamlit


def add_tab_to_beginning_of_each_line(text, tabs_quantity=1):
    lines = text.split("\n")
    tabbed_lines = ["    " * tabs_quantity + line for line in lines]
    tabbed_text = "\n".join(tabbed_lines)
    return tabbed_text
