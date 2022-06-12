from player.templates.pawn import *
from setup.setup import *
from setup.suit import *
from setup.table import *
from setup.controls import *

class Player:
    def __init__(self, id, name):
        """
        Base template for Player classes
        :param id: int
        :param name: str
        """
        self.id = id
        self.name = name
        self.points = 0
        self.round = 0
        self.cards_took = []
        self.cards_played = []
        self.self_cards = []
        self.has_10 = False
        self.has_shot = False
        self.is_shooting = False
        self.shoot_blocked = False
        self.possible_takes = []
        self.guaranteed_takes = []
        self.pawns = [Pawn(i) for i in [0, 1, 2, 3]]
        self.risk_tolerance = risk_tolerance

    def deal_hand(self, list_card):
        """
        Deals hand to Player
        :param list_card: list(Card)
        :return: None
        """
        self.hand = Hand(list_card)
        self.list_hand = self.hand.to_list()

    def pass_cards(self):
        """
        Chooses pass and removes pass from hand, returns chosen pass in a list
        :return: list(Card)
        """
        cards = choose_pass(self.hand)
        remaining_hand = [c for c in self.list_hand if c.to_int() not in [i.to_int() for i in cards]]
        self.hand = Hand(remaining_hand)
        return cards

    def receive_pass(self, cards):
        """
        Receives a pass and appends pass to hand
        :param cards: list(Card)
        :return: None
        """
        new_hand = self.hand.to_list() + cards
        self.hand = Hand(new_hand)

    def count_points(self):
        """
        Tallies points
        :return: int
        """
        if len([i for i in self.cards_took if i.suit == "h"]) == 13:
            if in_hand(d_jack, Hand(self.cards_took)):
                self.points -= 100
                remaining_takes = [i for i in self.cards_took if not i.is_eq(d_jack)]
            else:
                remaining_takes = self.cards_took
            for card in remaining_takes:
                if card.is_eq(club_10):
                    pass
                else:
                    self.points -= card.points
        else:
            for card in self.cards_took:
                self.points += card.points
        if bool(len([c for c in self.cards_took if c.is_eq(club_10)])):
            self.points -= 10
            if self.points == 0:
                self.points = -50
            else:
                self.points *= 2
            self.has_10 = True
        return self.points

    def running_count(self):
        """
        Returns a running count of points without changing the field
        :param cards_took: list(Card)
        :return: int
        """
        points = Player.count_points(self)
        self.points = 0
        return points

    def set_tolerance(self, tolerance):
        """
        Sets risk_tolerance to tolerance
        :param tolerance: float
        :return: None
        """
        self.risk_tolerance = tolerance

    def legal_moves(self, first_card):
        """
        All legal moves given the first card of the round (never called when playing first)
        :param first_card: Card()
        :return: list(Card)
        """

        if first_card.suit == "c":
            return self.hand.diamonds + self.hand.spades + self.hand.hearts if not self.hand.clubs else self.hand.clubs
        elif first_card.suit == "d":
            return self.hand.clubs + self.hand.spades + self.hand.hearts if not self.hand.diamonds else self.hand.diamonds
        elif first_card.suit == "s":
            return self.hand.clubs + self.hand.diamonds + self.hand.hearts if not self.hand.spades else self.hand.spades
        elif first_card.suit == "h":
            return self.hand.clubs + self.hand.diamonds + self.hand.spades if not self.hand.hearts else self.hand.hearts

    def has_suit(self, first_card):
        """
        Whether Player owns the suit of firstcard or not
        :param first_card: Card()
        :return: bool
        """

        if first_card.suit == "c":
            return bool(len(self.hand.clubs))
        elif first_card.suit == "d":
            return bool(len(self.hand.diamonds))
        elif first_card.suit == "s":
            return bool(len(self.hand.spades))
        elif first_card.suit == "h":
            return bool(len(self.hand.hearts))

    def update_round(self, table):
        """
        Updates Player after a round
        :param table: Table()
        :return: None
        """
        self.round += 1
        if is_taking(table, self.card):
            self.cards_took += table.cards
        if all_same_suit(table, self.card):
            player_ids = player_order(card_index(self.card, table.cards))
            for i in range(4):
                self.pawns[player_ids[i]].play_card(table.cards[i])
        else:
            suit = table.suit
            no_suit_players = no_suits(table)
            if no_suit_players:
                for pawn in no_suit_players:
                    self.pawns[pawn].is_missing(suit)
        for p in self.pawns:
            Pawn.update_round(p, table)
        self.cards_played += table.cards

    def is_missing_Suit(self, table):
        other_pawns = [p for p in self.pawns if p.id != self.id]
        cloned_pawns = [p.create_clone(table.suit) if p.id not in table.player_ids else p for p in other_pawns]
        target_combinations = calculate_combinations(order_pools(cloned_pawns, self.cards_played, self.hand))
        total_combinations = calculate_combinations(order_pools(other_pawns, self.cards_played, self.hand))
        if total_combinations == 0:
            chance = 0
        else:
            chance = target_combinations / total_combinations
        return chance

    def choose_card(self):
        """
        Behaviour: Farm
        Chooses card to play when playing first in round
        :return: Card()
        """
        clubs = self.hand.clubs
        diamonds = self.hand.diamonds
        spades = self.hand.spades
        hearts = self.hand.hearts
        card_list = []
        for card in self.hand.list:
            suit = card.suit
            if suit == "c":
                clubs_left = [c for c in all_clubs if c.value not in (
                        [i.value for i in clubs] + [k.value for k in Hand(self.cards_played).clubs])]
                len_clubs = len(clubs_left)
                clubs_left.append(card)
                position = [club.to_int() for club in sorted(clubs_left, key=lambda x: x.value)].index(
                    card.to_int())
                c_scale = len([c for c in clubs if c.value > 10])
                card_list.append([card, len_clubs - position - c_scale])
            elif suit == "d":
                diamonds_left = [d for d in all_diamonds if d.value not in (
                        [i.value for i in diamonds] + [k.value for k in Hand(self.cards_played).diamonds])]
                len_diamonds = len(diamonds_left)
                diamonds_left.append(card)
                position = [diamond.to_int() for diamond in sorted(diamonds_left, key=lambda x: x.value)].index(
                    card.to_int())
                if played(d_jack, self.cards_played):
                    d_scale = len([d for d in diamonds if d.value > 11])
                else:
                    d_scale = 0
                card_list.append([card, len_diamonds - position - d_scale])
            elif suit == "s":
                spades_left = [s for s in all_spades if s.value not in (
                        [i.value for i in spades] + [k.value for k in Hand(self.cards_played).spades])]
                len_spades = len(spades_left)
                spades_left.append(card)
                position = [spade.to_int() for spade in sorted(spades_left, key=lambda x: x.value)].index(
                    card.to_int())
                if card.value != 12:
                    s_scale = len([s for s in spades if s.value >= 12])
                    if in_hand(q_spades, self.hand):
                        s_scale += 1
                    card_list.append([card, len_spades - position - s_scale])
                else:
                    card_list.append([card, -1])
            elif suit == "h":
                hearts_left = [h for h in all_hearts if h.value not in (
                        [i.value for i in hearts] + [k.value for k in Hand(self.cards_played).hearts])]
                len_hearts = len(hearts_left)
                hearts_left.append(card)
                position = [heart.to_int() for heart in sorted(hearts_left, key=lambda x: x.value)].index(
                    card.to_int())
                card_list.append([card, len_hearts - position - (len(hearts) + card.points / 50)])
        return sorted(card_list, key=lambda x: (x[-1], x[0].value))[-1][0]

    def block_j(self):
        """
        Behaviour: Blocking
        Blocks J of Diamonds
        :return: Card()
        """
        high_diamonds = [i for i in self.hand.diamonds if i.value > 11]
        low_diamonds = [i for i in self.hand.diamonds if i.value < 11]
        if high_diamonds:
            return self.hand.diamonds[-1]
        else:
            return low_diamonds[0]

    def avoid_taking(self, table):
        """
        Behaviour: Avoiding Taking
        :param table: Table()
        :return: Card()
        """
        highest = return_highest(table)

        if table.suit == "c":
            clubs = Suit(self.hand.clubs)
            lower_clubs = clubs.lower_cards(highest)
            if highest.value > 10:
                if in_hand(club_10, self.hand):
                    return club_10
                else:
                    return clubs.highest if not lower_clubs else lower_clubs[-1]
            else:
                if not lower_clubs:
                    return clubs.next_highest if clubs.highest.value == 10 else clubs.highest
                else:
                    return lower_clubs[-1]

        elif table.suit == "d":
            diamonds = Suit(self.hand.diamonds)
            lower_diamonds = diamonds.lower_cards(d_jack)
            higher_diamonds = diamonds.higher_cards(d_jack)
            if not lower_diamonds:
                if higher_diamonds:
                    return higher_diamonds[0]
                else:
                    return self.hand.diamonds[0]
            else:
                return lower_diamonds[-1]

        elif table.suit == "s":
            spades = Suit(self.hand.spades)
            lower_spades = spades.lower_cards(highest)
            if highest.value > 12:
                if in_hand(q_spades, self.hand):
                    return q_spades
                else:
                    return spades.highest if not lower_spades else lower_spades[-1]
            else:
                if not lower_spades:
                    return spades.next_highest if spades.highest.value >= 12 else spades.highest
                else:
                    return lower_spades[-1]

        elif table.suit == "h":
            hearts = Suit(self.hand.hearts)
            lower_hearts = hearts.lower_cards(highest)
            higher_hearts = hearts.higher_cards(heart_10)
            ten_point_hearts = [heart for heart in hearts.cards if heart.points <= 10]
            if not lower_hearts:
                if highest.value > 10:
                    if higher_hearts:
                        return higher_hearts[0]
                    else:
                        return self.hand.hearts[0]
                else:
                    if not ten_point_hearts:
                        if higher_hearts:
                            return higher_hearts[0]
                        else:
                            return self.hand.hearts[0]
                    else:
                        return ten_point_hearts[-1]
            else:
                return lower_hearts[-1]

    def safest_take(self, table):
        """
        Behaviour: Taking with best card
        :param table: Table()
        :return: Card()
        """
        highest = return_highest(table)
        table_points = table.points

        if table.suit == "c":
            clubs = Suit(self.hand.clubs)
            if table_points < 0:
                return club_10 if highest.value < 10 and in_hand(club_10, self.hand) else clubs.highest
            else:
                return clubs.highest

        elif table.suit == "d":
            diamonds = Suit(self.hand.diamonds)
            if j_blocked(table):
                lower_diamonds = [d for d in self.hand.diamonds if d.value < 11]
                if lower_diamonds:
                    return lower_diamonds[-1]
                else:
                    return [d for d in self.hand.diamonds if d.value > 11][0]
            else:
                if table_points < 0:
                    return diamonds.highest
                else:
                    return d_jack if in_hand(d_jack, self.hand) and highest.value < 11 else Player.avoid_taking(self,
                                                                                                                table)

        elif table.suit == "s":
            spades = Suit(self.hand.spades)
            if spades.highest.value == 12:
                if spades.next_highest.value == 12:
                    return self.hand.spades[-2]
                else:
                    return spades.next_highest
            else:
                return spades.highest

        elif table.suit == "h":
            hearts = Suit(self.hand.hearts)
            higher_hearts = hearts.higher_cards(highest)
            ten_point_hearts = [heart for heart in hearts.cards if heart.points <= 10]
            if not ten_point_hearts:
                if higher_hearts:
                    return higher_hearts[0]
                else:
                    return self.hand.hearts[-1]
            else:
                return ten_point_hearts[-1]

    def give_l(self):
        """
        Behaviour: Playing when Player is missing the suit
        :return: Card()
        """
        clubs = self.hand.clubs
        diamonds = self.hand.diamonds
        spades = self.hand.spades
        hearts = self.hand.hearts
        card_list = []
        for card in self.hand.list:
            suit = card.suit
            if suit == "c":
                clubs_left = [c for c in all_clubs if c.value not in
                              [i.value for i in clubs] and c.value not in [k.value for k in
                                                                           Hand(self.cards_played).clubs]]
                len_clubs = len(clubs_left)
                if len_clubs:
                    clubs_left.append(card)
                    position = [club.to_int() for club in sorted(clubs_left, key=lambda x: x.value)].index(
                        card.to_int())
                    c_scale = len([c for c in clubs if c.value > 10])
                    card_list.append([card, len_clubs - position + c_scale])
                else:
                    card_list.append([card, 99])
            elif suit == "d":
                diamonds_left = [d for d in all_diamonds if d.value not in
                                 [i.value for i in diamonds] and d.value not in [k.value for k in
                                                                                 Hand(self.cards_played).diamonds]]
                len_diamonds = len(diamonds_left)
                if len_diamonds:
                    diamonds_left.append(card)
                    position = [diamond.to_int() for diamond in
                                sorted(diamonds_left, key=lambda x: x.value)].index(
                        card.to_int())
                    d_scale = len([d for d in diamonds if d.value > 11])
                    if played(d_jack, self.cards_played):
                        card_list.append([card, len_diamonds - position + d_scale])
                    else:
                        if card.value != 11:
                            card_list.append([card, len_diamonds])
                        else:
                            card_list.append([card, 100])
                else:
                    card_list.append([card, 99])
            elif suit == "s":
                spades_left = [s for s in all_spades if s.value not in
                               [i.value for i in spades] and s.value not in [k.value for k in
                                                                             Hand(self.cards_played).spades]]
                len_spades = len(spades_left)
                if len_spades:
                    spades_left.append(card)
                    position = [spade.to_int() for spade in sorted(spades_left, key=lambda x: x.value)].index(
                        card.to_int())
                    if card.value != 12:
                        s_scale = len([s for s in spades if s.value >= 12])
                        card_list.append([card, len_spades - position + s_scale])
                    else:
                        card_list.append([card, -1])
                else:
                    card_list.append([card, 99])
            elif suit == "h":
                hearts_left = [h for h in all_hearts if h.value not in
                               [i.value for i in hearts] and h.value not in [k.value for k in
                                                                             Hand(self.cards_played).hearts]]
                len_hearts = len(hearts_left)
                if len_hearts:
                    hearts_left.append(card)
                    position = [heart.to_int() for heart in sorted(hearts_left, key=lambda x: x.value)].index(
                        card.to_int())
                    card_list.append([card, len_hearts - position - card.points / 50])
                else:
                    card_list.append([card, 99])
        sorted_list = sorted(card_list, key=lambda x: (x[-1], -x[0].value))

        return sorted_list[0][0]

    def gamble(self, table):
        """
        Deciding what to play when playing 2nd/3rd and/or uncertain
        :param moves: list(Card) (legal moves)
        :param table: Table()
        :return: Card()
        """
        if Player.is_missing_Suit(self, table) >= self.risk_tolerance:
            return Player.avoid_taking(self, table)
        else:
            return Player.safest_take(self, table)

    def can_shoot(self):
        """
        Whether Player can shoot or not
        :return: bool
        """
        hearts_played = [i.value for i in self.cards_played if i.suit == "h"]
        hearts_took = [i.value for i in self.cards_took if i.suit == "h"]
        return len(list(set(hearts_took + hearts_played))) == len(hearts_took)

    def play_first(self):
        """
        Plays first in the round
        :return: Card()
        """
        if in_hand(club_3, self.hand):
            return club_3
        else:
            return Player.choose_card(self)

    def play_second(self, table):
        """
        Plays second in the round
        :param table: Table()
        :return: Card()
        """
        return null_card

    def play_third(self, table):
        """
        Plays third in the round
        :param table: Table()
        :return: Card()
        """
        return null_card

    def play_last(self, table):
        """
        Plays last in round
        :param table: Table()
        :return: Card()
        """
        return null_card

# blank Player
null_player = Player(-1, "null")