from collections import deque
from astar import parse, WAREHOUSE, neighbours, manhattan, euclidean, zero, double_manhattan
import heuristics_open_grid as og  # reuses the open grid defined there (prints its table too)


def true_costs(grid, goal):
    dist = {goal: 0}
    q = deque([goal])
    while q:
        p = q.popleft()
        for n in neighbours(grid, p):
            if n not in dist:
                dist[n] = dist[p] + 1
                q.append(n)
    return dist


def check(label, grid, goal):
    dist = true_costs(grid, goal)
    print(label)
    for name, h in [("h=0", zero), ("manhattan", manhattan),
                    ("euclidean", euclidean), ("2*manhattan", double_manhattan)]:
        over = sum(1 for p, d in dist.items() if h(p, goal) > d + 1e-9)
        print(f"  {name:<12} overestimates on {over}/{len(dist)} cells")


if __name__ == "__main__":
    g, _, goal = parse(WAREHOUSE)
    check("Lab warehouse", g, goal)
    check("Open grid", og.grid, og.goal)
