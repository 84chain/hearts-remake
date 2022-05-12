str_values = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k", "a"]

class Card:
    def __init__(self, card_info):
        """
        A card with a suit, value, point count
        :param card_info: string representing a card, suit ('c', 'd', 's', 'h') first then value (from strvalues)
        :param cardinfo: could also be int (0-51)
        """

        if type(card_info) == Card:
            self.suit = card_info.suit
            self.value = card_info.value
            self.card_str = card_info.card_str
            self.points = card_info.points
        else:
            try:
                if card_info < 0:
                    self.suit = "n"
                    self.value = 0
                    self.card_str = "0"
                    self.str = self.card_str
                else:
                    self.suit = ['c', 'd', 's', 'h'][card_info // 13]
                    self.value = card_info % 13 + 2
                    self.card_str = str_values[card_info % 13]
                    self.str = str_values[card_info % 13].upper()
            except:
                self.suit = card_info[0]
                self.card_str = card_info[1:]

                if self.card_str == "j":
                    self.value = 11
                    self.str = "J"
                elif self.card_str == "q":
                    self.value = 12
                    self.str = "Q"
                elif self.card_str == "k":
                    self.value = 13
                    self.str = "K"
                elif self.card_str == "a":
                    self.value = 14
                    self.str = "A"
                else:
                    self.value = int(self.card_str)
                    self.str = self.card_str

        if self.suit == "s" and self.value == 12:
            self.points = 100
        elif self.suit == "d" and self.value == 11:
            self.points = -100
        elif self.suit == "c" and self.value == 10:
            self.points = 10
        elif self.suit == "h":
            if 4 < self.value < 11:
                self.points = 10
            elif self.value > 10:
                self.points = 10 * (self.value - 9)
            else:
                self.points = 0
        else:
            self.points = 0

    def to_string(self):
        """
        Card in {Value} of {Suit} format
        :return: str
        """
        suit_dict = {"c": "Clubs",
                    "d": "Diamonds",
                    "s": "Spades",
                    "h": "Hearts"}
        return f"{self.str} of {suit_dict[self.suit]}"

    def to_short_string(self):
        """
        Converts back to input (cardstr)
        :return: str
        """
        return f"{self.suit}{self.card_str}"

    def is_eq(self, card):
        """
        Whether self is equal to card
        object == checks for memory location
        :param card: Card()
        :return: bool
        """
        return self.suit == card.suit and self.value == card.value

    def to_int(self):
        """
        Converts card to int (0-51)
        :return: int
        """
        if self.suit == "n":
            return -1
        else:
            return (['c', 'd', 's', 'h'].index(self.suit)) * 13 + self.value - 2


# IMPORTANT CARDS
club_10 = Card("c10")
d_jack = Card("dj")
q_spades = Card("sq")
heart_10 = Card("h10")
club_3 = Card("c3")
null_card = Card("n0")

all_clubs = [Card(f"c{i}") for i in str_values]
all_diamonds = [Card(f"d{i}") for i in str_values]
all_spades = [Card(f"s{i}") for i in str_values]
all_hearts = [Card(f"h{i}") for i in str_values]
all_cards = all_clubs + all_diamonds + all_spades + all_hearts
all_int_cards = [c.to_int() for c in all_cards]