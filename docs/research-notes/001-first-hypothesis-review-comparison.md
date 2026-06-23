# Research Note 001: First LLM Hypothesis Review Comparison

**Repository:** `cellauto-lab`
**Date:** 2026-06-18
**Author:** Leonardo Sigales / SYNTRAN Labs
**Status:** `draft — experiment-pending`

---

## Summary

On 2026-06-18, the same structured experiment summary batch — the top 10 rules by heuristic interest score from the full 256-rule ECA sweep — was submitted to two LLMs using the prompt template in [`prompts/hypothesis-review.md`](../../prompts/hypothesis-review.md). The two models were:

- **ChatGPT o3** (high thinking mode) — response file: [`hypotheses/review_20260618_eca01.json`](../../hypotheses/review_20260618_eca01.json)
- **Claude Opus 4.8 Max** — response file: [`hypotheses/review_20260618_001.json`](../../hypotheses/review_20260618_001.json)

Both models, independently and without knowledge of the other's response, identified the same dominant structure in the batch: the ten rules cluster into five near-identical pairs.

This note documents what each model found, how their approaches differed, what hypotheses remain to be tested, and what the result says about the workflow — not about ECA behavior.

---

## Research Context

The primary research question driving this project is:

> Can an LLM-assisted workflow systematically explore the 256 ECA rules, measure emergent behavioral properties, generate structured summaries, and support falsifiable hypothesis generation — while maintaining reproducibility, auditability, and honest epistemic standards?

See [`docs/research-question.md`](../research-question.md) for full scope.

Elementary cellular automata are used as a controlled testbed because the behavioral ground truth is largely known, the rule space is finite, and overclaiming is easy to detect. The current artifact is about **method behavior** — whether the workflow produced disciplined, falsifiable, schema-conformant output — not about a claim of new ECA discovery.

---

## Source Artifacts Reviewed

| Artifact | Role in this note |
|---|---|
| [`hypotheses/review_20260618_eca01.json`](../../hypotheses/review_20260618_eca01.json) | ChatGPT hypothesis response (6 hypotheses) |
| [`hypotheses/review_20260618_001.json`](../../hypotheses/review_20260618_001.json) | Claude Opus hypothesis response (3 hypotheses + review_notes) |
| [`hypotheses/review_20260618_comparison.md`](../../hypotheses/review_20260618_comparison.md) | Human reviewer analysis written before this note |
| [`prompts/hypothesis-review.md`](../../prompts/hypothesis-review.md) | Prompt template used for both submissions |
| [`schemas/hypothesis_response.schema.json`](../../schemas/hypothesis_response.schema.json) | Schema used to validate responses |
| [`docs/methodology.md`](../methodology.md) | Simulation parameters and metric definitions |

The summaries submitted covered rules 59, 115, 25, 67, 97, 41, 83, 27, 107, and 121 — the top 10 rules ranked by a heuristic interest score combining `entropy_score`, `activity_score`, and `compression_ratio`. All simulations used `n_cells=100`, `n_steps=200`, `initial_condition='single_seed'`, `boundary_condition='fixed_zero'`, `random_seed=42`.

---

## What Both Models Found

### Five near-identical rule pairs

Both models identified independently that the ten rules form five pairs with near-matching metrics:

| Pair | Key shared metrics |
|---|---|
| 59 / 115 | `density_mean` 0.5851 vs 0.5851, `transition_count` both 35.33, `entropy_score` both 3.2435 |
| 25 / 67 | `density_mean` 0.4589 vs 0.4590, `entropy_score` both 3.2273 |
| 97 / 41 | `density_mean` 0.4007 vs 0.4008, `entropy_score` both 3.1706 |
| 83 / 27 | `density_mean` both 0.5008, `entropy_score` both 2.9073, `density_final` both 0.33 |
| 107 / 121 | `activity_score` 0.6929 vs 0.6921, `density_mean` 0.5953 vs 0.5969 |

### The 107/121 pair as anomalous

Both models flagged 107/121 as the outlier pair: its metrics match on `activity_score` and `density_mean` but diverge substantially on `density_final` (0.40 vs 0.52), `entropy_score` (2.883 vs 2.821), and `compression_ratio` (0.027 vs 0.040 — a ~1.5× difference). The other four pairs match to 3–5 decimal places on most metrics.

