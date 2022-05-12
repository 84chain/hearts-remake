import random

from player.players.aggressive_player import *


# HELPERS
def playerorder(id):
    return [id, (id + 1) % 4, (id + 2) % 4, (id + 3) % 4]


def nextfirstplayer(table, playedorder):
    for card in table.cards:
        if is_taking(table, card):
            return playedorder[table.cards.index(card)]


class Game:
    def __init__(self, print_bool):
        self.deck = [Card(suit + value) for suit in "cdsh" for value in
                     [str(n) for n in range(2, 11)] + ["j", "q", "k", "a"]]
        random.shuffle(self.deck)

        self.gamejson = []
        self.passdirection = -1
        self.print = print_bool

        hands = [self.deck[:13], self.deck[13:26], self.deck[26:39], self.deck[39:]]

        self.player1 = AggressivePlayer(0, 0)
        self.player2 = AggressivePlayer(1, 1)
        self.player3 = AggressivePlayer(2, 2)
        self.player4 = AggressivePlayer(3, 3)
        self.players = [self.player1, self.player2, self.player3, self.player4]
        self.passedhanddata = []

        for i in range(4):
            self.players[i].deal_hand(hands[i])

        self.initialhanddata = [{"Player": 0, "Hand": self.player1.hand.to_string()},
                                {"Player": 1, "Hand": self.player2.hand.to_string()},
                                {"Player": 2, "Hand": self.player3.hand.to_string()},
                                {"Player": 3, "Hand": self.player4.hand.to_string()}]

        if self.print:
            Game.printHand(self)

        Game.passCards(self)

        self.passedhanddata = [{"Player": 0, "Hand": self.player1.hand.to_string()},
                               {"Player": 1, "Hand": self.player2.hand.to_string()},
                               {"Player": 2, "Hand": self.player3.hand.to_string()},
                               {"Player": 3, "Hand": self.player4.hand.to_string()}]

        if self.print:
            Game.printHand(self)


    def setName(self, name):
        self.player1.name = name

    def getHand(self):
        return self.player1.hand.to_string()

    def passCards(self):
        if self.print:
            print(f"---HANDS DEALT, PASSING {['', 'RIGHT', 'ACROSS', 'LEFT'][self.passdirection]}---\n")
        p1pass = self.player1.pass_cards()
        p2pass = self.player2.pass_cards()
        p3pass = self.player3.pass_cards()
        p4pass = self.player4.pass_cards()

        self.passes = [p1pass, p2pass, p3pass, p4pass]
        for p in range(4):
            newp = (p - self.passdirection) % 4
            if self.print:
                print(f"Player {p} passed {[c.to_short_string() for c in self.passes[p]]} to Player {newp}")
        if self.print:
            print()

        if self.passdirection == -1:
            self.player1.receive_pass(p4pass)
            self.player2.receive_pass(p1pass)
            self.player3.receive_pass(p2pass)
            self.player4.receive_pass(p3pass)
        elif self.passdirection == 2:
            self.player1.receive_pass(p3pass)
            self.player2.receive_pass(p4pass)
            self.player3.receive_pass(p1pass)
            self.player4.receive_pass(p2pass)
        elif self.passdirection == 1:
            self.player1.receive_pass(p2pass)
            self.player2.receive_pass(p3pass)
            self.player3.receive_pass(p4pass)
            self.player4.receive_pass(p1pass)

        if self.print:
            print("---PASSED CARDS---\n")

    def printHand(self):
        if self.passedhanddata != []:
            for i in self.passedhanddata:
                print(i)
        else:
            for i in self.initialhanddata:
                print(i)
        print()

    def play(self):
        # ROUND 1
        has3 = [player for player in self.players if in_hand(club_3, player.hand)][0].id
        order1 = playerorder(has3)
        table1 = Table()
        it1 = 0
        orderlist = []

        while it1 < 4:
            c_player = self.players[order1[it1]]
            card = c_player.play_card(table1)
            table1.card_played(card, c_player)
            self.gamejson.append({"Player": c_player.id,
                                  "Card": card.to_short_string()})
            it1 += 1
        cardlist = []
        for card in table1.cards:
            cardlist.append(card.to_string())
        for p in self.players:
            p.update(table1)
        orderlist.append(playerorder(nextfirstplayer(table1, order1)))

        # ROUND 2-13
        for rounds in range(2, 14):
            table = Table()
            it = 0
            order = orderlist[-1]
            while it < 4:
                c_player = self.players[order[it]]
                card = c_player.play_card(table)
                table.card_played(card, c_player)
                self.gamejson.append({"Player": c_player.id, "Card": card.to_short_string()})
                it += 1
            cardlist = []
            for card in table.cards:
                cardlist.append(card.to_string())
            for p in self.players:
                p.update(table)
            orderlist.append(playerorder(nextfirstplayer(table, order)))

        self.pointdata = []
        for p in self.players:
            p.count_points()
            self.pointdata.append({"Player": p.id,
                                   "Points": p.points})

        return self.pointdata

    def pplay(self):
        # ROUND 1
        has3 = [player for player in self.players if in_hand(club_3, player.hand)][0].id
        order1 = playerorder(has3)
        table1 = Table()
        it1 = 0
        orderlist = []

        while it1 < 4:
            c_player = self.players[order1[it1]]
            card = c_player.play_card(table1)
            table1.card_played(card, c_player)
            self.gamejson.append({"Player": c_player.id,
                                  "Card": card.to_short_string()})
            it1 += 1
        cardlist = []
        for card in table1.cards:
            cardlist.append(card.to_string())
        for p in self.players:
            p.update(table1)
        print(f"Round {1} OVER:\n{', '.join(cardlist)}\n")
        orderlist.append(playerorder(nextfirstplayer(table1, order1)))

        # ROUND 2-13
        for rounds in range(2, 14):
            table = Table()
            it = 0
            order = orderlist[-1]
            while it < 4:
                c_player = self.players[order[it]]
                card = c_player.play_card(table)
                table.card_played(card, c_player)
                self.gamejson.append({"Player": c_player.id, "Card": card.to_short_string()})
                it += 1
            cardlist = []
            for card in table.cards:
                cardlist.append(card.to_string())
            for p in self.players:
                p.update(table)
            print(f"Round {rounds} OVER:\n{', '.join(cardlist)}\n")
            orderlist.append(playerorder(nextfirstplayer(table, order)))

        self.pointdata = []
        for p in self.players:
            p.count_points()
            self.pointdata.append({"Player": p.id,
                                   "Points": p.points})
        for p in self.players:
            if p.has_10:
                print(f"Player {p.id}: {p.points} points! (10 of clubs)")
            else:
                print(f"Player {p.id}: {p.points} points!")

        return self.pointdata

    def getResult(self):
        return self.gamejson

    def run(self, print_result):
        if self.print:
            g = Game.pplay(self)
            print("\nGAME OVER\n")
            for p in g:
                print(f"Player {p['Player']}: {p['Points']} points")
        else:
            g = Game.play(self)
            if print_result:
                print("\nGAME OVER\n")
                for p in g:
                    print(f"Player {p['Player']}: {p['Points']} points")


    def reset(self):
        self.deck = [Card(suit + value) for suit in "cdsh" for value in
                     [str(n) for n in range(2, 11)] + ["j", "q", "k", "a"]]
        random.shuffle(self.deck)

        self.gamejson = []

        hands = [self.deck[:13], self.deck[13:26], self.deck[26:39], self.deck[39:]]

        self.player1 = AggressivePlayer(0, 0)
        self.player2 = AggressivePlayer(1, 1)
        self.player3 = AggressivePlayer(2, 2)
        self.player4 = AggressivePlayer(3, 3)
        self.players = [self.player1, self.player2, self.player3, self.player4]

        for i in range(4):
            self.players[i].deal_hand(hands[i])

        self.handdata = [{"Player": 0, "Hand": self.player1.hand.to_string()},
                         {"Player": 1, "Hand": self.player2.hand.to_string()},
                         {"Player": 2, "Hand": self.player3.hand.to_string()},
                         {"Player": 3, "Hand": self.player4.hand.to_string()}]