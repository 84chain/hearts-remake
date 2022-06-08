from player.templates.player import *


class AltruisticPlayer(Player):
    """
    Type of Player that is altruistic towards all players
    """

    def assign_teammate(self, teammate):
        """
        Assigns teammate
        :param teammate: Player()
        :return: None
        """
        self.teammate = teammate

    def choose_card(self):
        clubs = self.hand.clubs
        diamonds = self.hand.diamonds
        spades = self.hand.spades
        hearts = self.hand.hearts
        missing_suits = []
        for suit in ["c", "d", "s", "h"]:
            if not self.teammate.has_suit(suit):
                table = Table()
                if suit == "c" and clubs:
                    clubs_left = [c for c in all_clubs if c.value not in (
                            [i.value for i in clubs] + [k.value for k in Hand(self.cards_played).clubs])]
                    clubs_left.append(clubs[0])
                    position = [club.to_int() for club in sorted(clubs_left, key=lambda x: x.value)].index(
                        clubs[0].to_int())
                    setattr(table, "suit", "c")
                    missing_suits.append([clubs[0], position])
                elif suit == "d" and diamonds:
                    diamonds_left = [d for d in all_diamonds if d.value not in (
                            [i.value for i in diamonds] + [k.value for k in Hand(self.cards_played).diamonds])]
                    diamonds_left.append(diamonds[0])
                    position = [diamond.to_int() for diamond in sorted(diamonds_left, key=lambda x: x.value)].index(
                        diamonds[0].to_int())
                    setattr(table, "suit", "d")
                    if played(d_jack, self.cards_played):
                        missing_suits.append([diamonds[0], position])
                elif suit == "s" and spades:
                    spades_left = [s for s in all_spades if s.value not in (
                            [i.value for i in spades] + [k.value for k in Hand(self.cards_played).spades])]
                    spades_left.append(spades[0])
                    position = [spade.to_int() for spade in sorted(spades_left, key=lambda x: x.value)].index(
                        spades[0].to_int())
                    setattr(table, "suit", "s")
                    if spades[0].value != 12:
                        missing_suits.append([spades[0], position])
                elif suit == "h" and hearts:
                    hearts_left = [h for h in all_hearts if h.value not in (
                            [i.value for i in hearts] + [k.value for k in Hand(self.cards_played).hearts])]
                    hearts_left.append(hearts[0])
                    position = [heart.to_int() for heart in sorted(hearts_left, key=lambda x: x.value)].index(
                        hearts[0].to_int())
                    setattr(table, "suit", "h")
                    missing_suits.append([hearts[0], position])
        if missing_suits:
            return sorted(missing_suits, key=lambda x: x[-1], reverse=True)[0][0]
        else:
            return Player.choose_card(self)

    def give_l(self):
        """
        Override for give_l that considers teammate is taking
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
                    if card.is_eq(club_10) and self.teammate.points <= 0:
                        card_list.append([card, -1])
                    elif card.is_eq(club_10) and self.teammate.points > 0:
                        card_list.append([card, 99])
                    else:
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
                            card_list.append([card, -2])
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
                        card_list.append([card, 99])
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
                    if card.points == 0:
                        card_list.append([card, position])
                    else:
                        card_list.append([card, len_hearts + position + card.points / 50])
                else:
                    card_list.append([card, 99])
        sorted_list = sorted(card_list, key=lambda x: (x[-1], -x[0].value))

        return sorted_list[0][0]

    def play_second(self, table):
        """
        Decides on what card to play when playing 2nd
        :param table: Table()
        :return: Card()
        """
        moves = AltruisticPlayer.legal_moves(self, table.first_card)

        if len(moves) == 1:
            return moves[0]
        else:
            if AltruisticPlayer.has_suit(self, table.first_card):
                if self.has_10:
                    return AltruisticPlayer.avoid_taking(self, table)
                else:
                    if Table.current_taker(table).id == self.teammate.id and self.teammate.has_10:
                        return AltruisticPlayer.safest_take(self, table)
                    else:
                        if table.suit == "d":
                            if played(d_jack, self.cards_played):
                                return AltruisticPlayer.avoid_taking(self, table)
                            else:
                                if in_hand(d_jack, self.hand):
                                    if jack_highest(self.cards_played, self.hand):
                                        return d_jack
                                    else:
                                        return AltruisticPlayer.avoid_taking(self, table)
                                else:
                                    diamonds_left = [d for d in all_diamonds if d.value not in
                                                     [i.value for i in self.hand.diamonds] and d.value not in [k.value
                                                                                                               for k
                                                                                                               in
                                                                                                               Hand(
                                                                                                                   self.cards_played).diamonds]
                                                     and d.value not in [j.value for j in table.cards if j.suit == "d"]]
                                    if can_block(self.hand):
                                        if table.points <= 100 and len(diamonds_left) <= (3 - table.length):
                                            return AltruisticPlayer.block_j(self)
                                        else:
                                            return AltruisticPlayer.avoid_taking(self, table)
                                    else:
                                        return AltruisticPlayer.avoid_taking(self, table)
                            # else:
                            #     return AggressivePlayer.avoid_taking(self, table)
                        else:
                            return AltruisticPlayer.gamble(self, table)
            else:
                if Table.current_taker(table).id == self.teammate.id:
                    return AltruisticPlayer.give_l(self)
                else:
                    return Player.give_l(self)

    def play_third(self, table):
        """
        Decides on what card to play when playing 3rd
        :param table: Table()
        :return: Card()
        """
        moves = AltruisticPlayer.legal_moves(self, table.first_card)

        if len(moves) == 1:
            return moves[0]
        else:
            if AltruisticPlayer.has_suit(self, table.first_card):
                if self.has_10:
                    return AltruisticPlayer.avoid_taking(self, table)
                else:
                    if Table.current_taker(table).id == self.teammate.id and self.teammate.has_10:
                        return AltruisticPlayer.safest_take(self, table)
                    else:
                        if table.suit == "d":
                            if played(d_jack, self.cards_played):
                                return AltruisticPlayer.avoid_taking(self, table)
                            else:
                                if in_hand(d_jack, self.hand):
                                    if jack_highest(self.cards_played, self.hand):
                                        return d_jack
                                    else:
                                        return AltruisticPlayer.avoid_taking(self, table)
                                else:
                                    diamonds_left = [d for d in all_diamonds if d.value not in
                                                     [i.value for i in self.hand.diamonds] and d.value not in [k.value
                                                                                                               for k
                                                                                                               in
                                                                                                               Hand(
                                                                                                                   self.cards_played).diamonds]
                                                     and d.value not in [j.value for j in table.cards if j.suit == "d"]]
                                    if can_block(self.hand):
                                        if table.points <= 100 and len(diamonds_left) <= (3 - table.length):
                                            return AltruisticPlayer.block_j(self)
                                        else:
                                            return AltruisticPlayer.avoid_taking(self, table)
                                    else:
                                        return AltruisticPlayer.avoid_taking(self, table)
                            # else:
                            #     return AggressivePlayer.avoid_taking(self, table)
                        else:
                            return AltruisticPlayer.gamble(self, table)
            else:
                if Table.current_taker(table).id == self.teammate.id:
                    return AltruisticPlayer.give_l(self)
                else:
                    return Player.give_l(self)

    def play_last(self, table):
        """
        Decides on what card to play when playing last
        :param table: Table()
        :return: Card()
        """
        moves = AltruisticPlayer.legal_moves(self, table.first_card)

        if len(moves) == 1:
            return moves[0]
        else:
            if AltruisticPlayer.has_suit(self, table.first_card):
                if Table.current_taker(table).id == self.teammate.id:
                    if self.teammate.has_10:
                        return AltruisticPlayer.safest_take(self, table)
                    elif self.has_10:
                        return AltruisticPlayer.avoid_taking(self, table)
                    else:
                        point_threshold = 100
                        return AltruisticPlayer.avoid_taking(self,
                                                             table) if table.points > point_threshold else AltruisticPlayer.safest_take(
                            self, table)
            else:
                if Table.current_taker(table).id == self.teammate.id:
                    return AltruisticPlayer.give_l(self)
                else:
                    return Player.give_l(self)

    def play_card(self, table):
        """
        Plays a card and updates fields
        :param table: Table()
        :return: Card()
        """
        duped_list = self.cards_played + table.cards
        self.cards_played = list(set(duped_list))

        if table.length == 0:
            card = AltruisticPlayer.play_first(self)
        elif table.length == 1:
            card = AltruisticPlayer.play_second(self, table)
        elif table.length == 2:
            card = AltruisticPlayer.play_third(self, table)
        elif table.length == 3:
            card = AltruisticPlayer.play_last(self, table)

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

        AltruisticPlayer.deal_hand(self, hand_list)

        return card