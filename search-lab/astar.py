import heapq
import math
from collections import deque

WAREHOUSE = """\
#################
#S....#.........#
#.###.#.#######.#
#...#.#.......#.#
###.#.#######.#.#
#...#.........#.#
#.###########.#.#
#.............#G#
#################"""

STEPS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


def parse(text):
    grid = text.splitlines()
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
            if ch == "G":
                goal = (r, c)
    return grid, start, goal


def manhattan(p, goal):
    return abs(p[0] - goal[0]) + abs(p[1] - goal[1])


def euclidean(p, goal):
    return math.hypot(p[0] - goal[0], p[1] - goal[1])


def zero(p, goal):
    return 0


def double_manhattan(p, goal):
    return 2 * manhattan(p, goal)


def neighbours(grid, p):
    for dr, dc in STEPS:
        r, c = p[0] + dr, p[1] + dc
        if 0 <= r < len(grid) and 0 <= c < len(grid[r]) and grid[r][c] != "#":
            yield (r, c)


def rebuild(parent, node):
    path = [node]
    while parent[node] is not None:
        node = parent[node]
        path.append(node)
    return path[::-1]


def astar(grid, start, goal, h=manhattan):
    """Returns (path or None, number of states expanded)."""
    counter = 0  # tie-breaker so the heap never compares positions
    frontier = [(h(start, goal), counter, start)]
    g = {start: 0}
    parent = {start: None}
    closed = set()
    expanded = 0
    while frontier:
        _, _, cur = heapq.heappop(frontier)
        if cur in closed:
            continue
        closed.add(cur)
        expanded += 1
        if cur == goal:
            return rebuild(parent, cur), expanded
        for nxt in neighbours(grid, cur):
            new_g = g[cur] + 1
            if new_g < g.get(nxt, float("inf")):
                g[nxt] = new_g
                parent[nxt] = cur
                counter += 1
                heapq.heappush(frontier, (new_g + h(nxt, goal), counter, nxt))
    return None, expanded


def bfs(grid, start, goal):
    frontier = deque([start])
    parent = {start: None}
    expanded = 0
    while frontier:
        cur = frontier.popleft()
        expanded += 1
        if cur == goal:
            return rebuild(parent, cur), expanded
        for nxt in neighbours(grid, cur):
            if nxt not in parent:
                parent[nxt] = cur
                frontier.append(nxt)
    return None, expanded


def report(name, result):
    path, expanded = result
    if path is None:
        return f"{name:<14} no solution   expanded={expanded}"
    return f"{name:<14} length={len(path) - 1:<4} expanded={expanded}"


if __name__ == "__main__":
    grid, s, g = parse(WAREHOUSE)
    path, n = astar(grid, s, g)
    print("A* path:", path)
    print()
    print(report("BFS", bfs(grid, s, g)))
    for name, fn in [("A* manhattan", manhattan), ("A* h=0", zero),
                     ("A* euclidean", euclidean), ("A* 2*manhattan", double_manhattan)]:
        print(report(name, astar(grid, s, g, fn)))
