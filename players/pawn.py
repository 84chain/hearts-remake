class Pawn:
    def __init__(self, id):
        self.card = -1
        self.id = id
        self.points = 0
        self.cards_left = 13

        self.has_clubs = True
        self.has_diamonds = True
        self.has_spades = True
        self.has_hearts = True

        self.hand = []
        self.cards = []
        self.cards_took = []

    def is_missing(self, suit):
        return [self.has_clubs, self.has_diamonds, self.has_spades, self.has_hearts][suit]

    def can_shoot(self, ctx):
        return len([i for i in ctx.cards_played if i >> 13 == 3]) == len([i for i in self.cards_took if i >> 13 == 3])

    def play(self, card):
        self.card = card
        self.cards.append(card)
        self.hand = [i for i in self.hand if i != card]
        self.cards_left -= 1

    def update(self, ctx):
        state = ctx.current_state
        if self.card == state.highest():
            self.cards_took += state.cards

    def clone(self, suit):
        p = Pawn(self.id)
        p.card = self.card
        p.cards = self.cards
        p.hand = self.hand
        p.cards_took = self.cards_took
        p.has_clubs = self.has_clubs
        p.has_diamonds = self.has_diamonds
        p.has_spades = self.has_spades
        p.has_hearts = self.has_hearts
        p.cards_left = self.cards_left

        if suit == 0:
            p.has_clubs = False
        elif suit == 1:
            p.has_diamonds = False
        elif suit == 2:
            p.has_spades = False
        elif suit == 3:
            p.has_hearts = False

        return p