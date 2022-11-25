import streamlit as st
import numpy as np
import plotly
from game import Game
from heuristics import pacman_heuristic, ghost_bfs
from mazes import mazes_dict
from alphabeta import get_action_with_minimax_alphabeta
from random import choice
from utils import Action

max_number = st.slider(
    "Max number of turns",
    min_value=0,
    max_value=3000,
    value=50,
)

maze = mazes_dict[st.selectbox("Maze :", mazes_dict.keys())]


dots = np.array([[0 if cell == 1 else 1 for cell in line] for line in maze])

game = Game(maze, dots, (1, 1), [(4, 2)], None, [None])
game.pacman.strategy = lambda game: get_action_with_minimax_alphabeta(
    game, pacman_heuristic, game.pacman, game.players
)
# Random ghost :
# game.ghosts[0].strategy = lambda game: Action(
#     game.ghosts[0], choice(game.get_legal_directions(game.ghosts[0].name))
# )

game.ghosts[0].strategy = lambda game: Action(
    game.ghosts[0], ghost_bfs(game.ghosts[0], game)
)


layout_list = game.run_and_get_layout(max_number)

frames = [
    {"name": f"{i}", "data": [], "layout": layout_list[i]}
    for i in range(len(layout_list))
]

sliderSteps = [
    {
        "method": "animate",
        "label": f"{i}",
        "args": [
            [f"{i}"],
            {
                "mode": "immediate",
                "transition": {"duration": 0},
                "frame": {"duration": 0, "redraw": "true"},
            },
        ],
    }
    for i in range(len(layout_list))
]
expand = 80
layout = {
    "height": game.maze.shape[0] * expand,
    "width": game.maze.shape[1] * expand,
    "xaxis": {"range": [0, game.maze.shape[1]], "visible": False},
    "yaxis": {
        "range": [0, game.maze.shape[0]],
        "scaleanchor": "x",
        "scaleratio": 1,
        "visible": False,
    },
    "sliders": [
        {
            "steps": sliderSteps,
        }
    ],
}
fig = plotly.graph_objects.Figure([], layout | layout_list[0], frames)

# Plot!
st.plotly_chart(fig, use_container_width=True)
