# Lab 2 - Search Algorithms

Aim: compare BFS, DFS, hill climbing, greedy best-first and A*.

Algorithm: use a queue, stack, improving heuristic neighbor or priority queue.
A* ranks by path cost plus heuristic; greedy search uses the heuristic only.

Run: `python3 Lab2/SearchAlgorithms.py` from the repository root.
Input: `datasets/roads.json` (directed weighted graph).

Results / Output: `outputs/search.csv` with routes, costs and execution times.
Pending execution; BFS minimizes hops, A* minimizes cost with an admissible
heuristic. Hill climbing may stop at a local minimum.

Performance analysis: BFS/DFS O(V+E) time and O(V) visited/frontier entries;
copying full paths adds up to O(V) per frontier entry. Priority searches use
a heap; A* may revisit nodes when a better cost is found. Compare measured
time, route cost and success; classification metrics do not apply.

Graphs: input graph and search flow in `docs/algorithm-flowcharts/search.mmd`.
Learning outcomes: informed vs uninformed search and optimality tradeoffs.
