from setup.setup import *
from setup.controls import *

class Altruism:
    def choose_card(self, ctx, player):
        [clubs, diamonds, spades, hearts] = split_hand(player.hand)

        clubs_left = [i for i in all_clubs if i not in clubs and i not in ctx.cards_played]
        diamonds_left = [i for i in all_diamonds if i not in diamonds and i not in ctx.cards_played]
        spades_left = [i for i in all_spades if i not in spades and i not in ctx.cards_played]
        hearts_left = [i for i in all_hearts if i not in hearts and i not in ctx.cards_played]

        missing_suits = []

        team_pawn = [i for i in player.pawns if i.id == player.teammate.id][0]

        for suit in range(4):
            if not team_pawn.has_suit(suit):
                if suit == 0:
                    if clubs:
                        clubs_left.append(min(clubs))
                        position = sorted(clubs_left).index(min(clubs))
                        missing_suits.append([min(clubs), position])
                elif suit == 1:
                    if diamonds:
                        diamonds_left.append(min(diamonds))
                        position = sorted(diamonds_left).index(min(diamonds))
                        if d_jack in ctx.cards_played:
                            missing_suits.append([min(diamonds), position])
                elif suit == 2:
                    if spades:
                        spades_left.append(min(spades))
                        position = sorted(spades_left).index(min(spades))
                        if min(spades) != q_spades:
                            missing_suits.append([min(spades), position])
                elif suit == 3:
                    if hearts:
                        hearts_left.append(min(hearts))
                        position = sorted(hearts_left).index(min(hearts))
                        missing_suits.append([min(hearts), position])

        if missing_suits:
            return sorted(missing_suits, key=lambda x: (x[1], x[0]))[-1][0]
        return player.choose_card(ctx)

    def avoid_taking(self, ctx, player):
        state = ctx.current_state

        suit = [i for i in player.hand if i >> 13 == state.suit]

        if min(suit) > state.highest():
            return player.safest_take(ctx)

        if state.suit == 0:
            if max(suit) == club_10 and player.teammate.points < 0:
                return club_10
            else:
                other_clubs = [i for i in suit if i < state.highest() and i != club_10]
                if other_clubs:
                    return max(other_clubs)
                else:
                    return max([i for i in suit if i < state.highest()])
        elif state.suit == 1:
            if jack_highest(player.hand, ctx.cards_played) and d_jack in player.hand:
                return d_jack
            else:
                return max([i for i in suit if i != d_jack and i < state.highest()])
        elif state.suit == 2:
            other_spades = [i for i in suit if i != q_spades and i < state.highest()]
            if other_spades:
                return max(other_spades)
            else:
                return max([i for i in suit if i != q_spades])
        elif state.suit == 3:
            return min(suit)

    def give_L(self, ctx, player):
        [clubs, diamonds, spades, hearts] = split_hand(player.hand)

        clubs_left = [i for i in all_clubs if i not in clubs and i not in ctx.cards_played]
        diamonds_left = [i for i in all_diamonds if i not in diamonds and i not in ctx.cards_played]
        spades_left = [i for i in all_spades if i not in spades and i not in ctx.cards_played]
        hearts_left = [i for i in all_hearts if i not in hearts and i not in ctx.cards_played]

        card_list = []

        for card in player.hand:
            if card >> 13 == 0:
                if clubs_left:
                    len_clubs = len(clubs_left)
                    clubs_left.append(card)
                    sorted_clubs = sorted(clubs_left)
                    position = sorted_clubs.index(card)
                    c_scale = len([i for i in clubs if i > club_10])

                    if card == club_10:
                        if player.teammate.points < 0:
                            rating = -1
                        else:
                            rating = 99
                    else:
                        rating = len_clubs - position + c_scale
                else:
                    rating = 13 - ctx.round
            elif card >> 13 == 1:
                if diamonds_left:
                    len_diamonds = len(diamonds_left)
                    diamonds.append(card)
                    sorted_diamonds = sorted(diamonds_left)
                    position = sorted_diamonds.index(card)
                    d_scale = len([i for i in diamonds if i > d_jack])
                    if d_jack in ctx.cards_played:
                        rating = len_diamonds - position + d_scale
                    else:
                        if card != d_jack:
                            rating = len_diamonds
                        else:
                            rating = -2
                else:
                    rating = 13 - ctx.round
            elif card >> 13 == 2:
                if spades_left:
                    len_spades = len(spades_left)
                    spades_left.append(card)
                    sorted_spades = sorted(spades_left)
                    position = sorted_spades.index(card)
                    s_scale = len([i for i in spades if i > q_spades])
                    if card != q_spades:
                        rating = len_spades - position + s_scale
                    else:
                        rating = 99
                else:
                    rating = 13 - ctx.round
            elif card >> 13 == 3:
                if hearts_left:
                    len_hearts = len(hearts_left)
                    hearts_left.append(card)
                    sorted_hearts = sorted(hearts_left)
                    position = sorted_hearts.index(card)
                    if not all_points[card]:
                        rating = position
                    else:
                        if player.teammate.has_10:
                            rating = 99
                        else:
                            rating = len_hearts + position + all_points[card] / 50
                else:
                    rating = 13 - ctx.round
            card_list.append([card, rating])
        return sorted(card_list, key=lambda x: (x[-1], x[0]), reverse=True)[0][0]

    def feed_shoot(self, ctx, player):
        state = ctx.current_state

        [clubs, diamonds, spades, hearts] = split_hand(player.hand)

        clubs_left = [i for i in all_clubs if i not in clubs and i not in ctx.cards_played]
        spades_left = [i for i in all_spades if i not in spades and i not in ctx.cards_played]

        suit = [i for i in player.hand if i >> 13 == state.suit]
        lower_suit = [i for i in suit if i < state.highest()]

        if min(suit) > state.highest():
            return Altruism.avoid_taking(self, ctx, player)

        if state.suit == 0:
            if len(clubs_left) >= len(suit) * 2:
                return max([i for i in lower_suit if i != club_10])
            else:
                return max(lower_suit)
        elif state.suit == 1:
            if d_jack in lower_suit:
                return d_jack
            else:
                return max(lower_suit)
        elif state.suit == 2:
            if len(spades_left) >= len(suit) * 2:
                return max([i for i in lower_suit if i != q_spades])
            else:
                return max(lower_suit)
        elif state.suit == 3:
            return max(lower_suit)

    def play_first(self, ctx, player):
        if club_3 in player.hand:
            return club_3
        else:
            return Altruism.choose_card(self, ctx, player)

    def play_2nd_or_3rd(self, ctx, player):
        state = ctx.current_state

        moves = player.legal_moves(state.suit)

        if len(moves) == 1:
            return moves[0]

        suit = [i for i in player.hand if i >> 13 == state.suit]

        if suit:
            if player.teammate.is_shooting:
                return Altruism.feed_shoot(self, ctx, player)
            elif player.has_10:
                return player.avoid_taking(ctx)
            elif player.teammate.has_10:
                return player.safest_take(ctx)
            else:
                if state.suit == 1:
                    if d_jack in ctx.cards_played:
                        if d_jack in suit:
                            return d_jack
                        else:
                            return player.avoid_taking(ctx)
                    else:
                        diamonds_left = [i for i in all_diamonds if i not in player.hand and i not in ctx.cards_played]
                        if can_block(player.hand) and state.points() <= 100 and len(diamonds_left) <= (3 - state.length()):
                            return player.block_j()
                        else:
                            return player.avoid_taking(ctx)
                elif state.suit == 3:
                    return min(suit)
                if player.is_missing_suit(ctx) >= player.risk_tolerance:
                    return player.safest_take(ctx)
                else:
                    if player.teammate in state.players:
                        position = state.players.index(player.teammate)
                        teammate_card = state.cards[position]
                        if is_taking(teammate_card, player.hand, ctx.cards_played):
                            return Altruism.avoid_taking(self, ctx, player)
                        else:
                            return player.avoid_taking(ctx)
                    else:
                        return Altruism.avoid_taking(self, ctx, player)
        else:
            if player.teammate in state.players:
                position = state.players.index(player.teammate)
                teammate_card = state.cards[position]
                if is_taking(teammate_card, player.hand, ctx.cards_played):
                    return Altruism.give_L(self, ctx, player)
                else:
                    return player.give_L(ctx)
            else:
                return Altruism.give_L(self, ctx, player)

    def play_last(self, ctx, player):
        state = ctx.current_state

        moves = player.legal_moves(state.suit)

        if len(moves) == 1:
            return moves[0]

        suit = [i for i in player.hand if i >> 13 == state.suit]

        if suit:
            if player.teammate.is_shooting:
                return Altruism.feed_shoot(self, ctx, player)
            elif player.has_10:
                return player.avoid_taking(ctx)
            elif player.teammate.has_10:
                return player.safest_take(ctx)
            else:
                if state.points() >= taking_point_threshold:
                    return Altruism.avoid_taking(self, ctx, player)
                else:
                    if state.suit == 1 and state.highest() < d_jack and d_jack in player.hand:
                        return player.safest_take(ctx)
                    else:
                        return Altruism.avoid_taking(self, ctx, player)
        else:
            return Altruism.give_L(self, ctx, player)