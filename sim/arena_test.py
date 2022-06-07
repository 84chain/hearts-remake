from player.players.arena.aggressive_arena_player import AggressiveArenaPlayer
from player.players.arena.random_arena_player import RandomArenaPlayer
from player.players.arena.arena_cheater import ArenaCheater
from sim.arena import Arena
from sim.hearts_game import HeartsGame
from setup.setup import risk_tolerance
import statistics
import math
import matplotlib.pyplot as plt
import csv

iterations = 1000 # minimum 1000 runs for statistical significance

def print_results(results):
    # print("Player 1 total points: ", points[0])
    # print("Player 2 total points: ", points[1])
    # print("Player 3 total points: ", points[2])
    # print("Player 4 total points: ", points[3])
    # print()
    print(f"Risk Tolerance: {risk_tolerance}")
    print("Iterations:", iterations)
    print()
    print("Player 1 average points: ", results["total_points"][0] / iterations,
          "stdev of mean: ", round(statistics.stdev(results["points"][0]) / math.sqrt(iterations), 2))
    print("Player 2 average points: ", results["total_points"][1] / iterations,
        "stdev of mean: ", round(statistics.stdev(results["points"][1]) / math.sqrt(iterations), 2))
    print("Player 3 average points: ", results["total_points"][2] / iterations,
          "stdev of mean: ", round(statistics.stdev(results["points"][2]) / math.sqrt(iterations), 2))
    print("Player 4 average points: ", results["total_points"][3] / iterations,
          "stdev of mean: ", round(statistics.stdev(results["points"][3]) / math.sqrt(iterations), 2))
    print()
    print("Average points: ", sum(results["total_points"]) / (iterations * 4),
          "avg stdev of mean: ", round(sum([statistics.stdev(results["points"][i]) for i in range(4)]) / (math.sqrt(iterations) * 4), 2))
    print("Average AI points:",sum(results["total_ai_points"]) / (iterations * len([i for i in results["ai_points"] if i])),
          "avg stdev of mean: ", round(sum([statistics.stdev(i) for i in results["ai_points"] if i]) / (math.sqrt(iterations) * 4), 2))
    print()
    print("Shoot attempts:", sum(results["shoot_attempts"]), "Successful shoots:", sum(results["successful_shoot"]))
    print("Shoot success rate:", round(sum(results["successful_shoot"]) * 100 / sum(results["shoot_attempts"])) if sum(results["shoot_attempts"]) != 0 else 0, "%")
    print("Shoot success percentage:", round(sum(results["successful_shoot"]) * 100 / iterations, 2), "%")
    print()
    print("Player 1 standings from first to last: ", [i / iterations for i in results["total_rankings"][0]])
    print("Player 2 standings                   : ", [i / iterations for i in results["total_rankings"][1]])
    print("Player 3 standings                   : ", [i / iterations for i in results["total_rankings"][2]])
    print("Player 4 standings                   : ", [i / iterations for i in results["total_rankings"][3]])
    print()

def collect_data(p1, p2, p3, p4, steps, stop, file):
    tolerances = [i / steps for i in range(int(stop * steps), steps + 1)]
    ai_ids = [p.id for p in players if p.name != "r"]
    random_ids = [p.id for p in players if p.name == "r"]

    for tolerance in tolerances:
        print(tolerance)
        p1.set_tolerance(tolerance)
        p2.set_tolerance(tolerance)
        p3.set_tolerance(tolerance)
        p4.set_tolerance(tolerance)
        a = Arena(p1, p2, p3, p4, g)
        pts, s, lstpts = a.play_games(iterations, verbose=False)
        list_points = [lstpts[i] for i in range(4) if i in random_ids]
        for player_points in list_points:
            for i in player_points:
                with open(file, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([tolerance, i])

g = HeartsGame()

p1 = AggressiveArenaPlayer(g, 0)
p2 = AggressiveArenaPlayer(g, 1)
p3 = AggressiveArenaPlayer(g, 2)
p4 = AggressiveArenaPlayer(g, 3)
players = [p1, p2, p3, p4]
a = Arena(p1, p2, p3, p4, g)
results = a.play_games(iterations, verbose=False)
print_results(results)

#collect_data(p1, p2, p3, p4, steps=500, stop=0, file='../test/1v3_p=random_it=1000_step=100.csv')