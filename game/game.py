from context import Context
from players.solo_player import *

class Game:
    def __init__(self):
        self.players = [SoloPlayer(i) for i in range(4)]
        ctx = Context()
        ctx.init(self.players)
        self.ctx = ctx

    def play(self):
        first_player = [i for i in self.players if club_3 in i.hand][0].id

        orders = []

        first_order = player_order(first_player)

        for i in first_order:
            player = self.players[i]
            card = player.play(self.ctx)
            self.ctx.play(card, player)

        orders.append(player_order(self.ctx.past_states[-1].taker()))

        for i in range(12):
            for j in orders[-1]:
                player = self.players[j]
                card = player.play(self.ctx)
                self.ctx.play(card, player)
            orders.append(player_order(self.ctx.past_states[-1].taker()))

        return self.ctx.result()


if __name__ == "__main__":
    points = [[], [], [], []]
    iterations = 100

    for iteration_num in range(iterations):
        g = Game()
        results = g.play()
        for player_num in range(4):
            points[player_num].append(results[player_num])

    for (index, point_totals) in enumerate(points):
        print(f"Player {index+1}: ", sum(point_totals) / len(point_totals))