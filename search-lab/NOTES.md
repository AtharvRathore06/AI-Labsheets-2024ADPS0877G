# Search lab - A* and BFS

Run: `python3 astar.py`, `python3 heuristics_open_grid.py`   Tests: `python3 -m pytest -q`

## Task 0 - formulation
| Component | Specification |
|---|---|
| State | `(row, col)` of the robot |
| Actions | Up, Down, Left, Right |
| Transition | move one cell if inside the map and not `#` |
| Initial state | position of `S` |
| Goal | position of `G` |
| Cost | 1 per move |

(a) only the position, since the map never changes. (b) leaving the map or entering `#`. (c) deterministic: an action always has one outcome. (d) a move sequence from S to G, ideally of minimum cost.

## Task 1 - design of the agent
1. State: a `(row, col)` tuple.
2. Warehouse: list of strings, indexed `grid[r][c]`.
3. Valid actions: `neighbours()` tries four offsets and rejects out-of-bounds cells and `#`.
4. Goal test: `cur == goal` when a node is popped.
5. Frontier entries: `(f, tie_breaker, position)` in a heap; separate dicts hold `g` and `parent`.
6. Path: follow `parent` from the goal back to the start, then reverse.

Reported on termination: found or not, the path, its length, states expanded.

## Task 2 - the prompt
I am implementing a goal-based search agent in Python using only the standard library.

PROBLEM
The environment is a grid given as an ASCII map:

#################
#S....#.........#
#.###.#.#######.#
#...#.#.......#.#
###.#.#######.#.#
#...#.........#.#
#.###########.#.#
#.............#G#
#################

# is an obstacle, . is free, S is the start and G is the goal.
The agent moves Up, Down, Left or Right, one cell at a time, and every move costs 1.
It cannot move into a # or outside the map.

TASK
Implement A* search with the Manhattan distance heuristic:
h(n) = |row - goal_row| + |col - goal_col|

REQUIREMENTS
1. Represent a state as a (row, col) tuple, and find S and G by scanning the map.
2. Write a function that returns the valid neighbouring cells of a position.
3. Use a priority queue (heapq) as the frontier, ordered by f(n) = g(n) + h(n). Add a counter as a tie-breaker so positions are never compared directly.
4. Keep a dictionary of the best known g(n) for each cell, and a closed set so the same state is never expanded twice.
5. Reconstruct the path using a parent dictionary.
6. Return the path (or None if the goal is unreachable) and the number of states expanded.
7. Print: whether a solution was found, the path, the path length (number of moves), and the number of states expanded.
8. The program must terminate on unreachable goals, not loop forever.

CODE STYLE
Short, clear function names and brief comments. No unnecessary classes. Pass the heuristic in as a function argument so I can swap it later.

TESTING
Add simple tests (assert or pytest) for:
1. The original map: a path exists, starts at S and ends at G.
2. Trivial case: "#####", "#SG##", "#####" gives a one-move path.
3. No solution: "#######", "#S....#", "###.###", "#...#G#", "#######" reports failure.
4. Alternative paths: a small map with two routes, checking that the returned path is a shortest one.

Before the code, explain the main components of the implementation. After the code, show the output on the warehouse map.

## Task 3 - tests
| Test | Result |
|---|---|
| 1 original map | found, length 40, 64 states expanded |
| 2 trivial `#SG#` | found, 1 step |
| 3 unreachable goal | returns no path and terminates |
| 4 two routes | returns the shorter, 4-step route |
Also: A* and BFS give the same path length on the main map.

## Task 4 - where things are in `astar.py`
| Concept | Location |
|---|---|
| State | `(row, col)` tuple |
| Action / transition | `neighbours()` |
| Goal test | `if cur == goal` in `astar()` |
| g(n) | `g` dict |
| h(n) | `manhattan()`, passed in as `h` |
| f(n) | `new_g + h(nxt, goal)`, the heap key |
| Frontier | `frontier`, a `heapq` heap |
| Visited | `closed` set |
| Path reconstruction | `parent` dict and `rebuild()` |

(a) a binary min-heap. (b) it pops the entry with the smallest f. (c) in `manhattan()`. (d) yes, when pushing a neighbour. (e) the `closed` set, and pushing a neighbour only if it found a cheaper g.

## Task 5 - BFS vs A* (lab map)
| Measure | BFS | A* |
|---|---|---|
| Solution found | yes | yes |
| Path length | 40 | 40 |
| States expanded | 64 | 64 |

(a) yes. (b) yes. (c) neither; they tie. (d) A* can expand fewer states when the heuristic steers away from useless regions, but this map is one winding corridor, so there is only one route and nothing to prune.

