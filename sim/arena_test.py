from player.players.arena.aggressive_arena_player import AggressiveArenaPlayer
from player.players.arena.random_arena_player import RandomArenaPlayer
from player.players.arena.arena_cheater import ArenaCheater
from sim.arena import Arena
from sim.hearts_game import HeartsGame

iterations = 10000

def print_results(points, standings):
    # print("Player 1 total points: ", points[0])
    # print("Player 2 total points: ", points[1])
    # print("Player 3 total points: ", points[2])
    # print("Player 4 total points: ", points[3])
    # print()
    print("Player 1 average points: ", points[0] / iterations)
    print("Player 2 average points: ", points[1] / iterations)
    print("Player 3 average points: ", points[2] / iterations)
    print("Player 4 average points: ", points[3] / iterations)
    print()
    print("Player 1 standings from first to last: ", [i / iterations for i in standings[0]])
    print("Player 2 standings                   : ", [i / iterations for i in standings[1]])
    print("Player 3 standings                   : ", [i / iterations for i in standings[2]])
    print("Player 4 standings                   : ", [i / iterations for i in standings[3]])
    print()


g = HeartsGame()

p = RandomArenaPlayer(g)
p2 = RandomArenaPlayer(g)
p3 = RandomArenaPlayer(g)
p4 = AggressiveArenaPlayer(g)


a = Arena(p, p2, p3, p4, g)
p, s = a.play_games(iterations, verbose=False)
print_results(p, s)