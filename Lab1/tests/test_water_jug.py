import unittest

from Lab1.Experiment1 import solve


class WaterJugTests(unittest.TestCase):
    def test_shortest_path_and_legal_moves(self):
        path = solve(4, 3, 2)
        self.assertEqual(len(path) - 1, 4)
        self.assertEqual(path[0][0], (0, 0))
        self.assertIn(2, path[-1][0])
        for ((a, b), _), (next_state, _) in zip(path, path[1:]):
            self.assertTrue(0 <= next_state[0] <= 4)
            self.assertTrue(0 <= next_state[1] <= 3)
            to_b, to_a = min(a, 3 - b), min(b, 4 - a)
            self.assertIn(next_state, [(4, b), (a, 3), (0, b), (a, 0),
                                       (a - to_b, b + to_b), (a + to_a, b - to_a)])

    def test_zero_and_impossible(self):
        self.assertEqual(solve(4, 3, 0), [((0, 0), "Start")])
        self.assertIsNone(solve(4, 2, 3))
        self.assertIsNone(solve(4, 3, 5))

    def test_invalid_inputs(self):
        for args in [(0, 3, 2), (4, -1, 2), (4, 3, -1)]:
            with self.assertRaises(ValueError):
                solve(*args)
