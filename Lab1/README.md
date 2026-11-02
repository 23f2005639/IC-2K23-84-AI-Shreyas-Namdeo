# Lab 1

Aim: solve three state-space problems using Python.

| Experiment | Problem statement | Algorithm | Expected result |
| --- | --- | --- | --- |
| 1 | Measure a target amount using two jugs. | BFS over fill, empty and pour moves; track visited states. | Jugs 4, 3; target 2: 4 moves. |
| 2 | Cross a river without cannibals outnumbering missionaries on either bank. | BFS over safe boat loads; retain parent states. | 3 missionaries, 3 cannibals, boat 2: 11 crossings. |
| 3 | Complete a 9x9 Sudoku without repeating digits in rows, columns or boxes. | Validate clues, try digits in empty cells, backtrack on conflicts. | Completed grid, or no solution. |

Run from the repository root:

```bash
python3 Lab1/Experiment1.py < Lab1/inputs/water_jug.txt
python3 Lab1/Experiment2.py < Lab1/inputs/river.txt
python3 Lab1/Experiment3.py < Lab1/inputs/sudoku.txt
```

Results / Output: programs print steps or a solved grid and elapsed seconds.
Use `> Lab1/outputs/experiment1.txt` after a command to save its output.
The examples above are expected results; this revision was not run or tested.

Performance analysis:

- Water Jug: O((A+1)(B+1)) time and space for capacities A, B.
- River: O((M+1)(C+1)K^2) time; O((M+1)(C+1) + K^2) space
  for populations M, C and boat capacity K.
- Sudoku: O(9^E) worst-case time and O(E) recursion space for E blanks.
- Execution times: pending execution. Accuracy, precision, recall and F1 do
  not apply to these search problems.

Visualizations (existing illustrations, not new execution screenshots):
[jugs](outputs/water_jug.svg), [river](outputs/river_crossing.svg),
[Sudoku](outputs/sudoku.svg).

Learning outcomes: state representation, production rules, shortest-path
search, constraint checking and backtracking.
