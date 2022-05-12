from player.templates.pawn import *
from player.players.aggressive_player import AggressivePlayer
from setup.setup import *

class Cheater(AggressivePlayer):
    def cheat(self, hand2, hand3, hand4):
        self.pawns[1].deal_hand(hand2)
        self.pawns[2].deal_hand(hand3)
        self.pawns[3].deal_hand(hand4)