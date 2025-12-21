from core.river_crossing import *
import time


def solve():
    start_time = time.time()

    states_to_explore = [INITIAL_STATE]

    explored_states = set([INITIAL_STATE])

    came_from = {INITIAL_STATE: None}

    nodes_explored = 0

    goal_found = None

    while states_to_explore:
        current_state = states_to_explore.pop()
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
        list: [state1, state2, ...]
    """
    path = [goal_state]
    current = goal_state

    while parent[current] is not None:
        prev_state, move = parent[current]
        path.append(prev_state)
        current = prev_state

    # Reverse to get path from start to goal
    path.reverse()
    return path