"""
benchmark.py - Standalone performance benchmark for the PetWars pathfinding
algorithms (Dijkstra, A*, Bellman-Ford).

This script does NOT modify any game file. It imports the real pathfinding
functions and the real map, initialises pygame to reproduce the in-game
runtime environment, and measures - for each route and each algorithm -
the same operation the game performs on a mouse click:

    t0 = time.perf_counter()
    path = <algorithm>_path(start, goal, terrain_map)
    elapsed_ms = (time.perf_counter() - t0) * 1000

Each route/algorithm is timed REPS times. Two files are written next to
this script:
  * benchmark_runs.csv     - EVERY individual run (full raw record)
  * benchmark_results.csv  - aggregated mean / median / min per config
Visited-vertex count comes from the *_visual generator (same metric the
game shows); path steps and path cost come from the returned path.

Usage:
    python benchmark.py
To run without a game window: set SDL_VIDEODRIVER=dummy before launching.
"""

import os
import csv
import time
import statistics

import pygame

from constants import terrain_map, MAP_WIDTH, MAP_HEIGHT, TILE_SIZE
from pathfinding import (
    dijkstra_path, astar_path, bellman_ford_path,
    dijkstra_visual, astar_visual, bellman_ford_visual,
)

# ---------------------------------------------------------------- configuration
REPS = 30  # repetitions per route/algorithm

# (label, start, goal) - edit freely; coordinates are (x, y) walkable cells.
ROUTES = [
    ("Short distance",  (1, 8),  (3, 3)),    # from hero start, short
    ("Medium distance", (1, 8),  (10, 2)),   # from hero start, medium
    ("Long distance",   (1, 8),  (13, 4)),   # from hero start, long
    ("Random 1",        (10, 9), (3, 3)),    # additional route
    ("Random 2",        (13, 5), (0, 2)),    # additional route
]

ALGORITHMS = [
    ("Dijkstra",     dijkstra_path,     dijkstra_visual),
    ("A*",           astar_path,        astar_visual),
    ("Bellman-Ford", bellman_ford_path, bellman_ford_visual),
]


def path_cost(path):
    cost = 0
    for (x1, y1), (x2, y2) in zip(path, path[1:]):
        cost += 3 if (x1 != x2 and y1 != y2) else 2
    return cost


def visited_count(visual_fn, start, goal):
    visited = 0
    for state in visual_fn(start, goal, terrain_map):
        if state.get("visited") is not None:
            visited = len(state["visited"])
        if state.get("done"):
            break
    return visited


def init_pygame_environment():
    pygame.init()
    try:
        pygame.display.set_mode((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))
    except pygame.error:
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.display.init()
        pygame.display.set_mode((1, 1))


def main():
    init_pygame_environment()

    raw_rows = []      # every individual run
    summary_rows = []  # aggregated

    print(f"PetWars pathfinding benchmark - {REPS} repetitions per route/algorithm\n")
    header = (f"{'Scenario':<17}{'Algorithm':<14}{'mean(ms)':>10}{'std(ms)':>9}"
              f"{'min(ms)':>9}{'visited':>9}{'steps':>7}{'cost':>6}")
    print(header)
    print("-" * len(header))

    for rlabel, start, goal in ROUTES:
        sg = f"{start}->{goal}"
        for albl, path_fn, visual_fn in ALGORITHMS:
            path_fn(start, goal, terrain_map)  # warm-up
            times_ms = []
            path = None
            for i in range(REPS):
                t0 = time.perf_counter()
                path = path_fn(start, goal, terrain_map)
                t1 = time.perf_counter()
                times_ms.append((t1 - t0) * 1000.0)

            visited = visited_count(visual_fn, start, goal)
            steps = len(path) if path else 0
            cost = path_cost(path) if path else 0

            # raw: one row per run
            for i, t in enumerate(times_ms, start=1):
                raw_rows.append([rlabel, sg, albl, i, f"{t:.6f}", visited, steps, cost])

            mean_ms = statistics.mean(times_ms)
            std_ms = statistics.stdev(times_ms)
            median_ms = statistics.median(times_ms)
            min_ms = min(times_ms)
            summary_rows.append([rlabel, sg, albl,
                                 f"{mean_ms:.4f}", f"{std_ms:.4f}",
                                 f"{median_ms:.4f}", f"{min_ms:.4f}",
                                 visited, steps, cost])
            print(f"{rlabel:<17}{albl:<14}{mean_ms:>10.4f}{std_ms:>9.4f}"
                  f"{min_ms:>9.4f}{visited:>9}{steps:>7}{cost:>6}")

    here = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(here, "benchmark_runs.csv")
    with open(raw_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scenario", "start_goal", "algorithm", "run", "time_ms",
                    "visited", "path_steps", "path_cost"])
        w.writerows(raw_rows)

    sum_path = os.path.join(here, "benchmark_results.csv")
    with open(sum_path, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scenario", "start_goal", "algorithm",
                    "mean_ms", "std_ms", "median_ms", "min_ms",
                    "visited", "path_steps", "path_cost"])
        w.writerows(summary_rows)

    print(f"\nRaw runs written to:  {raw_path}  ({len(raw_rows)} rows)")
    print(f"Summary written to:   {sum_path}")
    pygame.quit()


if __name__ == "__main__":
    main()
