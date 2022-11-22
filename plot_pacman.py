def create_maze(array, pacman_line, pacman_column):
    expand = 100
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
                    "opacity": 1.0,
                    "line": {"width": 0},
                }
                layout["shapes"].append(shape)
    pacman = {
        "type": "path",
        "path": f"M {0.5002 + pacman_line} {0 + pacman_column} C {0.3027 + pacman_line} {0 + pacman_column} {0.132 + pacman_line} {0.1147 + pacman_column} {0.0508 + pacman_line} {0.2812 + pacman_column} L {0.5002 + pacman_line} {0.5002 + pacman_column} L {0.0508 + pacman_line} {0.7189 + pacman_column} C {0.132 + pacman_line} {0.8854 + pacman_column} {0.3027 + pacman_line} {1 + pacman_column} {0.5002 + pacman_line} {1 + pacman_column} C {0.7764 + pacman_line} {1 + pacman_column} {1 + pacman_line} {0.7761 + pacman_column} {1 + pacman_line} {0.5002 + pacman_column} S {0.7764 + pacman_line} {0 + pacman_column} {0.5002 + pacman_line} {0 + pacman_column} Z",
        "fillcolor": "yellow",
        "line": {"width": 0},
    }
    layout["shapes"].append(pacman)
    return layout
