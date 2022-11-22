def create_maze(array):
    expand = 100
    print("SHAPE", array.shape[1])
    layout = {
        "shapes": [],
        "height": (array.shape[0]) * expand,
        "width": (array.shape[1]) * expand,
        "xaxis": {"range": [0, array.shape[1]], "visible": False},
        "yaxis": {"range": [0, array.shape[0]], "visible": False},
        "plot_bgcolor": "black",
    }
    for i, line in enumerate(array):
        for j, cell in enumerate(line):
            if cell == 1:
                shape = {
                    "type": "rect",
                    "xref": "x",
                    "yref": "y",
                    "x0": j,
                    "y0": i,
                    "x1": j + 1,
                    "y1": i + 1,
                    "fillcolor": "#0330fc",
                    "opacity": 0.8,
                    "line": {"width": 0},
                }
                layout["shapes"].append(shape)
    return layout
