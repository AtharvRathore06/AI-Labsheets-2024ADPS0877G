# Logic lab - logical planning

Run: `python3 planner.py`, `swipl -q queries.pl`   Tests: `python3 -m pytest -q`

## Task 0 - the planning problem
(a) I = {At(Robot,A), At(Package,A)}   (b) G = {At(Package,C)}
(c)(d) Actions:

| Action | Preconditions | Effects |
|---|---|---|
| Move(x,y), x-y in {A-B, B-A, B-C, C-B} | At(Robot,x) | not At(Robot,x), At(Robot,y) |
| PickUp(Package,l) | At(Robot,l), At(Package,l) | not At(Package,l), Holding(Package) |
| Drop(Package,l) | At(Robot,l), Holding(Package) | not Holding(Package), At(Package,l) |

PickUp(Package,A) is applicable in I: At(Robot,A) and At(Package,A) both hold.
Drop(Package,C) is not: At(Robot,C) and Holding(Package) are both false.

**Think about it:** being in the action list is not enough; every precondition has to hold in the current state, which is the S |= Pre(a) check.

## Task 1 - plan by hand
| State | Facts |
|---|---|
| S0 | At(Robot,A), At(Package,A) |
| S1 after PickUp(Package,A) | At(Robot,A), Holding(Package) |
| S2 after Move(A,B) | At(Robot,B), Holding(Package) |
| S3 after Move(B,C) | At(Robot,C), Holding(Package) |
| S4 after Drop(Package,C) | At(Robot,C), At(Package,C) |

S4 satisfies G. The handout's sketch (move to B, then PickUp at B) does not work: the package stays at A, so PickUp(Package,B) is not applicable.

## Task 2 - the prompt and where the ideas appear
I want to implement a simple planning agent in Python using only the standard library.

REPRESENTATION
- A state is a set of logical propositions, written as strings such as "At(Robot,A)" and "At(Package,A)".
- Each action has: a name, positive preconditions, negative preconditions, positive effects (add list) and negative effects (delete list).
- An action is applicable if all of its positive preconditions are in the state and none of its negative preconditions are in the state.
- Applying an action: first remove its negative effects from the state, then add its positive effects.

PLANNER
- Use breadth-first search over states to find a sequence of actions that achieves a goal.
- The goal is a set of propositions, and it is achieved when all of them are in the state.
- Do not revisit states that were already seen.
- If no plan exists, report "No plan found" instead of inventing actions or looping forever.
- Print the plan as a list of action names, then print the state reached after each action.

WAREHOUSE PROBLEM
Locations: A, B, C. The robot can move between A-B and B-C in both directions (not directly A-C).
- Initial state: At(Robot,A), At(Package,A)
- Goal: At(Package,C)
- Move(x,y): precondition At(Robot,x); effects: not At(Robot,x), At(Robot,y)
- PickUp(Package,l): preconditions At(Robot,l) and At(Package,l); effects: not At(Package,l), Holding(Package)
- Drop(Package,l): preconditions At(Robot,l) and Holding(Package); effects: not Holding(Package), At(Package,l)
Generate the actions for every valid location rather than typing each one by hand.

TESTS
Write tests (assert or pytest) for these cases:
A. The original problem returns a valid plan. Replay it step by step, checking that every action is applicable and that the final state satisfies the goal.
B. The same problem with the PickUp action removed returns "No plan found".
C. With PickUp removed, the goal At(Robot,C) is solvable, but the goal At(Package,C) is not (the robot reaching C is not the package reaching C).
D. PickUp(Package,A) is not applicable when the robot is at B and the package is at A.
E. Drop(Package,C) is not applicable in the initial state.

CODE STYLE
- Short, clear function names and brief comments. Use a small dataclass or tuple for actions.

OUTPUT
Before the code, explain the implementation and list every assumption you make (for example closed-world assumption, deterministic actions, ground facts only). After the code, show the output for the warehouse problem and point out where in the code each of these appears: preconditions, effects, goal test, and BFS.

