from player.templates.pawn import *
from player.players.aggressive_player import Player
from setup.setup import *
from setup.card import Card

class ArenaPlayer(Player):
    def __init__(self, game):
        self.game = game
        Player.__init__(self, 0, "")

    def reset_player(self):
        self.card = -1
        self.points = 0
        self.cards_took = []
        self.cards_played = []
        self.self_cards = []
        self.has_10 = False
        self.pawns = [Pawn(i) for i in [0, 1, 2, 3]]

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

        table = Table()
        for i in range(state.turn):
            table.card_played(Card(state.round_played[i]), self)
        duped_list = self.cards_played + table.cards
        self.cards_played = list(set(duped_list))

        if len(valid_moves) == 1:
            card = Card(valid_moves[0])
        elif state.turn == 0:
            card = Player.play_first(self)
        elif state.turn == 1:
            card = Player.play_second(self, table)
        elif state.turn == 2:
            card = Player.play_third(self, table)
        elif state.turn == 3:
            card = Player.play_last(self, table)
        self.card = card
        self.cards_played.append(card)
        self.self_cards.append(card)

        return card.to_int()

    def update(self, state):
        table = Table()
        for i in range(4):
            table.card_played(Card(state.round_played[i]), self.pawns[i])
        if is_taking(table, self.card):
            self.cards_took += table.cards
        if all_same_suit_alt(table, self.card):
            player_ids = player_order(card_index(self.card, table.cards))
            for i in range(4):
                self.pawns[player_ids[i]].play_card(Card(table.cards[i]))
        else:
            suit = table.suit
            no_suit_players = no_suits(table, self.card)
            if no_suit_players:
                for pawn in no_suit_players:
                    self.pawns[pawn].is_missing(suit)