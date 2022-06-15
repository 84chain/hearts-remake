import random
from tqdm import tqdm

from player.players.teams.team_player import *


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

        self.teams = [i for i in team_cards]
        random.shuffle(self.teams)

        self.pass_direction = pass_direction  # 1, -1, 2

        hands = [self.deck[:13], self.deck[13:26], self.deck[26:39], self.deck[39:]]
        self.player_0 = TeamPlayer(0, 0)
        self.player_1 = TeamPlayer(1, 1)
        self.player_2 = TeamPlayer(2, 2)
        self.player_3 = TeamPlayer(3, 3)
        self.players = [self.player_0, self.player_1, self.player_2, self.player_3]
        self.pass_data = []

        for i in range(4):
            self.players[i].deal_hand(hands[i])
            self.players[i].team_card = self.teams[i]

        black_ids = [self.teams.index(black_king), self.teams.index(black_ace)]
        red_ids = [self.teams.index(red_king), self.teams.index(red_ace)]

        self.real_teams = [
            [i for i in black_ids if i != 0][0] if 0 in black_ids else [i for i in red_ids if i != 0][0],
            [i for i in black_ids if i != 1][0] if 1 in black_ids else [i for i in red_ids if i != 1][0],
            [i for i in black_ids if i != 2][0] if 2 in black_ids else [i for i in red_ids if i != 2][0],
            [i for i in black_ids if i != 3][0] if 3 in black_ids else [i for i in red_ids if i != 3][0]
        ]

        ace_player = [p for p in self.players if p.team_card.is_eq(black_ace)][0]
        for i in range(4):
            self.players[i].ace_reveal(ace_player)

        Game.passCards(self)

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
        card_list = []
        for card in first_table.cards:
            card_list.append(card.to_string())

        round_1_teams = []
        for p in self.players:
            p.update_round(first_table)
            if p.teammate is not None:
                round_1_teams.append(p.teammate.id)
        if round_1_teams == self.real_teams:
            return 1
        order_list.append(player_order(next_first_player(first_table, first_player_order)))

        # ROUND 2-13
        for rounds in range(2, 14):
            table = Table()
            order = order_list[-1]
            for p in range(4):
                c_player = self.players[order[p]]
                card = c_player.play_card(table)
                table.card_played(card, c_player)
            card_list = []
            for card in table.cards:
                card_list.append(card.to_string())
            round_teams = []
            for p in self.players:
                p.update_round(table)
                if p.teammate is not None:
                    round_teams.append(p.teammate.id)
            if round_teams == self.real_teams:
                return rounds
            order_list.append(player_order(next_first_player(table, order)))

        pointdata = []
        for p in self.players:
            p.count_points()
            pointdata.append({"Player": p.id,
                              "Points": p.points})

        # reset
        # Game.reset(self)
        return 0


# Testing team guessing algorithm
iterations = 1000
data = []
for _ in tqdm(range(iterations), desc="Game.play()"):
    g = Game(random.choice([1, -1, 2]))
    result = g.play()
    data.append(result)

print(sum(data) / (iterations - len([i for i in data if i == 0])))