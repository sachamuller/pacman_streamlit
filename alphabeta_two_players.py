import numpy as np
from utils import Action


def get_pacman_action_with_minimax(
    game,
    evaluate_game_state,
    pacman,
    ghost,
):
    return Action(
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
        )[0],
    )


def minimax(
    game,
    depth,
    alpha,  # - inf
    beta,  # + inf
    is_max_player: bool,
    evaluate_game_state,
    max_player,
    min_player,
):
    if depth == 0 or game.game_over or game.game_won:
        return "", evaluate_game_state(game)

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
            )
            if highest_evaluation < evaluation:
                highest_evaluation = evaluation
                best_direction = direction
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
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
            )
            if lowest_evaluation > evaluation:
                lowest_evaluation = evaluation
                best_direction = direction
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return best_direction, lowest_evaluation