## Task 6 - heuristics
Lab map:

| Heuristic | Found | Length | Expanded |
|---|---|---|---|
| Manhattan | yes | 40 | 64 |
| h = 0 | yes | 40 | 64 |
| Euclidean | yes | 40 | 64 |
| 2 x Manhattan | yes | 40 | 64 |

All identical for the reason above. To see real differences I used an open 10x10 grid with a partial wall (`heuristics_open_grid.py`):

| Heuristic | Found | Length | Expanded |
|---|---|---|---|
| BFS | yes | 18 | 93 |
| Manhattan | yes | 18 | 93 |
| h = 0 | yes | 18 | 93 |
| Euclidean | yes | 18 | 93 |
| 2 x Manhattan | yes | 18 | 19 |

Findings:
- Manhattan matched BFS in expansions here. Many cells have the same f = g + h, and my tie-break is first-in-first-out, so A* explores all of them. A tie-break that prefers larger g would likely cut this.
- Euclidean is admissible but weaker than Manhattan on a 4-move grid, so it prunes less.
- 2 x Manhattan overestimates, so it is not admissible. It acts greedy, expanding far fewer states (19) with no guarantee of optimality. It happened to stay optimal on this grid.
- h = 0 reduces A* to uniform-cost search, which is BFS here.

## Task 6 (continued) - why Manhattan, and admissibility
**Why Manhattan suits this warehouse.** The robot moves only up, down, left or right, each move costing 1, and each move changes either the row difference or the column difference to the goal by exactly 1. So at least |dr| + |dc| moves are always needed, even with no obstacles. Obstacles can only add moves, never remove them. That makes Manhattan distance a lower bound on the true remaining cost, i.e. admissible (h(n) <= h*(n)), and it is also consistent, since one move changes h by at most 1 = the step cost. With these properties A* with a closed set returns an optimal path.

**Checking admissibility by experiment** (`admissibility_check.py` compares each heuristic with the true remaining cost h*, computed by BFS backwards from the goal):

| Heuristic | Overestimates on lab warehouse | Overestimates on open grid |
|---|---|---|
| h = 0 | 0 / 64 cells | 0 / 93 cells |
| Manhattan | 0 / 64 | 0 / 93 |
| Euclidean | 0 / 64 | 0 / 93 |
| 2 x Manhattan | 18 / 64 | 92 / 93 |

**Think about it (too optimistic vs too aggressive).**
- *Too optimistic* (h much below h*, e.g. h = 0): still admissible, so A* stays optimal, but it has little guidance and expands about as many states as blind search.
- *Too aggressive* (h above h*, e.g. 2 x Manhattan): no longer admissible. A* trusts the inflated estimate, behaves more like greedy search, and expands far fewer states (19 vs 93 on the open grid), but optimality is no longer guaranteed. It stayed optimal in both of my maps (on the lab map only because there is a single route), so the risk is real but not shown by these runs.
- The best heuristic is the one closest to h* without exceeding it.

## Task 7 - evaluating the LLM-generated agent
1. **Correct immediately:** all of it; the program and the 5 tests passed on the first run.
2. **Bugs / design problems:** none in the code. One thing worth noting is the FIFO tie-breaking, which makes A* equal BFS on open grids.
3. **How found:** the heuristic experiments on the open grid exposed the tie-breaking behaviour.
4. **Unfamiliar terminology:** the heap tie-breaker counter (needed so equal f values never compare positions) is the least obvious part.
5. **Modified:** no manual modifications after generation.
6. **Most useful tests:** the unreachable-goal test (catches infinite loops) and the shortest-route test (catches a non-optimal search).
7. **Trusted without testing?** No; correctness of the loop, closed set and path rebuild is exactly what the tests check.
8. **About A*:** its guarantee depends on admissibility, and an admissible heuristic can still give no speed-up if the map or the tie-breaking leaves nothing to prune.

## Final reflection
1. **Why formulate first.** The formulation (states, actions, transitions, costs, goal) decides what the algorithm needs. Without it, you cannot say what "valid move", "goal" or "optimal" mean, so you cannot test the code either.
2. **Informed search.** A* uses problem-specific knowledge, the heuristic h(n), in addition to the path cost so far. Blind search only knows the cost so far.
3. **Why the heuristic matters.** It sets both speed and correctness: a tighter admissible heuristic prunes more, h = 0 prunes nothing, and an inadmissible one (2 x Manhattan) can be fast but may return a non-optimal path.
4. **Risk of accepting untested code.** The code can look right and be wrong: a missing closed set loops forever, a wrong goal test returns the wrong cell, a bad heuristic returns a non-optimal path. Tests on known cases (trivial, unreachable, two routes) catch these.
