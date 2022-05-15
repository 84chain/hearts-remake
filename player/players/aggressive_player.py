from player.templates.player import *

# DEBUGGING
debug = False


class AggressivePlayer(Player):
    """
    Type of Player that is aggressive towards all other players
    """
    def play_second(self, table):
        """
        Decides on a card to play when playing second
        :param table: Table()
        :return: Card()
        """
        moves = AggressivePlayer.legal_moves(self, table.first_card)

        if len(moves) == 1:
            return moves[0]
        else:
            if AggressivePlayer.has_suit(self, table.first_card):
                if not self.pawns[1].has_suit(table.suit) or not self.pawns[2].has_suit(table.suit):
                    if table.suit == "d":
                        if played(d_jack, self.cards_played):
                            return AggressivePlayer.avoid_taking(self, table)
                        else:
                            if in_hand(d_jack, self.hand):
                                if jack_highest(self.cards_played, self.hand):
                                    return d_jack
                                else:
                                    return AggressivePlayer.avoid_taking(self, table)
                            else:
                                diamonds_left = [d for d in all_diamonds if d.value not in
                                                [i.value for i in self.hand.diamonds] and d.value not in [k.value for k
                                                                                                          in
                                                                                                          Hand(
                                                                                                              self.cards_played).diamonds]
                                                and d.value not in [j.value for j in table.cards if j.suit == "d"]]
                                if can_block(self.hand):
                                    if table.points <= 100 and len(diamonds_left) <= (3 - table.length):
                                        return AggressivePlayer.block_j(self)
                                    else:
                                        return AggressivePlayer.avoid_taking(self, table)
                                else:
                                    return AggressivePlayer.avoid_taking(self, table)
                    else:
                        return AggressivePlayer.avoid_taking(self, table)
                else:
                    return AggressivePlayer.gamble(self, table)
            else:
                return AggressivePlayer.give_l(self)

    def play_third(self, table):
        """
        Decides on what card to play when playing third
        :param table: Table()
        :return: Card()
        """
        moves = AggressivePlayer.legal_moves(self, table.first_card)

        if len(moves) == 1:
            return moves[0]
        else:
            if AggressivePlayer.has_suit(self, table.first_card):
                if not self.pawns[1].has_suit(table.suit):
                    if table.suit == "d":
                        if played(d_jack, self.cards_played):
                            return AggressivePlayer.avoid_taking(self, table)
                        else:
                            if in_hand(d_jack, self.hand):
                                if jack_highest(self.cards_played, self.hand):
                                    return d_jack
                                else:
                                    return AggressivePlayer.avoid_taking(self, table)
                            else:
                                diamonds_left = [d for d in all_diamonds if d.value not in
                                                [i.value for i in self.hand.diamonds] and d.value not in [k.value for k
                                                                                                          in
                                                                                                          Hand(
                                                                                                              self.cards_played).diamonds]
                                                and d.value not in [j.value for j in table.cards if j.suit == "d"]]
                                if can_block(self.hand):
                                    if table.points <= 100 and len(diamonds_left) <= (3 - table.length):
                                        return AggressivePlayer.block_j(self)
                                    else:
                                        return AggressivePlayer.avoid_taking(self, table)
                                else:
                                    return AggressivePlayer.avoid_taking(self, table)
                    else:
                        return AggressivePlayer.avoid_taking(self, table)
                else:
                    return AggressivePlayer.gamble(self, table)
            else:
                return AggressivePlayer.give_l(self)

    def play_last(self, table):
        """
        Decides on what card to play when playing last
        :param table: Table()
        :return: Card()
        """
        moves = AggressivePlayer.legal_moves(self, table.first_card)

        if len(moves) == 1:
            return moves[0]
        else:
            if AggressivePlayer.has_suit(self, table.first_card):
                return AggressivePlayer.avoid_taking(self, table) if table.points > 100 else AggressivePlayer.safest_take(self, table)
            else:
                return AggressivePlayer.give_l(self)

    def play_card(self, table):
        """
        Plays a card and updates fields
        :param table: Table()
        :return: Card()
        """
        duped_list = self.cards_played + table.cards
        self.cards_played = list(set(duped_list))

        if table.length == 0:
            card = AggressivePlayer.play_first(self)
        elif table.length == 1:
            card = AggressivePlayer.play_second(self, table)
        elif table.length == 2:
            card = AggressivePlayer.play_third(self, table)
        elif table.length == 3:
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

        AggressivePlayer.deal_hand(self, hand_list)

        return card