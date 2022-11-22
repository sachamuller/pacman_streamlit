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
maze_2 = deepcopy(maze)
maze_2[0][0] = 0

layout1 = create_maze(maze)
layout2 = create_maze(maze_2)

frames = [
    {"name": "frame1", "data": [], "layout": layout1},
    {"name": "frame2", "data": [], "layout": layout2},
]

sliderSteps = [
    {
        "method": "animate",
        "label": "frame1",
        "args": [
            ["frame1"],
            {
                "mode": "immediate",
                "transition": {"duration": 0},
                "frame": {"duration": 0, "redraw": "true"},
            },
        ],
    },
    {
        "method": "animate",
        "label": "frame2",
        "args": [
            ["frame2"],
            {
                "mode": "immediate",
                "transition": {"duration": 0},
                "frame": {"duration": 0, "redraw": "true"},
            },
        ],
    },
]

layout = {
    "sliders": [
        {
            "currentvalue": {
                "visible": True,
                "xanchor": "right",
            },
            "steps": sliderSteps,
        }
    ]
}

fig = plotly.graph_objects.Figure([], layout, frames)

# Plot!
st.plotly_chart(fig, use_container_width=True)
