from typing import Tuple, List
import time
import heapq

from core.river_crossing import INITIAL_STATE, GOAL_STATE, is_goal, get_successors, heuristic

def solve():
    """
    Solve the Missionaries and Cannibals problem using Greedy Best-First Search.

    Returns:
        tuple: (nodes_explored, path, time_sec)
            - nodes_explored: The number of nodes explored during the search.
            - path: A list of states representing the path from INITIAL_STATE to GOAL_STATE.
            - time_sec: The execution time in seconds.
    """
    start_time = time.time()

    priority_queue = [(heuristic(INITIAL_STATE), INITIAL_STATE, [INITIAL_STATE])]
    visited = set()
    nodes_explored = 0

    while priority_queue:
        h_val, current_state, path = heapq.heappop(priority_queue)

        if current_state in visited:
            continue

        visited.add(current_state)
        nodes_explored += 1

        if is_goal(current_state):
            end_time = time.time()
            return path, nodes_explored, (end_time - start_time) * 1000

        for next_state in get_successors(current_state):
            if next_state not in visited:
                new_path = path + [next_state]
                heapq.heappush(priority_queue, (heuristic(next_state), next_state, new_path))

    end_time = time.time()
    return [], nodes_explored, (end_time - start_time) * 1000  # No solution found