from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class Action:
    name: str
    pos_pre: frozenset = frozenset()
    neg_pre: frozenset = frozenset()
    add: frozenset = frozenset()
    delete: frozenset = frozenset()


def act(name, pos_pre=(), neg_pre=(), add=(), delete=()):
    return Action(name, frozenset(pos_pre), frozenset(neg_pre), frozenset(add), frozenset(delete))


def applicable(state, a):
    return a.pos_pre <= state and not (a.neg_pre & state)


def apply(state, a):
    return (state - a.delete) | a.add


def plan(initial, goal, actions):
    """BFS over states. Returns a list of actions, or None if no plan exists."""
    start = frozenset(initial)
    goal = frozenset(goal)
    frontier = deque([start])
    parent = {start: None}
    while frontier:
        state = frontier.popleft()
        if goal <= state:
            steps = []
            while parent[state] is not None:
                prev, a = parent[state]
                steps.append(a)
                state = prev
            return steps[::-1]
        for a in actions:
            if applicable(state, a):
                nxt = apply(state, a)
                if nxt not in parent:
                    parent[nxt] = (state, a)
                    frontier.append(nxt)
    return None


def warehouse_actions(with_pickup=True):
    acts = []
    for x, y in [("A", "B"), ("B", "A"), ("B", "C"), ("C", "B")]:
        acts.append(act(f"Move({x},{y})",
                        pos_pre=[f"At(Robot,{x})"],
                        add=[f"At(Robot,{y})"],
                        delete=[f"At(Robot,{x})"]))
    if with_pickup:
        for loc in "ABC":
            acts.append(act(f"PickUp(Package,{loc})",
                            pos_pre=[f"At(Robot,{loc})", f"At(Package,{loc})"],
                            add=["Holding(Package)"],
                            delete=[f"At(Package,{loc})"]))
    for loc in "ABC":
        acts.append(act(f"Drop(Package,{loc})",
                        pos_pre=[f"At(Robot,{loc})", "Holding(Package)"],
                        add=[f"At(Package,{loc})"],
                        delete=["Holding(Package)"]))
    return acts


def show(initial, actions_taken):
    state = frozenset(initial)
    print("S0", sorted(state))
    for i, a in enumerate(actions_taken, 1):
        assert applicable(state, a), f"{a.name} not applicable"
        state = apply(state, a)
        print(f"S{i}", sorted(state), "  after", a.name)


if __name__ == "__main__":
    init = {"At(Robot,A)", "At(Package,A)"}
    goal = {"At(Package,C)"}
    result = plan(init, goal, warehouse_actions())
    if result is None:
        print("No plan found")
    else:
        print("Plan:", [a.name for a in result])
        show(init, result)
