from utils import Action

MAX_DEPTH = 3


def get_action_with_minimax_alphabeta(game, player, players):
    next_action_value, next_action = get_value_min_or_max(
        game,
        player.name,
        players,
        current_depth=0,
        heuristic=player.heuristic,
        alpha=None,
        beta=None,
    )
    return Action(player, next_action)


def get_value_min_or_max(
    game,
    player_id: int,
    players,
    current_depth: int,
    heuristic,
    alpha: float,
    beta: float,
):

    # if the game is over or we reached the maximal depth
    if game.game_over or game.game_won or current_depth == MAX_DEPTH:
        return heuristic(game), ""

    if player_id == 0:  # means it's pacman, who is max
        return get_max(game, player_id, players, current_depth, heuristic, alpha, beta)
    else:  # means it's a ghost
        return get_min(game, player_id, players, current_depth, heuristic, alpha, beta)


def get_successor_value(
    game, player_id, players, current_depth, direction, heuristic, alpha, beta
):
    next_game_state = game.project_next_state(Action(players[player_id], direction))

    # if players is the last players, the ply is over and we start the next ply
    if player_id == len(game.players) - 1:
        next_player = 0  # pacman's turn again
        next_depth = current_depth + 1  # new depth
    # if not, we keep going with this ply and simply move on to the next player_id
    else:
        next_player = player_id + 1
        next_depth = current_depth

    return get_value_min_or_max(
        next_game_state, next_player, players, next_depth, heuristic, alpha, beta
    )


def get_max(
    game,
    player_id: int,
    players,
    current_depth: int,
    heuristic,
    alpha: float,
    beta: float,
):

    max_action, max_action_value = None, None

    for direction in game.get_legal_directions(player_id):
        next_value, next_action = get_successor_value(
            game, player_id, players, current_depth, direction, heuristic, alpha, beta
        )

        if max_action_value is None or next_value > max_action_value:
            max_action = direction
            max_action_value = next_value

        if beta is not None and max_action_value > beta:
            return max_action_value, max_action

        alpha = max(alpha, max_action_value) if alpha is not None else max_action_value

    return max_action_value, max_action


def get_min(
    game,
    player_id: int,
    players,
    current_depth: int,
    heuristic,
    alpha: float,
    beta: float,
):

    min_action, min_action_value = None, None

    for direction in game.get_legal_directions(player_id):
        next_value, next_action = get_successor_value(
            game, player_id, players, current_depth, direction, heuristic, alpha, beta
        )

        if min_action_value is None or next_value < min_action_value:
            min_action = direction
            min_action_value = next_value

        if alpha is not None and min_action_value < alpha:
            return min_action_value, min_action

        beta = min(beta, min_action_value) if beta is not None else min_action_value

    return min_action_value, min_action
