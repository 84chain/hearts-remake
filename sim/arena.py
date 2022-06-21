import logging

import numpy as np
import random
from setup.hand import Hand
from setup.setup import team_cards
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
        self.results = list()

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
        state = self.game.get_deal_state()  # deal hands to state

        # deal hands to players
        for i in range(4):
             players[i].deal_hand(Hand(state.hands[i]).to_list())

        # set teams of players
        teams = [i for i in team_cards]
        random.shuffle(teams)
        for i in range(4):
            players[i].team_card = teams[i]
            if teams[i].is_eq(black_ace):
                ace_player = players[i]

        # black ace shows
        for i in range(4):
            players[i].ace_reveal(ace_player)

        # record teams
        game_teams = [{"player": i.id, "card": i.team_card} for i in players]

        # players choose pass
        passes = [i.pass_cards() for i in players]
        int_passes = [Hand(i).to_int() for i in passes]  # converted to integer
        pass_dir = random.choice([-1, 1, 2])  # randomly chosen pass direction

        # pass cards to state
        state = self.game.get_pass_state(int_passes, pass_dir)

        # pass cards to player
        for i in range(4):
            players[(i + pass_dir) % 4].receive_pass(passes[i])

        has_shooter = 0
        has_shot = 0

        for round_num in range(13):
            for turn in range(4):
                if verbose:
                    print("Round ", str(round_num + 1), ", Turn ", str(turn + 1), ", Player ",
                          str(state.current_player + 1))

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
            if True in [i.is_shooting for i in players]:
                has_shooter = 1
            self.player1.update_round(state)
            self.player2.update_round(state)
            self.player3.update_round(state)
            self.player4.update_round(state)
            if verbose:
                print("\n")

        final_points, shoot_results = self.game.get_score(state)
        if 1 in shoot_results:
            if players[shoot_results.index(1)].name != "r":
                has_shot = 1

        if verbose:
            print("Game over! Result ", final_points)
            total = 0
            for val in state.point_cards:
                total += val

        return {
            "points": final_points,
            "shooter": has_shooter,
            "shot": has_shot,
            "teams": game_teams
        }

    def play_games(self, num, verbose=False):
        """
        Plays num games
        Returns:
            list of total points collected
            dict of placings
        """

        total_points = np.zeros(4)
        points = [[], [], [], []]
        total_rankings = np.zeros([4, 4])
        black_wins = 0
        red_wins = 0
        ties = 0

        total_ai_points = np.zeros(4)
        ai_points = [[], [], [], []]

        ai_players = [i.id for i in [self.player1, self.player2, self.player3, self.player4] if i.name != "r"]
        shoot_attempts = []
        successful_shoot = []

        for _ in tqdm(range(num), desc="Arena.playGames"):
            game_result = self.play_game(verbose=verbose)

            game_points = game_result["points"]
            shoot_attempt = game_result["shooter"]
            shoot_result = game_result["shot"]
            teams = game_result["teams"]
            black_ids = [i["player"] for i in teams if i["card"].suit == "c"]
            red_ids = [i["player"] for i in teams if i["card"].suit == "d"]

            rankings = [sorted(game_points).index(x) for x in game_points]
            shoot_attempts.append(shoot_attempt)
            successful_shoot.append(shoot_result)

            black_points = sum([game_points[i] for i in black_ids])
            red_points = sum([game_points[i] for i in red_ids])

            if black_points == red_points:
                ties += 1
            else:
                if black_points < red_points:
                    black_wins += 1
                else:
                    red_wins += 1

            for i in range(4):
                if i in ai_players:
                    total_ai_points[i] += game_points[i]
                    ai_points[i].append(game_points[i])

                total_points[i] += game_points[i]
                points[i].append(game_points[i])
                total_rankings[i][rankings[i]] += 1

            self.player1.reset_player()
            self.player2.reset_player()
            self.player3.reset_player()
            self.player4.reset_player()

        return {
            "total_points": total_points,
            "total_ai_points": total_ai_points,
            "total_rankings": total_rankings,
            "points": points,
            "ai_points": ai_points,
            "shoot_attempts": shoot_attempts,
            "successful_shoot": successful_shoot,
            "black_wins": black_wins,
            "red_wins": red_wins,
            "ties": ties
        }