import numpy as np
import generated_queries as g
from queries import by_enumeration, QUERIES

results = [g.q1, g.q2, g.q3]
for (label, var, ev), q in zip(QUERIES, results):
    got = float(q.values[1])
    ref = by_enumeration(var, ev)
    status = "PASS" if np.isclose(got, ref, atol=1e-10) else "FAIL"
    print(f"{label:<20} generated={got:.4f} reference={ref:.4f} {status}")
