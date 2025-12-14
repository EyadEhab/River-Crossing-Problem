import unittest
import time
import sys
from search.dfs import solve_dfs
from core.river_crossing import INITIAL_STATE, GOAL_STATE, is_valid_state, get_successors

class TestDFS(unittest.TestCase):
    def test_dfs_solution(self):
        path_cost, execution_time, solution_path = solve_dfs()
        print(f"\nDFS Execution Time: {execution_time:.2f} ms")
        print(f"DFS Solution Path: {solution_path}")
        
        self.assertGreater(path_cost, 0)
        self.assertGreaterEqual(execution_time, 0)
        self.assertGreater(len(solution_path), 0)
        
        # Verify the first state in the path is the initial state
        first_state, _, _ = solution_path[0]
        self.assertEqual(first_state, INITIAL_STATE)
        
        # Verify the last state in the path is the goal state
        _, _, last_state = solution_path[-1]
        self.assertEqual(last_state, GOAL_STATE)
        
        # Verify all states are valid
        for current_state, move, next_state in solution_path:
            self.assertTrue(is_valid_state(current_state))
            self.assertTrue(is_valid_state(next_state))
        
        # Verify each transition is valid (next_state is a successor of current_state)
        for current_state, move, next_state in solution_path:
            self.assertIn(next_state, get_successors(current_state))
        
        # Path cost should equal the number of moves
        self.assertEqual(path_cost, len(solution_path))

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestDFS))
    unittest.TextTestRunner(stream=sys.stdout).run(suite)