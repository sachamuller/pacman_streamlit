from game import Orientations


def create_layout(game):
    expand = 100
    layout = {
        "shapes": [],
        "height": (game.maze.shape[0]) * expand,
        "width": (game.maze.shape[1]) * expand,
        "xaxis": {"range": [0, game.maze.shape[1]], "visible": False},
        "yaxis": {"range": [0, game.maze.shape[0]], "visible": False},
        "plot_bgcolor": "black",
    }

    # adding walls
    add_walls(game.maze, layout)

    # adding pacman
    add_pacman(game.pacman, layout)

    # adding food dots
    add_food_dots(game.dots, layout)

    return layout


def add_walls(maze, layout):
    for i, line in enumerate(maze):
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


def add_food_dots(dots_array, layout, dots_size=0.1):
    for i, line in enumerate(dots_array):
        for j, dot in enumerate(line):
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
            if dot == 1:
                layout["shapes"].append(shape)
            else:
                # if we simply remove the dots, some bugs can happen as plotly animations works better
                # when each object is present across all frames, this is why we make them invisible, see :
                # https://community.plotly.com/t/graph-lines-disappear-in-certain-frames-of-animation/49184
                shape["opacity"] = 0.0
                layout["shapes"].append(shape)


def add_pacman(pacman, layout):
    if pacman.orientation == Orientations.east:
        path = f"M {0.5 + pacman.column} {0 + pacman.line} C {0.3027 + pacman.column} {0 + pacman.line} {0.132 + pacman.column} {0.1147 + pacman.line} {0.0508 + pacman.column} {0.2812 + pacman.line} L {0.5 + pacman.column} {0.5 + pacman.line} L {0.0508 + pacman.column} {0.7189 + pacman.line} C {0.132 + pacman.column} {0.8854 + pacman.line} {0.3027 + pacman.column} {1 + pacman.line} {0.5 + pacman.column} {1 + pacman.line} C {0.7764 + pacman.column} {1 + pacman.line} {1 + pacman.column} {0.7761 + pacman.line} {1 + pacman.column} {0.5 + pacman.line} S {0.7764 + pacman.column} {0 + pacman.line} {0.5 + pacman.column} {0 + pacman.line} Z"
    elif pacman.orientation == Orientations.west:
        path = f"M {0.5 + pacman.column} {1 + pacman.line} C {0.6974 + pacman.column} {1 + pacman.line} {0.8681 + pacman.column} {0.8857 + pacman.line} {0.9492 + pacman.column} {0.7192 + pacman.line} L {0.5 + pacman.column} {0.5 + pacman.line} L {0.9492 + pacman.column} {0.2811 + pacman.line} C {0.8685 + pacman.column} {0.115 + pacman.line} {0.6974 + pacman.column} {0 + pacman.line} {0.5 + pacman.column} {0 + pacman.line} C {0.2237 + pacman.column} {0 + pacman.line} {0 + pacman.column} {0.2243 + pacman.line} {0 + pacman.column} {0.5 + pacman.line} S {0.224 + pacman.column} {1 + pacman.line} {0.5 + pacman.column} {1 + pacman.line} Z"
    elif pacman.orientation == Orientations.south:
        path = f"M {1 + pacman.column} {0.5 + pacman.line} C {1 + pacman.column} {0.3024 + pacman.line} {0.8853 + pacman.column} {0.1316 + pacman.line} {0.7188 + pacman.column} {0.0504 + pacman.line} L {0.5 + pacman.column} {0.5 + pacman.line} L {0.2809 + pacman.column} {0.0504 + pacman.line} C {0.1 + pacman.column} {0.1316 + pacman.line} {0 + pacman.column} {0.3024 + pacman.line} {0 + pacman.column} {0.5 + pacman.line} C {0 + pacman.column} {0.7763 + pacman.line} {0.2237 + pacman.column} {1 + pacman.line} {0.5 + pacman.column} {1 + pacman.line} S {1 + pacman.column} {0.7759 + pacman.line} {1 + pacman.column} {0.5 + pacman.line} Z"
    elif pacman.orientation == Orientations.north:
        path = f"M {0 + pacman.column} {0.5 + pacman.line} C {0 + pacman.column} {0.6971 + pacman.line} {0.1146 + pacman.column} {0.8678 + pacman.line} {0.2811 + pacman.column} {0.9489 + pacman.line} L {0.5 + pacman.column} {0.5 + pacman.line} L {0.719 + pacman.column} {0.9489 + pacman.line} C {0.8854 + pacman.column} {0.8678 + pacman.line} {1 + pacman.column} {0.6971 + pacman.line} {1 + pacman.column} {0.5 + pacman.line} C {1 + pacman.column} {0.2236 + pacman.line} {0.7761 + pacman.column} {0 + pacman.line} {0.5 + pacman.column} {0 + pacman.line} S {0 + pacman.column} {0.2239 + pacman.line} {0 + pacman.column} {0.5 + pacman.line} Z"
    pacman = {
        "type": "path",
        "path": path,
        "fillcolor": "yellow",
        "line": {"width": 0},
    }
    layout["shapes"].append(pacman)
