from setup.setup import *
from setup.controls import *

class Aggression:
    @staticmethod
    def play_first(ctx, player):
        if club_3 in player.hand:
            return club_3
        return player.choose_card(ctx)

    @staticmethod
    def play_2nd_or_3rd(ctx, player):
        state = ctx.current_state
        moves = player.legal_moves(state.suit)

        if len(moves) == 1:
            return moves[0]

        suit = [i for i in player.hand if i >> 13 == state.suit]

        if suit:
            if state.suit == 1:
                if d_jack in ctx.cards_played:
                    return player.safest_take(ctx)
                if d_jack in suit:
                    if jack_highest(player.hand, ctx.cards_played):
                        return d_jack
                    else:
                        return player.avoid_taking(ctx)
                else:
                    diamonds_left = [i for i in all_diamonds if i not in player.hand and i not in ctx.cards_played]
                    if can_block(player.hand) and (state.points() <= 100) and (len(diamonds_left) <= (3 - state.length())):
                        return player.block_j()
                    else:
                        return player.avoid_taking(ctx)
            else:
                if player.is_missing_suit(ctx) >= player.risk_tolerance:
                    return player.safest_take(ctx)
                else:
                    return player.avoid_taking(ctx)
        else:
            return player.give_L(ctx)

    @staticmethod
    def play_last(ctx, player):
        state = ctx.current_state
        moves = player.legal_moves(state.suit)

        if len(moves) == 1:
            return moves[0]

        suit = [i for i in player.hand if i >> 13 == state.suit]

        if suit:
            if state.points() >= taking_point_threshold:
                return player.avoid_taking(ctx)
            else:
                if state.suit == 1 and state.highest() < d_jack and d_jack in player.hand:
                    return player.safest_take(ctx)
                else:
                    return player.avoid_taking(ctx)
        else:
            return player.give_L(ctx)