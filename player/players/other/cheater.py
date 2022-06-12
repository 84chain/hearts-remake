from player.players.teams.aggressive_player import AggressivePlayer


class Cheater(AggressivePlayer):
    """
    Cheater knows all Pawn hands at the start of the game
    """

    def cheat(self, hand2, hand3, hand4):
        self.pawns[1].deal_hand(hand2)
        self.pawns[2].deal_hand(hand3)
        self.pawns[3].deal_hand(hand4)
