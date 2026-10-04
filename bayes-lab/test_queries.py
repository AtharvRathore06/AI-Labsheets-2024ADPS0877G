import numpy as np
from pgmpy.inference import VariableElimination
from queries import build_model, by_enumeration, QUERIES, EDGES


def test_structure():
    m = build_model()
    assert set(m.edges()) == set(EDGES)


def test_queries_match_enumeration():
    infer = VariableElimination(build_model())
    for _, var, ev in QUERIES:
        got = float(infer.query([var], evidence=ev, show_progress=False).values[1])
        assert np.isclose(got, by_enumeration(var, ev))


def test_swapped_wetgrass_columns_change_answer():
    from pgmpy.factors.discrete import TabularCPD
    m = build_model()
    m.remove_cpds(m.get_cpds("WetGrass"))
    m.add_cpds(TabularCPD("WetGrass", 2, [[0.99, 0.10, 0.01, 0.10],
                                          [0.01, 0.90, 0.99, 0.90]],
                          evidence=["Rain", "Sprinkler"], evidence_card=[2, 2]))
    assert m.check_model()
    wrong = float(VariableElimination(m).query(["Rain"], evidence={"WetGrass": 1},
                                               show_progress=False).values[1])
    right = by_enumeration("Rain", {"WetGrass": 1})
    assert not np.isclose(wrong, right)