### No evidence of periodicity in this batch

All ten rules showed `periodicity_score = 0.0` under the baseline conditions. Both models noted this and incorporated it into their hypotheses without treating it as conclusive.

---

## How The Models Differed

### ChatGPT o3: empirical persistence testing

ChatGPT produced 6 hypotheses, each asking whether an observed pattern survives a parameter change:

- **h001, h002, h004:** Do the pairings hold under random initial conditions, tested across 20 seeds?
- **h003:** Does the rank ordering between the two sub-groups (97/41 vs 25/67) hold when `n_steps` is doubled to 400?
- **h005:** Does the 83/27 similarity persist under a periodic boundary condition?
- **h006:** Do all six top rules remain non-periodic on a larger grid (`n_cells=200, n_steps=400`)?

ChatGPT's hypotheses include quantitative thresholds (e.g., "mean absolute difference < 0.01 for `density_mean`") and multi-seed sweep designs. All hypotheses were schema-conformant on delivery. h005 is currently blocked because `boundary_condition='periodic'` is not implemented in v1 (see [`README.md`](../../README.md) known limitations); it is stored with status `inconclusive`.

### Claude Opus 4.8 Max: structural mechanism identification

Claude produced 3 hypotheses and a `review_notes` field summarizing the session.

**h001 — Mirror equivalence and the odd-grid test:**
Claude proposed that the five pairs are *reflection-equivalent rules* — rules whose neighborhood lookup tables are related by swapping the outputs for mirrored neighborhoods (110↔011, 100↔001). Under this framing, the near-equality of row-level metrics is *expected*, not anomalous, because reflection-invariant metrics (density, transition count, entropy, periodicity) are unchanged when a space-time diagram is horizontally reversed. The residual differences visible in the current data are attributed to the seed falling at index `n_cells // 2 = 50` on a 100-cell (even) grid — slightly off-center. On an odd grid (`n_cells=101`), the seed lands at the true center, and paired metric differences should collapse toward zero.

This is verifiable directly in [`src/cellauto_lab/simulator.py`](../../src/cellauto_lab/simulator.py) line 61: `state[n_cells // 2] = 1`.

**h002 — Why 107/121 diverges more:**
If mirror equivalence is the underlying structure, the 107/121 gap (1.5× `compression_ratio`, 0.12 `density_final` difference) must be a larger off-center artifact for those two specific rules than for the other four pairs. Testing at `n_cells=101` should either shrink the gap to the ~0.001 level of the other pairs (centering artifact confirmed) or leave it persistent (something else is driving the difference).

**h003 — Period-2 density oscillation from odd rule numbers:**
All ten rule numbers are odd, which means each maps neighborhood `000→1`. Combined with the derivable consequence that each also maps `111→0`, any large uniform background region should oscillate with period 2 between all-0 and all-1. Claude predicted that `density_final` at `n_steps=201` should differ substantially from `density_final` at `n_steps=200` (anti-correlated swing of ~0.2 or more), while `density_mean` stays stable near 0.5. This requires only one additional simulation step per rule.

**Schema note:** Claude's response was missing `"status": "proposed"` on all three hypotheses — a schema violation. The field was added before saving. This is recorded here as a process observation, not a criticism of the model.

---

## Epistemic Assessment

### Why this is not a cellular automata discovery

The five rule pairs correspond to known ECA reflection symmetries. ECA rules come in equivalence classes under complement (flipping all 0s and 1s) and reflection (mirroring the neighborhood). These symmetries reduce the 256 distinct rules to 88 equivalence classes (see Wolfram, *A New Kind of Science*, 2002; and Riedel & Zenil, arXiv:1802.08769, 2018 — both in [`docs/references.md`](../references.md)). The fact that metrics of reflection-equivalent rules are similar under symmetric initial conditions is a consequence of this well-documented structure, not a new finding.

What is observable about the method:

- Both models, given only metric data, recovered structure that corresponds to a known mathematical property of ECA rule encoding.
- Neither model cited external literature, as the prompt instructed.
- The governance layer (structured prompt, schema validation, human review step) prevented the observation from being stated as a discovery before it could be verified.
- The workflow produced structured, falsifiable hypotheses that point at concrete follow-up simulations.
- One model (Claude) proposed a structural explanation; the other (ChatGPT) proposed empirical robustness checks. These are complementary, not competing.

