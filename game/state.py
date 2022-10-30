from setup.setup import *

class State:
    def __init__(self):
        self.cards = []
        self.player_ids = []
        self.players = []
        self.suit = None

    def update(self, card, player):
        if not self.cards:
            self.suit = card >> 13

        self.cards.append(card)
        self.player_ids.append(player.id)
        self.players.append(player)

    def highest(self):
        try:
            return max([i for i in self.cards if i >> 13 == self.suit])
        except:
            return -1

    def length(self):
        return len(self.cards)

    def taker(self):
        return self.player_ids[self.cards.index(State.highest(self))]

    def points(self):
        return sum([all_points[i] for i in self.cards])