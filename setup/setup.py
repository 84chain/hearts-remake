# Contains helpers and classes for other classes
import statistics
from math import comb

from .hand import *
from .card import *
from .suit import *
from .controls import *


# HELPERS
def c_comb(n, k):
    """
    Custom combinations that returns 0 if n or k are negative
    :param n: int
    :param k: int
    :return: int
    """
    if n < 0 or k < 0:
        return 0
    else:
        return comb(n, k)

def multiple_max(value_list):
    """
    Maximum value finder that returns None if there is a tie for max value
    :param value_list: list(int)
    :return: int or None
    """
    max_value = max(value_list)
    if len([i for i in value_list if i == max_value]) > 1:
        return None
    else:
        return max_value

def return_highest(table):
    """
    Highest card of the correct suit that is currently taking
    :param table: Table()
    :return: Card()
    """
    same_suits = []
    for c in table.cards:
        if c.suit == table.suit:
            same_suits.append(c)
    same_suits.sort(key=lambda card: int(card.value), reverse=True)
    return same_suits[0]


def in_hand(card, hand):
    """
    Whether the card is in the hand
    :param card: Card()
    :param hand: Hand()
    :return: bool
    """
    suit = card.suit
    if suit == "c":
        return bool(len([club for club in hand.clubs if club.is_eq(card)]))
    elif suit == "d":
        return bool(len([diamond for diamond in hand.diamonds if diamond.is_eq(card)]))
    elif suit == "s":
        return bool(len([spade for spade in hand.spades if spade.is_eq(card)]))
    elif suit == "h":
        return bool(len([heart for heart in hand.hearts if heart.is_eq(card)]))


def played(card, cards_played):
    """
    Whether a card has been played
    :param card: Card()
    :param cards_played: list(Card)
    :return:
    """
    return len([c for c in cards_played if c.is_eq(card)]) == 1


def j_blocked(table):
    """
    If J of Diamonds is already blocked in the current table
    :param table: Table()
    :return: bool
    """
    return bool(len([card for card in table.cards if (card.suit == "d" and card.value > 11)]))


def is_taking(table, card):
    """
    Whether the card is taking the table
    :param table: Table()
    :param card: Card()
    :return: bool
    """
    highest = return_highest(table)
    return highest.is_eq(card)


def jack_highest(cards_played, hand):
    """
    Whether J is the highest diamond left
    :param cards_played: list(Card)
    :param hand: Hand()
    :return: bool
    """
    p_hand = Hand(cards_played)
    suit_cards = [val for val in [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] if
                  val not in [c.value for c in p_hand.diamonds] and val not in [c.value for c in hand.diamonds]]
    if len(suit_cards) == 0:
        return False
    return suit_cards[-1] == 11


def can_block(hand):
    """
    Whether current hand can block J of Diamonds
    :param hand: Hand()
    :return: bool
    """
    return bool(len([i for i in hand.diamonds if i.value > 11]))


def all_same_suit(table, card):
    """
    Whether all cards played in the current table are of the same suit
    :param table: Table()
    :param card: Card() that the Player() played this Table()
    :return: bool
    """
    ind = table.cards.index(card)
    order_list = [0, 1, 2, 3]
    order_list.remove(ind)
    suit_list = []
    for i in order_list:
        suit_list.append(table.cards[i].suit)
    return suit_list.count(suit_list[0]) == len(suit_list)


def all_same_suit_alt(table, card):
    """
    all_same_suit but for the sim
    :param table: Table()
    :param card: Card()
    :return: bool
    """
    ind = -1
    for i in range(4):
        if card.is_eq(table.cards[i]):
            ind = i
            break
    order_list = [0, 1, 2, 3]
    order_list.remove(ind)
    suit_list = []
    for i in order_list:
        suit_list.append(table.cards[i].suit)
    return suit_list.count(suit_list[0]) == len(suit_list)


def no_suits(table):
    """
    Player ids that did not have the correct suit
    :param table: Table()
    :param card: Card()
    :return: list(int)
    """
    ids = []
    for i in range(4):
        if table.cards[i].suit != table.cards[0].suit:
            ids.append(table.players[i].id)
    return ids


def possible_takes(hand, cards_played):
    """
    Finds possible takes in hand
    :param hand: Hand()
    :param cards_played: list(Card)
    :return: list(Card)
    """
    int_hand = [c.to_int() for c in hand.to_list()]
    cards_left = [c for c in all_int_cards if c not in (int_hand + Hand(cards_played).to_int_list())]
    clubs_left = [i for i in cards_left if i < 13]
    diamonds_left = [i for i in cards_left if i >= 13 and i < 26]
    spades_left = [i for i in cards_left if i >= 26 and i < 39]
    hearts_left = [i for i in cards_left if i >= 39]
    takes = []
    if hand.clubs:
        if clubs_left:
            for card in hand.clubs:
                if card.to_int() < clubs_left[-1]:
                    takes.append(card)
    if hand.diamonds:
        if diamonds_left:
            for card in hand.diamonds:
                if card.to_int() < diamonds_left[-1]:
                    takes.append(card)
    if hand.spades:
        if spades_left:
            for card in hand.spades:
                if card.to_int() < spades_left[-1]:
                    takes.append(card)
    if hand.hearts:
        if hearts_left:
            for card in hand.hearts:
                if card.to_int() < hearts_left[-1]:
                    takes.append(card)
    return takes


