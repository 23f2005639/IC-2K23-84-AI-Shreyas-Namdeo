# Lab 4 - Knowledge Representation

Aim: infer facts using production rules and a semantic network.

Algorithm: repeatedly apply satisfied rules until no new facts appear;
traverse parent links with a visited set to handle cycles.

Run: `python3 Lab4/KnowledgeRepresentation.py` from the repository root.
Input: small in-code rule set and sparrow/bird/animal network.

Results / Output: inferred facts, inheritance query and execution time in
`outputs/results.txt`. Pending execution.

Performance analysis: chaining scans all rules until reaching a fixed point;
network traversal takes O(V+E). Classification metrics do not apply.

Visualization: `docs/architecture-diagrams/semantic-network.mmd`.
Learning outcomes: forward chaining, inheritance and cycle handling.
