from astar import astar, bfs, manhattan, euclidean, zero, double_manhattan, report

rows = ["#" * 12] + ["#" + "." * 10 + "#" for _ in range(10)] + ["#" * 12]
grid = rows
start, goal = (1, 1), (10, 10)
# a few obstacles so the heuristic has something to trip over
grid = [list(r) for r in grid]
for r in range(2, 9):
    grid[r][5] = "#"
grid = ["".join(r) for r in grid]

print(report("BFS", bfs(grid, start, goal)))
for name, fn in [("A* manhattan", manhattan), ("A* h=0", zero),
                 ("A* euclidean", euclidean), ("A* 2*manhattan", double_manhattan)]:
    print(report(name, astar(grid, start, goal, fn)))
