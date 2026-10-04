from collections import deque

WAREHOUSE = """\
#####################
#S....#............G#
#.##....##########..#
#....##.............#
#.######.###.#.###..#
#........#..........#
#####################"""

MOVES = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}


def parse(text):
    grid = [list(row) for row in text.splitlines()]
    start = goal = None
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch == "S":
                start = (r, c)
            elif ch == "G":
                goal = (r, c)
    return grid, start, goal


def neighbours(grid, pos):
    r, c = pos
    for name, (dr, dc) in MOVES.items():
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[nr]) and grid[nr][nc] != "#":
            yield name, (nr, nc)


def find_path(grid, start, goal):
    """Breadth-first search. Returns a list of (action, position) or None."""
    frontier = deque([start])
    came_from = {start: None}
    while frontier:
        cur = frontier.popleft()
        if cur == goal:
            path = []
            while came_from[cur] is not None:
                prev, action = came_from[cur]
                path.append((action, cur))
                cur = prev
            return path[::-1]
        for action, nxt in neighbours(grid, cur):
            if nxt not in came_from:
                came_from[nxt] = (cur, action)
                frontier.append(nxt)
    return None


def draw(grid, path):
    out = [row[:] for row in grid]
    for _, (r, c) in path[:-1]:
        out[r][c] = "*"
    return "\n".join("".join(row) for row in out)


if __name__ == "__main__":
    grid, start, goal = parse(WAREHOUSE)
    path = find_path(grid, start, goal)
    if path is None:
        print("No path exists")
    else:
        print("Moves:", " ".join(a for a, _ in path))
        print("Length:", len(path))
        print(draw(grid, path))
