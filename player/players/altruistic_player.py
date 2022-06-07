from player.templates.player import *


class AltruisticPlayer(Player):
    """
    Type of Player that is altruistic towards all players
    """

    def choose_card(self):
        pass

    def play_second(self, table):
        pass

    def play_third(self, table):
        pass

    def play_last(self, table):
        pass

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
