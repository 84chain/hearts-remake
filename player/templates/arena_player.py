from .player import *
from setup.setup import *
from setup.controls import *


class ArenaPlayer(Player):
    def __init__(self, game, id):
        self.game = game
        Player.__init__(self, id, "a")

    def reset_player(self):
        self.card = -1
        self.points = 0
        self.round = 0
        self.pawns = [Pawn(i) for i in [0, 1, 2, 3]]

        self.hand = Hand([])
        self.cards_took = []
        self.cards_played = []
        self.self_cards = []

        self.has_10 = False
        self.has_shot = False
        self.is_shooting = False
        self.shoot_blocked = False

        self.teammate = None
        self.team_card = null_card
        self.team_chances = [-1 if i == self.id else 0 for i in range(4)]

        self.possible_takes = []
        self.guaranteed_takes = []
        self.risk_tolerance = risk_tolerance

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
        else:
            if self.is_shooting:
                if state.turn == 0:
                    card = Player.shoot_first(self)
                elif state.turn == 1 or state.turn == 2:
                    card = Player.shoot_2nd_or_3rd(self, table)
                elif state.turn == 3:
                    card = Player.shoot_last(self, table)
            else:
                if state.turn == 0:
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

        if card.suit == "c":
            c_temp = [club for club in self.hand.clubs if club.value != card.value]
            hand_list = c_temp + self.hand.diamonds + self.hand.spades + self.hand.hearts
        elif card.suit == "d":
            d_temp = [diamond for diamond in self.hand.diamonds if diamond.value != card.value]
            hand_list = self.hand.clubs + d_temp + self.hand.spades + self.hand.hearts
        elif card.suit == "s":
            s_temp = [spade for spade in self.hand.spades if spade.value != card.value]
            hand_list = self.hand.clubs + self.hand.diamonds + s_temp + self.hand.hearts
        elif card.suit == "h":
            h_temp = [heart for heart in self.hand.hearts if heart.value != card.value]
            hand_list = self.hand.clubs + self.hand.diamonds + self.hand.spades + h_temp

        ArenaPlayer.deal_hand(self, hand_list)

        return card.to_int()

    def update_round(self, state):
        self.round += 1
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
        self.cards_played += table.cards
        if Player.can_shoot(self):
            if num_guaranteed_takes(self.hand, self.cards_played) >= (minimum_takes - self.round):
                self.is_shooting = True
                self.guaranteed_takes = guaranteed_takes(self.hand, self.cards_played)
                self.possible_takes = possible_takes(self.hand, self.cards_played)
            else:
                self.is_shooting = False
        else:
            self.is_shooting = False