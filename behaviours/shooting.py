from setup.setup import *
from setup.controls import *

class Shooting:
    @staticmethod
    def shoot_first(ctx, player):
        if club_3 in player.hand:
            return club_3

        suits = []
        c = ctx
        for i in [0, 1, 2]:
            if player.is_missing_suit(c):
                suits.append(i)

        if suits:
            possible_plays = [i for i in player.possible_takes if i >> 13 in suits]
            if possible_plays:
                return min(possible_plays)
            else:
                if player.guaranteed_takes:
                    return min(player.guaranteed_takes)
                elif player.possible_takes:
                    return max(player.possible_takes)
                else:
                    return sorted(player.hand, key=lambda x: x & card_mask)[0]
        else:
            if player.guaranteed_takes:
                return min(player.guaranteed_takes)
            elif player.possible_takes:
                return max(player.possible_takes)
            else:
                return sorted(player.hand, key=lambda x: x & card_mask)[0]

    @staticmethod
    def shoot_2nd_or_3rd(ctx, player):
        state = ctx.current_state

        moves = player.legal_moves(state.suit)

        if len(moves) == 1:
            return moves[0]

        suit = [i for i in player.hand if i >> 13 == state.suit]

        if suit:
            possible_suits = map(lambda x: x >> 13, player.possible_takes)
            possible_moves = filter(lambda x: x >> 13 == state.suit, player.possible_takes)
            if state.suit in possible_suits and not player.is_missing_suit(ctx):
                return min(possible_moves)
            else:
                return player.safest_take(ctx)
        else:
            non_heart_takes = [i for i in player.possible_takes if i >> 13 != 3]
            if non_heart_takes:
                return min(non_heart_takes)
            else:
                player.is_shooting = False
                return player.give_L(ctx)

    @staticmethod
    def shoot_last(ctx, player):
        state = ctx.current_state

        moves = player.legal_moves(state.suit)

        if len(moves) == 1:
            return moves[0]

        suit = [i for i in player.hand if i >> 13 == state.suit]

        if suit:
            possible_suits = map(lambda x: x >> 13, player.possible_takes)
            if state.suit in possible_suits:
                possible_moves = [i for i in player.possible_takes if i >> 13 == state.suit]
                if state.points() == 0:
                    return min(possible_moves)
                elif state.points() < 0:
                    possible_takes = [i for i in possible_moves if i > state.highest()]
                    if possible_takes:
                        return min(possible_takes)
                    else:
                        return player.safest_take(ctx)
                else:
                    return player.safest_take(ctx)
            else:
                return player.safest_take(ctx)
        else:
            non_heart_takes = [i for i in player.possible_takes if i >> 13 != 3]
            if non_heart_takes:
                return min(non_heart_takes)
            else:
                player.is_shooting = False
                return player.give_L(ctx)

    @staticmethod
    def block_first(ctx, player):
        return player.play_first(ctx)

    @staticmethod
    def block_2nd_or_3rd(ctx, player):
        state = ctx.current_state

        moves = player.legal_moves(ctx)

        if len(moves) == 1:
            return moves[0]

        suit = [i for i in player.hand if i >> 13 == state.suit]

        if suit:
            if state.points() < blocking_point_threshold:
                return player.safest_take(ctx)
            elif player.is_missing_suit(ctx) > 0 and state.suit == 2:
                return player.safest_take(ctx)
            else:
                return player.avoid_taking(ctx)
        else:
            return player.give_L(ctx)

    @staticmethod
    def block_last(ctx, player):
        state = ctx.current_state

        moves = player.legal_moves(ctx)

        if len(moves) == 1:
            return moves[0]

        suit = [i for i in player.hand if i >> 13 == state.suit]

        if suit:
            if state.points() < blocking_point_threshold:
                return player.safest_take(ctx)
            elif player.is_missing_suit(ctx) > 0 and state.suit == 2:
                return player.safest_take(ctx)
            else:
                return player.avoid_taking(ctx)
        else:
            return player.give_L(ctx)