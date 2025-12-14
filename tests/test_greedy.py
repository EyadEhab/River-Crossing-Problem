import unittest
from search.greedy import solve
from core.river_crossing import INITIAL_STATE, GOAL_STATE, is_valid_state, get_successors
import time
import sys

class TestGreedy(unittest.TestCase):
    def test_greedy_solution(self):
        path, execution_time = solve()
        print(f"\nGreedy Execution Time: {execution_time:.2f} ms")
        print(f"Greedy Solution Path: {path}")
        
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], INITIAL_STATE)
        self.assertEqual(path[-1], GOAL_STATE)
        
        for state in path:
            self.assertTrue(is_valid_state(state))
        
        for i in range(len(path) - 1):
            self.assertIn(path[i + 1], get_successors(path[i]))
        
        self.assertGreaterEqual(execution_time, 0)

if __name__ == '__main__':
    start_time = time.time()
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(TestGreedy))
    unittest.TextTestRunner(stream=sys.stdout).run(suite)
    end_time = time.time()
    print(f"\nTotal execution time: {(end_time - start_time) * 1000:.2f} ms")