from setup.card import *
from setup.controls import *

import math

logf = [
    0,
    0,
    0.6931471805599453,
    1.791759469228055,
    3.1780538303479453,
    4.787491742782046,
    6.579251212010101,
    8.525161361065415,
    10.60460290274525,
    12.80182748008147,
    15.104412573075518,
    17.502307845873887,
    19.98721449566189,
    22.552163853123425,
    25.191221182738683,
    27.899271383840894,
    30.671860106080675,
    33.50507345013689,
    36.39544520803305,
    39.339884187199495,
    42.335616460753485,
    45.38013889847691,
    48.47118135183523,
    51.60667556776438,
    54.784729398112326,
    58.003605222980525,
    61.26170176100201,
    64.55753862700634,
    67.88974313718154,
    71.25703896716801,
    74.65823634883017,
    78.09222355331532,
    81.55795945611504,
    85.05446701758153,
    88.5808275421977,
    92.13617560368711,
    95.71969454214322,
    99.33061245478744,
    102.96819861451382,
    106.63176026064347,
    110.3206397147574,
    114.0342117814617,
    117.77188139974507,
    121.53308151543864,
    125.3172711493569,
    129.12393363912722,
    132.95257503561632,
    136.80272263732638,
    140.67392364823428,
    144.5657439463449,
    148.47776695177305,
    152.40959258449737,
    156.3608363030788
]


def c_comb(n, k):
    if n < 0 or k < 0:
        return 0
    else:
        return round(math.exp(logf[n] - logf[n - k] - logf[k]))


def multiple_max(value_list):
    max_value = max(value_list)
    if len([i for i in value_list if i == max_value]) > 1:
        return None
    else:
        return max_value


def j_blocked(state):
    diamonds = [i for i in state.cards if i >> 13 == 1]
    if diamonds:
        higher_diamonds = [i for i in diamonds if i > d_jack]
        return bool(higher_diamonds)
    else:
        return False


def jack_highest(hand, cards_played):
    highest_in_hand = max([i for i in hand if i >> 13 == 1])
    highest_in_played = max([i for i in cards_played if i >> 13 == 1])
    return highest_in_played < d_jack and highest_in_hand < d_jack


def can_block(hand):
    return bool([i for i in hand if i >> 13 == 1 and i > d_jack])


def all_same_suit(state, card):
    other_cards = []
    for c in state.cards:
        if c != card:
            other_cards.append(c >> 13)
    return len(set(other_cards)) == 1


def no_suits(state):
    no_suits_ids = []
    for i in range(4):
        if state.cards[i] >> 13 != state.suit:
            no_suits_ids.append(state.player_ids[i])
    return no_suits_ids


def player_order(position):
    positions = [
        [0, 1, 2, 3],
        [1, 2, 3, 0],
        [2, 3, 0, 1],
        [3, 0, 1, 2]
    ]
    return positions[position]


def split_hand(hand):
    clubs = []
    diamonds = []
    spades = []
    hearts = []
    for card in hand:
        if card >> 13 == 0:
            clubs.append(card)
        elif card >> 13 == 1:
            diamonds.append(card)
        elif card >> 13 == 2:
            spades.append(card)
        else:
            hearts.append(card)
    return [clubs, diamonds, spades, hearts]


def is_taking(card, hand, cards_played):
    suit = card >> 13
    suit_played = [i for i in cards_played if i >> 13 == suit]
    suit_hand = [i for i in hand if i >> 13 == suit]

    all_suit = [all_clubs, all_diamonds, all_spades, all_hearts][suit]
    cards_left = [i for i in all_suit if i not in suit_hand and i not in suit_played]

    if len(cards_left) < 4:
        return True
    else:
        cards_left.append(card)
        sorted_cards = sorted(cards_left)
        position = sorted_cards.index(card)
        return position * 2 <= len(cards_left)


def possible_takes(hand, cards_played):
    [clubs, diamonds, spades, hearts] = split_hand(hand)
    clubs_left = [i for i in all_clubs if i not in clubs and i not in cards_played]
    diamonds_left = [i for i in all_diamonds if i not in diamonds and i not in cards_played]
    spades_left = [i for i in all_spades if i not in spades and i not in cards_played]
    hearts_left = [i for i in all_hearts if i not in hearts and i not in cards_played]

    suit_pairs = [
        [clubs, clubs_left],
        [diamonds, diamonds_left],
        [spades, spades_left],
        [hearts, hearts_left]
    ]

    takes = []

    for pair in suit_pairs:
        suit = pair[0]
        left = pair[1]
        if len(suit) and len(left):
            for card in suit:
                if card < max(left):
                    takes.append(card)

    return takes


