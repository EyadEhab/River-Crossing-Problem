import unittest
from search.greedy import solve
from core.river_crossing import INITIAL_STATE, GOAL_STATE, is_valid_state, get_successors

class TestGreedy(unittest.TestCase):
    def test_greedy_solution(self):
        path, time_sec = solve()
        
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], INITIAL_STATE)
        self.assertEqual(path[-1], GOAL_STATE)
        
        for state in path:
            self.assertTrue(is_valid_state(state))
        
        for i in range(len(path) - 1):
            self.assertIn(path[i + 1], get_successors(path[i]))
        
        self.assertGreaterEqual(time_sec, 0)

if __name__ == '__main__':
    unittest.main()