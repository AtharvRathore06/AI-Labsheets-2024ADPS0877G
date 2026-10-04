import itertools
import numpy as np
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

EDGES = [("Cloudy", "Rain"), ("Cloudy", "Sprinkler"),
         ("Rain", "WetGrass"), ("Sprinkler", "WetGrass")]


def build_model():
    m = DiscreteBayesianNetwork(EDGES)
    m.add_cpds(
        TabularCPD("Cloudy", 2, [[0.5], [0.5]]),
        TabularCPD("Rain", 2, [[0.8, 0.2], [0.2, 0.8]],
                   evidence=["Cloudy"], evidence_card=[2]),
        TabularCPD("Sprinkler", 2, [[0.5, 0.9], [0.5, 0.1]],
                   evidence=["Cloudy"], evidence_card=[2]),
        # columns: (R,S) = 00, 01, 10, 11
        TabularCPD("WetGrass", 2, [[0.99, 0.10, 0.10, 0.01],
                                   [0.01, 0.90, 0.90, 0.99]],
                   evidence=["Rain", "Sprinkler"], evidence_card=[2, 2]),
    )
    assert m.check_model()
    return m


def joint(c, r, s, w):
    pr = {0: 0.2, 1: 0.8}[c]
    ps = {0: 0.5, 1: 0.1}[c]
    pw = {(0, 0): 0.01, (0, 1): 0.90, (1, 0): 0.90, (1, 1): 0.99}[(r, s)]
    return (0.5
            * (pr if r else 1 - pr)
            * (ps if s else 1 - ps)
            * (pw if w else 1 - pw))


def by_enumeration(query, evidence):
    """P(query var = 1 | evidence) by summing the full joint."""
    names = ["Cloudy", "Rain", "Sprinkler", "WetGrass"]
    num = den = 0.0
    for vals in itertools.product([0, 1], repeat=4):
        row = dict(zip(names, vals))
        if any(row[k] != v for k, v in evidence.items()):
            continue
        p = joint(*vals)
        den += p
        if row[query] == 1:
            num += p
    return num / den


QUERIES = [
    ("P(S=1 | W=1)", "Sprinkler", {"WetGrass": 1}),
    ("P(C=1 | W=1)", "Cloudy", {"WetGrass": 1}),
    ("P(R=1 | W=1, S=0)", "Rain", {"WetGrass": 1, "Sprinkler": 0}),
]

if __name__ == "__main__":
    model = build_model()
    infer = VariableElimination(model)
    prior = {"Sprinkler": 0.5 * 0.5 + 0.5 * 0.1, "Cloudy": 0.5, "Rain": 0.5 * 0.2 + 0.5 * 0.8}
    print(f"{'query':<20}{'prior':>8}{'pgmpy':>10}{'enumeration':>14}")
    for label, var, ev in QUERIES:
        post = float(infer.query([var], evidence=ev, show_progress=False).values[1])
        enum = by_enumeration(var, ev)
        assert np.isclose(post, enum, atol=1e-10)
        print(f"{label:<20}{prior.get(var, float('nan')):>8.3f}{post:>10.4f}{enum:>14.4f}")
