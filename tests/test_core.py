"""
Unit tests for core/river_crossing.py
Tests only the core problem representation — no search algorithms involved.
"""

import unittest
from core.river_crossing import (
    INITIAL_STATE,
    GOAL_STATE,
    is_valid_state,
    is_goal,
    get_successors,
    heuristic
)

class TestRiverCrossingCore(unittest.TestCase):

    def test_initial_and_goal_states(self):
        self.assertEqual(INITIAL_STATE, (3, 3, 1))
        self.assertEqual(GOAL_STATE, (0, 0, 0))

    def test_valid_states(self):
        # Valid states
        self.assertTrue(is_valid_state((3, 3, 1)))  # start
        self.assertTrue(is_valid_state((0, 0, 0)))  # goal
        self.assertTrue(is_valid_state((2, 2, 0)))  # balanced on both banks
        self.assertTrue(is_valid_state((0, 3, 0)))  # no missionaries on left → safe
        self.assertTrue(is_valid_state((3, 0, 1)))  # no cannibals on left → safe

    def test_invalid_states(self):
        # Invalid: cannibals > missionaries on left
        self.assertFalse(is_valid_state((2, 3, 1)))
        # Invalid: cannibals > missionaries on right → (M_L=1, C_L=0) → right has (2M,3C)
        self.assertFalse(is_valid_state((1, 0, 0)))
        self.assertFalse(is_valid_state((2, 1, 0)))  # right: (1M, 2C) → unsafe
        # Out of bounds
        self.assertFalse(is_valid_state((4, 3, 1)))
        self.assertFalse(is_valid_state((-1, 2, 0)))

    def test_goal_check(self):
        self.assertTrue(is_goal(GOAL_STATE))
        self.assertFalse(is_goal(INITIAL_STATE))
        self.assertFalse(is_goal((1, 1, 0)))

    def test_successor_generation(self):
        successors = get_successors(INITIAL_STATE)
        expected = [
            (3, 1, 0),  # send 2 cannibals
            (2, 2, 0),  # send 1 missionary + 1 cannibal
            (1, 3, 0)   # send 2 missionaries → but (1,3,0) is invalid! → should NOT be included
        ]
        # Note: (1,3,0) is invalid → only 3 valid moves from start
        # Actual valid successors from (3,3,1):
        # - (2,2,0) → OK
        # - (3,1,0) → OK
        # - (3,2,0) → (0,1) move → but (3,2,0): left=(3M,2C) OK, right=(0M,1C) OK → valid!
        # Wait: (0,1) is a valid move → gives (3,2,0)
        # So total 3 successors

        # Let's verify exact set
        expected_set = {(3, 1, 0), (2, 2, 0), (3, 2, 0)}
        self.assertEqual(set(successors), expected_set)
        # Ensure all are valid
        for s in successors:
            self.assertTrue(is_valid_state(s))

    def test_heuristic_sanity(self):
        # Goal state → h = 0
        self.assertEqual(heuristic(GOAL_STATE), 0.0)
        # Initial state → (3+3)/2 = 3.0
        self.assertEqual(heuristic(INITIAL_STATE), 3.0)
        # Intermediate state
        self.assertEqual(heuristic((2, 2, 1)), 2.0)
        # Heuristic must be >= 0
        self.assertGreaterEqual(heuristic((1, 1, 0)), 0)

    def test_heuristic_admissibility(self):
        """
        While full admissibility requires knowing true cost,
        we at least ensure heuristic doesn't exceed a known upper bound.
        Max people = 6 → max heuristic = 3.0, which is reasonable.
        """
        for m in range(4):
            for c in range(4):
                for b in [0, 1]:
                    h_val = heuristic((m, c, b))
                    self.assertGreaterEqual(h_val, 0)
                    self.assertLessEqual(h_val, 3.0)

if __name__ == '__main__':
    unittest.main()