def choose_pass(hand):
    """
    Chooses the highest rated pass out of all possible passes
    :param hand: Hand()
    :return: list(Card) <- len(list(Card)) always 3
    """
    return [Card(c) for c in generate_passes(hand.to_list())[0]["pass"]]


def choose_shoot_pass(hand):
    """
    Chooses pass for shooting the moon
    :param hand: Hand()
    :return: list(Card)
    """
    possible_pass = possible_takes(hand, [])
    sorted_pass = sorted([Card(i) for i in possible_pass], key=lambda x: x.value)
    return sorted_pass[:3]


def rate_remaining_hand(h):
    """
    Applies a rating to the remaining hand after the current pass is popped from the array
    :param h: [list(Card), Hand()] ([the pass, remaining hand])
    :return: dict
    """
    clubs = h[-1].clubs
    diamonds = h[-1].diamonds
    spades = h[-1].spades
    hearts = h[-1].hearts

    c_scale = statistics.mean([club_weights[v] for v in range(2, 15) if v not in [c.value for c in clubs]])
    if len(diamonds) + len([d for d in h[0] if d % 13 == 1]) <= 2:
        d_scale = statistics.mean([diamond_weights[v] for v in range(2, 15) if v not in [c.value for c in diamonds]])
    else:
        d_scale = 0
    s_scale = statistics.mean([spade_weights[v] for v in range(2, 15) if v not in [c.value for c in spades]])
    h_scale = statistics.mean([hearts_weights[v] for v in range(2, 15) if v not in [c.value for c in hearts]])

    c_rating = c_scale * suits_preference["c"]
    d_rating = d_scale * suits_preference["d"]
    s_rating = s_scale * suits_preference["s"]
    h_rating = h_scale * suits_preference["h"]

    rating_sum = c_rating + d_rating + s_rating + h_rating
    empty_suits = []
    for i in [clubs, diamonds, spades, hearts]:
        if not i:
            empty_suits.append(i)
    rating_sum += len(empty_suits) * suits_preference["e"]

    return {
        "pass": h[0],
        "c": c_rating,
        "d": d_rating,
        "s": s_rating,
        "h": h_rating,
        "sum": rating_sum
    }


def generate_passes(list_hand):
    """
    Generates all possible passes, rates each hand, and sorts the list
    :param list_hand: list(Card)
    :return: list(dict)
    """
    str_list_hand = [c.to_int() for c in list_hand]
    passes = []
    hands = []
    rated_hands = []
    for i in range(13):
        for j in range(i + 1, 13):
            for k in range(j + 1, 13):
                passes.append([c.to_int() for c in [list_hand[i], list_hand[j], list_hand[k]]])

    for p in passes:
        hands.append([p, Hand([Card(c) for c in str_list_hand if c not in p])])
    for h in hands:
        rated_hands.append(rate_remaining_hand(h))
    sorted_hands = sorted(rated_hands, key=lambda x: x["sum"], reverse=True)
    return sorted_hands


def long_to_list(long):
    """
    Converts a long to list of card integer references
    :param long: long
    :return: list(int)
    """
    list_of_cards = []
    mask = 1
    for i in range(52):
        if long & mask != 0:
            list_of_cards.append(i)
        mask <<= 1
    return list_of_cards


def card_index(card, list_card):
    """
    Returns the index of card in listcard
    :param card: Card()
    :param list_card: list(Card)
    :return: int
    """
    return [i.to_int() for i in list_card].index(card.to_int())


def player_order(player_position):
    """
    Returns order of players from player's position
    :param player_position: int
    :return: list(int)
    """
    positions = [[0, 1, 2, 3],
                 [1, 2, 3, 0],
                 [2, 3, 0, 1],
                 [3, 0, 1, 2]]
    return positions[player_position]


def has_shot(cards_took):
    """
    Whether player has shot the moon
    :param cards_took: list(Card)
    :return: bool
    """
    return len([i for i in cards_took if i.suit == "h"]) == 13


def guaranteed_takes(hand, cards_played):
    """
    Finds guaranteed takes in hand
    :param hand: Hand()
    :param cards_played: list(Card)
    :return: list(Card)
    """
    takes = []
    int_hand = hand.to_int_list()
    int_cards_played = [c.to_int() for c in cards_played]
    cards_left = [c for c in all_int_cards if c not in (int_hand + int_cards_played)]
    clubs_left = [i for i in cards_left if i < 13]
    diamonds_left = [i for i in cards_left if i >= 13 and i < 26]
    spades_left = [i for i in cards_left if i >= 26 and i < 39]
    hearts_left = [i for i in cards_left if i >= 39]
    if hand.clubs:
        if clubs_left:
            for card in hand.clubs:
                if card.to_int() > clubs_left[-1]:
                    takes.append(card)
        else:
            takes += hand.clubs
    if hand.diamonds:
        if diamonds_left:
            for card in hand.diamonds:
                if card.to_int() > diamonds_left[-1]:
                    takes.append(card)
        else:
            takes += hand.diamonds
    if hand.spades:
        if spades_left:
            for card in hand.spades:
                if card.to_int() > spades_left[-1]:
                    takes.append(card)
        else:
            takes += hand.spades
    if hand.hearts:
        if hearts_left:
            for card in hand.hearts:
                if card.to_int() > hearts_left[-1]:
                    takes.append(card)
        else:
            takes += hand.hearts
    return takes


