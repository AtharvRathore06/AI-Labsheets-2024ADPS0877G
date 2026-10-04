import numpy as np
import pandas as pd
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.parameter_estimator import DiscreteMLE
from queries import build_model, EDGES

ref = build_model()

# CPT column convention for WetGrass
cpd = ref.get_cpds("WetGrass")
print("WetGrass variable order:", cpd.variables)
print(cpd.values.shape)
for r in (0, 1):
    for s in (0, 1):
        print(f"R={r} S={s}  P(W=1)={cpd.values[1, r, s]}")

# different seeds, N=100
rows = []
for seed in [1, 2, 3, 4, 5]:
    d = ref.simulate(n_samples=100, seed=seed, show_progress=False)
    m = DiscreteBayesianNetwork(EDGES)
    m.fit(d, estimator=DiscreteMLE())
    rows.append({"seed": seed, "estimate": float(m.get_cpds("Rain").values[1, 1])})
df = pd.DataFrame(rows)
print(df.to_string(index=False))
print("mean", round(df.estimate.mean(), 4), "std", round(df.estimate.std(), 4))
