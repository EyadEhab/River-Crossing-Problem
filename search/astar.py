from typing import List, Tuple, Optional, Dict
import heapq
import time
from core.river_crossing import *


def _reconstruct(came_from: Dict[Tuple[int, int, int], Optional[Tuple[int, int, int]]],
                 current: Tuple[int, int, int]) -> List[Tuple[int, int, int]]:
    path: List[Tuple[int, int, int]] = [current]
    while came_from[current] is not None:
        current = came_from[current]  # type: ignore
        path.append(current)
    path.reverse()
    return path


def solve() -> Tuple[int, List[Tuple[int, int, int]], float]:
    start_time = time.perf_counter()
    open_heap: List[Tuple[float, Tuple[int, int, int]]] = []
    came_from: Dict[Tuple[int, int, int], Optional[Tuple[int, int, int]]] = {INITIAL_STATE: None}
    g_score: Dict[Tuple[int, int, int], float] = {INITIAL_STATE: 0.0}
    visited: set[Tuple[int, int, int]] = set()

    heapq.heappush(open_heap, (heuristic(INITIAL_STATE), INITIAL_STATE))

    nodes_explored = 0

    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in visited:
            continue
        visited.add(current)
        nodes_explored += 1

        if is_goal(current):
            path = _reconstruct(came_from, current)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return path, nodes_explored, elapsed_ms

        for neighbor in get_successors(current):
            tentative_g = g_score[current] + 1.0
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor)
                heapq.heappush(open_heap, (f, neighbor))

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return [], nodes_explored, elapsed_ms


