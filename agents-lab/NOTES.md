# Agents lab - goal-based warehouse agent

Run: `python3 agent.py`   Tests: `python3 -m pytest -q`

## Task 1 - understanding the problem
1. **Environment:** a 7x21 grid of cells; `#` blocked, `.` free, one `S` and one `G`. Fully observable, deterministic, static, single agent.
2. **Goal:** reach `G` from `S` without entering an obstacle.
3. **Actions:** Up, Down, Left, Right, one cell each.
4. **State the agent needs:** its current position (the map and goal are fixed knowledge).
5. **Goal-based, not simple reflex:** a reflex agent maps the current percept straight to an action (e.g. "if free on the right, go right") and can loop or get stuck in a dead end. This agent has an explicit goal and searches through sequences of moves to find one that reaches it before it acts.

**Think about it (twice as large):** BFS would still be correct and still return a shortest path, but it expands cells in every direction, so work and memory grow with the area (about 4x for double the width and height). Other difficulties: memory for the frontier, and many equal-cost paths. An informed search (A* with Manhattan distance) would be the natural upgrade.

## Task 2 - design
```mermaid
flowchart LR
    E[Environment: grid map] -->|percept: map, own position| S[State: position, goal]
    S --> D[Decision component: BFS plans a path]
    D -->|next action: Up/Down/Left/Right| A[Actuator: move one cell]
    A --> E
```
| Component | In the code |
|---|---|
| Environment | `WAREHOUSE` string -> `parse()` grid |
| Current state | `(row, col)` tuple |
| Goal | position of `G` |
| Actions | `MOVES` dict, filtered by `neighbours()` |
| Decision-making | `find_path()` (BFS) |

## Task 3 - prompt engineering
**Prompt used (summary):** 
I am building a goal-based agent in Python for a warehouse navigation problem.

ENVIRONMENT
The warehouse is this ASCII map:

#####################
#S....#............G#
#.##....##########..#
#....##.............#
#.######.###.#.###..#
#........#..........#

#####################

S is the start, G is the goal, # is an obstacle, and . is free space.
The vehicle can move Up, Down, Left or Right, one cell at a time.
It cannot move into a # cell or outside the map. Every move costs 1.

REQUIREMENTS
1. Represent the warehouse as a two-dimensional grid and find the positions of S and G by scanning the map.
2. Represent a state as a (row, column) position.
3. Implement a function that returns the valid neighbouring cells of a position.
4. Find a collision-free path from S to G using a search algorithm. Choose the algorithm yourself, and explain in comments or text why it suits this problem.
5. Avoid revisiting cells, so the search always terminates.
6. If a path exists, print the sequence of moves (Up/Down/Left/Right), the path length, and the map with the path marked by *.
7. If no path exists, print a clear message instead of crashing or looping.

CODE STYLE
- Plain Python 3 with the standard library only.
- Short, clear function names and brief comments. No unnecessary classes.
- Put the map in a variable so I can change it easily.

TESTING
After the main program, add a few simple tests (using assert or pytest) for:
- the original map has a path,
- a map where the goal is next to the start,
- a map where the goal is walled off (should report no path),
- the path never passes through a #.

Before the code, state which search algorithm you chose and why. After the code, show the output on the warehouse map above.

1. **Did the LLM generate a working program on the first attempt?** Yes. It ran and produced a valid path first time, and the four tests passed first time.
2. **How could the prompt be improved?** Not needed here, but a better prompt would also ask for tests (blocked goal, adjacent goal) and say explicitly "shortest path", since that decides between BFS and DFS.
3. **Algorithm chosen:** breadth-first search.
4. **Why:** all moves cost 1 and the map is small, so BFS is simple and guarantees a shortest path. DFS can return a long winding path, and A*/Dijkstra add machinery that buys nothing with uniform cost on a small grid.

## Result
```
Moves: Right x3, Down, Right x3, Up, Right x12      Length: 20
#####################
#S***.#************G#
#.##****##########..#
#....##.............#
#.######.###.#.###..#
#........#..........#
#####################
```
Tests (all pass): path exists on the main map, path never enters `#`, adjacent goal gives 1 move, blocked goal returns no path.
