from typing import Literal


from core.river_crossing import *
from collections import deque
import time


def solve_bfs():
    """
    Solve the Missionaries and Cannibals problem using Breadth-First Search (BFS).

    Returns:
        tuple: (path_cost, execution_time, solution_path)
            - path_cost: number of moves in the solution (g(n))
            - execution_time: wall-clock time in seconds
            - solution_path: list of tuples [(current_state, move, next_state), ...]
    """
    start_time = time.time()

    # BFS setup
    queue = deque[tuple[Literal[0, 1, 2, 3], Literal[0, 1, 2, 3], Literal[0, 1]]]([INITIAL_STATE])
    visited = set[tuple[Literal[0, 1, 2, 3], Literal[0, 1, 2, 3], Literal[0, 1]]]([INITIAL_STATE])
    parent = {INITIAL_STATE: None}  # parent[state] = (prev_state, move_taken)

    found = False
    goal_state = None

    while queue:
        current_state = queue.popleft()

        if is_goal(current_state):
            found = True
            goal_state = current_state
            break

        for next_state in get_successors(current_state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
                # Calculate the move that led to next_state
                move = _calculate_move(current_state, next_state)
                parent[next_state] = (current_state, move)

    execution_time = (time.time() - start_time) * 1000 # Convert to milliseconds

    if not found:
        return 0, execution_time, []

    # Reconstruct the solution path
    solution_path = _reconstruct_path(parent, goal_state)
    path_cost = len(solution_path)

    return path_cost, execution_time, solution_path


def _calculate_move(from_state, to_state):
    """
    Calculate the move (missionaries, cannibals) that transitions from_state to to_state.

    Returns:
        tuple: (missionaries_moved, cannibals_moved)
    """
    M_L_from, C_L_from, boat_from = from_state
    M_L_to, C_L_to, boat_to = to_state

    if boat_from == 1 and boat_to == 0:  # Boat moving from left to right
        # Missionaries/cannibals moved from left to right
        m_moved = M_L_from - M_L_to
        c_moved = C_L_from - C_L_to
    elif boat_from == 0 and boat_to == 1:  # Boat moving from right to left
        # Missionaries/cannibals moved from right to left
        m_moved = M_L_to - M_L_from
        c_moved = C_L_to - C_L_from
    else:
        raise ValueError(f"Invalid state transition: {from_state} -> {to_state}")

    return (m_moved, c_moved)


def _reconstruct_path(parent, goal_state):
    """
    Reconstruct the solution path from INITIAL_STATE to goal_state using the parent mapping.

    Returns:
        list: [(current_state, move, next_state), ...]
    """
    path = []
    current = goal_state

    while parent[current] is not None:
        prev_state, move = parent[current]
        path.append((prev_state, move, current))
        current = prev_state

    # Reverse to get path from start to goal
    path.reverse()
    return path
