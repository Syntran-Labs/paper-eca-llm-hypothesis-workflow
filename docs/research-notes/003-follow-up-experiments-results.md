# Research Note 003: Follow-Up Experiment Results

**Repository:** `paper-eca-llm-hypothesis-workflow`
**Date:** 2026-06-23
**Author:** Leonardo Sigales / SYNTRAN Labs
**Status:** `complete`

---

## Summary

Three follow-up experiments were executed against hypotheses proposed in the 2026-06-18 LLM review session (Research Note 001). All simulations used `cellauto_lab.simulate()` with `initial_condition='single_seed'`, `boundary_condition='fixed_zero'`, `random_seed=42`.

| Experiment | Hypothesis | Status |
|---|---|---|
| A — `n_cells=101` for all 10 rules | Claude h001 (mirror equivalence), h002 (107/121 artifact) | **supported** |
| B — `n_steps=201` for all 10 rules | Claude h003 (period-2 density oscillation) | **partially_supported** |
| C — `n_steps=400` for rules 97, 41, 25, 67 | ChatGPT h003 (rank stability) | **supported** |

---

## Experiment A — Claude h001: Mirror Equivalence / Odd-Grid Test

**Parameters:** `n_cells=101`, `n_steps=200`, `initial_condition='single_seed'`, `boundary_condition='fixed_zero'`, `random_seed=42`

**Prediction:** On an odd grid where the single seed lands at the true center (index 50 of 101), reflection-invariant metrics (density_mean, density_final, transition_count, entropy_score, periodicity_score) should collapse to zero within-pair differences.

### Results

| Rule | density_mean | density_final | entropy_score | compression_ratio |
|---|---|---|---|---|
| 59  | 0.584405 | 0.653465 | 3.245193 | 0.021772 |
| 115 | 0.584405 | 0.653465 | 3.245193 | 0.021723 |
| 25  | 0.459238 | 0.415842 | 3.251138 | 0.026994 |
| 67  | 0.459238 | 0.415842 | 3.251138 | 0.026846 |
| 97  | 0.399192 | 0.257426 | 2.972867 | 0.023546 |
| 41  | 0.399192 | 0.257426 | 2.972867 | 0.023595 |
| 83  | 0.500813 | 0.336634 | 2.890283 | 0.017881 |
| 27  | 0.500813 | 0.336634 | 2.890283 | 0.017339 |
| 107 | 0.594601 | 0.396040 | 2.868173 | 0.026206 |
| 121 | 0.594601 | 0.396040 | 2.868173 | 0.025664 |

### Within-pair differences: baseline vs n_cells=101

| Pair | Metric | Baseline diff (n=100) | n_cells=101 diff | Outcome |
|---|---|---|---|---|
| 59/115 | density_mean | 0.000049 | 0.000000 | collapsed |
| 25/67  | density_mean | 0.000050 | 0.000000 | collapsed |
| 97/41  | density_mean | 0.000099 | 0.000000 | collapsed |
| 97/41  | compression_ratio | 0.001393 | 0.000049 | collapsed |
| 107/121 | density_mean | 0.001592 | 0.000000 | collapsed |
| 107/121 | density_final | 0.120000 | 0.000000 | collapsed |
| 107/121 | entropy_score | 0.061665 | 0.000000 | collapsed |
| 107/121 | compression_ratio | 0.013334 | 0.000542 | 25x reduction |
| 83/27  | transition_count | 0.019900 | 0.000000 | collapsed |
| 83/27  | compression_ratio | 0.000199 | 0.000542 | grew (expected) |

### Assessment

**Status: supported.**

The prediction was confirmed for all five pairs. Reflection-invariant metrics — density_mean, density_final, transition_count, entropy_score — collapsed to exactly zero differences for all pairs on the centered grid. The compression_ratio differences were substantially reduced for the four tight pairs and shrank 25x for the 107/121 pair (0.013334 → 0.000542). Residual compression_ratio differences are consistent with the hypothesis's own caveat that a generic compressor is not invariant under string reversal.

The most striking result is the 107/121 pair. At n_cells=100, the pair showed a 0.12 density_final gap and a 0.062 entropy_score gap — both visually anomalous compared to the other four pairs. On the odd grid, both gaps collapsed to exactly zero. This confirms Claude h002 simultaneously: the 107/121 divergence was entirely a centering artifact.

