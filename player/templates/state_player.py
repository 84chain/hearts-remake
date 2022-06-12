from player.players.aggressive_player import Player
from setup.card import Card
from setup.setup import *
from setup.table import Table


class StatePlayer(Player):
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

    def update_round(self, state):
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
            no_suit_players = no_suits(table)
            if no_suit_players:
                for pawn in no_suit_players:
                    self.pawns[pawn].is_missing(suit)
