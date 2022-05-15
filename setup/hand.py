from setup.card import Card

class Hand:
    def __init__(self, list_card):
        """
        Hand records a hand, separated by suit
        :param list_card: list(Card)
        """
        self.clubs = []
        self.diamonds = []
        self.spades = []
        self.hearts = []

        if type(list_card) == int:
            list_of_cards = []
            mask = 1
            for i in range(52):
                if list_card & mask != 0:
                    list_of_cards.append(i)
                mask <<= 1
            h = Hand(list_of_cards)
            self.clubs = h.clubs
            self.diamonds = h.diamonds
            self.spades = h.spades
            self.hearts = h.hearts

        elif list_card:
            for i in list_card:
                try:
                    if i // 13 == 0:
                        self.clubs.append(Card(i))
                    elif i // 13 == 1:
                        self.diamonds.append(Card(i))
                    elif i // 13 == 2:
                        self.spades.append(Card(i))
                    elif i // 13 == 3:
                        self.hearts.append(Card(i))
                except:
                    if i.suit == "c":
                        self.clubs.append(i)
                    elif i.suit == "d":
                        self.diamonds.append(i)
                    elif i.suit == "s":
                        self.spades.append(i)
                    elif i.suit == "h":
                        self.hearts.append(i)

        if self.clubs != [] or len(self.clubs) != 1:
            self.clubs.sort(key=lambda card: int(card.value))
        if self.diamonds != [] or len(self.diamonds) != 1:
            self.diamonds.sort(key=lambda card: int(card.value))
        if self.spades != [] or len(self.spades) != 1:
            self.spades.sort(key=lambda card: int(card.value))
        if self.hearts != [] or len(self.hearts) != 1:
            self.hearts.sort(key=lambda card: int(card.value))
        self.list = self.clubs + self.diamonds + self.spades + self.hearts

    def to_list(self):
        """
        Converts back to input, unintended effect of sorting hand in clubs/diamonds/spades/hearts order
        :return: list(Card)
        """
        return self.list

    def to_string(self):
        """
        Converts to a string separated by ', '. Unintended effect of sorting hand
        :return: str
        """
        out_list = []
        for card in self.list:
            out_list.append(card.to_short_string())
        return ", ".join(out_list)

    def to_int_list(self):
        """
        Converts to list of int
        :return: list(int)
        """
        return [c.to_int() for c in self.list]

    def to_int(self):
        """
        Converts into an int
        :return: int
        """
        temp_hand = ""
        int_hand = Hand.to_int_list(self)
        for i in range(52):
            if i in int_hand:
                temp_hand += "1"
            else:
                temp_hand += "0"
        return int(temp_hand, 2)

    def decode(self, int_hand):
        """
        Decodes a hand converted into int back into a hand
        :param int_hand: int
        :return: Hand()
        """
        bit_hand = format(int_hand, '52b')
        hand_ints = []
        for i in range(52):
            if bit_hand[i] == "1":
                hand_ints.append(i)
        return Hand(hand_ints)