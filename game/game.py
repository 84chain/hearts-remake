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
            for i in orders[-1]:
                player = self.players[i]
                card = player.play(self.ctx)
                self.ctx.play(card, player)
            orders.append(player_order(self.ctx.past_states[-1].taker()))

        print(self.ctx.result())


if __name__ == "__main__":
    g = Game()
    g.play()
