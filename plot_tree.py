from igraph import Graph, EdgeSeq
import plotly


def plot_tree(tree, show=True):

    # code adapted from https://plotly.com/python/tree-plots/

    tree_dict_list = tree.convert_to_dict_list()
    tree.build_nodes_dict()

    G = Graph()
    G = G.ListDict(tree_dict_list)
    nr_vertices = G.vcount()
    v_label = [str(round(tree.nodes_dict[i].value, 2)) for i in range(nr_vertices)]

    lay = G.layout_reingold_tilford(mode="in", root=[0])

    position = {k: lay[k] for k in range(nr_vertices)}
    Y = [lay[k][1] for k in range(nr_vertices)]
    M = max(Y)

    es = EdgeSeq(G)  # sequence of edges
    E = [e.tuple for e in G.es]  # list of edges

    L = len(position)
    Xn = [position[k][0] for k in range(L)]
    Yn = [2 * M - position[k][1] for k in range(L)]
    Xe = []
    Ye = []
    # coordinated of the labels of the actions (which will go on the edges)
    X_actions_labels = []
    Y_actions_labels = []
    actions_labels = []
    for edge in E:
        Xe += [position[edge[0]][0], position[edge[1]][0], None]
        Ye += [2 * M - position[edge[0]][1], 2 * M - position[edge[1]][1], None]
        X_actions_labels.append((position[edge[0]][0] + position[edge[1]][0]) / 2)
        Y_actions_labels.append(
            ((2 * M - position[edge[0]][1]) + (2 * M - position[edge[1]][1])) / 2
        )
        actions_labels.append(str(tree.nodes_dict[edge[1]].from_action.name))

    data = []
    data.append(
        {
            "x": Xe,
            "y": Ye,
            "mode": "lines",
            "type": "scatter",
            "line": dict(color="rgb(210,210,210)", width=1),
            "text": actions_labels,
            "hoverinfo": "text",
        }
    )
    data.append(
        {
            "x": Xn,
            "y": Yn,
            "mode": "markers",
            "type": "scatter",
            "marker": dict(
                symbol="circle-dot",
                size=20,
                color="#6175c1",  #'#DB4551',
            ),
            "text": v_label,
            "hoverinfo": "text",
            "opacity": 0.8,
        }
    )

    def make_annotations(pos, text, font_size=10, font_color="rgb(250,250,250)"):
        L = len(pos)
        if len(text) != L:
            raise ValueError("The lists pos and text must have the same len")
        annotations = []
        for k in range(L):
            annotations.append(
                dict(
                    text=text[
                        k
                    ],  # or replace labels with a different list for the text within the circle
                    x=pos[k][0],
                    y=2 * M - position[k][1],
                    xref="x1",
                    yref="y1",
                    font=dict(color=font_color, size=font_size),
                    showarrow=False,
                )
            )
        return annotations

    def make_actions_annotations(
        X_actions_labels,
        Y_actions_labels,
        actions_labels,
        font_size=10,
        font_color="rgb(0,0,0)",
        max_number_annotations=300,
    ):
        annotations = []
        for k in range(len(actions_labels)):
            annotations.append(
                dict(
                    text=actions_labels[
                        k
                    ],  # or replace labels with a different list for the text within the circle
                    x=X_actions_labels[k],
                    y=Y_actions_labels[k],
                    xref="x1",
                    yref="y1",
                    font=dict(color=font_color, size=font_size),
                    showarrow=False,
                )
            )
        for k in range(max_number_annotations - len(actions_labels)):
            annotations.append(
                dict(
                    text="",
                    x=0,
                    y=0,
                    xref="x1",
                    yref="y1",
                )
            )
        return annotations

    layout = {
        "annotations": make_annotations(position, v_label)
        + make_actions_annotations(X_actions_labels, Y_actions_labels, actions_labels),
        "font_size": 12,
        "showlegend": False,
        "margin": dict(l=40, r=40, b=85, t=100),
        "hovermode": "closest",
        "plot_bgcolor": "rgb(248,248,248)",
    }

    if show:
        fig = plotly.graph_objects.Figure(data, layout)
        fig.show()
    return data, layout


def get_tree_ith_move(layout_list, data_list, move_id):
    data = data_list[move_id]
    layout = layout_list[move_id]
    print(layout)
    max_x = max(data[1]["x"])
    min_x = min(data[1]["x"])
    max_y = max(data[1]["y"])
    min_y = min(data[1]["y"])
    global_layout = {
        "xaxis": {
            "range": [min_x - (max_x - min_x) / 10, max_x + (max_x - min_x) / 10],
            "visible": False,
        },
        "yaxis": {
            "range": [min_y - (max_y - min_y) / 10, max_y + (max_y - min_y) / 10],
            "visible": False,
        },
    }
    fig = plotly.graph_objects.Figure(data, global_layout | layout)
    return fig


def get_tree_fig_from_data_and_layout_list(layout_list, data_list):
    max_x = max([max(data_list[i][1]["x"]) for i in range(len(data_list))])
    min_x = min([min(data_list[i][1]["x"]) for i in range(len(data_list))])
    max_y = max([max(data_list[i][1]["y"]) for i in range(len(data_list))])
    min_y = min([min(data_list[i][1]["y"]) for i in range(len(data_list))])
    frames = [
        {"name": f"{i*2}", "data": data_list[i], "layout": layout_list[i]}
        for i in range(len(layout_list))
    ]

    sliderSteps = [
        {
            "method": "animate",
            "label": f"{i*2}",
            "args": [
                [f"{i*2}"],
                {
                    "mode": "immediate",
                    "transition": {"duration": 0},
                    "frame": {"duration": 0, "redraw": True},
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
        ],
        "xaxis": {"range": [min_x - 1, max_x + 1], "visible": False},
        "yaxis": {
            "range": [min_y - 1, max_y + 1],
            "visible": False,
        },
    }
    fig = plotly.graph_objects.Figure(data_list[0], layout | layout_list[0], frames)
    return fig
