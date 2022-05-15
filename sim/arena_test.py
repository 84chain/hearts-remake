from player.players.arena.aggressive_arena_player import AggressiveArenaPlayer
from player.players.arena.random_arena_player import RandomArenaPlayer
from player.players.arena.arena_cheater import ArenaCheater
from sim.arena import Arena
from sim.hearts_game import HeartsGame
import statistics
import math

iterations = 1000

def print_results(points, standings, list_points):
    # print("Player 1 total points: ", points[0])
    # print("Player 2 total points: ", points[1])
    # print("Player 3 total points: ", points[2])
    # print("Player 4 total points: ", points[3])
    # print()
    print("Player 1 average points: ", points[0] / iterations,
          "stdev of mean: ", round(statistics.stdev(list_points[0]) / math.sqrt(iterations), 2))
    print("Player 2 average points: ", points[1] / iterations,
        "stdev of mean: ", round(statistics.stdev(list_points[1]) / math.sqrt(iterations), 2))
    print("Player 3 average points: ", points[2] / iterations,
          "stdev of mean: ", round(statistics.stdev(list_points[2]) / math.sqrt(iterations), 2))
    print("Player 4 average points: ", points[3] / iterations,
          "stdev of mean: ", round(statistics.stdev(list_points[3]) / math.sqrt(iterations), 2))
    print()
    print("Player 1 standings from first to last: ", [i / iterations for i in standings[0]])
    print("Player 2 standings                   : ", [i / iterations for i in standings[1]])
    print("Player 3 standings                   : ", [i / iterations for i in standings[2]])
    print("Player 4 standings                   : ", [i / iterations for i in standings[3]])
    print()


g = HeartsGame()

p = AggressiveArenaPlayer(g)
p2 = AggressiveArenaPlayer(g)
p3 = AggressiveArenaPlayer(g)
p4 = RandomArenaPlayer(g)

a = Arena(p, p2, p3, p4, g)
p, s, pt = a.play_games(iterations, verbose=False)
print_results(p, s, pt)