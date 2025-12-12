import unittest
from search.astar import solve
from core.river_crossing import INITIAL_STATE, GOAL_STATE, is_valid_state, get_successors

class TestAStar(unittest.TestCase):
    def test_astar_solution(self):
        path, nodes_explored, time_ms = solve()
        
        self.assertGreater(len(path), 0)
        self.assertEqual(path[0], INITIAL_STATE)
        self.assertEqual(path[-1], GOAL_STATE)
        
        for state in path:
            self.assertTrue(is_valid_state(state))
        
        for i in range(len(path) - 1):
            self.assertIn(path[i + 1], get_successors(path[i]))
        
        self.assertGreater(nodes_explored, 0)
        self.assertGreaterEqual(time_ms, 0)

if __name__ == '__main__':
    unittest.main()