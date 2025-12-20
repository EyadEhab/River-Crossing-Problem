from core.river_crossing import *
from collections import deque
import time


def solve():
    start_time = time.time()

    states_to_explore = deque([INITIAL_STATE])

    explored_states = set([INITIAL_STATE])

    came_from = {INITIAL_STATE: None}

    nodes_explored = 0

    goal_found = None

    while states_to_explore:
        current_state = states_to_explore.popleft()
        nodes_explored += 1

        if is_goal(current_state):
            goal_found = current_state
            break

        for next_state in get_successors(current_state):
            if next_state not in explored_states:
                explored_states.add(next_state)
                states_to_explore.append(next_state)

                move_taken = _calculate_move(current_state, next_state)
                came_from[next_state] = (current_state, move_taken)

    execution_time = (time.time() - start_time) * 1000

    if goal_found is None:
        return [], nodes_explored, execution_time

    solution_path = _reconstruct_path(came_from, goal_found)

    return solution_path, nodes_explored, execution_time


def _calculate_move(start_state, end_state):
    missionaries_start, cannibals_start, boat_start = start_state
    missionaries_end, cannibals_end, boat_end = end_state

    if boat_start == 1 and boat_end == 0:
        missionaries_moved = missionaries_start - missionaries_end
        cannibals_moved = cannibals_start - cannibals_end

    elif boat_start == 0 and boat_end == 1:
        missionaries_moved = missionaries_end - missionaries_start
        cannibals_moved = cannibals_end - cannibals_start

    else:
        raise ValueError(f"Invalid boat movement: {start_state} -> {end_state}")

    return (missionaries_moved, cannibals_moved)


def _reconstruct_path(came_from, goal_state):
    path = [goal_state]
    current_state = goal_state

    while came_from[current_state] is not None:
        previous_state, move_taken = came_from[current_state]
        path.append(previous_state)
        current_state = previous_state

    path.reverse()
    return path
