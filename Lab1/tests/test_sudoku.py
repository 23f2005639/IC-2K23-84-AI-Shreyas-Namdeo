import unittest

from Lab1.Experiment3 import solve


PUZZLE = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


class SudokuTests(unittest.TestCase):
    def test_solution_preserves_clues_and_rules(self):
        original = [row[:] for row in PUZZLE]
        answer = solve(PUZZLE)
        digits = set(range(1, 10))
        self.assertIsNotNone(answer)
        self.assertEqual(PUZZLE, original)
        for row in range(9):
            self.assertEqual(set(answer[row]), digits)
            self.assertEqual({answer[r][row] for r in range(9)}, digits)
            for col in range(9):
                if PUZZLE[row][col]:
                    self.assertEqual(answer[row][col], PUZZLE[row][col])
        for row in (0, 3, 6):
            for col in (0, 3, 6):
                self.assertEqual({answer[r][c] for r in range(row, row + 3)
                                  for c in range(col, col + 3)}, digits)
        self.assertEqual(solve(answer), answer)

    def test_duplicate_clues(self):
        for first, second in [((0, 0), (0, 4)), ((0, 0), (4, 0)), ((0, 0), (1, 1))]:
            grid = [[0] * 9 for _ in range(9)]
            for row, col in (first, second):
                grid[row][col] = 1
            with self.assertRaises(ValueError):
                solve(grid)

    def test_malformed_grid(self):
        for grid in [[], [[0] * 8 for _ in range(9)], [[10] * 9 for _ in range(9)],
                     [[1.5] * 9 for _ in range(9)]]:
            with self.assertRaises(ValueError):
                solve(grid)

    def test_valid_but_unsolvable(self):
        grid = [[0] * 9 for _ in range(9)]
        grid[0] = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        grid[1][8] = 9
        self.assertIsNone(solve(grid))
