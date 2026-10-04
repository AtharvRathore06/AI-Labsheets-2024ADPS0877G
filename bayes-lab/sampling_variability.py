from pgmpy.parameter_estimator import DiscreteMLE
from queries import build_model, EDGES
from pgmpy.models import DiscreteBayesianNetwork

truth = build_model()
for n in (100, 1000):
    print(f"N={n}")
    for seed in (1, 2, 3, 4, 5):
        data = truth.simulate(n_samples=n, seed=seed, show_progress=False)
        m = DiscreteBayesianNetwork(EDGES)
        m.fit(data, estimator=DiscreteMLE())
        est = float(m.get_cpds("Rain").values[1, 1])
        print(f"  seed {seed}: P(R=1|C=1) = {est:.3f}")