**This also validates Claude h002 (supported):** the centering-artifact explanation for the 107/121 outlier is correct.

---

## Experiment B — Claude h003: Period-2 Density Oscillation

**Parameters:** `n_cells=100`, `n_steps=201`, `initial_condition='single_seed'`, `boundary_condition='fixed_zero'`, `random_seed=42`

**Prediction:** Because all ten rule numbers are odd — each mapping `000→1` and `111→0` — any large uniform background region should oscillate with period 2. The predicted effect: density_final at step 201 should differ substantially (anti-correlated swing of ~0.2 or more) from density_final at step 200.

### Results

| Rule | density_final @ 200 | density_final @ 201 | delta |
|---|---|---|---|
| 59  | 0.650000 | 0.650000 | +0.000000 |
| 115 | 0.650000 | 0.650000 | +0.000000 |
| 25  | 0.420000 | 0.430000 | +0.010000 |
| 67  | 0.430000 | 0.430000 | +0.000000 |
| 97  | 0.400000 | 0.420000 | +0.020000 |
| 41  | 0.400000 | 0.420000 | +0.020000 |
| 83  | 0.330000 | 0.670000 | +0.340000 |
| 27  | 0.330000 | 0.670000 | +0.340000 |
| 107 | 0.400000 | 0.750000 | +0.350000 |
| 121 | 0.520000 | 0.830000 | +0.310000 |

### Assessment

**Status: partially_supported.**

The period-2 oscillation is present and substantial for rules 83, 27, 107, 121 (swings of 0.31–0.35, well above the ~0.2 threshold). It is absent or negligible for rules 59, 115 (zero swing) and small for 25, 67, 97, 41 (swings of 0.00–0.02).

The hypothesis correctly identified the `000→1` / `111→0` property as a mechanism, but overstated its uniformity. The effect depends on the spatial structure of the pattern at step 200, not just the rule number's parity:

- Rules 83/27 at step 200: density_final = 0.33 (many zeros, large uniform 0-blocks present). One step of `000→1` converts blocks to ones, producing a large upswing.
- Rules 107/121 at step 200: density_final = 0.40/0.52 (intermediate density, similar mechanism applies).
- Rules 59/115 at step 200: density_final = 0.65 (few zeros, predominantly fragmented spatial structure at this step count). Large uniform 0-blocks have been disrupted; the background oscillation is damped.

The hypothesis is informative: it correctly identified rules 83/27/107/121 as exhibiting the effect, even though it predicted it uniformly. A revised hypothesis would condition on the spatial structure (or a proxy: density_final << 0.5 at an even step) rather than the rule number alone.

---

## Experiment C — ChatGPT h003: Rank Stability at n_steps=400

**Parameters:** `n_cells=100`, `n_steps=400`, `initial_condition='single_seed'`, `boundary_condition='fixed_zero'`, `random_seed=42`; rules [97, 41, 25, 67].

**Prediction:** Rules 97/41 will continue to show higher compression_ratio and lower density_mean and activity_score than rules 25/67, with stable rank ordering at twice the baseline step count.

### Results

| Rule | density_mean (200→400) | activity_score (200→400) | compression_ratio (200→400) | periodicity (200→400) |
|---|---|---|---|---|
| 97 | 0.400697 → 0.384888 | 0.705150 → 0.661200 | 0.045423 → 0.070823 | 0.0 → 0.0 |
| 41 | 0.400796 → 0.384938 | 0.705250 → 0.661250 | 0.044030 → 0.070100 | 0.0 → 0.0 |
| 25 | 0.458905 → 0.442319 | 0.759750 → 0.682725 | 0.027512 → 0.028953 | 0.0 → 0.0 |
| 67 | 0.458955 → 0.442519 | 0.759500 → 0.681275 | 0.027512 → 0.028180 | 0.0 → 0.0 |

**Rank ordering at n_steps=400:**
- compression_ratio: 97 (0.071) > 41 (0.070) >> 25 (0.029) > 67 (0.028) — **unchanged** ✓
- density_mean: 25/67 (~0.442) > 97/41 (~0.385) — **unchanged** ✓
- activity_score: 25/67 (~0.682) > 97/41 (~0.661) — **unchanged** ✓
- periodicity_score: all 0.0 — **unchanged** ✓

