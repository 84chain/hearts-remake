from player.players.teams.aggressive_player import AggressivePlayer
from player.templates.arena_player import *
from player.players.teams.shoot_player import ShootPlayer
from setup.setup import *


class AggressiveArenaPlayer(ArenaPlayer, AggressivePlayer, ShootPlayer):
    def __init__(self, game, id):
        self.game = game
        ArenaPlayer.__init__(self, game, id)

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
        AggressiveArenaPlayer.is_missing_Suit(self, table)

        if len(valid_moves) == 1:
            card = Card(valid_moves[0])
        else:
            if self.is_shooting:
                if state.turn == 0:
                    card = ShootPlayer.shoot_first(self)
                elif state.turn == 1 or state.turn == 2:
                    card = ShootPlayer.shoot_2nd_or_3rd(self, table)
                elif state.turn == 3:
                    card = ShootPlayer.shoot_last(self, table)
            else:
                if state.turn == 0:
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

        AggressiveArenaPlayer.deal_hand(self, hand_list)

        return card.to_int()
