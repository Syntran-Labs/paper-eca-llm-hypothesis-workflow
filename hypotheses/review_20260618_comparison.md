# Hypothesis Review Comparison — Session 2026-06-18

**Batch reviewed:** Rules 59, 115, 25, 67, 97, 41, 83, 27, 107, 121 (top 10 by interest score)
**Prompt used:** `prompts/hypothesis-review.md` v2.0
**Source summaries:** `notebooks/001_ca_rule_space_exploration.ipynb`, Restart & Run All, 2026-06-18

---

## Models compared

| | Model A | Model B |
|---|---|---|
| **File** | `review_20260618_eca01.json` | `review_20260618_001.json` |
| **Model** | ChatGPT 5.5 (high thinking) | Claude Opus 4.8 Max |
| **Hypotheses** | 6 | 3 |
| **Schema valid on delivery** | Yes | No — missing `status` field (corrected before saving) |

---

## What both models found

Both identified independently that the ten rules cluster into five near-identical pairs:

| Pair | Observation |
|---|---|
| 59 / 115 | Metrics match to 4–5 decimal places |
| 25 / 67 | Metrics match to 4–5 decimal places |
| 97 / 41 | Metrics match to 4–5 decimal places |
| 83 / 27 | Metrics match to 4–5 decimal places |
| 107 / 121 | Match on activity and density_mean but diverge on density_final and compression_ratio (~1.5x gap) |

Both flagged 107/121 as the anomalous pair.

---

## How they differed

### ChatGPT: empirical persistence testing

ChatGPT treated the pairings as observations and asked: *do they survive a change of conditions?*

- h001–h002: test if 59/115 and 83/27 stay similar under random initial conditions (20-seed sweep)
- h003: test if rank ordering of 97/41 vs 25/67 survives doubling n_steps
- h004: test if 107/121 divergence persists under random IC
- h005: test if 83/27 similarity survives switching to periodic boundary (**blocked — periodic boundary not implemented in v1**)
- h006: test if all 6 top rules stay non-periodic on a larger grid

All hypotheses are directly testable with current tooling except h005.

**ChatGPT's strength:** quantitative thresholds (e.g. "mean absolute difference < 0.01"), multi-seed sweep design, coverage of more rule groups.

---

### Claude Opus: structural mechanism identification

Claude asked: *why are the pairs similar?* and proposed a structural explanation before designing tests.

**h001 — Mirror equivalence hypothesis:**
The pairs are reflection-equivalent rules: swapping neighborhood outputs for `110↔011` and `100↔001` maps one rule to the other. Row-level metrics are reflection-invariant by construction, so identical pairs are *predicted* by the rule encoding — not anomalous. The residual differences exist because the seed lands at position `n_cells // 2 = 50` on a 100-cell (even) grid, which is *off-center*. On an odd grid (`n_cells=101`), `101 // 2 = 50` is the true center, so within-pair differences should collapse to ~0.

This is verifiable directly in `simulator.py:61` — `state[n_cells // 2] = 1`.

**h002 — Why 107/121 diverges more than other pairs:**
If mirror equivalence holds, the 107/121 gap (1.5× compression_ratio, density_final 0.4 vs 0.52) must be a larger off-center artifact for those specific rules. Test: run at n_cells=101 and n_cells=401 and check whether the gap shrinks toward the ~0.001 level of the other pairs.

**h003 — Odd-rule period-2 background oscillation:**
All 10 rule numbers are odd, meaning each maps `000→1`. Combined with `111→0` (also derivable from odd rule numbers), any large uniform region flips every step. Prediction: `density_final` at step 201 should differ substantially from step 200 (anti-correlated swing ≥ 0.2). Test: re-run with `n_steps=201` and compare.

**Claude's strength:** identified the structural reason for all pairings in a single insight, proposed a test that is more informative (one run at n_cells=101 validates or falsifies mirror equivalence for all five pairs simultaneously).

---

## Reviewer assessment

### Best hypothesis to run first

**Claude h001** (mirror equivalence, odd grid test).

One simulation call per rule at `n_cells=101` either confirms that all four tight pairs collapse to ~0 difference and 107/121 diverges more — or it doesn't. If it confirms, we have a structural classification principle for the entire 256-rule space. If it doesn't, we learn that fixed_zero boundary effects are stronger than the symmetry.

This is more informative per compute cost than the 20-seed random IC sweeps in ChatGPT h001/h002/h004.

### Second priority

**Claude h003** (period-2 density oscillation). Requires only one extra step per rule — trivial to run.

### Third priority

**ChatGPT h003** (rank ordering stability at n_steps=400). Tests a different dimension (temporal stability) that Claude did not address.

### h005 status

ChatGPT h005 (periodic boundary) is `inconclusive` — marked as such in the saved file. Periodic boundary is not in v1. It becomes executable if `simulate()` adds a `periodic` boundary mode.

---

## Schema notes

- ChatGPT response was schema-valid on delivery.
- Claude response was missing `"status": "proposed"` on all three hypotheses. Added before saving.
- Claude's `review_notes` field (optional in schema) contains a useful session-level summary — preserved as-is.

---

## Suggested next step

Run Claude h001 and h003 in a new notebook cell, compare paired metric differences at n_cells=101 vs n_cells=100, and record the outcome as the first completed hypothesis test in this project.
