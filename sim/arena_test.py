import csv
import math
import statistics
from multiprocessing import Pool

from player.players.arena.aggressive_arena_player import AggressiveArenaPlayer
from player.players.arena.random_arena_player import RandomArenaPlayer
from setup.setup import *
from setup.controls import *
from sim.arena import Arena
from sim.hearts_game import HeartsGame

iterations = 1000  # minimum 1000 runs for statistical significance
threads = 5 # best performance

def play_threaded_games(players, num, thread_num):
    """
    Plays num games, but in thread_num threads
    Returns:
        list of total points collected
        dict of placings
    """
    results = []
    map_inputs = [int(num / thread_num) for _ in range(thread_num)]
    if __name__ == '__main__':
        with Pool(processes=thread_num) as pool:
            a = Arena(players[0], players[1], players[2], players[3], HeartsGame())
            result = pool.imap(a.play_games, map_inputs)
            for i in result:
                results.append(i)
        pool.close()
    return results


def print_results(results):
    """
    Prints results of game, organized
    :param results: dict()
    :return: None
    """
    # print("Player 1 total points: ", points[0])
    # print("Player 2 total points: ", points[1])
    # print("Player 3 total points: ", points[2])
    # print("Player 4 total points: ", points[3])
    # print()
    try:
        if __name__ == "__main__":
            print(f"Risk Tolerance: {risk_tolerance}")
            print("Iterations:", iterations)
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
              "avg stdev of mean: ",
              round(sum([statistics.stdev(results["points"][i]) for i in range(4)]) / (math.sqrt(iterations) * 4), 2))
        print("Average AI points:",
              sum(results["total_ai_points"]) * threads / (iterations * len([i for i in results["ai_points"] if i != []])),
              "avg stdev of mean: ",
              round(sum([statistics.stdev(i) for i in results["ai_points"] if i != []]) / (math.sqrt(iterations) * len(ai_players) * threads), 2))
        print()
        print("Shoot attempts:", sum(results["shoot_attempts"]), "Successful shoots:", sum(results["successful_shoot"]))
        print("Shoot success rate:", round(sum(results["successful_shoot"]) * 100 / sum(results["shoot_attempts"])) if sum(
            results["shoot_attempts"]) != 0 else 0, "%")
        print("Shoot success percentage:", round(sum(results["successful_shoot"]) * 100 / iterations, 2), "%")
        print()
        print("Player 1 standings from first to last: ", [i / iterations for i in results["total_rankings"][0]])
        print("Player 2 standings                   : ", [i / iterations for i in results["total_rankings"][1]])
        print("Player 3 standings                   : ", [i / iterations for i in results["total_rankings"][2]])
        print("Player 4 standings                   : ", [i / iterations for i in results["total_rankings"][3]])
        print()
    except:
        pass


def merge_results(results):
    """
    Merges list of threaded results to be processed by print_results
    :param results: list(dict)
    :return: dict
    """
    result_total_points = [i["total_points"] for i in results]
    result_total_ai_points = [i["total_ai_points"] for i in results]
    result_total_rankings = [i["total_rankings"] for i in results]
    result_points = [i["points"] for i in results]
    result_ai_points = [i["ai_points"] for i in results]
    result_shoot_attempts = [i["shoot_attempts"] for i in results]
    result_successful_shoot = [i["successful_shoot"] for i in results]

    total_points = [
        sum([i[0] for i in result_total_points]),
        sum([i[1] for i in result_total_points]),
        sum([i[2] for i in result_total_points]),
        sum([i[3] for i in result_total_points])
    ]

    total_ai_points = [
        sum([i[0] for i in result_total_ai_points]),
        sum([i[1] for i in result_total_ai_points]),
        sum([i[2] for i in result_total_ai_points]),
        sum([i[3] for i in result_total_ai_points])
    ]


    rankings_0, rankings_1, rankings_2, rankings_3 = [
        i[0] for i in result_total_rankings], [
        i[1] for i in result_total_rankings], [
        i[2] for i in result_total_rankings], [
        i[3] for i in result_total_rankings]

    total_rankings = [
        [sum([i[0] for i in rankings_0]),
         sum([i[1] for i in rankings_0]),
         sum([i[2] for i in rankings_0]),
         sum([i[3] for i in rankings_0])],

        [sum([i[0] for i in rankings_1]),
         sum([i[1] for i in rankings_1]),
         sum([i[2] for i in rankings_1]),
         sum([i[3] for i in rankings_1])],

        [sum([i[0] for i in rankings_2]),
         sum([i[1] for i in rankings_2]),
         sum([i[2] for i in rankings_2]),
         sum([i[3] for i in rankings_2])],

        [sum([i[0] for i in rankings_3]),
         sum([i[1] for i in rankings_3]),
         sum([i[2] for i in rankings_3]),
         sum([i[3] for i in rankings_3])],
    ]
    points = [i for k in result_points for i in k]
    ai_points = [i for k in result_ai_points for i in k]
    shoot_attempts = [i for k in result_shoot_attempts for i in k]
    successful_shoot = [i for k in result_successful_shoot for i in k]

    return {
        "total_points": total_points,
        "total_ai_points": total_ai_points,
        "total_rankings": total_rankings,
        "points": points,
        "ai_points": ai_points,
        "shoot_attempts": shoot_attempts,
        "successful_shoot": successful_shoot
    }


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
ai_players = [i for i in players if i.name == "a"]
a = Arena(p1, p2, p3, p4, g)

results = play_threaded_games(players, iterations, thread_num=threads)
# results = a.play_games(iterations)
print_results(merge_results(results))


# collect_data(p1, p2, p3, p4, steps=500, stop=0, file='../test/1v3_p=random_it=1000_step=100.csv')