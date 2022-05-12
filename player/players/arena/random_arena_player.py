import random
from player.templates.arena_player import ArenaPlayer

class RandomArenaPlayer(ArenaPlayer):
    def __init__(self, game):
        self.game = game
        ArenaPlayer.__init__(self, game)

    def play(self, state):
        legal_moves = self.game.get_valid_moves(state)
        valid_moves = []
        for i in range(52):
            if legal_moves[i] == 1:
                valid_moves.append(i)
        return random.choice(valid_moves)

    def update(self, state):
        pass