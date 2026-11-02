"""Missionaries and cannibals using BFS."""

from collections import deque
from time import perf_counter


def solve(monk_total, rival_total, boat_limit):
    """Return safe shortest crossings, or None if no crossing exists."""
    if any(type(value) is not int for value in
           (monk_total, rival_total, boat_limit)):
        raise ValueError("Use integer populations and capacity.")
    if (min(monk_total, rival_total) < 0
            or monk_total + rival_total == 0 or boat_limit < 1):
        raise ValueError("Use nonnegative counts and a positive capacity.")

    def bank_safe(monk_left, rival_left):
        monk_right = monk_total - monk_left
        rival_right = rival_total - rival_left
        return (0 <= monk_left <= monk_total
                and 0 <= rival_left <= rival_total
                and (monk_left == 0 or monk_left >= rival_left)
                and (monk_right == 0 or monk_right >= rival_right))

    if not bank_safe(monk_total, rival_total):
        raise ValueError("The starting bank is unsafe.")

    river_start = (monk_total, rival_total, True)
    river_queue = deque([river_start])
    river_trail = {river_start: None}
    boat_loads = [
        (monk_load, rival_load)
        for monk_load in range(min(monk_total, boat_limit) + 1)
        for rival_load in range(min(rival_total, boat_limit - monk_load) + 1)
        if monk_load + rival_load > 0
    ]
    while river_queue:
        river_state = river_queue.popleft()
        monk_left, rival_left, boat_left = river_state
        if monk_left == rival_left == 0:
            river_steps = []
            while river_state != river_start:
                old_state, boat_load = river_trail[river_state]
                river_steps.append((river_state, boat_load))
                river_state = old_state
            return [(river_start, (0, 0))] + river_steps[::-1]
        river_sign = -1 if boat_left else 1
        for monk_load, rival_load in boat_loads:
            fresh_monk = monk_left + river_sign * monk_load
            fresh_rival = rival_left + river_sign * rival_load
            fresh_state = (fresh_monk, fresh_rival, not boat_left)
            if (bank_safe(fresh_monk, fresh_rival)
                    and fresh_state not in river_trail):
                boat_load = (monk_load, rival_load)
                river_trail[fresh_state] = (river_state, boat_load)
                river_queue.append(fresh_state)
    return None


def main():
    try:
        monk_total = int(input("Missionaries [3]: ") or "3")
        rival_total = int(input("Cannibals [3]: ") or "3")
        boat_limit = int(input("Boat capacity [2]: ") or "2")
        river_clock = perf_counter()
        river_answer = solve(monk_total, rival_total, boat_limit)
        river_seconds = perf_counter() - river_clock
    except (ValueError, EOFError) as error:
        print(f"Invalid input: {error}")
        return
    if river_answer is None:
        print("No solution.")
    else:
        for trip_no, (bank_state, boat_load) in enumerate(river_answer):
            monk_left, rival_left, boat_left = bank_state
            boat_side = "L" if boat_left else "R"
            trip_way = "R -> L" if boat_left else "L -> R"
            trip_note = "Start" if trip_no == 0 else f"{boat_load} {trip_way}"
            print(f"Step {trip_no}: {trip_note} | "
                  f"Left: {monk_left}M {rival_left}C | "
                  f"Right: {monk_total - monk_left}M "
                  f"{rival_total - rival_left}C | Boat: {boat_side}")
        print(f"Total crossings: {len(river_answer) - 1}")
    print(f"Execution time: {river_seconds:.6f} seconds")


if __name__ == "__main__":
    main()
