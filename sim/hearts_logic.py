import numpy as np

class State:
    THREE_OF_CLUBS = 2  # bitmask for three of clubs

    def __init__(self):
        self.round = 0
        self.turn = 0
        self.hands = [0, 0, 0, 0]  # 4 longs, with each long containing 52 bits to model a set of cards
        self.current_player = -1
        self.round_played = [-1, -1, -1, -1]  # 4 ints, each int representing a single card
        self.cards_played = [0, 0, 0, 0]  # same with self.hands
        self.point_cards = [0, 0, 0, 0]  # 4 ints, with each int containing 15 bits for the 15 possible point cards

    def set_first_player(self):
        for i in range(4):
            if self.hands[i] & self.THREE_OF_CLUBS != 0:
                self.current_player = i
                break

    def get_legal_moves(self):
        # first round
        if self.round == 0 and self.turn == 0:
            return self.THREE_OF_CLUBS

        # first turn in round
        if self.turn == 0:
            return self.hands[self.current_player]

        suit = self.round_played[0] // 13
        suit_mask = ((1 << 13) - 1) << (13 * suit)
        matching_suit_cards = self.hands[self.current_player] & suit_mask
        # no cards of matching suit
        if matching_suit_cards == 0:
            return self.hands[self.current_player]

        return matching_suit_cards

    def execute_move(self, action):
        action_mask = 1 << action
        self.hands[self.current_player] &= ~action_mask  # remove action card from hand
        self.current_player = (self.current_player + 1) % 4
        self.round_played[self.turn] = action
        self.cards_played[self.current_player] |= action_mask  # add action card to cards_played of current_player
        self.turn += 1

        if self.turn == 4:  # fourth card played in round
            self.turn = 0
            self.round += 1
            self.trick_winner()
            self.take_hand()

    def trick_winner(self):  # sets self.current_player to the trick taker
        round_suit = self.round_played[0] // 13
        highest_value = self.round_played[0] % 13
        first_player_index = self.current_player
        for i in range(1, 4):
            if self.round_played[i] // 13 == round_suit and self.round_played[i] % 13 > highest_value:
                self.current_player = (first_player_index + i) % 4
                highest_value = self.round_played[i] % 13

    def take_hand(self):
        for card in self.round_played:
            # dude just trust me
            if card // 13 == 3:
                self.point_cards[self.current_player] |= 1 << (card - 39)
            elif card == 8: # 10 of clubs (0 * 13 + 10 - 2)
                self.point_cards[self.current_player] |= 1 << 13
            elif card == 22: # J of diamonds (1 * 13 + 11 - 2)
                self.point_cards[self.current_player] |= 1 << 14
            elif card == 36: # Q of spades (2 * 13 + 12 - 2)
                self.point_cards[self.current_player] |= 1 << 15

    def count_points(self):
        points = np.zeros(4)
        for i in range(4):
            pile = self.point_cards[i]

            moon_mask = (1 << 13) - 1
            if pile & moon_mask == moon_mask:  # has shot the moon
                points[i] = -200
                if (pile >> 15) & 1:  # queen of spades check
                    points[i] -= 100
            else:
                for j in range(3, 9):
                    if (pile >> j) & 1:
                        points[i] += 10
                if (pile >> 12) & 1:
                    points[i] += 50
                if (pile >> 11) & 1:
                    points[i] += 40
                if (pile >> 10) & 1:
                    points[i] += 30
                if (pile >> 9) & 1:
                    points[i] += 20
                if (pile >> 15) & 1:  # queen of spades check
                    points[i] += 100

            if (pile >> 14) & 1:  # jack of diamonds check
                points[i] -= 100

            if (pile >> 13) & 1 and not (pile & (pile - 1)):  # ten of clubs logic
                points[i] = -50
            elif (pile >> 13) & 1:
                points[i] *= 2
        return points

    @classmethod
    def copy_state(cls, state):
        new_state = cls()
        new_state.round = state.round
        new_state.turn = state.turn
        new_state.hands = state.hands.copy()
        new_state.current_player = state.current_player
        new_state.round_played = state.round_played.copy()
        new_state.cards_played = state.cards_played.copy()
        new_state.point_cards = state.point_cards.copy()
        return new_state