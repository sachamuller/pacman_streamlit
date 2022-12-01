import numpy as np

from utils import (
    Directions,
    euclidean_distance,
    manhattan_distance_between_players,
)


def pacman_heuristic(maze, dots, power_pellets, pacman, ghost):
    result = 100 * -dots.sum()
    if dots.sum() == 0:
        result += 10000
    if ghost.line == pacman.line and ghost.column == pacman.column:
        if ghost.is_zombie:
            result += 1000
        else:
            result -= 1000
    food_column, food_line = np.where(dots == 1)
    print(np.where(dots == 1))
    for i in range(len(food_column)):
        result -= euclidean_distance(
            [food_line[i], food_column[i]], [pacman.line, pacman.column]
        )
    return result


def ghost_strategy(ghost, game, acceptable_distance=5):
    direction = ghost_bfs(ghost, game)
    if ghost.is_zombie:
        # if zombie and pacman is too close we take opposite direction as we would have taken to reach pacman
        if manhattan_distance_between_players(game.pacman, ghost) < acceptable_distance:
            return get_opposite_direction(direction)
    return direction


def ghost_bfs(ghost, game):
    my_map = -1 * np.ones(game.maze.shape)
    pacman_line = game.pacman.line
    pacman_column = game.pacman.column

    if ghost.line == pacman_line and ghost.column == pacman_column:
        return Directions.stay

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


def get_opposite_direction(direction):
    if direction == Directions.down:
        return Directions.up
    if direction == Directions.up:
        return Directions.down
    if direction == Directions.right:
        return Directions.left
    if direction == Directions.left:
        return Directions.right
    if direction == Directions.stay:
        return direction
