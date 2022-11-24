from utils import manhattan_distance


def pacman_heuristic(game):
    return -game.dots.sum()


def ghost_heuristic(game):
    print(game)
    result = 0
    for ghost in game.ghosts:
        distance = manhattan_distance(ghost, game.pacman)
        print("DIST :", distance)
        if distance == 0:
            result += -1000
        else:
            result += -1 / distance
    print("GHOST HEUR :", result)
    return result
