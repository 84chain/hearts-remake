from player.players.teams.aggressive_player import *
from player.players.teams.altruistic_player import *
from player.players.teams.shoot_player import *

# TODO: analyze_teams, play is flawed

class TeamPlayer(Player):
    """
    Type of player that plays in a teams game mode
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

    def analyze_teams(self, table):
        """
        Analyzes game so far and tries to deduce teammate
        :param table: Table()
        :return: None
        """
        if self.team_card.is_eq(black_king) or all_same_suit(table, self.card):
            pass
        elif self.team_card.is_eq(black_ace):
            if is_taking(table, self.card):
                if table.points > 0 and table.suit != "h":
                    likely_opponents = [p["player"] for p in table.table if p["card"].points > 0]
                    for i in likely_opponents:
                        if table.cards[i.id].is_eq(q_spades):
                            self.team_chances[i.id] -= loss_on_L * 2
                        else:
                            self.team_chances[i.id] -= loss_on_L
                elif table.points < 0 and return_highest(table).value != 12:
                    likely_teammate = [p["player"] for p in table.table if p["card"].is_eq(d_jack)][0]
                    self.team_chances[likely_teammate.id] += gain_on_L * 2
                elif table.points == 0 or table.suit == "h":
                    likely_teammates = [p["player"] for p in table.table if p["card"].suit != table.suit]
                    for i in likely_teammates:
                        self.team_chances[i.id] += gain_on_L
                else:
                    likely_teammates = [p["player"] for p in table.table if p["card"].suit != table.suit]
                    for i in likely_teammates:
                        self.team_chances[i.id] += gain_on_L
            else:
                taker = Table.current_taker(table)
                if table.points > 0 and table.suit != "h":
                    likely_teammates = [p["player"] for p in table.table if p["card"].points > 0]
                    for i in likely_teammates:
                        if table.cards[i.id].is_eq(q_spades):
                            self.team_chances[i.id] += gain_on_L * 2
                        else:
                            self.team_chances[i.id] += gain_on_L
                    self.team_chances[taker.id] -= loss_on_L
                elif table.points < 0 and return_highest(table).value != 12:
                    likely_opponent = [p["player"] for p in table.table if p["card"].is_eq(d_jack)][0]
                    teammate_id = [i for i in range(4) if i not in [self.id, taker.id, likely_opponent.id]][0]
                    self.team_chances[teammate_id] += gain_on_L * 2
                    self.team_chances[likely_opponent.id] -= loss_on_L
                    self.team_chances[taker.id] -= loss_on_L
                elif table.points == 0 or table.suit == "h":
                    likely_opponent = [p["player"] for p in table.table if p["card"].suit != table.suit][0]
                    teammate_id = [i for i in range(4) if i not in [self.id, taker.id, likely_opponent.id]][0]
                    self.team_chances[teammate_id] += gain_on_L
                    self.team_chances[likely_opponent.id] -= loss_on_L
                    self.team_chances[taker.id] -= loss_on_L
                else:
                    likely_opponent = [p["player"] for p in table.table if p["card"].suit != table.suit][0]
                    teammate_id = [i for i in range(4) if i not in [self.id, taker.id, likely_opponent.id]][0]
                    self.team_chances[teammate_id] += gain_on_L
                    self.team_chances[likely_opponent.id] -= loss_on_L
                    self.team_chances[taker.id] -= loss_on_L
        else:
            if is_taking(table, self.card):
                if table.points > 0 and table.suit != "h":
                    likely_opponents = [p["player"] for p in table.table if p["card"].points > 0]
                    for i in likely_opponents:
                        if table.cards[i.id].is_eq(q_spades):
                            self.team_chances[i.id] -= loss_on_L * 2
                        else:
                            self.team_chances[i.id] -= loss_on_L
                elif table.points < 0 and return_highest(table).value != 12:
                    likely_teammate = [p["player"] for p in table.table if p["card"].is_eq(d_jack)][0]
                    self.team_chances[likely_teammate.id] += gain_on_L * 2
                elif table.points == 0 or table.suit == "h":
                    likely_teammates = [p["player"] for p in table.table if p["card"].suit != table.suit]
                    for i in likely_teammates:
                        self.team_chances[i.id] += gain_on_L
            else:
                taker = Table.current_taker(table)
                if table.points > 0 and table.suit != "h":
                    likely_teammates = [p["player"] for p in table.table if p["card"].points > 0]
                    for i in likely_teammates:
                        if table.cards[i.id].is_eq(q_spades):
                            self.team_chances[i.id] += gain_on_L * 2
                        else:
                            self.team_chances[i.id] += gain_on_L
                    self.team_chances[taker.id] -= loss_on_L
                elif table.points < 0 and return_highest(table).value != 12:
                    likely_opponent = [p["player"] for p in table.table if p["card"].is_eq(d_jack)][0]
                    teammate_id = [i for i in range(4) if i not in [self.id, taker.id, likely_opponent.id]][0]
                    self.team_chances[teammate_id] += gain_on_L * 2
                    self.team_chances[likely_opponent.id] -= loss_on_L
                    self.team_chances[taker.id] -= loss_on_L
                elif table.points == 0 or table.suit == "h":
                    likely_opponent = [p["player"] for p in table.table if p["card"].suit != table.suit][0]
                    teammate_id = [i for i in range(4) if i not in [self.id, taker.id, likely_opponent.id]][0]
                    self.team_chances[teammate_id] += gain_on_L
                    self.team_chances[likely_opponent.id] -= loss_on_L
                    self.team_chances[taker.id] -= loss_on_L
                else:
                    likely_opponent = [p["player"] for p in table.table if p["card"].suit != table.suit][0]
                    teammate_id = [i for i in range(4) if i not in [self.id, taker.id, likely_opponent.id]][0]
                    self.team_chances[teammate_id] += gain_on_L
                    self.team_chances[likely_opponent.id] -= loss_on_L
                    self.team_chances[taker.id] -= loss_on_L

        likely_teammate_chance = multiple_max(self.team_chances)
        if likely_teammate_chance is not None and not self.team_card.is_eq(black_king):
            teammate_id = self.team_chances.index(likely_teammate_chance)
            teammate = [p for p in table.players if p.id == teammate_id][0]
            TeamPlayer.assign_teammate(self, teammate)
        # self.team_chances = [team_chances_cap(i) for i in self.team_chances]


    def play_first(self):
        """
        Override for play_first that considers teams, shooting, and shoot block
        :return: Card()
        """
        if self.is_shooting:
            return ShootPlayer.shoot_first(self)
        elif self.teammate is not None:
            if AltruisticPlayer.is_missing_Suit(self, Table()) <= self.risk_tolerance:
                return AggressivePlayer.play_first(self)
            else:
                return AltruisticPlayer.play_first(self)
        else:
            return AggressivePlayer.play_first(self)

    def play_second(self, table):
        """
        Override for play_second that considers teams, shooting, and shoot block
        :param table: Table()
        :return: Card()
        """
        if self.is_shooting:
            return ShootPlayer.shoot_2nd_or_3rd(self, table)
        elif not self.shoot_blocked:
            return ShootPlayer.block_2nd_or_3rd(self, table)
        elif self.teammate is not None:
            if self.teammate.id in table.player_ids:
                teammate_card = [i["card"] for i in table.table if i["player"].id == self.teammate.id][0]
                if is_taking(table, teammate_card):
                    return AltruisticPlayer.play_second(self, table)
                else:
                    return AggressivePlayer.play_second(self, table)
            else:
                if AltruisticPlayer.is_missing_Suit(self, table) <= self.risk_tolerance:
                    return AggressivePlayer.play_second(self, table)
                else:
                    return AltruisticPlayer.play_second(self, table)
        else:
            return AggressivePlayer.play_second(self, table)

    def play_third(self, table):
        """
        Override for play_third that considers teams, shooting, and shoot block
        :param table: Table()
        :return: Card()
        """
        if self.is_shooting:
            return ShootPlayer.shoot_2nd_or_3rd(self, table)
        elif not self.shoot_blocked:
            return ShootPlayer.block_2nd_or_3rd(self, table)
        elif self.teammate is not None:
            if self.teammate.id in table.player_ids:
                teammate_card = [i["card"] for i in table.table if i["player"].id == self.teammate.id][0]
                if is_taking(table, teammate_card):
                    return AltruisticPlayer.play_third(self, table)
                else:
                    return AggressivePlayer.play_third(self, table)
            else:
                if AltruisticPlayer.is_missing_Suit(self, table) <= self.risk_tolerance:
                    return AggressivePlayer.play_third(self, table)
                else:
                    return AltruisticPlayer.play_third(self, table)
        else:
            return AggressivePlayer.play_third(self, table)

    def play_last(self, table):
        """
        Override for play_last that considers teams, shooting, and shoot block
        :param table: Table()
        :return: Card()
        """
        if self.is_shooting:
            return ShootPlayer.shoot_last(self, table)
        elif not self.shoot_blocked:
            return ShootPlayer.block_last(self, table)
        elif self.teammate is not None:
            teammate_card = [i["card"] for i in table.table if i["player"].id == self.teammate.id][0]
            if is_taking(table, teammate_card):
                return AltruisticPlayer.play_last(self, table)
            else:
                return AggressivePlayer.play_last(self, table)
        else:
            return AggressivePlayer.play_last(self, table)

    def play_card(self, table):
        """
        Plays a card and updates fields
        :param table: Table()
        :return: Card()
        """
        duped_list = self.cards_played + table.cards
        self.cards_played = list(set(duped_list))

        if table.length == 0:
            card = TeamPlayer.play_first(self)
        elif table.length == 1:
            card = TeamPlayer.play_second(self, table)
        elif table.length == 2:
            card = TeamPlayer.play_third(self, table)
        elif table.length == 3:
            card = TeamPlayer.play_last(self, table)

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

        TeamPlayer.deal_hand(self, hand_list)

        return card

    def update_round(self, table):
        """
        Override for update_round that includes shooting, shoot block, teams
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
        if Player.can_shoot(self):
            if num_guaranteed_takes(self.hand, self.cards_played) >= (minimum_takes - self.round):
                self.is_shooting = True
                self.guaranteed_takes = guaranteed_takes(self.hand, self.cards_played)
                self.possible_takes = possible_takes(self.hand, self.cards_played)
            else:
                self.is_shooting = False
        else:
            self.is_shooting = False
        shoot_pawns = [p.can_shoot() for p in self.pawns]
        if True in shoot_pawns:
            self.shoot_blocked = False
        else:
            self.shoot_blocked = True
        TeamPlayer.analyze_teams(self, table)