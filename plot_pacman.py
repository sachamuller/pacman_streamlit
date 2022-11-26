import plotly

from mazes import expand_dict
from utils import Orientations


def create_layout(game):
    expand = 100
    width = 1000
    layout = {
        "shapes": [],
        "plot_bgcolor": "black",
    }

    # adding walls
    add_walls(game.maze, layout)

    # adding food dots
    add_food_dots(game.dots, layout)

    # adding pacman
    for player in game.players:
        if player != game.pacman:
            add_ghost(player, layout)
    add_pacman(game.pacman, layout)

    add_game_over_or_game_won(game.game_over, game.game_won, layout)

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
    smaller = 0.75
    if pacman.orientation == Orientations.east:
        path = f"M {0.5  * smaller + pacman.column + (1-smaller)/2} {0  * smaller + pacman.line + (1-smaller)/2} C {0.3027  * smaller + pacman.column + (1-smaller)/2} {0  * smaller + pacman.line + (1-smaller)/2} {0.132  * smaller + pacman.column + (1-smaller)/2} {0.1147  * smaller + pacman.line + (1-smaller)/2} {0.0508  * smaller + pacman.column + (1-smaller)/2} {0.2812  * smaller + pacman.line + (1-smaller)/2} L {0.5  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} L {0.0508  * smaller + pacman.column + (1-smaller)/2} {0.7189  * smaller + pacman.line + (1-smaller)/2} C {0.132  * smaller + pacman.column + (1-smaller)/2} {0.8854  * smaller + pacman.line + (1-smaller)/2} {0.3027  * smaller + pacman.column + (1-smaller)/2} {1  * smaller + pacman.line + (1-smaller)/2} {0.5  * smaller + pacman.column + (1-smaller)/2} {1  * smaller + pacman.line + (1-smaller)/2} C {0.7764  * smaller + pacman.column + (1-smaller)/2} {1  * smaller + pacman.line + (1-smaller)/2} {1  * smaller + pacman.column + (1-smaller)/2} {0.7761  * smaller + pacman.line + (1-smaller)/2} {1  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} S {0.7764  * smaller + pacman.column + (1-smaller)/2} {0  * smaller + pacman.line + (1-smaller)/2} {0.5  * smaller + pacman.column + (1-smaller)/2} {0  * smaller + pacman.line + (1-smaller)/2} Z"
    elif pacman.orientation == Orientations.west:
        path = f"M {0.5  * smaller + pacman.column + (1-smaller)/2} {1  * smaller + pacman.line + (1-smaller)/2} C {0.6974  * smaller + pacman.column + (1-smaller)/2} {1  * smaller + pacman.line + (1-smaller)/2} {0.8681  * smaller + pacman.column + (1-smaller)/2} {0.8857  * smaller + pacman.line + (1-smaller)/2} {0.9492  * smaller + pacman.column + (1-smaller)/2} {0.7192  * smaller + pacman.line + (1-smaller)/2} L {0.5  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} L {0.9492  * smaller + pacman.column + (1-smaller)/2} {0.2811  * smaller + pacman.line + (1-smaller)/2} C {0.8685  * smaller + pacman.column + (1-smaller)/2} {0.115  * smaller + pacman.line + (1-smaller)/2} {0.6974  * smaller + pacman.column + (1-smaller)/2} {0  * smaller + pacman.line + (1-smaller)/2} {0.5  * smaller + pacman.column + (1-smaller)/2} {0  * smaller + pacman.line + (1-smaller)/2} C {0.2237  * smaller + pacman.column + (1-smaller)/2} {0  * smaller + pacman.line + (1-smaller)/2} {0  * smaller + pacman.column + (1-smaller)/2} {0.2243  * smaller + pacman.line + (1-smaller)/2} {0  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} S {0.224  * smaller + pacman.column + (1-smaller)/2} {1  * smaller + pacman.line + (1-smaller)/2} {0.5  * smaller + pacman.column + (1-smaller)/2} {1  * smaller + pacman.line + (1-smaller)/2} Z"
    elif pacman.orientation == Orientations.south:
        path = f"M {1  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} C {1  * smaller + pacman.column + (1-smaller)/2} {0.3024  * smaller + pacman.line + (1-smaller)/2} {0.8853  * smaller + pacman.column + (1-smaller)/2} {0.1316  * smaller + pacman.line + (1-smaller)/2} {0.7188  * smaller + pacman.column + (1-smaller)/2} {0.0504  * smaller + pacman.line + (1-smaller)/2} L {0.5  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} L {0.2809  * smaller + pacman.column + (1-smaller)/2} {0.0504  * smaller + pacman.line + (1-smaller)/2} C {0.1  * smaller + pacman.column + (1-smaller)/2} {0.1316  * smaller + pacman.line + (1-smaller)/2} {0  * smaller + pacman.column + (1-smaller)/2} {0.3024  * smaller + pacman.line + (1-smaller)/2} {0  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} C {0  * smaller + pacman.column + (1-smaller)/2} {0.7763  * smaller + pacman.line + (1-smaller)/2} {0.2237  * smaller + pacman.column + (1-smaller)/2} {1  * smaller + pacman.line + (1-smaller)/2} {0.5  * smaller + pacman.column + (1-smaller)/2} {1  * smaller + pacman.line + (1-smaller)/2} S {1  * smaller + pacman.column + (1-smaller)/2} {0.7759  * smaller + pacman.line + (1-smaller)/2} {1  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} Z"
    elif pacman.orientation == Orientations.north:
        path = f"M {0  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} C {0  * smaller + pacman.column + (1-smaller)/2} {0.6971  * smaller + pacman.line + (1-smaller)/2} {0.1146  * smaller + pacman.column + (1-smaller)/2} {0.8678  * smaller + pacman.line + (1-smaller)/2} {0.2811  * smaller + pacman.column + (1-smaller)/2} {0.9489  * smaller + pacman.line + (1-smaller)/2} L {0.5  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} L {0.719  * smaller + pacman.column + (1-smaller)/2} {0.9489  * smaller + pacman.line + (1-smaller)/2} C {0.8854  * smaller + pacman.column + (1-smaller)/2} {0.8678  * smaller + pacman.line + (1-smaller)/2} {1  * smaller + pacman.column + (1-smaller)/2} {0.6971  * smaller + pacman.line + (1-smaller)/2} {1  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} C {1  * smaller + pacman.column + (1-smaller)/2} {0.2236  * smaller + pacman.line + (1-smaller)/2} {0.7761  * smaller + pacman.column + (1-smaller)/2} {0  * smaller + pacman.line + (1-smaller)/2} {0.5  * smaller + pacman.column + (1-smaller)/2} {0  * smaller + pacman.line + (1-smaller)/2} S {0  * smaller + pacman.column + (1-smaller)/2} {0.2239  * smaller + pacman.line + (1-smaller)/2} {0  * smaller + pacman.column + (1-smaller)/2} {0.5  * smaller + pacman.line + (1-smaller)/2} Z"
    pacman_shape = {
        "type": "path",
        "path": path,
        "fillcolor": "yellow",
        "line": {"width": 0},
    }
    layout["shapes"].append(pacman_shape)


