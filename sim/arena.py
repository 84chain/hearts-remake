import logging

import numpy as np
from tqdm import tqdm

from setup.card import *

log = logging.getLogger(__name__)


class Arena:
    """
    An Arena class where any 2 agents can be pit against each other.
    """

    def __init__(self, player1, player2, player3, player4, game):
        """
        Input:
            player 1,2,3,4: functions that takes board as input, return action
            game: Game object
        """
        self.player1 = player1
        self.player2 = player2
        self.player3 = player3
        self.player4 = player4
        self.game = game

    def play_game(self, verbose=False):
        """
        Executes one episode of a game.
        Returns:
            either
                winner: player who won the game (1 if player1, -1 if player2)
            or
                draw result returned from the game that is neither 1, -1, nor 0.
        """
        players = [self.player1, self.player2, self.player3, self.player4]
        state = self.game.get_init_state()

        for round_num in range(13):
            for turn in range(4):
                if verbose:
                    print("Round ", str(round_num+1), ", Turn ", str(turn+1), ", Player ", str(state.current_player+1))

                # action = players[state.current_player](state)
                action = players[state.current_player].play(state)  # TEMPORARY
                valid_moves = self.game.get_valid_moves(state)
                if verbose:
                    print("Action played: ", Card(action).to_short_string())
                if valid_moves[action] == 0:
                    log.error(f'Action {Card(action).to_short_string()} is not valid!')
                    log.debug(f'valids = {valid_moves}')
                    assert valid_moves[action] > 0

                state = self.game.get_next_state(state, action)
            self.player1.update(state)
            self.player2.update(state)
            self.player3.update(state)
            self.player4.update(state)
            if verbose:
                print("\n")

        final_points = self.game.get_score(state)
        if verbose:
            print("Game over! Result ", final_points)
            total = 0
            for val in state.point_cards:
                total += val
        return final_points

    def play_games(self, num, verbose=False):
        """
        Plays num games
        Returns:
            list of total points collected
            dict of placings
        """

        total_points = np.zeros(4)
        total_rankings = np.zeros([4, 4])

        for _ in tqdm(range(num), desc="Arena.playGames"):
            game_result = self.play_game(verbose=verbose)
            rankings = [sorted(game_result).index(x) for x in game_result]

            for i in range(4):
                total_points[i] += game_result[i]
                total_rankings[i][rankings[i]] += 1

            self.player1.reset_player()
            self.player2.reset_player()
            self.player3.reset_player()
            self.player4.reset_player()

        return total_points, total_rankings