def num_guaranteed_takes(hand, cards_played):
    """
    Finds number of guaranteed takes in hand
    :param hand: Hand()
    :param cards_played: list(Card)
    :return: int
    """
    return len(guaranteed_takes(hand, cards_played))


def contains_suit(list_card, suit):
    """
    Checks if any of the cards in list is of the given suit
    :param list_card: list(Card)
    :param suit: one of ['c', 'd', 's', 'h']
    :return: bool
    """
    return bool(len([c for c in list_card if c.suit == suit]))


def reverse_bits(card):
    return 51 - card.to_int()

def team_chances_cap(chance):
    """
    Takes a float that represents likelyhood of teammate and maps it to between 0 and 1
    :param chance:
    :return:
    """
    if chance == -1:
        return chance
    else:
        if chance > 1:
            return 1
        elif chance < 0:
            return 0
        else:
            return chance

def create_pool(pawn, cards_played, own_hand):
    """
    Creates pools of possible cards for pawns
    :param pawn: Pawn()
    :param cards_played: list(Card)
    :param own_hand: Hand() -> self.hand
    :return: dict
    """
    unavailable_hand = Hand(cards_played + own_hand.to_list())
    cards_left = [c for c in all_cards if not in_hand(c, unavailable_hand)]
    clubs_left = [c for c in cards_left if c.suit == "c"]
    diamonds_left = [c for c in cards_left if c.suit == "d"]
    spades_left = [c for c in cards_left if c.suit == "s"]
    hearts_left = [c for c in cards_left if c.suit == "h"]
    clubs = len(clubs_left) - len(pawn.hand.clubs) if pawn.has_clubs else 0
    diamonds = len(diamonds_left) - len(pawn.hand.diamonds) if pawn.has_diamonds else 0
    spades = len(spades_left) - len(pawn.hand.spades) if pawn.has_spades else 0
    hearts = len(hearts_left) - len(pawn.hand.hearts) if pawn.has_hearts else 0
    return {"id": pawn.id,
            "clubs": clubs,
            "diamonds": diamonds,
            "spades": spades,
            "hearts": hearts,
            "hand": pawn.cards_left,
            "size": clubs + diamonds + spades + hearts}


def intersection(pool1, pool2):
    """
    Returns the intersection between 2 pools
    :param pool1: dict
    :param pool2: dict
    :return: dict
    """
    return {"clubs": min(pool1["clubs"], pool2["clubs"]),
            "diamonds": min(pool1["diamonds"], pool2["diamonds"]),
            "spades": min(pool1["spades"], pool2["spades"]),
            "hearts": min(pool1["hearts"], pool2["hearts"]),
            "hand": min(pool1["hand"], pool2["hand"]),
            "size": min(pool1["size"], pool2["size"])}


def union(pool1, pool2):
    """
    Returns the union of 2 pools
    :param pool1: dict
    :param pool2: dict
    :return: dict
    """
    return {"clubs": max(pool1["clubs"], pool2["clubs"]),
            "diamonds": max(pool1["diamonds"], pool2["diamonds"]),
            "spades": max(pool1["spades"], pool2["spades"]),
            "hearts": max(pool1["hearts"], pool2["hearts"]),
            "hand": max(pool1["hand"], pool2["hand"]),
            "size": max(pool1["size"], pool2["size"])}


def not_in(pool1, pool2):
    """
    Returns everything in pool1 that is not in pool 2
    :param pool1: dict
    :param pool2: dict
    :return: dict
    """
    return {"clubs": max(0, pool1["clubs"] - pool2["clubs"]),
            "diamonds": max(0, pool1["clubs"] - pool2["clubs"]),
            "spades": max(0, pool1["spades"] - pool2["spades"]),
            "hearts": max(0, pool1["hearts"] - pool2["hearts"]),
            "hand": max(0, pool1["hand"] - pool2["hand"]),
            "size": max(0, pool1["size"] - pool2["size"])}


def subset(pool1, pool2):
    """
    Returns True if pool1 is a subset of pool2
    :param pool1: dict
    :param pool2: dict
    :return: Boolean
    """
    for suit in ["clubs", "diamonds", "spades", "hearts"]:
        if pool1[suit] > pool2[suit]:
            return False
    else:
        return True


def order_pools(pawns, cards_played, own_hand):
    """
    Returns players ordered as "L", "U", "R", and case number
    :param pawns: list(Pawn)
    :param cards_played: list(Card)
    :param own_hand: Hand()
    :return: dict
    """
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
