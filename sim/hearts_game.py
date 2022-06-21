from __future__ import print_function

import random

import numpy as np

from sim.hearts_logic import State

# TODO: add passing and teams

class HeartsGame(object):
    def get_deal_state(self):
        self.state = State()
        self.deal_cards(self.state)
        return self.state


    def get_pass_state(self, passes, pass_dir):
        self.state.pass_cards(passes, pass_dir)
        self.state.set_first_player()
        return self.state

    def deal_cards(self, state):
        cards = list(range(52))
        random.shuffle(cards)
        for i in range(4):
            mask = 0
            for j in range(13):
                mask |= 1 << cards[13 * i + j]
            state.hands[i] = mask

    def get_next_state(self, state, action):
        # if player takes action in current state, return next (state, player)
        # action must be a valid move
        s = State.copy_state(state)
        s.execute_move(action)
        return s

    def get_valid_moves(self, state):
        legal_moves = state.get_legal_moves()
        valid_moves = np.zeros(52)

        mask = 1
        for i in range(52):
            if legal_moves & mask != 0:
                valid_moves[i] = 1
            mask <<= 1
        return valid_moves

    def get_game_ended(self, state):
        return state.round == 13

    def number_representation(self, state):
        return hash(state)

    def get_score(self, state):
        return state.count_points()

    def get_rankings(self, state):
        points = self.get_score(state)
        rankings = [sorted(points).index(x) for x in points]
        for i in range(4):
            if rankings[i] == 0:
                rankings[i] = 1
            elif rankings[i] == 1:
                rankings[i] = 0.9
            elif rankings[i] == 2:
                rankings[i] = -0.9
            else:
                rankings[i] = -1
        return rankings

    @staticmethod
    def display(state):
        print(state.round)
        for hand in state.hands:
            print(hand)
        print(state.current_player)
        print(state.round_played)
        for hand in state.cards_played:
            print(hand)
        for hand in state.point_cards:
            print(hand)
