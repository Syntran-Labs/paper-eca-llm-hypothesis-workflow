# Methodology

**Repository:** `paper-eca-llm-hypothesis-workflow`
**Status:** Active

---

## Overview

`cellauto-lab` uses a notebook-first, metrics-driven methodology for exploring elementary cellular automata (ECA) rule space. The methodology is designed to be:

- **Reproducible**: all experiments use explicit parameters, fixed random seeds, and recorded metadata
- **Auditable**: observations, metrics, and interpretations are stored separately
- **Honest**: no claims beyond what the simulation evidence supports
- **LLM-ready**: structured summaries are designed for later LLM review, with explicit placeholders

---

## Simulation Design

### Grid Parameters

| Parameter | v1 Default | Rationale |
|---|---|---|
| `n_cells` | 100 | Wide enough to observe bulk behavior; fits standard display |
| `n_steps` | 200 | Enough to pass transients for most rules |
| `boundary_condition` | `fixed_zero` | Simplest and most common; avoids wrap-around artifacts |
| `initial_condition` | `single_seed` | Deterministic; reveals rule symmetry clearly |
| `random_seed` | 42 | Fixed for reproducibility when random IC is used |

### Wolfram Rule Encoding

Rule numbers use the canonical Wolfram encoding:

- Neighborhood `(left, center, right)` has index value `left × 4 + center × 2 + right`
- Bit `i` of the rule number determines the output for neighborhood with index `i`
- Ordering: `111` (index 7) down to `000` (index 0)

This is verified by smoke tests against known rules (0, 30, 90, 110, 184, 255).

---

## Metrics

Seven primary metrics are computed from the space-time matrix (shape: `n_steps + 1` × `n_cells`):

| Metric | What It Measures | Interpretation Limit |
|---|---|---|
| `density_mean` | Average fraction of 1s across all time steps | Does not distinguish spatial from temporal structure |
| `density_final` | Fraction of 1s at the last time step | Sensitive to transient length |
| `transition_count` | Mean horizontal state changes per row | Measures spatial fragmentation; misses temporal patterns |
| `activity_score` | Fraction of cells that change per time step | Does not capture whether change is patterned or random |
| `entropy_score` | Shannon entropy of row-density distribution | Row-level only; misses spatial block patterns |
| `periodicity_score` | Fraction of consecutive identical rows (post-transient) | Finite-grid cycles may be boundary artifacts |
| `compression_ratio` | Compressed size / raw size | Proxy, not proof, of algorithmic complexity |

All metrics are computed with `zlib` compression and `numpy` vectorized operations. No external statistical libraries are required.

---

## Experiment Loop

```text
1. Configure parameters
2. Simulate all 256 rules
3. Compute metrics for each rule
4. Build results dataframe
5. Rank rules by heuristic interest score
6. Generate structured summaries for top rules
7. Submit summaries to LLM via prompts/hypothesis-review.md (manual)
8. Validate LLM response against schemas/hypothesis_response.schema.json
9. Human operator reviews hypotheses with docs/hypothesis-quality-checklist.md
10. Execute accepted hypotheses as follow-up simulations
11. Record results and update hypothesis statuses
```

Steps 7–11 are documented in [docs/ai-hypothesis-loop.md](ai-hypothesis-loop.md). The first full cycle through all steps was completed on 2026-06-23.

---

## Structured Summary Format

Each experiment summary contains:

```json
{
  "experiment_id": "rule_030_single_seed",
  "timestamp_utc": "...",
  "rule_number": 30,
  "parameters": { ... },
  "observation": "Factual description of what was simulated.",
  "metrics": { ... },
  "interpretation_placeholder": "",
  "hypothesis_placeholder": "",
  "next_experiments_placeholder": []
}
```

The `interpretation_placeholder`, `hypothesis_placeholder`, and `next_experiments_placeholder` fields are intentionally empty in v1. They are designed to be populated by a SYNTRAN AIEOS agent in a future iteration.

---

## Epistemological Discipline

Following the `scientific-research` domain pack:

1. **Observations** and **interpretations** are never mixed in the same field
2. Every behavioral label (e.g., "chaotic", "complex") is marked as **tentative**
3. The interest score used for ranking is a **heuristic proxy**, not a ground truth
4. Single-run results are not treated as conclusive
5. Metric limitations are documented in the [Metrics](#metrics) section above and in [docs/methodology.md](methodology.md)

---

## Limitations

- All results depend on the specific grid size, step count, and initial condition
- `fixed_zero` boundary may introduce edge artifacts in some rules
- The `entropy_score` uses row-level density; block entropy would be more sensitive to spatial structure
- The `periodicity_score` may detect boundary-induced cycles as genuine periodicity
- The `compression_ratio` is a proxy; it does not measure Kolmogorov complexity
- The interest score is a heuristic based on metric combinations; it may rank some rules incorrectly
- Single-seed initial conditions may not represent typical rule behavior
- v1 contains no LLM integration; all interpretation fields are placeholders

---

## Validation

The following tests must pass before any result is accepted:

- `tests/test_rules.py`: rule encoding correctness, including known-value spot checks
- `tests/test_simulator.py`: output shape, binary values, determinism, boundary cases
- `tests/test_metrics.py`: metric keys, value ranges, reproducibility

Run with: `pytest tests/`