### What the metrics can and cannot support

- `compression_ratio` is a proxy for descriptive regularity, not Kolmogorov complexity. See [`docs/methodology.md`](../methodology.md).
- `entropy_score` is computed from row-level density distributions; it misses spatial block structure within rows.
- `periodicity_score = 0.0` for all ten rules does not mean these rules have no periodic behavior — it means no consecutive identical rows were detected after the transient under these specific conditions.
- A single `single_seed` initial condition is insufficient to characterize typical rule behavior.

---

## Best Next Hypotheses To Execute

Ranked by informativeness per compute cost:

### 1. Claude h001 — Mirror equivalence / odd-grid test (highest priority)

```python
# For each rule R in [59, 115, 25, 67, 97, 41, 83, 27, 107, 121]:
simulate(R, n_cells=101, n_steps=200, initial_condition='single_seed',
         boundary_condition='fixed_zero', random_seed=42)
```

One simulation call per rule. If within-pair metric differences collapse toward zero for the four tight pairs and remain large for 107/121, this supports the mirror-equivalence centering-artifact explanation for the entire batch simultaneously.

### 2. Claude h003 — Period-2 density swing (trivial cost)

```python
# For each rule R in the batch:
simulate(R, n_cells=100, n_steps=201, initial_condition='single_seed',
         boundary_condition='fixed_zero', random_seed=42)
# Compare density_final at n_steps=201 vs n_steps=200
```

One additional step per rule. Tests the odd-rule period-2 oscillation prediction directly.

### 3. ChatGPT h003 — Temporal stability at n_steps=400

```python
# For rule_number in [97, 41, 25, 67]:
simulate(R, n_cells=100, n_steps=400, initial_condition='single_seed',
         boundary_condition='fixed_zero', random_seed=42)
```

Tests whether the rank ordering between 97/41 and 25/67 is stable over longer runs.

### 4. ChatGPT h001/h002/h004 — Random seed sweeps

20-seed sweeps for pairs 59/115, 83/27, and 107/121 under random initial conditions. Higher compute cost; most useful after the low-cost structural tests above have been run.

### Blocked

ChatGPT h005 (periodic boundary) is `inconclusive` until `boundary_condition='periodic'` is implemented in [`src/cellauto_lab/simulator.py`](../../src/cellauto_lab/simulator.py).

---

## Claims Not Made

This note explicitly does not claim:

- Discovery of new ECA behavior. Rule pairing by reflection equivalence is documented in the ECA literature.
- That any LLM proved mirror equivalence. Both models proposed hypotheses based on metric patterns; neither proved anything.
- That `compression_ratio` or `entropy_score` measure true algorithmic complexity.
- That the workflow is validated. This is the first session; one batch is not a validation.
- That these results are publication-ready as cellular automata research.
- That Claude Opus is a better research assistant than ChatGPT o3, or vice versa. The outputs are complementary.

---

## What Would Make This Stronger

- Execute h001 and h003 and store metric outputs as artifacts.
- Update hypothesis statuses in the JSON files (`proposed` → `supported` or `rejected`) based on results.
- Add a negative control: submit a batch of rules known to be behaviorally dissimilar and verify that the models do not spuriously group them.
- Repeat the full session on a second batch of rules (e.g., the next 10 by interest score).
- Compare the prompt's schema rejection rate across models and sessions.
- Run an ungoverned baseline (same summaries, no schema, no constraint rules) and compare output quality.

---

## Gaps and Limitations

- No simulation experiments have been run yet for any hypothesis in this note. All findings are based on a single baseline run and LLM inference.
- The comparison is between exactly two models in one session. Variance across sessions has not been measured.
- The human review step (applying `docs/hypothesis-quality-checklist.md`) has not been fully documented for this batch. The statuses assigned reflect a first-pass assessment.
- `docs/references.md` includes references to ECA symmetry work (Riedel & Zenil 2018) but the connection between that literature and the mirror-equivalence observation has not been formally checked.

---

## Next Step

Execute Claude h001 (odd-grid test at `n_cells=101`) and Claude h003 (period-2 density swing at `n_steps=201`). Record outputs. Update hypothesis statuses. Write a follow-up note recording results.
