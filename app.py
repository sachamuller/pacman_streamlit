import streamlit as st
import numpy as np
import plotly
from plot_pacman import create_layout
from game import Game, Action, Directions

maze = np.array(
    [
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1],
    ]
)

dots = np.array([[0 if cell == 1 else 1 for cell in line] for line in maze])

game = Game(maze, dots, (1, 1), (4, 2))

action_list = [
    Action(game.pacman, Directions.up),
    Action(game.pacman, Directions.up),
    Action(game.pacman, Directions.right),
    Action(game.pacman, Directions.right),
    Action(game.pacman, Directions.right),
    Action(game.pacman, Directions.left),
    Action(game.pacman, Directions.left),
    Action(game.pacman, Directions.left),
    Action(game.pacman, Directions.up),
    Action(game.pacman, Directions.up),
    Action(game.pacman, Directions.right),
    Action(game.pacman, Directions.right),
    Action(game.pacman, Directions.right),
    Action(game.pacman, Directions.up),
    Action(game.pacman, Directions.left),
    Action(game.pacman, Directions.left),
    Action(game.pacman, Directions.down),
    Action(game.pacman, Directions.down),
    Action(game.pacman, Directions.left),
    Action(game.pacman, Directions.down),
    Action(game.pacman, Directions.down),
    Action(game.pacman, Directions.down),
    Action(game.pacman, Directions.right),
    Action(game.pacman, Directions.right),
    Action(game.pacman, Directions.right),
    Action(game.pacman, Directions.right),
]

layout_list = []
for action in action_list:
    layout_list.append(create_layout(game))
    game.next_state(action)
layout_list.append(create_layout(game))
print(layout_list[-1])

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

layout = {
    "sliders": [
        {
            "steps": sliderSteps,
        }
    ]
}
fig = plotly.graph_objects.Figure([], layout | layout_list[0], frames)

# Plot!
st.plotly_chart(fig, use_container_width=True)
