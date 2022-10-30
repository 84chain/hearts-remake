import random

from state import State
from setup.setup import *

class Context:
    def __init__(self):
        self.round = 1
        self.cards_played = []
        self.players = []
        self.player_ids = []

        self.current_state = State()
        self.past_states = []

    def init(self, players):
        self.players = players
        self.player_ids = [i.id for i in players]
        deck = all_cards
        random.shuffle(deck)

        for i in range(4):
            players[i].set_hand(deck[i * 13: (i + 1) * 13])
            players[i].initialize_pawns(self.player_ids)

    def execute_pass(self, direction):
        passes = []
        for i in self.players:
            passes.append(i.get_pass())
        for i in range(4):
            self.players[(i + direction) % 4].receive_pass(passes[i])

    def play(self, card, player):
        self.current_state.update(card, player)
        self.cards_played.append(card)

        if self.current_state.length() == 4:
            self.past_states.append(self.current_state)
            self.current_state = State()
            self.round += 1

            for p in self.players:
                p.update(self)

    def result(self):
        return "\n".join([f"Player {i.id}: {i.get_points()} points" for i in self.players])