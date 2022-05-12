class Suit:
    def __init__(self, cards):
        """
        Suit provides more specific information about a particular suit
        :param cards: list(Card) (all of a certain suit)
        """
        self.cards = cards
        if cards:
            self.suit = cards[0].suit
            self.highest = cards[-1]
            if len(cards) > 1:
                self.next_highest = cards[-2]
            else:
                self.next_highest = self.highest

    def lower_cards(self, card):
        """
        All cards in the suit that are lower than the given card
        :param card: Card()
        :return: list(Card)
        """
        return [i for i in self.cards if i.value < card.value]

    def higher_cards(self, card):
        """
        All cards in the suit that are higher than the given card
        :param card: Card()
        :return: list(Card)
        """
        return [i for i in self.cards if i.value > card.value]