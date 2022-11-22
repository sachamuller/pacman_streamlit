import streamlit as st
import numpy as np
import plotly
from plot_pacman import create_maze
from copy import deepcopy

one = st.checkbox("Add block 1")
two = st.checkbox("Add block 2")


maze = np.array(
    [
        [1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, two * 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 0, one * 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1],
    ]
)

dots = np.array([[0 if cell == 1 else 1 for cell in line] for line in maze])


pacman_line = st.slider("Pacman line :", 0, maze.shape[0], 0)

layout_list = []
for pacman_line in range(0, 5):
    for pacman_column in range(0, 5):
        layout_list.append(create_maze(maze, pacman_line, pacman_column, dots))

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
