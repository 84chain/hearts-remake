from player.players.cheater import Cheater
from player.templates.arena_player import ArenaPlayer
from setup.card import Card
from setup.setup import *
from setup.hand import Hand

class ArenaCheater(Cheater, ArenaPlayer):
    def __init__(self, game, id):
        self.game = game
        Cheater.__init__(self, id, "c")
        ArenaPlayer.__init__(self, game, id)

    def play(self, state):
        self.cheat(state.hands[1], state.hands[2], state.hands[3])
        legal_moves = self.game.get_valid_moves(state)
        valid_moves = []
        for i in range(52):
            if legal_moves[i] == 1:
                valid_moves.append(i)

        hand_list = []
        for i in long_to_list(state.hands[state.current_player]):
            hand_list.append(Card(i))
        self.hand = Hand(hand_list)

        table = Table()
        for i in range(state.turn):
            table.card_played(Card(state.round_played[i]), self)
        duped_list = self.cards_played + table.cards
        self.cards_played = list(set(duped_list))

        if len(valid_moves) == 1:
            card = Card(valid_moves[0])
        elif state.turn == 0:
            card = Cheater.play_first(self)
        elif state.turn == 1:
            card = Cheater.play_second(self, table)
        elif state.turn == 2:
            card = Cheater.play_third(self, table)
        elif state.turn == 3:
            card = Cheater.play_last(self, table)
        self.card = card
        self.cards_played.append(card)
        self.self_cards.append(card)

        return card.to_int()