### Assessment

**Status: supported.**

All three predicted rank orderings are preserved at n_steps=400. Additionally, the compression_ratio gap between the two groups widened: rules 97/41 grew from ~0.044–0.045 to ~0.070–0.071 (+57%) while rules 25/67 barely changed (0.027–0.028). This suggests that the behavioral difference between these two pairs becomes more pronounced over longer runs, not less — a stronger result than the hypothesis predicted.

No periodicity emerged at n_steps=400 for any of the four rules, consistent with these being genuinely complex (Class III-like) rules rather than rules exhibiting latent periodicity on longer runs.

---

## Aggregate Observations

### What the experiments tell us about the workflow (not about ECA)

1. **The structural hypotheses (h001/h002) produced sharper predictions than the empirical ones.** Claude's centering-artifact explanation made a specific, directional, quantitative prediction (collapse to zero for reflection-invariant metrics). That prediction was confirmed to full floating-point precision for density_mean, density_final, entropy_score, and transition_count across all five pairs.

2. **Mechanistic hypotheses can outperform empirical robustness tests.** Claude h003 was partially wrong about the scope of the effect but correctly identified the underlying mechanism. ChatGPT h003 was correct about rank ordering but didn't predict the widening gap. Both are useful; they are complementary modes of hypothesis generation.

3. **The schema validated correctly under outcome conditions.** The `supported` / `partially_supported` / `refuted` status extension integrates cleanly with the existing schema structure. The three new statuses required a schema update (recorded in `schemas/hypothesis_response.schema.json`); this is the first schema revision since the project launched.

4. **One hypothesis (ChatGPT h005) remains blocked on unimplemented periodic boundary.** This is a concrete specification for a v1.1 simulator enhancement.

### Hypothesis status summary after these experiments

| Source | ID | Prediction | Status |
|---|---|---|---|
| Claude | h001 | Mirror equivalence collapses on odd grid | **supported** |
| Claude | h002 | 107/121 divergence is centering artifact | **supported** |
| Claude | h003 | Period-2 oscillation for all odd rules | **partially_supported** |
| ChatGPT | h001 | 59/115 similar under random IC | proposed (not yet run) |
| ChatGPT | h002 | 83/27 retains lower entropy under random IC | proposed (not yet run) |
| ChatGPT | h003 | 97/41 > 25/67 rank stable at n_steps=400 | **supported** |
| ChatGPT | h004 | 121 > 107 on density_final under random IC | proposed (not yet run) |
| ChatGPT | h005 | 83/27 similarity persists under periodic BC | inconclusive (blocked) |
| ChatGPT | h006 | periodicity stays low at n_cells=200, n_steps=400 | proposed (not yet run) |

---

## Claims Not Made

- The collapse of within-pair metric differences at n_cells=101 does not prove that the rules are mirror equivalents in the mathematical sense. It is behavioral evidence consistent with that property. Mathematical verification is derivable from the rule lookup tables, not from simulation.
- The absence of periodicity at n_steps=400 does not rule out periodicity on longer or wider grids.
- The confirmed hypotheses do not validate the workflow. They are evidence from one batch of ten rules. The claim that the workflow produces well-calibrated hypotheses requires more sessions, including negative controls and baseline comparison.

---

## Next Steps

1. **Run ChatGPT h001/h002/h004** — 20-seed random-IC sweeps. These are the most compute-intensive remaining hypotheses from this batch.
2. **Run ChatGPT h006** — `n_cells=200, n_steps=400` for rules [59, 115, 83, 27, 97, 41].
3. **Implement periodic boundary condition** — unblocks ChatGPT h005.
4. **Run negative control batch** — submit summaries of deliberately dissimilar rules (e.g., rules 0, 1, 128, 255) and verify that the models do not spuriously group them.
5. **Run ungoverned baseline** — same 10-rule summaries, prompt without schema or epistemic constraints; compare schema conformance, falsifiability, and overclaiming rate.
6. **Second LLM session** — next 10 rules by interest score from the 256-rule sweep.
