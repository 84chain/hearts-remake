import random
import csv

from player.players.aggressive_player import *


# HELPERS
def player_order(id):
    return [id, (id + 1) % 4, (id + 2) % 4, (id + 3) % 4]


def next_first_player(table, played_order):
    for card in table.cards:
        if is_taking(table, card):
            return played_order[table.cards.index(card)]


class Game:
    def __init__(self, pass_direction):
        self.deck = [Card(suit + value) for suit in "cdsh" for value in
                     [str(n) for n in range(2, 11)] + ["j", "q", "k", "a"]]
        random.shuffle(self.deck)

        self.vector = []

        self.pass_direction = pass_direction # 1, -1, 2

        hands = [self.deck[:13], self.deck[13:26], self.deck[26:39], self.deck[39:]]
        self.player_0 = AggressivePlayer(0, 0)
        self.player_1 = AggressivePlayer(1, 1)
        self.player_2 = AggressivePlayer(2, 2)
        self.player_3 = AggressivePlayer(3, 3)
        self.players = [self.player_0, self.player_1, self.player_2, self.player_3]
        self.pass_data = []

        for i in range(4):
            self.players[i].deal_hand(hands[i])

        # dealt hand
        self.vector.append(self.player_0.hand.to_int())

        p_0_pass = Game.passCards(self)

        # pass
        self.vector.append(Hand(p_0_pass).to_int())

        self.vector.append(self.pass_direction)

        # post-pass
        self.vector.append(self.player_0.hand.to_int())


    def passCards(self):
        p_0_pass = self.player_0.pass_cards()
        p_1_pass = self.player_1.pass_cards()
        p_2_pass = self.player_2.pass_cards()
        p_3_pass = self.player_3.pass_cards()

        self.passes = [p_0_pass, p_1_pass, p_2_pass, p_3_pass]

        if self.pass_direction == -1:
            self.player_0.receive_pass(p_3_pass)
            self.player_1.receive_pass(p_0_pass)
            self.player_2.receive_pass(p_1_pass)
            self.player_3.receive_pass(p_2_pass)
        elif self.pass_direction == 2:
            self.player_0.receive_pass(p_2_pass)
            self.player_1.receive_pass(p_3_pass)
            self.player_2.receive_pass(p_0_pass)
            self.player_3.receive_pass(p_1_pass)
        elif self.pass_direction == 1:
            self.player_0.receive_pass(p_1_pass)
            self.player_1.receive_pass(p_2_pass)
            self.player_2.receive_pass(p_3_pass)
            self.player_3.receive_pass(p_0_pass)

        return p_0_pass

    def reset(self):
        self.deck = [Card(suit + value) for suit in "cdsh" for value in
                     [str(n) for n in range(2, 11)] + ["j", "q", "k", "a"]]
        random.shuffle(self.deck)

        self.vector = []

        self.pass_direction = -1  # 1, -1, 2

        hands = [self.deck[:13], self.deck[13:26], self.deck[26:39], self.deck[39:]]
        self.player_0 = AggressivePlayer(0, 0)
        self.player_1 = AggressivePlayer(1, 1)
        self.player_2 = AggressivePlayer(2, 2)
        self.player_3 = AggressivePlayer(3, 3)
        self.players = [self.player_0, self.player_1, self.player_2, self.player_3]
        self.pass_data = []

        for i in range(4):
            self.players[i].deal_hand(hands[i])

        # dealt hand
        self.vector.append(self.player_0.hand.to_int_list())

        p_0_pass = Game.passCards(self)

        # pass
        self.vector.append(card_list_to_flags(p_0_pass))

        if self.pass_direction < 0:
            self.vector.append([1, 0, 0])
        elif self.pass_direction == 2:
            self.vector.append([0, 1, 0])
        elif self.pass_direction == 1:
            self.vector.append([0, 0, 1])

        # post-pass
        self.vector.append(self.player_0.hand.to_int_list())

    def play(self):
        # ROUND 1
        player_with_3 = [player for player in self.players if in_hand(club_3, player.hand)][0].id
        first_player_order = player_order(player_with_3)
        first_table = Table()
        order_list = []

        for p in range(4):
            c_player = self.players[first_player_order[p]]
            card = c_player.play_card(first_table)
            first_table.card_played(card, c_player)

            # recording data
            if c_player.id == 0:
                vector = []
                points = c_player.running_count()
                vector_player_order = first_player_order.index(0)
                int_suit = ['c', 'd', 's', 'h'].index(first_table.suit)

                # append to vector
                vector.append(1)
                vector.append(Hand([i for i in first_table.cards]).to_int())
                vector.append(Hand(c_player.cards_played).to_int())
                vector.append(int_suit)
                vector.append(vector_player_order)
                vector.append(Hand([i for i in c_player.cards_took if i.suit == "h"]).to_int())
                vector.append(points)

                # save
                with open('game_data.csv', 'a', encoding='UTF8') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.vector + vector)


        card_list = []
        for card in first_table.cards:
            card_list.append(card.to_string())


        for p in self.players:
            p.update(first_table)
        order_list.append(player_order(next_first_player(first_table, first_player_order)))

        # ROUND 2-13
        for rounds in range(2, 14):
            table = Table()
            order = order_list[-1]
            for p in range(4):
                c_player = self.players[order[p]]
                card = c_player.play_card(table)
                table.card_played(card, c_player)

                if c_player.id == 0:
                    vector = []
                    points = c_player.running_count()
                    vector_player_order = order.index(0)
                    int_suit = ['c', 'd', 's', 'h'].index(table.suit)

                    # append to vector
                    vector.append(rounds)
                    vector.append(Hand([i for i in first_table.cards]).to_int())
                    vector.append(Hand(c_player.cards_played).to_int())
                    vector.append(int_suit)
                    vector.append(vector_player_order)
                    vector.append(Hand([i for i in c_player.cards_took if i.suit == "h"]).to_int())
                    vector.append(points)

                    # save
                    with open('game_data.csv', 'a', encoding='UTF8') as f:
                        writer = csv.writer(f)
                        writer.writerow(self.vector + vector)

            card_list = []
            for card in table.cards:
                card_list.append(card.to_string())
            for p in self.players:
                p.update(table)
            order_list.append(player_order(next_first_player(table, order)))

        pointdata = []
        for p in self.players:
            p.count_points()
            pointdata.append({"Player": p.id,
                                   "Points": p.points})

        # reset
        Game.reset(self)

        return pointdata

iterations = 100
for i in range(iterations):
    if i % 3 == 0:
        pass_direction = -1
    elif i % 3 == 1:
        pass_direction = 1
    else:
        pass_direction = 2
    g = Game(pass_direction)
    print(i, g.play())