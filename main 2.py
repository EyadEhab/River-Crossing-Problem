"""
Interactive runner for the River Crossing Problem Solver.
Allows the user to select and run one of the five search algorithms.
"""

import sys
from typing import List, Tuple

# Import all solvers
from search.bfs import solve as bfs_solve
from search.dfs import solve as dfs_solve
from search.iddfs import solve as iddfs_solve
from search.astar import solve as astar_solve
from search.greedy import solve as greedy_solve
from core.river_crossing import GOAL_STATE, INITIAL_STATE, MOVES


def reconstruct_moves(path: List[Tuple[int, int, int]]) -> List[Tuple[int, int]]:
    """Reconstruct the move sequence (m, c) from a state path."""
    moves = []
    for i in range(len(path) - 1):
        M1, C1, B1 = path[i]
        M2, C2, B2 = path[i + 1]
        if B1 == 1:  # boat moved from left to right → subtraction
            m_move = M1 - M2
            c_move = C1 - C2
        else:  # boat moved from right to left → addition
            m_move = M2 - M1
            c_move = C2 - C1
        moves.append((m_move, c_move))
    return moves


def print_solution(path: List[Tuple[int, int, int]], g_n=None, time_sec=0.0):
    if not path:
        print("❌ No solution found.")
        return

    print(f"\n✅ Solution found! Goal state reached: {GOAL_STATE}")
    print("-" * 70)

    # Reconstruct moves
    moves = reconstruct_moves(path)

    # Print step-by-step (as in your Phase 1 doc)
    print(f"{'Step':<5} {'State (M_L, C_L, B)':<20} {'Move (M, C)':<15} {'Action'}")
    print("-" * 70)
    print(f"{0:<5} {str(INITIAL_STATE):<20} {'-':<15} Start")

    for i, (state, move) in enumerate(zip(path[1:], moves), start=1):
        M_L, C_L, B = state
        m, c = move
        direction = "→ Right" if path[i - 1][2] == 1 else "← Left"
        print(f"{i:<5} {str(state):<20} {str(move):<15} ({m}M, {c}C) {direction}")

    # Metrics
    path_length = len(path) - 1
    print("\n📊 Performance Metrics:")
    print(f"  • Path Length (moves): {path_length}")
    if g_n is not None:
        print(f"  • Nodes Explored (g(n)): {g_n}")
    else:
        print(f"  • Nodes Explored (g(n)): N/A (Greedy does not track this)")
    print(f"  • Execution Time: {time_sec * 1000:.2f} ms")


def main():
    algorithms = {
        "1": ("BFS", bfs_solve, True),
        "2": ("DFS", dfs_solve, True),
        "3": ("IDDFS", iddfs_solve, True),
        "4": ("A*", astar_solve, True),
        "5": ("Greedy", greedy_solve, False),  # No g(n)
    }

    print("🌊 River Crossing Problem Solver")
    print("Select a search algorithm to run:\n")

    for key, (name, _, _) in algorithms.items():
        print(f"  {key}. {name}")

    choice = input("\nEnter your choice (1–5): ").strip()

    if choice not in algorithms:
        print("❌ Invalid choice. Please run again and select 1–5.")
        return

    algo_name, solver, returns_gn = algorithms[choice]

    print(f"\n▶️  Running {algo_name}...\n")

    try:
        if returns_gn:
            path, g_n, time_sec = solver()
            print_solution(path, g_n, time_sec)
        else:
            path, time_sec = solver()
            print_solution(path, None, time_sec)
    except Exception as e:
        print(f"❌ Error while running {algo_name}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()