| Idea | Where |
|---|---|
| Preconditions | `applicable()` |
| Effects | `apply()`: `(state - delete) | add` |
| Goal | `goal <= state` in `plan()` |
| BFS | `deque` frontier and `parent` dict in `plan()` |

Assumptions: closed-world (anything not in the state is false), actions are deterministic, the state is a set of ground facts, and BFS therefore returns a plan with the fewest actions.

## Task 3 - tests
| Test | Initial state | Goal | Plan found | Result | Valid? |
|---|---|---|---|---|---|
| A solvable | {At(Robot,A), At(Package,A)} | At(Package,C) | yes | PickUp(A), Move(A,B), Move(B,C), Drop(C) | yes: replayed step by step, every precondition checked |
| B impossible | same, PickUp removed | At(Package,C) | no | `None` ("No plan found") | yes: correct, no invented action |
| C irrelevant actions | same, PickUp removed | At(Robot,C) | yes | robot reaches C | yes |
| C (cont.) | same, PickUp removed | At(Package,C) | no | `None` | yes: robot reaching C does not count as the package reaching C |

Extra tests: PickUp is not applicable when robot and package are apart, Drop is not applicable at the start, and a negative precondition blocks an action. All 7 pass.

## Task 4 - logic and search
Current state -> check preconditions (S |= Pre(a)) -> **if they hold, the action is applicable** -> generate successor state S' = Apply(S, a) -> search over alternatives (BFS queue of states) -> goal test.
Logic decides what is possible; search decides what to try. Logical reasoning is the applicability check and the state update; search is the BFS loop that picks which applicable action to expand next and remembers visited states.

## Task 5 - can the LLM verify its own plan?
The independent check is `show()` in `planner.py`: it replays the plan, asserts each action is applicable, and prints the state after each step. For the plan above it printed S0..S4 exactly as in the Task 1 table, with no assertion failing.

**Which to trust:** (b), the independently executed transitions. They are computed by code that mechanically applies the rules. A generated explanation is fluent text that can contain a wrong state or a skipped precondition and still read convincingly. A generated explanation is not an independent verification.

## Reflection questions
1. Preconditions and effects are the specification. Fixing them first lets you check the generated code against something exact, instead of judging whether it "looks right".
2. Without precondition checks the robot could pick up a package it is not next to, or Drop the package at C while still at A, so the plan would "deliver" a package that was never carried there.
3. Because validity needs each action applicable in the state where it runs. A plan can read sensibly and still use an action whose preconditions are false at that step.
4. It produced the program structure (action representation, BFS, printing) and test ideas quickly.
5. Applicability and effect logic, the claim "no plan" in the impossible case, and that the final state satisfies the goal. These were checked by replaying plans and by tests.
6. In deciding applicability (S |= Pre(a)), in updating the state with effects, and in the goal test (G is satisfied by the final state).
7. Planning is search over states. States are nodes, applicable actions are edges, the goal is a goal test, so BFS, DFS or A* from the search module apply directly; logic only generates the edges.

## Task 6/7 - Prolog (run in SWI-Prolog 9.0.4 with `queries.pl`)
```
?- can_move(a,b).  true
?- can_move(a,c).  false
?- valid_move(a,b).  true
?- valid_move(b,c).  true
?- valid_move(a,c).  false
?- valid_plan([a,b,c]).  true
?- valid_plan([a,c]).  false
?- reduce_speed.  true
```
(a) can_move(a,b) is true because the fact `connected(a,b)` matches the rule body.
(b) can_move(a,c) is not established: there is no `connected(a,c)` fact and no rule can derive one, so under Prolog's closed-world reading it fails.
(c) The rule `can_move(X,Y) :- connected(X,Y).` is the implication Connected(X,Y) -> CanMove(X,Y), written head-first, with X and Y universally quantified.

**Challenge:** if the Python planner proposed Move(a,c), `valid_move(a,c)` fails, so the knowledge base does not support it and the move is rejected.

**Task 8:** wet_road is a fact; slippery :- wet_road gives slippery; reduce_speed :- slippery gives reduce_speed.
WetRoad => (WetRoad -> Slippery) => Slippery => (Slippery -> ReduceSpeed) => ReduceSpeed, so the query succeeds.
