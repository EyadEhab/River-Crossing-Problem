"""
Main runner for the River Crossing Problem Solver.
Executes all five search algorithms and displays a comparative summary.
"""

from search.bfs import solve as bfs_solve
from search.dfs import solve as dfs_solve
from search.iddfs import solve as iddfs_solve
from search.astar import solve as astar_solve
from search.greedy import solve as greedy_solve

from core.river_crossing import GOAL_STATE


def print_solution_summary(algo_name: str, path, g_n=None, time_sec=0.0):
    path_length = len(path) - 1  # number of moves
    if g_n is None:
        # For Greedy: we don't have g(n); use path length as proxy for cost
        print(f"{algo_name:<18} | {path_length:<12} | {'N/A':<15} | {time_sec * 1000:<10.2f}")
    else:
        # For others: g_n is interpreted as "nodes explored" or "path cost"
        print(f"{algo_name:<18} | {path_length:<12} | {g_n:<15} | {time_sec * 1000:<10.2f}")


def main():
    print("Running all search algorithms for the Missionaries and Cannibals problem...\n")

    # Run each solver
    bfs_path, bfs_g, bfs_time = bfs_solve()
    dfs_path, dfs_g, dfs_time = dfs_solve()
    iddfs_path, iddfs_g, iddfs_time = iddfs_solve()
    astar_path, astar_g, astar_time = astar_solve()
    greedy_path, greedy_time = greedy_solve()  # Greedy does NOT return g(n)

    # Validate all found the goal
    all_paths = [bfs_path, dfs_path, iddfs_path, astar_path, greedy_path]
    for i, path in enumerate(all_paths):
        if not path or path[-1] != GOAL_STATE:
            algo_names = ["BFS", "DFS", "IDDFS", "A*", "Greedy"]
            print(f"⚠️  Warning: {algo_names[i]} did not reach the goal state!")

    # Print results table
    print(f"{'Algorithm':<18} | {'Path Length':<12} | {'Nodes Explored':<15} | {'Time (ms)':<10}")
    print("-" * 70)
    print_solution_summary("BFS", bfs_path, bfs_g, bfs_time)
    print_solution_summary("DFS", dfs_path, dfs_g, dfs_time)
    print_solution_summary("IDDFS", iddfs_path, iddfs_g, iddfs_time)
    print_solution_summary("A*", astar_path, astar_g, astar_time)
    print_solution_summary("Greedy", greedy_path, None, greedy_time)

    print("\n✅ All algorithms executed.")


if __name__ == "__main__":
    main()