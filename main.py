"""
Main runner for the River Crossing Problem Solver.
Executes all five search algorithms and displays a comparative summary.
"""

from search.bfs import solve as bfs_solve
from search.dfs import solve as dfs_solve
from search.astar import solve as astar_solve
from search.greedy import solve as greedy_solve

from core.river_crossing import GOAL_STATE


def print_solution_summary(algo_name: str, path, nodes_explored=0, time_sec=0.0):
    path_length = len(path) - 1  # number of moves
    print(f"{algo_name:<18} | {path_length:<12} | {nodes_explored:<15} | {time_sec * 1000:<10.2f}")


def main():
    print("Running all search algorithms for the Missionaries and Cannibals problem...\n")

    # Run each solver
    bfs_path, bfs_nodes, bfs_time = bfs_solve()
    dfs_path, dfs_nodes, dfs_time = dfs_solve()
    astar_path, astar_nodes, astar_time = astar_solve()
    greedy_path, greedy_nodes, greedy_time = greedy_solve()

    # Validate all found the goal
    all_paths = [bfs_path, dfs_path, astar_path, greedy_path]
    for i, path in enumerate(all_paths):
        final_state = None
        if path:
            final_state = path[-1]

        if not path or final_state != GOAL_STATE:
            algo_names = ["BFS", "DFS", "A*", "Greedy"]
            print(f"⚠️  Warning: {algo_names[i]} did not reach the goal state!")

    # Print results table
    print(f"{'Algorithm':<18} | {'Path Length':<12} | {'Nodes Explored':<15} | {'Time (ms)':<10}")
    print("-" * 70)
    print_solution_summary("BFS", bfs_path, bfs_nodes, bfs_time)
    print_solution_summary("DFS", dfs_path, dfs_nodes, dfs_time)
    print_solution_summary("A*", astar_path, astar_nodes, astar_time)
    print_solution_summary("Greedy", greedy_path, greedy_nodes, greedy_time)

    print("\n✅ All algorithms executed.")


if __name__ == "__main__":
    main()