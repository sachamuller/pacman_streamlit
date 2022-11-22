def create_maze(maze_array, pacman_line, pacman_column, dots_array):
    expand = 100
    layout = {
        "shapes": [],
        "height": (maze_array.shape[0]) * expand,
        "width": (maze_array.shape[1]) * expand,
        "xaxis": {"range": [0, maze_array.shape[1]], "visible": False},
        "yaxis": {"range": [0, maze_array.shape[0]], "visible": False},
        "plot_bgcolor": "black",
    }

    # adding walls
    for i, line in enumerate(maze_array):
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

    # adding pacman
    pacman = {
        "type": "path",
        "path": f"M {0.5002 + pacman_line} {0 + pacman_column} C {0.3027 + pacman_line} {0 + pacman_column} {0.132 + pacman_line} {0.1147 + pacman_column} {0.0508 + pacman_line} {0.2812 + pacman_column} L {0.5002 + pacman_line} {0.5002 + pacman_column} L {0.0508 + pacman_line} {0.7189 + pacman_column} C {0.132 + pacman_line} {0.8854 + pacman_column} {0.3027 + pacman_line} {1 + pacman_column} {0.5002 + pacman_line} {1 + pacman_column} C {0.7764 + pacman_line} {1 + pacman_column} {1 + pacman_line} {0.7761 + pacman_column} {1 + pacman_line} {0.5002 + pacman_column} S {0.7764 + pacman_line} {0 + pacman_column} {0.5002 + pacman_line} {0 + pacman_column} Z",
        "fillcolor": "yellow",
        "line": {"width": 0},
    }
    layout["shapes"].append(pacman)

    # adding food dots
    layout = add_food_dots(dots_array, layout)

    return layout


def add_food_dots(dots_array, layout, dots_size=0.1):
    for i, line in enumerate(dots_array):
        for j, dot in enumerate(line):
            if dot == 1:
                shape = {
                    "type": "circle",
                    "xref": "x",
                    "yref": "y",
                    "x0": j + (1 - dots_size) / 2,
                    "y0": i + (1 - dots_size) / 2,
                    "x1": j + (1 + dots_size) / 2,
                    "y1": i + (1 + dots_size) / 2,
                    "fillcolor": "white",
                    "opacity": 1.0,
                    "line": {"width": 0},
                }
                layout["shapes"].append(shape)
    return layout