def guaranteed_takes(hand, cards_played):
    [clubs, diamonds, spades, hearts] = split_hand(hand)
    clubs_left = [i for i in all_clubs if i not in clubs and i not in cards_played]
    diamonds_left = [i for i in all_diamonds if i not in diamonds and i not in cards_played]
    spades_left = [i for i in all_spades if i not in spades and i not in cards_played]
    hearts_left = [i for i in all_hearts if i not in hearts and i not in cards_played]

    suit_pairs = [
        [clubs, clubs_left],
        [diamonds, diamonds_left],
        [spades, spades_left],
        [hearts, hearts_left]
    ]

    takes = []

    for pair in suit_pairs:
        suit = pair[0]
        left = pair[1]
        if len(suit) and len(left):
            for card in suit:
                if card > max(left):
                    takes.append(card)

    return takes


def num_guaranteed_takes(hand, cards_played):
    return len(guaranteed_takes(hand, cards_played))


def has_shot(cards_took):
    return len([i for i in cards_took if i >> 13 == 3]) == 13


def choose_pass(hand):
    return generate_passes(hand)[-1][0]


def choose_shoot_pass(hand):
    possible_pass = possible_takes(hand, [])
    return sorted(possible_pass, key=lambda x: x & card_mask)[:-3]


def generate_passes(hand):
    passes = [], hands = [], rated_hands = []

    for i in range(13):
        for j in range(i + 1, 13):
            for k in range(j + i, 13):
                passes.append([hand[i], hand[j], hand[k]])

    for p in passes:
        hands.append([p, [i for i in hand if i not in p]])
    for h in hands:
        rated_hands.append(rate_remaining_hand(h))

    return sorted(rated_hands, key=lambda x: x[-1])


def rate_remaining_hand(h):
    p = h[0]
    hand = h[1]

    empty_suits = 0

    [clubs, diamonds, spades, hearts] = split_hand(hand)

    c_weights = [club_weights[all_clubs.index(i)] for i in all_clubs if i not in clubs]
    d_weights = [diamond_weights[all_diamonds.index(i)] for i in all_diamonds if i not in diamonds]
    s_weights = [spade_weights[all_spades.index(i)] for i in all_spades if i not in spades]
    h_weights = [heart_weights[all_hearts.index(i)] for i in all_hearts if i not in hearts]

    c_scale = sum(c_weights) / len(c_weights)
    d_scale = 0
    s_scale = sum(s_weights) / len(s_weights)
    h_scale = sum(h_weights) / len(h_weights)

    if (len(diamonds) + len([i for i in p if i >> 13 == 1]) <= 2):
        d_scale = sum(d_weights) / len(d_weights)

    c_rating = c_scale * suits_preference[0]
    d_rating = d_scale * suits_preference[1]
    s_rating = s_scale * suits_preference[2]
    h_rating = h_scale * suits_preference[3]

    for suit in [clubs, diamonds, spades, hearts]:
        if not suit:
            empty_suits += 1

    empty_rating = empty_suits * suit[4]

    rating_sum = c_rating + d_rating + s_rating + h_rating + empty_rating

    return [p, rating_sum]


def create_pool(pawn, cards_played, hand):

    clubs_left = [i for i in all_clubs if i not in cards_played and i not in hand]
    diamonds_left = [i for i in all_diamonds if i not in cards_played and i not in hand]
    spades_left = [i for i in all_spades if i not in cards_played and i not in hand]
    hearts_left = [i for i in all_hearts if i not in cards_played and i not in hand]
    clubs = len(clubs_left) - len(pawn.hand.clubs) if pawn.has_clubs else 0
    diamonds = len(diamonds_left) - len(pawn.hand.diamonds) if pawn.has_diamonds else 0
    spades = len(spades_left) - len(pawn.hand.spades) if pawn.has_spades else 0
    hearts = len(hearts_left) - len(pawn.hand.hearts) if pawn.has_hearts else 0

    return {
            "clubs": clubs,
            "diamonds": diamonds,
            "spades": spades,
            "hearts": hearts,
            "hand": pawn.cards_left,
            "size": clubs + diamonds + spades + hearts
    }


def intersection(pool1, pool2):
    return {
        "clubs": min(pool1["clubs"], pool2["clubs"]),
        "diamonds": min(pool1["diamonds"], pool2["diamonds"]),
        "spades": min(pool1["spades"], pool2["spades"]),
        "hearts": min(pool1["hearts"], pool2["hearts"]),
        "hand": min(pool1["hand"], pool2["hand"]),
        "size": min(pool1["size"], pool2["size"])
    }


def union(pool1, pool2):
    return {
        "clubs": max(pool1["clubs"], pool2["clubs"]),
        "diamonds": max(pool1["diamonds"], pool2["diamonds"]),
        "spades": max(pool1["spades"], pool2["spades"]),
        "hearts": max(pool1["hearts"], pool2["hearts"]),
        "hand": max(pool1["hand"], pool2["hand"]),
        "size": max(pool1["size"], pool2["size"])
    }


