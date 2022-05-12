from player.templates.pawn import *
from player.players.aggressive_player import AggressivePlayer
from player.templates.arena_player import ArenaPlayer
from setup.setup import *


class AggressiveArenaPlayer(ArenaPlayer):
    def __init__(self, game):
        self.game = game
        ArenaPlayer.__init__(self, game)

    def play(self, state):
        legal_moves = self.game.get_valid_moves(state)
        valid_moves = []
        for i in range(52):
            if legal_moves[i] == 1:
                valid_moves.append(i)

        hand_list = []
        for i in long_to_list(state.hands[state.current_player]):
            hand_list.append(Card(i))
        self.hand = Hand(hand_list)

        # TEST BEGINS
        # pools = order_pools([i for i in self.pawns if i.id != self.id], self.cardsPlayed, self.hand)
        # print(pools)
        # print([[i.hasClubs, i.hasDiamonds, i.hasSpades, i.hasHearts] for i in self.pawns])
        # TEST ENDS

        table = Table()
        for i in range(state.turn):
            table.card_played(Card(state.round_played[i]), self)
        duped_list = self.cards_played + table.cards
        self.cards_played = list(set(duped_list))

        if len(valid_moves) == 1:
            card = Card(valid_moves[0])
        elif state.turn == 0:
            card = AggressivePlayer.play_first(self)
        elif state.turn == 1:
            card = AggressivePlayer.play_second(self, table)
        elif state.turn == 2:
            card = AggressivePlayer.play_third(self, table)
        elif state.turn == 3:
            card = AggressivePlayer.play_last(self, table)
        self.card = card
        self.cards_played.append(card)
        self.self_cards.append(card)

        return card.to_int()