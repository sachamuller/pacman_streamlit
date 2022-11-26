from copy import deepcopy
from random import choice
import streamlit as st
import traceback

from alphabeta import get_action_with_minimax_alphabeta
from game import Game
from heuristics import (
    get_heuristic_from_streamlit,
    my_heuristic_definition,
    add_tab_to_beginning_of_each_line,
)
from mazes import game_board_dict
from my_strategies import ghost_bfs
from plot_pacman import get_fig_from_layout_list
from utils import Action

st.title("Playing Pac-Man with Minimax")

max_number = st.slider(
    "Max number of turns",
    min_value=0,
    max_value=1500,
    value=50,
)

maze_name = st.selectbox("Maze :", game_board_dict.keys())
game_board = game_board_dict[maze_name]

ghost_difficulty = st.radio(
    "Ghost difficulty", options=["random", "clever"], horizontal=True
)

heuristic_text = st.text_area(
    my_heuristic_definition,
    """# Write your code here
# No need to indent from the function definition
return -dots.sum()""",
)

game_initiatlization = Game(game_board, None, [None])


if st.button("Compute game"):
    game = deepcopy(game_initiatlization)

    if ghost_difficulty == "random":
        game.ghosts[0].strategy = lambda game: Action(
            game.ghosts[0], choice(game.get_legal_directions(game.ghosts[0].name))
        )
    if ghost_difficulty == "clever":
        game.ghosts[0].strategy = lambda game: Action(
            game.ghosts[0], ghost_bfs(game.ghosts[0], game)
        )

    try:
        heuristic = get_heuristic_from_streamlit(heuristic_text)

        game.pacman.strategy = lambda game: get_action_with_minimax_alphabeta(
            game, heuristic, game.pacman, game.players
        )

        layout_list = game.run_and_get_layout(max_number)

    except Exception as error:

        error_title = "\n".join(traceback.format_exception_only(error))
        error_body = "\n".join(traceback.format_exception(error)[-5:])
        print(traceback.format_exception_only(error))
        st.error(error_title + f"\n\nTraceback : \n\n {error_body}")

    else:
        fig = get_fig_from_layout_list(layout_list, game, maze_name)

        # Plot!
        st.plotly_chart(fig, use_container_width=True)
