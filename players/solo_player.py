from setup.setup import *
from setup.controls import *
from players.player import Player
from behaviours.aggression import Aggression
from behaviours.altruism import Altruism
from behaviours.shooting import Shooting

class SoloPlayer(Player):
    def __init__(self, id):
        super().__init__(id)
        self.aggression = Aggression()
        self.altruism = Altruism()
        self.shooting = Shooting()

    def set_hand(self, hand):
        self.hand = hand
        self.guaranteed_takes = guaranteed_takes(self.hand, [])
        self.possible_takes = guaranteed_takes(self.hand, [])
        if num_guaranteed_takes(self.hand, []) >= minimum_takes:
            self.is_shooting = True

    def get_pass(self):
        if self.is_shooting:
            cards = choose_shoot_pass(self.hand)
        else:
            cards = choose_pass(self.hand)
        self.hand = [i for i in self.hand if i not in cards]

    def receive_pass(self, cards):
        self.hand += cards
        if num_guaranteed_takes(self.hand, []) >= minimum_takes:
            self.is_shooting = True
            self.guaranteed_takes = guaranteed_takes(self.hand, [])
            self.possible_takes = guaranteed_takes(self.hand, [])

    def play_first(self, ctx):
        if self.is_shooting:
            return self.shooting.shoot_first(ctx, self)
        else:
            return self.aggression.play_first(ctx, self)

    def play_2nd_or_3rd(self, ctx):
        if self.is_shooting:
            return self.shooting.shoot_2nd_or_3rd(ctx, self)
        elif not self.shoot_blocked:
            return self.shooting.block_2nd_or_3rd(ctx, self)
        else:
            return self.aggression.play_2nd_or_3rd(ctx, self)

    def play_last(self, ctx):
        if self.is_shooting:
            return self.shooting.shoot_last(ctx, self)
        elif not self.shoot_blocked:
            return self.shooting.block_last(ctx, self)
        else:
            return self.aggression.play_last(ctx, self)

    def play(self, ctx):
        state = ctx.current_state

        if state.length() == 0:
            card = SoloPlayer.play_first(self, ctx)
        elif state.length() == 3:
            card = SoloPlayer.play_last(self, ctx)
        else:
            card = SoloPlayer.play_2nd_or_3rd(self, ctx)

        self.card = card
        self.cards.append(card)
        self.hand = [i for i in self.hand if i != card]

        return card

    def update(self, ctx):
        state = ctx.current_state

        if self.card == state.highest():
            self.cards_took += state.cards

        if all_same_suit(state, self.card):
            first_index = [i.id for i in self.pawns].index(state.player_ids[0])
            for i in range(4):
                index = (first_index + i) % 4
                self.pawns[index].play(state.cards[index])
        else:
            no_suit_players = no_suits(state)
            if no_suit_players:
                for p in no_suit_players:
                    index = self.pawns.index(p)
                    self.pawns[index].is_missing(state.suit)

        if Player.can_shoot(self, ctx) and num_guaranteed_takes(self.hand, ctx.cards_played) >= (minimum_takes - ctx.round):
            self.is_shooting = True
            self.guaranteed_takes = guaranteed_takes(self.hand, ctx.cards_played)
            self.possible_takes = possible_takes(self.hand, ctx.cards_played)
        else:
            self.is_shooting = False

        for p in self.pawns:
            p.update(ctx)
            if not p.can_shoot(ctx):
                self.shoot_blocked = True