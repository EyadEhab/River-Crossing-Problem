import unittest
import time
import sys
from search.bfs import solve_bfs
from core.river_crossing import INITIAL_STATE, GOAL_STATE, is_valid_state, get_successors

class TestBFS(unittest.TestCase):
    def test_bfs_solution(self):
        path_cost, execution_time, solution_path = solve_bfs()
        print(f"\nBFS Execution Time: {execution_time:.2f} ms")
        print(f"BFS Solution Path: {solution_path}")

        # Non-empty solution path
        self.assertGreater(len(solution_path), 0)

        # Extract states from solution path for validation
        path = [INITIAL_STATE] + [next_state for _, _, next_state in solution_path]

        # Starts and ends correctly
        self.assertEqual(path[0], INITIAL_STATE)
        self.assertEqual(path[-1], GOAL_STATE)

        # All states in path are valid
        for state in path:
            self.assertTrue(is_valid_state(state))

        # Each transition is a valid move
        for i in range(len(path) - 1):
            successors = get_successors(path[i])
            self.assertIn(path[i + 1], successors)

        # Path cost matches solution path length
        self.assertEqual(path_cost, len(solution_path))

        # Execution time is reasonable
        self.assertGreaterEqual(execution_time, 0)

        # Solution path format validation
        for current_state, move, next_state in solution_path:
            self.assertIsInstance(move, tuple)
            self.assertEqual(len(move), 2)
            self.assertIsInstance(current_state, tuple)
            self.assertEqual(len(current_state), 3)
            self.assertIsInstance(next_state, tuple)
            self.assertEqual(len(next_state), 3)

if __name__ == '__main__':
    start_time = time.time()
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestBFS))
    unittest.TextTestRunner(stream=sys.stdout).run(suite)
    end_time = time.time()
    print(f"\nTotal execution time: {(end_time - start_time) * 1000:.2f} ms")