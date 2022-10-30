from setup.setup import *
from setup.controls import *
from players.pawn import Pawn

class Player:
    def __init__(self, id):
        self.id = id
        self.points = 0
        self.team_card = -1
        self.card = -1

        self.pawns = []

        self.hand = []
        self.cards_took = []
        self.cards = []
        self.team_chances = [0, 0, 0, 0]
        self.team_chances[self.id] = -1
        self.possible_takes = []
        self.guaranteed_takes = []

        self.has_10 = False
        self.is_shooting = False
        self.shoot_blocked = False

        self.teammate = None
        self.ace_player = None
        self.risk_tolerance = risk_tolerance

    def initialize_pawns(self, ids):
        self.pawns = [Pawn(i) for i in ids]

    def set_hand(self, hand):
        self.hand = hand
        self.guaranteed_takes = guaranteed_takes(self.hand, [])
        self.possible_takes = possible_takes(self.hand, [])

    def get_pass(self):
        cards = choose_pass(self.hand)
        self.hand = [i for i in self.hand if i not in cards]
        return cards

    def receive_pass(self, cards):
        self.hand += cards
        self.hand = sorted(self.hand)

    def get_points(self):
        points = 0
        if q_spades in self.cards_took:
            points += 100
        for i in self.cards_took:
            if i >> 13 == 3:
                points += all_points[i]
        if club_10 in self.cards_took:
            points *= 2
        if has_shot(self.cards_took):
            points *= -1
        if d_jack in self.cards_took:
            if club_10 in self.cards_took:
                points -= 200
            else:
                points -= 100
        self.points = points
        return points

    def legal_moves(self, suit):
        suit_cards = [i for i in self.hand if i >> 13 == suit]
        if suit_cards:
            return suit_cards
        else:
            return self.hand

    def ace_reveal(self, ace_player):
        if self.team_card == black_ace:
            self.team_chances = [0.33, 0.33, 0.33, 0.33]
            self.team_chances[self.id] = -1
        else:
            if self.team_card == black_king:
                self.teammate = ace_player
            else:
                self.team_chances =[0.5, 0.5, 0.5, 0.5]
                self.team_chances[self.id] = -1
                self.team_chances[ace_player.id] = 0
                self.ace_player = ace_player

    def is_missing_suit(self, ctx):
        other_pawns = [p for p in self.pawns if p.id != self.id]
        cloned_pawns = [p.create_clone(ctx.current_state.suit) if p.id not in ctx.current_state.player_ids else p for p in other_pawns]
        target_combinations = calculate_combinations(order_pools(cloned_pawns, ctx.cards_played, self.hand))
        total_combinations = calculate_combinations(order_pools(other_pawns, ctx.cards_played, self.hand))
        if total_combinations == 0:
            chance = 0
        else:
            chance = target_combinations / total_combinations
        return chance

    def choose_card(self, ctx):
        [clubs, diamonds, spades, hearts] = split_hand(self.hand)

        clubs_left = [i for i in self.hand if i not in clubs and i not in ctx.cards_played]
        diamonds_left = [i for i in self.hand if i not in diamonds and i not in ctx.cards_played]
        spades_left = [i for i in self.hand if i not in spades and i not in ctx.cards_played]
        hearts_left = [i for i in self.hand if i not in hearts and i not in ctx.cards_played]

        card_list = []

        for card in self.hand:
            if card >> 13 == 0:
                len_clubs = len(clubs_left)
                clubs_left.append(card)
                position = sorted(clubs_left).index(card)
                c_scale = len([i for i in clubs if i != club_10])
                rating = len_clubs - position - c_scale
            elif card >> 13 == 1:
                len_diamonds = len(diamonds_left)
                diamonds_left.append(card)
                position = sorted(diamonds_left).index(card)
                d_scale = 0
                if d_jack in ctx.cards_played:
                    d_scale = len([i for i in diamonds if i > d_jack])
                rating = len_diamonds - position - d_scale
            elif card >> 13 == 2:
                len_spades = len(spades_left)
                spades_left.append(card)
                position = sorted(spades_left).index(card)
                if card != q_spades:
                    s_scale = len([i for i in spades if i >= q_spades])
                    if q_spades in self.hand:
                        s_scale += 1
                    rating = len_spades - position - s_scale
                else:
                    rating = -1
            elif card >> 13 == 3:
                len_hearts = len(hearts_left)
                hearts_left.append(card)
                position = sorted(hearts_left).index(card)
                rating = len_hearts - position - (len(hearts) + all_points[card]) / 50
            card_list.append([card, rating])
        return sorted(card_list, key=lambda x: (-x[-1], x[0]))[0][0]

    def block_j(self):
        high_diamonds = [i for i in self.hand if i >> 13 == 1 and i > d_jack]
        if high_diamonds:
            return min(high_diamonds)
        else:
            return max([i for i in self.hand if i >> 13 == 1 and i < d_jack])

    def avoid_taking(self, ctx):
        state = ctx.current_state

        suit = [i for i in self.hand if i >> 13 == state.suit]

        if min(suit) > state.highest():
            return Player.safest_take(self, ctx)

        if state.suit == 0:
            if state.highest > club_10 and club_10 in suit:
                return club_10
            else:
                return max([i for i in suit if i < state.highest()])
        elif state.suit == 1:
            if min(suit) < d_jack:
                return max([i for i in suit if i < d_jack])
            else:
                return Player.block_j(self)
        elif state.suit == 2:
            if state.highest() > q_spades and q_spades in suit:
                return q_spades
            else:
                return max([i for i in suit if i != q_spades and i < state.highest()])
        elif state.suit == 3:
            return max([i for i in suit if i < state.highest()])

    def safest_take(self, ctx):
        state = ctx.current_state

        suit = [i for i in self.hand if i >> 13 == state.suit]

        if state.suit == 0:
            if not (state.points() + self.points) and state.highest() < club_10 and club_10 in suit:
                return club_10
            else:
                return max([i for i in suit if i != club_10])
        elif state.suit == 1:
            if jack_highest(self.hand, ctx.cards_played) and d_jack in suit:
                return d_jack
            elif d_jack in ctx.cards_played:
                return max(suit)
            else:
                if j_blocked(state):
                    return Player.avoid_taking(self, ctx)
                else:
                    return max([i for i in suit if i != d_jack])
        elif state.suit == 2:
            if (q_spades in suit or q_spades in ctx.cards_played) and q_spades not in state.cards:
                return max([i for i in suit if i != q_spades])
            else:
                return Player.safest_take(self, ctx)
        elif state.suit == 3:
            ten_point_hearts = [i for i in suit if i < h_10]
            if state.highest() < h_10 and ten_point_hearts:
                return max(ten_point_hearts)
            else:
                return min([i for i in suit if i > state.highest()])

    def give_L(self, ctx):
        [clubs, diamonds, spades, hearts] = split_hand(self.hand)

        clubs_left = [i for i in self.hand if i not in clubs and i not in ctx.cards_played]
        diamonds_left = [i for i in self.hand if i not in diamonds and i not in ctx.cards_played]
        spades_left = [i for i in self.hand if i not in spades and i not in ctx.cards_played]
        hearts_left = [i for i in self.hand if i not in hearts and i not in ctx.cards_played]

        card_list = []

        for card in self.hand:
            if card >> 13 == 0:
                if clubs_left:
                    len_clubs = len(clubs_left)
                    clubs_left.append(card)
                    sorted_clubs = sorted(clubs_left)
                    position = sorted_clubs.index(card)
                    c_scale = len([i for i in clubs if i > club_10])

                    if card == club_10:
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
                        rating = len_hearts + position + all_points[card] / 50
                else:
                    rating = 13 - ctx.round
            card_list.append([card, rating])
        return sorted(card_list, key=lambda x: (x[-1], x[0]), reverse=True)[0][0]

    def can_shoot(self, ctx):
        return len([i for i in ctx.cards_played if i >> 13 == 3]) == len([i for i in self.cards_took if i >> 13 == 3])