from copy import deepcopy
from numpy.random import shuffle

from plot_pacman import create_layout
from utils import Directions, Orientations


class Game:
    def __init__(
        self,
        game_board,
        pacman_strategy,
        ghosts_strategy,
    ):
        self.maze = game_board.maze
        self.dots = game_board.dots
        self.power_pellets = game_board.power_pellets

        self.pacman = Pacman(game_board.pacman_start, strategy=pacman_strategy)
        self.ghosts = [
            Ghost(i + 1, game_board.ghost_start[i], strategy=ghosts_strategy[i])
            for i in range(len(game_board.ghost_start))
        ]
        self.players = [self.pacman] + self.ghosts

        self.game_over = False
        self.game_won = False

        # Check game is valid and update some things if necessary
        self.check_players_names_are_unique()
        self.update_dots()
        self.update_power_pellets()
        self.update_aliveness()
        self.is_game_over_or_won()

    def next_state(self, action):
        if not self.game_over or not self.game_won:
            for player in self.players:
                if player.name == action.player.name:
                    player.next(action, self.maze)
            self.update_dots()
            self.update_power_pellets()
            self.update_aliveness()
            self.update_ghost_timers()
            self.is_game_over_or_won()

    def project_next_state(self, action):
        game_copy = deepcopy(self)
        game_copy.next_state(action)
        return game_copy

    def check_players_names_are_unique(self):
        for i, player in enumerate(self.players):
            if player.name in [p.name for j, p in enumerate(self.players) if j != i]:
                raise ValueError(
                    f"All players should have unique names but {player.name} is used at least twice."
                )

    def update_dots(self):
        self.dots[self.pacman.line][self.pacman.column] = 0

    def update_power_pellets(self):
        if self.power_pellets[self.pacman.line][self.pacman.column] == 1:
            for ghost in self.ghosts:
                ghost.get_zombified()
            self.power_pellets[self.pacman.line][self.pacman.column] = 0

    def update_ghost_timers(self):
        for ghost in self.ghosts:
            ghost.update_zombie_timer()
            ghost.update_death_timer()

    def update_aliveness(self):
        self.pacman.is_still_alive(self.ghosts)
        for ghost in self.ghosts:
            ghost.is_still_alive(self.pacman)

    def is_game_over_or_won(self):
        if not self.pacman.alive:
            self.game_over = True
        elif self.dots.sum() == 0:
            self.game_won = True

    def get_legal_directions(self, player_name):
        player = [p for p in self.players if p.name == player_name][0]
        available_actions = [Directions.stay]
        if not self.maze[player.line + 1][player.column]:
            available_actions.append(Directions.up)
        if not self.maze[player.line - 1][player.column]:
            available_actions.append(Directions.down)
        if not self.maze[player.line][player.column + 1]:
            available_actions.append(Directions.right)
        if not self.maze[player.line][player.column - 1]:
            available_actions.append(Directions.left)
        shuffle(available_actions)
        return available_actions

    def run_and_get_layout(self, max_turns=None):
        list_layout = [create_layout(self)]
        count_turns = 0
        while (
            not self.game_over
            and not self.game_won
            and (max_turns is not None and count_turns < max_turns)
        ):
            for player in self.players:
                action = player.strategy(self)
                self.next_state(action)
                list_layout.append(create_layout(self))
                count_turns += 1
        return list_layout

    def __repr__(self) -> str:
        result = ""
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                done = False
                if self.maze[i][j]:
                    result += "X"
                    done = True
                if self.pacman.line == i and self.pacman.column == j and not done:
                    result += "P"
                    done = True
                for ghost in self.ghosts:
                    if ghost.line == i and ghost.column == j and not done:
                        result += "G"
                        done = True
                if self.dots[i][j] and not done:
                    result += "."
                    done = True
                if not done:
                    result += " "
            result += "\n"
        return result


class Player:
    def __init__(self, name, position, orientation, alive, strategy):
        self.name = name
        self.line = position[0]
        self.column = position[1]
        self.orientation = orientation
        self.alive = alive
        self.strategy = strategy

    def next(self, action, maze):
        if self.alive:
            self.next_position(action, maze)
            self.next_orientation(action)

    def next_position(self, action, maze):
        if action.direction == Directions.up and not maze[self.line + 1][self.column]:
            self.line += 1
        if action.direction == Directions.down and not maze[self.line - 1][self.column]:
            self.line -= 1
        if (
            action.direction == Directions.right
            and not maze[self.line][self.column + 1]
        ):
            self.column += 1
        if action.direction == Directions.left and not maze[self.line][self.column - 1]:
            self.column -= 1
        # if stay, on ne fait rien

    def next_orientation(self, action):
        if action.direction == Directions.up:
            self.orientation = Orientations.north
        if action.direction == Directions.down:
            self.orientation = Orientations.south
        if action.direction == Directions.right:
            self.orientation = Orientations.west
        if action.direction == Directions.left:
            self.orientation = Orientations.east

    def is_still_alive(self, ghosts, pacman):
        NotImplemented


class Pacman(Player):
    def __init__(
        self, position, orientation=Orientations.west, alive=True, strategy=None
    ):
        super().__init__(0, position, orientation, alive, strategy)

    def is_still_alive(self, ghosts):
        for ghost in ghosts:
            if (
                self.line == ghost.line
                and self.column == ghost.column
                and not ghost.is_zombie
                and ghost.alive
            ):
                self.alive = False


class Ghost(Player):
    def __init__(
        self,
        id=0,
        position=(0, 0),
        orientation=Orientations.east,
        alive=True,
        strategy=None,
        color="red",
    ):
        super().__init__(id, position, orientation, alive, strategy)
        self.is_zombie = False
        self.zombie_timer = -1
        self.death_timer = -1
        self.color = color
        self.initial_position = position

    def is_still_alive(self, pacman, time=10):
        if self.is_zombie:
            if self.line == pacman.line and self.column == pacman.column:
                self.alive = False
                self.death_timer = time
                self.is_zombie = False
                self.zombie_timer = -1
                self.line = self.initial_position[0]
                self.column = self.initial_position[1]

    def get_zombified(self, time=20):
        self.is_zombie = True
        self.zombie_timer = time

    def update_zombie_timer(self):
        if self.zombie_timer >= 0:
            self.zombie_timer -= 1
            if self.zombie_timer == -1:
                self.is_zombie = False

    def update_death_timer(self):
        if self.death_timer >= 0:
            self.death_timer -= 1
            if self.death_timer == -1:
                self.alive = True
