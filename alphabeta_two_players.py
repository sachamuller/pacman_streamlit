import numpy as np
from utils import Action
from tree import Node, Tree
from plot_tree import plot_tree
from utils import NodeTypes


def get_pacman_action_with_minimax(
    game,
    evaluate_game_state,
    pacman,
    ghost,
):
    initial_node = Node(
        value=None, parent_node=None, from_action=None, node_type=NodeTypes.max
    )
    action = Action(
        pacman,
        minimax(
            game,
            depth=5,
            alpha=-np.inf,
            beta=np.inf,
            is_max_player=True,
            evaluate_game_state=evaluate_game_state,
            max_player=pacman,
            min_player=ghost,
            parent_node=initial_node,
            from_action=None,
        )[0],
    )
    tree_data, tree_layout = plot_tree(Tree(initial_node), show=False)
    return action, tree_data, tree_layout


def minimax(
    game,
    depth,
    alpha,  # - inf
    beta,  # + inf
    is_max_player: bool,
    evaluate_game_state,
    max_player,
    min_player,
    parent_node,
    from_action,
):

    if from_action is None:
        # means this is the first time we enter minimax and parent_node is the initial one
        current_node = parent_node
    else:
        current_node = Node(
            value=None,
            parent_node=parent_node,
            from_action=from_action,
            node_type=NodeTypes.max if is_max_player else NodeTypes.min,
        )

    if depth == 0 or game.game_over or game.game_won:
        evaluation = evaluate_game_state(game)
        current_node.update_value(evaluation)
        return "", evaluation

    if is_max_player:
        highest_evaluation = -np.inf
        best_direction = None
        for direction in game.get_legal_directions(max_player.name):
            min_direction, evaluation = minimax(
                game.project_next_state(Action(max_player, direction)),
                depth - 1,
                alpha,
                beta,
                False,
                evaluate_game_state,
                max_player,
                min_player,
                parent_node=current_node,
                from_action=direction,
            )
            if highest_evaluation < evaluation:
                highest_evaluation = evaluation
                best_direction = direction
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        current_node.update_value(highest_evaluation)
        return best_direction, highest_evaluation

    else:
        lowest_evaluation = +np.inf
        best_direction = None
        for direction in game.get_legal_directions(min_player.name):
            max_direction, evaluation = minimax(
                game.project_next_state(Action(min_player, direction)),
                depth - 1,
                alpha,
                beta,
                True,
                evaluate_game_state,
                max_player,
                min_player,
                parent_node=current_node,
                from_action=direction,
            )
            if lowest_evaluation > evaluation:
                lowest_evaluation = evaluation
                best_direction = direction
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        current_node.update_value(lowest_evaluation)
        return best_direction, lowest_evaluation
