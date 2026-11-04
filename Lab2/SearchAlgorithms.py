"""Compare search methods on a small weighted graph."""

import csv
import heapq
import json
from collections import deque
from pathlib import Path
from time import perf_counter


def find_route(road_map, road_hint, origin, destination, method):
    """Return a route; hill climbing can stop at a local minimum."""
    if method not in {"BFS", "DFS", "Hill", "Best", "A*"}:
        raise ValueError("Unknown search method.")
    if origin not in road_map or destination not in road_map:
        raise ValueError("Unknown start or goal.")
    for town, links in road_map.items():
        if town not in road_hint or road_hint[town] < 0:
            raise ValueError("Each node needs a nonnegative heuristic.")
        if any(stop not in road_map or fare <= 0
               for stop, fare in links.items()):
            raise ValueError("Edges need valid endpoints and positive costs.")

    if method == "Hill":
        hill_route = [origin]
        while hill_route[-1] != destination:
            hill_here = hill_route[-1]
            hill_options = [town for town in road_map[hill_here]
                            if town not in hill_route]
            if not hill_options:
                return None
            hill_next = min(hill_options, key=road_hint.get)
            if road_hint[hill_next] >= road_hint[hill_here]:
                return None
            hill_route.append(hill_next)
        return hill_route

    if method in {"BFS", "DFS"}:
        road_queue = deque([[origin]])
        road_seen = {origin}
        while road_queue:
            road_route = (road_queue.popleft() if method == "BFS"
                          else road_queue.pop())
            if road_route[-1] == destination:
                return road_route
            for town in road_map[road_route[-1]]:
                if town not in road_seen:
                    road_seen.add(town)
                    road_queue.append(road_route + [town])
        return None

    road_heap = [(road_hint[origin], 0, [origin])]
    road_costs = {origin: 0}
    while road_heap:
        _, spent_fare, road_route = heapq.heappop(road_heap)
        road_here = road_route[-1]
        if spent_fare != road_costs[road_here]:
            continue
        if road_here == destination:
            return road_route
        for town, fare in road_map[road_here].items():
            next_fare = spent_fare + fare
            if next_fare < road_costs.get(town, float("inf")):
                road_costs[town] = next_fare
                road_rank = road_hint[town]
                if method == "A*":
                    road_rank += next_fare
                heapq.heappush(road_heap, (road_rank, next_fare,
                                          road_route + [town]))
    return None


def main():
    lab_home = Path(__file__).resolve().parent
    try:
        road_data = json.loads(
            (lab_home.parent / "datasets/roads.json").read_text())
        road_map, road_hint = road_data["edges"], road_data["heuristic"]
        (lab_home / "outputs").mkdir(exist_ok=True)
        with (lab_home / "outputs/search.csv").open("w", newline="") as report:
            road_writer = csv.writer(report)
            road_writer.writerow(["method", "route", "cost", "seconds"])
            for method in ("BFS", "DFS", "Hill", "Best", "A*"):
                road_clock = perf_counter()
                route = find_route(road_map, road_hint, "A", "F", method)
                road_seconds = perf_counter() - road_clock
                route_cost = (sum(road_map[left][right]
                                  for left, right in zip(route, route[1:]))
                              if route else None)
                road_writer.writerow([method, route, route_cost, road_seconds])
                print(method, route, route_cost, road_seconds)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Cannot search: {error}")


if __name__ == "__main__":
    main()
