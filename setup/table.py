from setup.setup import *
from setup.card import *

class Table:
    def __init__(self):
        """
        The current table, the state of the current round
        """
        self.cards = []
        self.players = []
        self.player_ids = []
        self.table = []
        self.length = 0
        self.suit = ""
        self.points = sum([i.points for i in self.cards])


    def card_played(self, card, player):
        """
        Plays a card to the table
        :param card: Card() played
        :param player: Player() who played the card
        :return: None
        """
        self.cards.append(card)
        self.players.append(player)
        self.table.append({"player": player, "card": card})
        self.player_ids.append(player.id)
        if len(self.cards) == 1:
            self.suit = card.suit
        self.length = len(self.cards)
        if self.length > 0:
            self.first_card = self.cards[0]
        else:
            self.first_card = null_card