from copy import deepcopy
from numpy.random import choice
import streamlit as st
import traceback

from alphabeta import get_action_with_minimax_alphabeta
from game import Game
from heuristics import get_heuristic_from_streamlit, my_heuristic_definition
from mazes import game_board_dict
from my_strategies import ghost_bfs
from plot_pacman import get_fig_from_layout_list
from utils import Action

st.title("Playing Pac-Man with Minimax")

st.header("Parameters")
max_number = st.slider(
    "Choose the maximum number of turns :",
    min_value=0,
    max_value=1500,
    value=50,
)

left_col, right_col = st.columns(2)

with left_col:

    maze_name = st.selectbox("Choose the maze :", game_board_dict.keys())
    game_board = game_board_dict[maze_name]

with right_col:
    ghost_difficulty = st.radio(
        "Choose the ghost behaviour :",
        options=["random", "chaser", "random-chaser"],
        horizontal=True,
    )

st.header("Write your own heuristic")

st.write(
    "Write an heuristic that plays Pac-Man. It should return a high value when Pac-Man is in a \
    favorable situation, and a low value when Pac-Man is in danger. You have access to the following objects :"
)
st.markdown(
    """
- `maze` : numpy array, `maze[i][j]` is 1 if there is a wall at line i and column j, else 0
- `dots` : numpy array, `dots[i][j]` is 1 if there is a dot to eat at line i and column j, else 0
- `pacman_line` : int, the line where Pac-Man is
- `pacman_column` : int, the column where Pac-Man is
- `ghost_line` : int, the line where the ghost is
- `ghost_column` : int, the column where the ghost is
"""
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
    if ghost_difficulty == "chaser":
        game.ghosts[0].strategy = lambda game: Action(
            game.ghosts[0], ghost_bfs(game.ghosts[0], game)
        )
    if ghost_difficulty == "random-chaser":
        game.ghosts[0].strategy = lambda game: choice(
            [
                Action(
                    game.ghosts[0],
                    choice(game.get_legal_directions(game.ghosts[0].name)),
                ),
                Action(game.ghosts[0], ghost_bfs(game.ghosts[0], game)),
            ],
            p=[0.1, 0.9],
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
        st.error(error_title + f"\n\nTraceback : \n\n {error_body}")

    else:
        fig = get_fig_from_layout_list(layout_list, game, maze_name)

        # Plot!
        st.plotly_chart(fig, use_container_width=True)