def not_in(pool1, pool2):
    return {
        "clubs": max(0, pool1["clubs"] - pool2["clubs"]),
        "diamonds": max(0, pool1["clubs"] - pool2["clubs"]),
        "spades": max(0, pool1["spades"] - pool2["spades"]),
        "hearts": max(0, pool1["hearts"] - pool2["hearts"]),
        "hand": max(0, pool1["hand"] - pool2["hand"]),
        "size": max(0, pool1["size"] - pool2["size"])
    }


def subset(pool1, pool2):
    for suit in ["clubs", "diamonds", "spades", "hearts"]:
        if pool1[suit] > pool2[suit]:
            return False
    else:
        return True


def order_pools(pawns, cards_played, own_hand):
    arrows = []
    players = [[p, create_pool(p, cards_played, own_hand)] for p in pawns]
    pools = [pool1, pool2, pool3] = [p[-1] for p in players]
    if subset(pool1, pool2):
        arrows.append([0, 1])
    elif subset(pool2, pool1):
        arrows.append([1, 0])
    if subset(pool2, pool3):
        arrows.append([1, 2])
    elif subset(pool3, pool2):
        arrows.append([2, 1])
    if subset(pool3, pool1):
        arrows.append([2, 0])
    elif subset(pool1, pool3):
        arrows.append([0, 2])
    if not len(arrows):
        case = 5
        ordered_players = sorted(players, key=lambda x: x[-1]["size"])
    else:
        if len(arrows) == 1:
            ordered_players = [players[arrows[0][0]], players[arrows[0][1]],
                               players[[i for i in [0, 1, 2] if i not in arrows[0]][0]]]
            case = 4
        else:
            heads = list(set([i[1] for i in arrows]))
            tails = list(set([i[0] for i in arrows]))
            if len(heads) == 2:
                if pools[heads[0]]["size"] <= pools[heads[1]]["size"]:
                    ordered_players = [players[[i for i in [0, 1, 2] if i not in heads][0]], players[heads[0]],
                                       players[heads[1]]]
                else:
                    ordered_players = [players[[i for i in [0, 1, 2] if i not in heads][0]], players[heads[1]],
                                       players[heads[0]]]
                case = 2
            elif len(tails) == 2:
                if pools[tails[0]]["size"] <= pools[tails[1]]["size"]:
                    ordered_players = [players[[i for i in [0, 1, 2] if i not in tails][0]], players[tails[0]],
                                       players[tails[1]]]
                else:
                    ordered_players = [players[[i for i in [0, 1, 2] if i not in tails][0]], players[tails[1]],
                                       players[tails[0]]]
                case = 3
            else:
                ordered_players = sorted(players, key=lambda x: x[-1]["size"])
                case = 1
    return {"players": ordered_players,
            "case": case}


def calculate_combinations(case_and_players):
    case = case_and_players["case"]
    players = [p[-1] for p in case_and_players["players"]]
    l = players[0]
    u = players[1]
    r = players[-1]
    combinations = 0
    if case == 1:
        combinations = c_comb(l["size"], l["hand"]) * c_comb(u["size"] - l["hand"], u["hand"])
    elif case == 2:
        u_hand_reduced = u["hand"] - not_in(u, intersection(u, r))["size"]
        combinations = c_comb(l["size"], l["hand"]) * c_comb(intersection(u, r)["size"], u_hand_reduced)
    elif case == 3:
        l_not_in_l_r = l["hand"] - not_in(l, intersection(l, r))["size"]
        for i in range(l["hand"]):
            combinations += c_comb(intersection(l, r)["size"], i) * c_comb(l_not_in_l_r, l["hand"] - i) * c_comb(
                r["size"] - i, r["hand"])
    elif case == 4:
        r_hand_reduced = r["hand"] - not_in(r, intersection(r, u))["size"]
        l_not_in_l_r = l["hand"] - not_in(l, intersection(l, r))["size"]
        for i in range(l["hand"]):
            combinations += c_comb(intersection(l, r)["size"], i) * c_comb(l_not_in_l_r, l["hand"] - i) * c_comb(
                intersection(r, u)["size"] - i, r_hand_reduced)
    elif case == 5:
        l_u_r = intersection(intersection(l, u), r)
        l_u_not_in_l_u_r = not_in(intersection(l, u), l_u_r)["size"]
        l_r_not_in_l_u_r = not_in(intersection(l, r), l_u_r)["size"]
        u_r_not_in_l_u_r = not_in(intersection(u, r), l_u_r)["size"]
        z_l = l["hand"] - not_in(l, union(intersection(l, u), intersection(l, r)))["size"]
        for i in range(l["hand"]):
            for j in range(l["hand"]):
                z_r = r["hand"] - not_in(r, u)["size"] + j
                for k in range(r["hand"]):
                    combinations += c_comb(l_u_r["size"], i) * c_comb(
                        l_r_not_in_l_u_r, j) * c_comb(
                        l_u_r["size"] - i, k) * c_comb(
                        l_u_not_in_l_u_r, z_l - (i + j)) * c_comb(
                        u_r_not_in_l_u_r, z_r - k
                    )
    return combinations
