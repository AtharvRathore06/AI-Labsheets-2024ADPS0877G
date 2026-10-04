# AI Lab 2024ADPS0873G

Four lab exercises for the AI course.

| Folder | Topic |
|---|---|
| `agents-lab` | goal-based agent, BFS pathfinding on a warehouse grid |
| `search-lab` | A* vs BFS, heuristic experiments |
| `logic-lab` | STRIPS-style planner in Python, Prolog checker |
| `bayes-lab` | Sprinkler Bayesian network, inference vs enumeration |

Each folder has code, pytest tests, and a `NOTES.md` with results and answers.
Run a lab with `python3 <script>.py` and `python3 -m pytest -q` from inside its folder.

## How this was made (LLM disclosure)

All code, tests and notes in this repo were produced by Claude (Anthropic) in one session, from the lab handouts. I did not write the code myself.
In that session the code was executed and the tests were run, and the numbers in the notes come from those runs.

What that means for each lab's "design before prompting" steps: the design was not done as a separate step before prompting. The design sections describe the design as implemented.

Things that were checked by running: all pytest suites, the BFS/A* comparisons, the Prolog queries (SWI-Prolog 9.0.4), the Bayes posteriors against brute-force enumeration.
The only failure during the session was a wrong expected value in one test (expected a 5-step warehouse plan, the shortest is 4); the test was corrected, not the planner.
