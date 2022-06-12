from player.templates.player import *


class ShootPlayer(Player):
    """
    Type of player that shoots the moon and blocks enemy shoots
    """

    def shoot_first(self):
        """
        Returns card to play when shooting first
        :return: Card()
        """
        if in_hand(club_3, self.hand):
            return club_3
        else:
            suits = []
            for suit in ["c", "d", "s"]:
                table = Table()
                setattr(table, "suit", suit)
                if ShootPlayer.is_missing_Suit(self, table) == 0:
                    suits.append(suit)
            if suits:
                possible_plays = [i for i in self.possible_takes if i.suit in suits]
                if possible_plays:
                    return sorted(possible_plays, key=lambda x: x.value)[0]
                else:
                    if self.guaranteed_takes:
                        return self.guaranteed_takes[0]
                    elif self.possible_takes:
                        return self.possible_takes[-1]
                    else:
                        return sorted(self.hand.to_list(), key=lambda x: x.value)[-1]
            else:
                if self.guaranteed_takes:
                    return self.guaranteed_takes[0]
                elif self.possible_takes:
                    return self.possible_takes[-1]
                else:
                    return sorted(self.hand.to_list(), key=lambda x: x.value)[-1]

    def shoot_2nd_or_3rd(self, table):
        """
        Returns card to play when shooting 2nd or 3rd
        :return: Card()
        """
        moves = ShootPlayer.legal_moves(self, table.first_card)
        if len(moves) == 1:
            return moves[0]
        else:
            if ShootPlayer.has_suit(self, table.first_card):
                possible_suits = [c.suit for c in self.possible_takes]
                possible_moves = [c for c in self.possible_takes if c.suit == table.suit]
                if table.suit in possible_suits:
                    if ShootPlayer.is_missing_Suit(self, table) == 0:
                        return possible_moves[0]
                    else:
                        return ShootPlayer.safest_take(self, table)
                else:
                    return ShootPlayer.safest_take(self, table)
            else:
                non_heart_takes = [i for i in self.possible_takes if i.suit != "h"]
                if non_heart_takes:
                    return non_heart_takes[0]
                else:
                    self.is_shooting = False
                    return ShootPlayer.give_l(self)

    def shoot_last(self, table):
        """
        Returns card to play when shooting last
        :param table: Table()
        :return: Card()
        """
        moves = ShootPlayer.legal_moves(self, table.first_card)
        if len(moves) == 1:
            return moves[0]
        else:
            if ShootPlayer.has_suit(self, table.first_card):
                possible_suits = [c.suit for c in self.possible_takes]
                if table.suit in possible_suits:
                    possible_moves = [c for c in self.possible_takes if c.suit == table.suit]
                    if table.points == 0:
                        return possible_moves[0]
                    elif table.points < 0:
                        possible_takes = [i for i in possible_moves if i.value > return_highest(table)]
                        if possible_takes:
                            return possible_takes[0]
                        else:
                            return ShootPlayer.safest_take(self, table)
                    else:
                        return ShootPlayer.safest_take(self, table)
                else:
                    return ShootPlayer.safest_take(self, table)
            else:
                non_heart_takes = [i for i in self.possible_takes if i.suit != "h"]
                if non_heart_takes:
                    return non_heart_takes[0]
                else:
                    self.is_shooting = False
                    return ShootPlayer.give_l(self)

    def block_first(self):
        """
        Returns card to play when blocking shoot first
        :return: Card()
        """
        pass

    def block_2nd_or_3rd(self, table):
        """
        Returns card to play when blocking shoot 2nd or 3rd
        :param table: Table()
        :return: Card()
        """
        pass

    def block_last(self, table):
        """
        Returns card to play when blocking shoot last
        :param table: Table()
        :return: Card()
        """
        pass

    def shoot(self, table):
        """
        Returns card to play when shooting is triggered
        :param table: Table()
        :return: Card()
        """
        if table.length == 0:
            return ShootPlayer.shoot_first(self)
        elif table.length == 3:
            return ShootPlayer.shoot_last(self, table)
        else:
            return ShootPlayer.shoot_2nd_or_3rd(self, table)

    def block_shoot(self, table):
        """
        Returns card to play when blocking shoot
        :param table: Table()
        :return: Card()
        """
        if table.length == 0:
            return ShootPlayer.block_first(self)
        elif table.length == 3:
            return ShootPlayer.block_last(self, table)
        else:
            return ShootPlayer.block_2nd_or_3rd(self, table)

    def play_card(self, table):
        """
        Plays a card and updates fields
        Only used to test ShootPlayer
        :param table: Table()
        :return: Card()
        """
        if self.is_shooting:
            card = ShootPlayer.shoot(self, table)
        else:
            card = ShootPlayer.block_shoot(self, table)

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

        ShootPlayer.deal_hand(self, hand_list)

        return card
