import numpy as np
from abc import ABC, abstractmethod


class AIPlayer(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def policy(self, current_state):
        """logic how to make turns"""
        pass


class SimplePlayer(AIPlayer):
    """it does random turns"""
    def __init__(self):
        super().__init__()

    def policy(self, game):
        """it chooses random cell"""
        available_indices, num_available = game.determine_available_cells()
        action = np.random.choice(available_indices)
        return action


class SmartPLayer(AIPlayer):
    def __init__(self):
        super().__init__()

    def policy(self, game):
        """logic which decides a turn to make by using minmax algorithm"""
        available_indices, num_available = game.determine_available_cells()

        if num_available == 9:
            action = np.random.choice(available_indices)
        else:
            action = self.__minmax(game, whose_turn=game.whose_turn)['position']
        return action

    def __minmax(self, game, whose_turn):
        """recursive algorithm that evaluates the reward of every step possible"""
        max_player = 1  # blue player, player1, X player
        other_player = 1 if whose_turn == 0 else 0

        available_indices, num_available = game.determine_available_cells()
        if game.winner == other_player:
            return {'position': None,
                    'score': 1 * num_available + 1 if other_player == max_player else -1 * num_available + 1}
        elif num_available == 0:
            return {'position': None, 'score': 0}

        if whose_turn == max_player:
            best = {'position': None, 'score': -np.inf}
        else:
            best = {'position': None, 'score': np.inf}
        for possible_move in available_indices:
            game.simulate_move(possible_move, whose_turn)
            simulation_score = self.__minmax(game, other_player)

            # undo move
            game.grid[possible_move] = -1
            game.winner = -1
            simulation_score['position'] = possible_move

            if whose_turn == max_player:  # X is max player
                if simulation_score['score'] > best['score']:
                    best = simulation_score
            else:
                if simulation_score['score'] < best['score']:
                    best = simulation_score

        return best
