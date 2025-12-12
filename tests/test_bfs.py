import unittest
from search.bfs import solve
from core.river_crossing import INITIAL_STATE, GOAL_STATE, is_valid_state, get_successors

class TestBFS(unittest.TestCase):
    def test_bfs_solution(self):
        path, nodes_explored, time_ms = solve()
        
        # Non-empty path
        self.assertGreater(len(path), 0)
        
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
        
        # Metrics are reasonable
        self.assertGreater(nodes_explored, 0)
        self.assertGreaterEqual(time_ms, 0)

if __name__ == '__main__':
    unittest.main()