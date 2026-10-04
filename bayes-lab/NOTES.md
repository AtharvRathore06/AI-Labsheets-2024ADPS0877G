# Bayes lab - sprinkler network

Run: `python3 queries.py`, `python3 extras.py`   Tests: `python3 -m pytest -q`   Needs `pgmpy>=1.0`.

## Homework: changing the query
`queries.py` builds the network (C -> R, C -> S, R,S -> W) with the specified CPTs and answers each query with `VariableElimination`, then checks it against brute-force enumeration of the 16-row joint.

| Query | Query var | Evidence | Prior | Posterior (pgmpy) | Enumeration |
|---|---|---|---|---|---|
| P(S=1 given W=1) | Sprinkler | WetGrass=1 | 0.300 | 0.4278 | 0.4278 |
| P(C=1 given W=1) | Cloudy | WetGrass=1 | 0.500 | 0.5746 | 0.5746 |
| P(R=1 given W=1, S=0) | Rain | WetGrass=1, Sprinkler=0 | 0.500 | 0.9922 | 0.9922 |

**Predictions before running:**
- Sprinkler should go up: wet grass is more likely when the sprinkler ran. It rose from 0.30 to 0.43, not by much, because rain also explains wet grass.
- Cloudy should rise slightly: wet grass is more likely when it rained, and rain is more likely when cloudy. It rose from 0.50 to 0.57.
- Rain should be near 1 once the sprinkler is ruled out, since rain is then almost the only explanation (a 0.01 chance of wet grass with neither). It is 0.9922.

**Inspecting generated code against a trusted call:** the `VariableElimination` calls in `queries.py` are the trusted reference, and `by_enumeration()` is the independent oracle. The checklist for any generated program: right query variable, right evidence dict (`{"WetGrass": 1}`, not 0), right evidence for the third query (both W=1 and S=0), and a posterior within 1e-10 of the table.

## Classroom exercise: what a WetGrass CPT column means
For `TabularCPD("WetGrass", 2, values, evidence=["Rain","Sprinkler"], evidence_card=[2,2])`, rows are WetGrass = 0 and 1, and the columns enumerate the parents with the **last evidence variable changing fastest**: (R=0,S=0), (R=0,S=1), (R=1,S=0), (R=1,S=1).
Verified against the library (`extras.py`): the stored variable order is `['WetGrass','Rain','Sprinkler']`, and P(W=1) is 0.01 for R=0,S=0; 0.90 for R=0,S=1; 0.90 for R=1,S=0; 0.99 for R=1,S=1, matching the specification.
Because the two middle columns are both 0.90, swapping them would not matter, but the test `test_swapped_wetgrass_columns_change_answer` swaps columns 3 and 4 (an actual mistake) and shows the model still passes `check_model()` yet gives a different posterior, so structural validity does not imply correctness.

## Classroom exercise: different datasets
MLE of P(R=1 given C=1) with N=100 (true value 0.8):

| Seed | Estimate |
|---|---|
| 1 | 0.6939 |
| 2 | 0.7955 |
| 3 | 0.7447 |
| 4 | 0.7679 |
| 5 | 0.7959 |

Mean 0.760, standard deviation 0.043. The differences are sampling variability: each dataset is a different random sample of about 50 cloudy cases, so relative frequencies differ from the true 0.8. It is not an inconsistency in pgmpy or the LLM, and it shrinks as N grows (the lab's sample-size experiment shows this).



