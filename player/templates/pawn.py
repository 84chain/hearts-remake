# Pawns as simplified opponents for Player to keep track of

from setup.setup import *


class Pawn:
    def __init__(self, id):
        """
        Pawn object to help Player() keep track of other players
        :param id: int
        """
        self.id = id
        self.points = 0
        self.round = 0
        self.card = null_card
        self.has_clubs = True
        self.has_diamonds = True
        self.has_spades = True
        self.has_hearts = True
        self.cards_played = []
        self.cards_took = []
        self.cards_left = 13
        self.hand = Hand([])

    def is_missing(self, suit):
        """
        Sets hasX to False for suit
        :param suit: ['c', 'd', 's', 'h']
        :return: None
        """
        if suit == "c":
            self.has_clubs = False
        elif suit == "d":
            self.has_diamonds = False
        elif suit == "s":
            self.has_spades = False
        elif suit == "h":
            self.has_hearts = False

    def has_suit(self, suit):
        """
        Whether the Pawn has a specific suit or not
        :param suit: ['c', 'd', 's', 'h']
        :return: bool
        """
        if suit == "c":
            return self.has_clubs
        elif suit == "d":
            return self.has_diamonds
        elif suit == "s":
            return self.has_spades
        elif suit == "h":
            return self.has_hearts

    def deal_hand(self, list_card):
        """
        Deals hand to Pawn
        :param list_card: list(Card)
        :return: None
        """
        self.hand = Hand(list_card)
        self.cards_played = Hand(list_card).to_list()

    def can_shoot(self):
        """
        Whether Pawn can shoot or not
        :return: bool
        """
        hearts_played = [i.value for i in self.cards_played if i.suit == "h"]
        hearts_took = [i.value for i in self.cards_took if i.suit == "h"]
        return len(list(set(hearts_took + hearts_played))) == len(hearts_took)

    def play_card(self, card):
        """
        Updates Pawn as card is played from Pawn
        :param card: Card()
        :return: None
        """

        if not in_hand(card, Hand(self.cards_played)):
            self.cards_played.append(card)

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

        self.cards_left -= 1
        self.card = card

        Pawn.deal_hand(self, hand_list)

    def update_round(self, table):
        """
        Updates Player after a round
        :param table: Table()
        :return: None
        """
        self.round += 1
        if is_taking(table, self.card):
            self.cards_took += table.cards
        self.cards_played += table.cards

    def create_clone(self, suit):
        """
        Creates a clone missing suit
        :param suit: ['c', 'd', 's', 'h']
        :return: Pawn
        """
        p = Pawn(self.id)
        p.points = self.points
        if suit == "c":
            p.has_clubs = False
        else:
            p.has_clubs = self.has_clubs
        if suit == "d":
            p.has_diamonds = False
        else:
            p.has_diamonds = self.has_diamonds
        if suit == "s":
            p.has_spades = False
        else:
            p.has_spades = self.has_spades
        if suit == "h":
            p.has_hearts = False
        else:
            p.has_hearts = self.has_hearts
        p.cards_played = self.cards_played
        p.cards_left = self.cards_left
        p.hand = self.hand
        return p
