from player.templates.player import *


class AggressivePlayer(Player):
    """
    Type of Player that is aggressive towards all other players
    """

    def deal_hand(self, list_card):
        """
        Override for deal_hand that includes shooting
        :param list_card: list(Card)
        :return: None
        """
        self.hand = Hand(list_card)
        self.list_hand = self.hand.to_list()
        if num_guaranteed_takes(self.hand, []) >= minimum_takes:
            self.is_shooting = True

    def pass_cards(self):
        """
        Override for pass_cards that includes shooting
        :return: list(Card)
        """
        if self.is_shooting:
            cards = choose_shoot_pass(self.hand)
        else:
            cards = choose_pass(self.hand)
        remaining_hand = [c for c in self.list_hand if c.to_int() not in [i.to_int() for i in cards]]
        self.hand = Hand(remaining_hand)
        return cards

    def receive_pass(self, cards):
        """
        Override for receive_pass that includes shooting
        :param cards: list(Card)
        :return: None
        """
        new_hand = self.hand.to_list() + cards
        self.hand = Hand(new_hand)
        if num_guaranteed_takes(self.hand, []) >= minimum_takes:
            self.is_shooting = True
            self.guaranteed_takes = guaranteed_takes(self.hand, [])
            self.possible_takes = possible_takes(self.hand, [])

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
                #if not self.pawns[1].has_suit(table.suit) or not self.pawns[2].has_suit(table.suit):
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
                    # else:
                    #     return AggressivePlayer.avoid_taking(self, table)
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
                #if not self.pawns[1].has_suit(table.suit):
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
                    # else:
                    #     return AggressivePlayer.avoid_taking(self, table)
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
                point_threshold = 100
                return AggressivePlayer.avoid_taking(self, table) if table.points > point_threshold else AggressivePlayer.safest_take(self, table)
            else:
                return AggressivePlayer.give_l(self)

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
                if AggressivePlayer.is_missing_Suit(self, table) == 0:
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
        moves = AggressivePlayer.legal_moves(self, table.first_card)
        if len(moves) == 1:
            return moves[0]
        else:
            if AggressivePlayer.has_suit(self, table.first_card):
                possible_suits = [c.suit for c in self.possible_takes]
                possible_moves = [c for c in self.possible_takes if c.suit == table.suit]
                if table.suit in possible_suits:
                    if AggressivePlayer.is_missing_Suit(self, table) == 0:
                        return possible_moves[0]
                    else:
                        return AggressivePlayer.safest_take(self, table)
                else:
                    return AggressivePlayer.safest_take(self, table)
            else:
                non_heart_takes = [i for i in self.possible_takes if i.suit != "h"]
                if non_heart_takes:
                    return non_heart_takes[0]
                else:
                    self.is_shooting = False
                    return AggressivePlayer.give_l(self)

    def shoot_last(self, table):
        """
        Returns card to play when shooting last
        :param table: Table()
        :return: Card()
        """
        moves = AggressivePlayer.legal_moves(self, table.first_card)
        if len(moves) == 1:
            return moves[0]
        else:
            if AggressivePlayer.has_suit(self, table.first_card):
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
                            return AggressivePlayer.safest_take(self, table)
                    else:
                        return AggressivePlayer.safest_take(self, table)
                else:
                    return AggressivePlayer.safest_take(self, table)
            else:
                non_heart_takes = [i for i in self.possible_takes if i.suit != "h"]
                if non_heart_takes:
                    return non_heart_takes[0]
                else:
                    self.is_shooting = False
                    return AggressivePlayer.give_l(self)

    def play_card(self, table):
        """
        Plays a card and updates fields
        :param table: Table()
        :return: Card()
        """
        duped_list = self.cards_played + table.cards
        self.cards_played = list(set(duped_list))

        if self.is_shooting:
            if table.length == 0:
                card = AggressivePlayer.shoot_first(self)
            elif table.length == 1 or table.length == 2:
                card = AggressivePlayer.shoot_2nd_or_3rd(self, table)
            elif table.length == 3:
                card = AggressivePlayer.shoot_last(self, table)
        else:
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

    def update_round(self, table):
        """
        Override for update_round that includes shooting
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
            no_suit_players = no_suits(table, self.card)
            if no_suit_players:
                for pawn in no_suit_players:
                    self.pawns[pawn].is_missing(suit)
        for p in self.pawns:
            Pawn.update_round(p, table)
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