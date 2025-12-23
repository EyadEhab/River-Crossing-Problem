# core/river_crossing.py

from typing import Tuple, List

# ----------------------------
# GLOBAL CONSTANTS
# ----------------------------

# Initial and goal states
INITIAL_STATE = (3, 3, 1)   # (M_left, C_left, Boat_position) — 1 = left, 0 = right
GOAL_STATE = (0, 0, 0)

# All possible moves (missionaries, cannibals) that the boat can carry
MOVES = [
    (1, 0),  # 1 missionary
    (2, 0),  # 2 missionaries
    (0, 1),  # 1 cannibal
    (0, 2),  # 2 cannibals
    (1, 1),  # 1 missionary + 1 cannibal
]

# Boat capacity (for future extensibility)
BOAT_CAPACITY = 2

# ----------------------------
# STATE VALIDITY CHECK
# ----------------------------

def is_valid_state(state: Tuple[int, int, int]) -> bool:
    """
    Check if a state is safe (no missionaries eaten).
    A state (M_L, C_L, B) is valid if:
      - On left bank: M_L == 0 or M_L >= C_L
      - On right bank: (3 - M_L) == 0 or (3 - M_L) >= (3 - C_L)
    """
    M_L, C_L, _ = state

    # Left bank check
    if M_L < 0 or C_L < 0 or M_L > 3 or C_L > 3:
        return False

    if M_L > 0 and C_L > M_L:
        return False

    # Right bank
    M_R = 3 - M_L
    C_R = 3 - C_L
    if M_R > 0 and C_R > M_R:
        return False

    return True

# ----------------------------
# GOAL TEST
# ----------------------------

def is_goal(state: Tuple[int, int, int]) -> bool:
    return state == GOAL_STATE

# ----------------------------
# GENERATE SUCCESSOR STATES
# ----------------------------

def get_successors(state: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    """
    Generate all valid successor states from the current state.
    """
    M_L, C_L, boat = state
    successors = []

    for m_move, c_move in MOVES:
        if boat == 1:  # Boat on left → moving to right
            new_M_L = M_L - m_move
            new_C_L = C_L - c_move
            new_boat = 0
        else:  # Boat on right → moving to left
            new_M_L = M_L + m_move
            new_C_L = C_L + c_move
            new_boat = 1

        new_state = (new_M_L, new_C_L, new_boat)

        if is_valid_state(new_state):
            successors.append(new_state)

    return successors

# ----------------------------
# HEURISTIC FUNCTION (for A* and Greedy)
# ----------------------------

def heuristic(state: Tuple[int, int, int]) -> float:
    """
    Admissible heuristic: minimum number of one-way trips needed.
    h(s) = ceil((M_L + C_L) / 2) — but float division is fine for comparison.
    Using ceiling ensures admissibility, but for simplicity, we can use:
    """
    M_L, C_L, _ = state
    return (M_L + C_L) / 2.0  # Still admissible because real trips >= this value

print(get_successors((1,1,0)))
