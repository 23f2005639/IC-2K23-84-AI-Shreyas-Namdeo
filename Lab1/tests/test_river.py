import unittest

from Lab1.Experiment2 import solve


class RiverTests(unittest.TestCase):
    def test_classic_shortest_safe_path(self):
        path = solve(3, 3, 2)
        self.assertEqual(len(path) - 1, 11)
        self.assertEqual(path[0][0], (3, 3, True))
        self.assertEqual(path[-1][0], (0, 0, False))
        for (m, c, _), _ in path:
            self.assertTrue(0 <= m <= 3 and 0 <= c <= 3)
            self.assertTrue(m == 0 or m >= c)
            self.assertTrue(3 - m == 0 or 3 - m >= 3 - c)
        for (previous, _), (current, load) in zip(path, path[1:]):
            self.assertNotEqual(previous[2], current[2])
            self.assertTrue(1 <= sum(load) <= 2)
            direction = -1 if previous[2] else 1
            self.assertEqual(current[:2], tuple(previous[i] + direction * load[i] for i in range(2)))

    def test_variants_and_impossible(self):
        self.assertIsNone(solve(3, 3, 1))
        self.assertEqual(len(solve(1, 1, 2)) - 1, 1)
        self.assertEqual(len(solve(0, 2, 2)) - 1, 1)

    def test_invalid_inputs(self):
        for args in [(-1, 3, 2), (0, 0, 2), (3, 3, 0), (2, 3, 2)]:
            with self.assertRaises(ValueError):
                solve(*args)
