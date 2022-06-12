from player.players.teams.shoot_player import *

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


