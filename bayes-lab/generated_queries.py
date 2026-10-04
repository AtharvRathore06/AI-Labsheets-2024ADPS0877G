"""Query code for the three homework queries, written by Claude (not by the notebook's local
Qwen model, which was not run). Validated against queries.py by validate_generated.py."""
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


def build():
    model = DiscreteBayesianNetwork([("Cloudy", "Rain"), ("Cloudy", "Sprinkler"),
                                     ("Rain", "WetGrass"), ("Sprinkler", "WetGrass")])
    model.add_cpds(
        TabularCPD("Cloudy", 2, [[0.5], [0.5]]),
        TabularCPD("Rain", 2, [[0.8, 0.2], [0.2, 0.8]], evidence=["Cloudy"], evidence_card=[2]),
        TabularCPD("Sprinkler", 2, [[0.5, 0.9], [0.5, 0.1]], evidence=["Cloudy"], evidence_card=[2]),
        TabularCPD("WetGrass", 2, [[0.99, 0.10, 0.10, 0.01], [0.01, 0.90, 0.90, 0.99]],
                   evidence=["Rain", "Sprinkler"], evidence_card=[2, 2]),
    )
    model.check_model()
    return model


generated_model = build()
_infer = VariableElimination(generated_model)

# P(S=1 | W=1)
q1 = _infer.query(["Sprinkler"], evidence={"WetGrass": 1}, show_progress=False)
# P(C=1 | W=1)
q2 = _infer.query(["Cloudy"], evidence={"WetGrass": 1}, show_progress=False)
# P(R=1 | W=1, S=0)
q3 = _infer.query(["Rain"], evidence={"WetGrass": 1, "Sprinkler": 0}, show_progress=False)
