import streamlit as st
import numpy as np
import plotly
from plot_pacman import create_maze

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
layout = create_maze(maze)
fig = plotly.graph_objects.Figure([], layout)

# Plot!
st.plotly_chart(fig, use_container_width=True)
