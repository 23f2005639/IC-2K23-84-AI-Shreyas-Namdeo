"""Water jug problem using BFS."""

from collections import deque
from math import gcd
from time import perf_counter


def solve(jug_limit, pot_limit, goal_units):
    """Return the shortest sequence, or None if the target is unreachable."""
    if any(type(value) is not int for value in
           (jug_limit, pot_limit, goal_units)):
        raise ValueError("Use integer capacities and target.")
    if jug_limit <= 0 or pot_limit <= 0 or goal_units < 0:
        raise ValueError("Use positive capacities and a nonnegative target.")
    if (goal_units > max(jug_limit, pot_limit)
            or goal_units % gcd(jug_limit, pot_limit)):
        return None

    dry_pair = (0, 0)
    jug_queue = deque([dry_pair])
    jug_trail = {dry_pair: None}
    while jug_queue:
        jug_pair = jug_queue.popleft()
        jug_fill, pot_fill = jug_pair
        if goal_units in jug_pair:
            jug_steps = []
            while jug_pair != dry_pair:
                old_pair, jug_action = jug_trail[jug_pair]
                jug_steps.append((jug_pair, jug_action))
                jug_pair = old_pair
            return [(dry_pair, "Start")] + jug_steps[::-1]

        into_pot = min(jug_fill, pot_limit - pot_fill)
        into_jug = min(pot_fill, jug_limit - jug_fill)
        jug_moves = [
            ((jug_limit, pot_fill), "Fill A"),
            ((jug_fill, pot_limit), "Fill B"),
            ((0, pot_fill), "Empty A"),
            ((jug_fill, 0), "Empty B"),
            ((jug_fill - into_pot, pot_fill + into_pot), "Pour A -> B"),
            ((jug_fill + into_jug, pot_fill - into_jug), "Pour B -> A"),
        ]
        for fresh_pair, jug_action in jug_moves:
            if fresh_pair not in jug_trail:
                jug_trail[fresh_pair] = (jug_pair, jug_action)
                jug_queue.append(fresh_pair)
    return None


def main():
    try:
        jug_limit = int(input("Jug A capacity: "))
        pot_limit = int(input("Jug B capacity: "))
        goal_units = int(input("Target amount: "))
        jug_clock = perf_counter()
        jug_answer = solve(jug_limit, pot_limit, goal_units)
        jug_seconds = perf_counter() - jug_clock
    except (ValueError, EOFError) as error:
        print(f"Invalid input: {error}")
        return
    if jug_answer is None:
        print("No solution.")
    else:
        for move_no, (jug_pair, jug_action) in enumerate(jug_answer):
            jug_fill, pot_fill = jug_pair
            print(f"Step {move_no}: {jug_action} | A={jug_fill}, B={pot_fill}")
        print(f"Total moves: {len(jug_answer) - 1}")
    print(f"Execution time: {jug_seconds:.6f} seconds")


if __name__ == "__main__":
    main()
