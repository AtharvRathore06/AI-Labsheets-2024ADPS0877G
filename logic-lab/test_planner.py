from planner import plan, warehouse_actions, act, applicable, apply

INIT = {"At(Robot,A)", "At(Package,A)"}
GOAL = {"At(Package,C)"}


def replay(init, steps):
    state = frozenset(init)
    for a in steps:
        assert applicable(state, a)
        state = apply(state, a)
    return state


def test_a_solvable():
    steps = plan(INIT, GOAL, warehouse_actions())
    assert steps is not None
    assert GOAL <= replay(INIT, steps)


def test_a_shortest_length():
    assert len(plan(INIT, GOAL, warehouse_actions())) == 4


def test_b_no_pickup_means_no_plan():
    assert plan(INIT, GOAL, warehouse_actions(with_pickup=False)) is None


def test_c_robot_at_c_is_not_package_at_c():
    acts = warehouse_actions(with_pickup=False)
    assert plan(INIT, {"At(Robot,C)"}, acts) is not None
    assert plan(INIT, GOAL, acts) is None


def test_pickup_not_applicable_when_apart():
    acts = {a.name: a for a in warehouse_actions()}
    state = frozenset({"At(Robot,B)", "At(Package,A)"})
    assert not applicable(state, acts["PickUp(Package,A)"])


def test_drop_not_applicable_at_start():
    acts = {a.name: a for a in warehouse_actions()}
    assert not applicable(frozenset(INIT), acts["Drop(Package,C)"])


def test_negative_precondition():
    a = act("Lock", pos_pre=["Door"], neg_pre=["Locked"], add=["Locked"])
    assert applicable(frozenset({"Door"}), a)
    assert not applicable(frozenset({"Door", "Locked"}), a)
