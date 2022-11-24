from utils import manhattan_distance, manhattan_distance_between_players
import numpy as np


def pacman_heuristic(game):
    ghost_impact = 1
    food_impact = 10

    for ghost in game.ghosts:
        distance_with_ghost = manhattan_distance_between_players(ghost, game.pacman)
        # if newGhostState.scaredTimer == 0:
        if distance_with_ghost == 0:
            return -10000
        else:
            ghost_score = -ghost_impact / distance_with_ghost
        # else:
        #     if distance_with_ghost == 0:
        #         ghost_score = ghost_impact
        #     else:
        #         ghost_score = 0

    closest_food = None
    food_coordinates = [
        (np.where(game.dots == 1)[0][i], np.where(game.dots == 1)[1][i])
        for i in range(len(np.where(game.dots == 1)[0]))
    ]
    for food in food_coordinates:
        food_distance = manhattan_distance(food, (game.pacman.line, game.pacman.column))
        if closest_food is None or food_distance < closest_food:
            closest_food = food_distance

    if closest_food == 0 or closest_food is None:
        food_distance = 1000
    else:
        food_distance = food_impact / food_distance

    food_quantity = 100 * 1 / game.dots.sum() if game.dots.sum() != 0 else 10000
    result = {
        "ghost_score": ghost_score,
        "food_distance": food_distance,
        "food_quantity": food_quantity,
    }

    return ghost_score + food_distance + food_quantity


def ghost_heuristic(game):
    result = 0
    for ghost in game.ghosts:
        distance = manhattan_distance_between_players(ghost, game.pacman)
        result += distance
    return result
