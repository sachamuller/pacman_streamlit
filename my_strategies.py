import numpy as np

from utils import (
    Directions,
    euclidean_distance,
    manhattan_distance,
    manhattan_distance_between_players,
)


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


def ghost_bfs(ghost, game):
    my_map = -1 * np.ones(game.maze.shape)
    pacman_line = game.pacman.line
    pacman_column = game.pacman.column

    current_cell = [ghost.line, ghost.column]
    my_map[ghost.line][ghost.column] = 0
    depth = 1
    my_map, frontier = get_neighbour_cells_and_paint_map(
        game, current_cell, depth, my_map
    )
    while len(frontier) > 0 and [pacman_line, pacman_column] not in frontier:
        current_cell = frontier.pop(0)
        depth = my_map[current_cell[0]][current_cell[1]] + 1
        my_map, new_frontier = get_neighbour_cells_and_paint_map(
            game, current_cell, depth, my_map
        )
        frontier += new_frontier

    # backtrack :
    backward_path = [[pacman_line, pacman_column]]
    depth = my_map[pacman_line][pacman_column]
    current_cell = [pacman_line, pacman_column]
    while my_map[backward_path[-1][0]][backward_path[-1][1]] != 0:
        current_cell = get_neighbour_with_adequate_depth(
            current_cell, depth, my_map, pacman_line, pacman_column
        )
        backward_path.append(current_cell)
        depth -= 1
    return get_direction_from_adjacent_cells(backward_path[-1], backward_path[-2])


def get_neighbour_cells_and_paint_map(game, cell, depth, my_map):
    neighbours = []
    for neighbour in [
        [cell[0] + 1, cell[1]],
        [cell[0] - 1, cell[1]],
        [cell[0], cell[1] + 1],
        [cell[0], cell[1] - 1],
    ]:
        if (
            game.maze[neighbour[0]][neighbour[1]] != 1
            and my_map[neighbour[0]][neighbour[1]] == -1
        ):
            neighbours.append(neighbour)
            my_map[neighbour[0]][neighbour[1]] = depth
    return my_map, neighbours


def get_neighbour_with_adequate_depth(cell, depth, my_map, pacman_line, pacman_column):
    candidates = []
    for neighbour in [
        [cell[0] + 1, cell[1]],
        [cell[0] - 1, cell[1]],
        [cell[0], cell[1] + 1],
        [cell[0], cell[1] - 1],
    ]:
        if my_map[neighbour[0]][neighbour[1]] == depth - 1:
            candidates.append(neighbour)
    if len(candidates) == 0:
        raise ValueError("Backtracking failed")
    candidates.sort(
        key=lambda x: euclidean_distance((x[0], x[1]), (pacman_line, pacman_column))
    )
    return candidates[0]


def get_direction_from_adjacent_cells(my_cell, my_future_cell):
    if my_future_cell[0] - my_cell[0] == -1:
        return Directions.down
    if my_future_cell[0] - my_cell[0] == +1:
        return Directions.up
    if my_future_cell[1] - my_cell[1] == -1:
        return Directions.left
    if my_future_cell[1] - my_cell[1] == +1:
        return Directions.right