def add_ghost(ghost, layout):
    smaller = 0.75
    path = f"M  {1.0* smaller + ghost.column + (1-smaller)/2}  {0.5* smaller + ghost.line + (1-smaller)/2} L  {1.0* smaller + ghost.column + (1-smaller)/2}  {0.0* smaller + ghost.line + (1-smaller)/2} L  {0.8334* smaller + ghost.column + (1-smaller)/2}  {0.19999999999999996* smaller + ghost.line + (1-smaller)/2} L  {0.6667000000000001* smaller + ghost.column + (1-smaller)/2}  {0.0* smaller + ghost.line + (1-smaller)/2} L  {0.5* smaller + ghost.column + (1-smaller)/2}  {0.19999999999999996* smaller + ghost.line + (1-smaller)/2} L  {0.33399999999999996* smaller + ghost.column + (1-smaller)/2}  {0.0* smaller + ghost.line + (1-smaller)/2} L  {0.16669999999999996* smaller + ghost.column + (1-smaller)/2}  {0.19999999999999996* smaller + ghost.line + (1-smaller)/2} L  {0.0* smaller + ghost.column + (1-smaller)/2}  {0.0* smaller + ghost.line + (1-smaller)/2} L  {0.0* smaller + ghost.column + (1-smaller)/2}  {0.5* smaller + ghost.line + (1-smaller)/2} C  {0.0* smaller + ghost.column + (1-smaller)/2}  {0.7764* smaller + ghost.line + (1-smaller)/2}  {0.2239* smaller + ghost.column + (1-smaller)/2}  {1.0* smaller + ghost.line + (1-smaller)/2}  {0.5* smaller + ghost.column + (1-smaller)/2}  {1.0* smaller + ghost.line + (1-smaller)/2} S  {1.0* smaller + ghost.column + (1-smaller)/2}  {0.7761* smaller + ghost.line + (1-smaller)/2}  {1.0* smaller + ghost.column + (1-smaller)/2}  {0.5* smaller + ghost.line + (1-smaller)/2} Z"
    ghost = {
        "type": "path",
        "path": path,
        "fillcolor": ghost.color,
        "line": {"width": 0},
    }
    layout["shapes"].append(ghost)


def add_game_over_or_game_won(game_over, game_won, layout):
    if game_over:
        text = "GAME OVER"
        bgcolor = "rgba(0, 0, 0, 0.5)"
    elif game_won:
        text = "YOU WON !"
        bgcolor = "rgba(0, 0, 0, 0.5)"
    else:
        # once again animations work better when the elements exist on all frames and are modified
        text = ""
        bgcolor = "rgba(0, 0, 0, 0)"

    layout["annotations"] = [
        {
            "xref": "paper",
            "yref": "paper",
            "x": 0.5,
            "xanchor": "center",
            "y": 0.5,
            "yanchor": "middle",
            "text": text,
            "showarrow": False,
            "font": {"size": 50},
            "bgcolor": bgcolor,
            # "borderpad": max(layout["height"], layout["width"]),
        }
    ]


def get_fig_from_layout_list(layout_list, game, maze_name):
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
                    "frame": {"duration": 0, "redraw": False},  # TODO
                },
            ],
        }
        for i in range(len(layout_list))
    ]
    expand = expand_dict[maze_name]
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
        "updatemenus": [
            {
                "showactive": False,
                "type": "buttons",
                "buttons": [
                    {
                        "method": "animate",
                        "args": [
                            None,
                            {
                                "mode": "immediate",
                                "fromcurrent": "true",
                                "transition": {"duration": 0},
                                "frame": {"duration": 50, "redraw": False},  # TODO
                            },
                        ],
                        "label": "Play",
                    },
                    {
                        "method": "animate",
                        "args": [
                            [None],
                            {
                                "mode": "immediate",
                                "transition": {"duration": 0},
                                "frame": {"duration": 0, "redraw": False},  # TODO
                            },
                        ],
                        "label": "Pause",
                    },
                ],
            }
        ],
        "sliders": [
            {
                "steps": sliderSteps,
            }
        ],
    }
    fig = plotly.graph_objects.Figure([], layout | layout_list[0], frames)
    return fig
