import streamlit as st
from game import Game
from heuristics import ghost_bfs
from mazes import game_board_dict
from alphabeta import get_action_with_minimax_alphabeta
from random import choice
from utils import Action
from plot_pacman import get_fig_from_layout_list

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
    "def my_heuristic(game):",
    """    return -game.dots.sum()""",
)


if st.button("Compute game"):
    game = Game(game_board, None, [None])

    heuristic_text = "global my_heuristic\ndef my_heuristic(game):\n" + heuristic_text
    print("HEHO")
    print(heuristic_text)
    exec(heuristic_text)
    # my_heuristic is marked as undefined in VS code but it is not as we retrieve its value
    # when we exec the test containing its definition !
    game.pacman.strategy = lambda game: get_action_with_minimax_alphabeta(
        game, my_heuristic, game.pacman, game.players
    )

    if ghost_difficulty == "random":
        game.ghosts[0].strategy = lambda game: Action(
            game.ghosts[0], choice(game.get_legal_directions(game.ghosts[0].name))
        )
    if ghost_difficulty == "clever":
        game.ghosts[0].strategy = lambda game: Action(
            game.ghosts[0], ghost_bfs(game.ghosts[0], game)
        )

    layout_list = game.run_and_get_layout(max_number)

    fig = get_fig_from_layout_list(layout_list, game, maze_name)

    # Plot!
    st.plotly_chart(fig, use_container_width=True)
