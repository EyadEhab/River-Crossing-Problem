"""
Constraint Satisfaction Problem (CSP) solver for the River Crossing Problem.

CSP Formulation:
- Variables: Each step i in the solution path represents a state
- Domain: For each state, the domain is all valid successor states
- Constraints: 
  1. State validity (no missionaries eaten)
  2. No cycles (no repeated states in the path)
  
Uses backtracking with forward checking to find a solution.
"""

from core.river_crossing import *
import time
from typing import List, Set, Tuple, Optional


def solve():
    """
    Solve the Missionaries and Cannibals problem using CSP with backtracking.
    
    Returns:
        tuple: (solution_path, nodes_explored, execution_time)
            - solution_path: list of states from initial to goal
            - nodes_explored: number of state assignments attempted
            - execution_time: wall-clock time in milliseconds
    """
    start_time = time.time()
    
    # Track visited states to avoid cycles (constraint)
    visited = set([INITIAL_STATE])
    
    # Track nodes explored (each assignment attempt)
    nodes_explored = [0]  # Using list to allow modification in nested function
    
    # Start backtracking search from initial state
    solution_path = _backtrack(INITIAL_STATE, visited, nodes_explored)
    
    execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    
    if solution_path is None:
        return [], nodes_explored[0], execution_time
    
    return solution_path, nodes_explored[0], execution_time


def _backtrack(current_state: Tuple[int, int, int], 
               visited: Set[Tuple[int, int, int]], 
               nodes_explored: List[int]) -> Optional[List[Tuple[int, int, int]]]:
    """
    Recursive backtracking function to find a solution.
    
    Args:
        current_state: Current state in the search
        visited: Set of visited states (to avoid cycles)
        nodes_explored: Counter for nodes explored (mutable list with single int)
    
    Returns:
        List of states from current_state to goal, or None if no solution
    """
    # Increment node counter
    nodes_explored[0] += 1
    
    # Goal test
    if is_goal(current_state):
        return [current_state]
    
    M_L, C_L, boat = current_state
    
    # Generate all valid successors manually (domain for this variable)
    # Instead of using get_successors, we iterate through MOVES directly
    for m_move, c_move in MOVES:
        # Calculate new state based on boat position
        if boat == 1:  # Boat on left → moving to right
            new_M_L = M_L - m_move
            new_C_L = C_L - c_move
            new_boat = 0
        else:  # Boat on right → moving to left
            new_M_L = M_L + m_move
            new_C_L = C_L + c_move
            new_boat = 1
        
        next_state = (new_M_L, new_C_L, new_boat)
        
        # Check if state is valid and not visited (constraints)
        if is_valid_state(next_state) and next_state not in visited:
            # Make assignment
            visited.add(next_state)
            
            # Recursively solve from next_state
            result = _backtrack(next_state, visited, nodes_explored)
            
            # If solution found, build path
            if result is not None:
                return [current_state] + result
            
            # Backtrack: undo assignment
            visited.remove(next_state)
    
    # No solution found from this state
    return None


def _calculate_move(from_state: Tuple[int, int, int], 
                   to_state: Tuple[int, int, int]) -> Tuple[int, int]:
    """
    Calculate the move (missionaries, cannibals) that transitions from_state to to_state.
    
    Args:
        from_state: Starting state
        to_state: Ending state
    
    Returns:
        tuple: (missionaries_moved, cannibals_moved)
    """
    M_L_from, C_L_from, boat_from = from_state
    M_L_to, C_L_to, boat_to = to_state
    
    if boat_from == 1 and boat_to == 0:  # Boat moving from left to right
        m_moved = M_L_from - M_L_to
        c_moved = C_L_from - C_L_to
    elif boat_from == 0 and boat_to == 1:  # Boat moving from right to left
        m_moved = M_L_to - M_L_from
        c_moved = C_L_to - C_L_from
    else:
        raise ValueError(f"Invalid state transition: {from_state} -> {to_state}")
    
    return (m_moved, c_moved)
