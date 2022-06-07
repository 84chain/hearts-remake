from player.templates.player import *

class GamePlayer(Player):
    def pass_cards(self, cards):
        remaining_hand = [c for c in self.list_hand if c.to_int() not in [i.to_int() for i in cards]]
        self.hand = Hand(remaining_hand)
        return cards

    def play_card(self, card):
        """
        Plays a card and updates fields
        :param table: Table()
        :return: Card()
        """
        if in_hand(card, self.hand):
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

            Player.deal_hand(self, hand_list)

            return card
        else:
            raise Exception