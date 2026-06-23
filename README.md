# cellauto-lab

**Status:** Open — Early Incubation  
**Organization:** [SYNTRAN Labs](https://syntran.io)  
**Workflow:** SYNTRAN AIEOS  
**Branch:** `main` is the current stable snapshot — see [Research Notes](docs/research-notes/) for the full trail

---

## What This Is

`cellauto-lab` is a governed research workspace that investigates one concrete question:

> **Can an LLM-assisted scientific workflow generate falsifiable, non-overclaiming hypotheses — reproducibly?**

We use [elementary cellular automata (ECA)](https://en.wikipedia.org/wiki/Elementary_cellular_automaton) as the testbed: 256 Wolfram rules whose behavioral classes are already well-documented. Because the ground truth is known, we can immediately detect when an LLM overclaims, hallucinates structure, or fails to be falsifiable.

This is **not** a paper about new ECA results. It is an open investigation into whether structured, governed LLM workflows produce meaningfully better scientific reasoning than unstructured prompting on the same task. The target publication is a methods paper.

---

## Why Cellular Automata?

ECA is ideal for evaluating AI-assisted hypothesis generation because:

1. **Ground truth exists.** Wolfram's behavioral classes and known symmetry structures give a reference point to catch confabulation.
2. **The rule space is finite.** All 256 rules can be exhaustively simulated in seconds — no sampling, no approximation.
3. **Overclaiming is detectable.** Claiming Rule 110 "proves" universality from a 200-step simulation is immediately falsifiable.
4. **Results are reproducible.** Fixed seeds, pure functions, NumPy vectorization — anyone can re-run and get the same numbers.

---

## Why SYNTRAN AIEOS?

SYNTRAN AIEOS is the governance layer that makes the methodology rigorous:

- **Observations and interpretations are stored separately** — the LLM never sees mixed signals
- **All LLM output is an artifact, not a conclusion** — stored under `hypotheses/`, labeled, versioned
- **Every hypothesis must pass a quality checklist** before being promoted to `accepted_for_testing`
- **Human authority is explicit** — the LLM proposes, the operator decides, the record is immutable
- **A structured JSON schema** validates every LLM response at submission time
- **A formal prompt template (v2.0)** enforces epistemic constraints before the model sees the data

Without this layer, you get interesting outputs. With it, you get auditable science.

---

## What Is Done

### Simulation engine — complete
- All 256 Wolfram ECA rules simulated via vectorized NumPy
- Two initial conditions: `single_seed`, `random` (seeded, reproducible)
- Fixed-zero boundary condition
- Full space-time grids, configurable size

### Behavioral metrics — complete (7 metrics per rule)
| Metric | What it measures |
|---|---|
| `density_mean` | Average live-cell density across all steps |
| `density_final` | Live-cell density at last step |
| `transition_count` | Spatial fragmentation (cell-state changes per row) |
| `activity_score` | Temporal change rate |
| `entropy_score` | Row-level density distribution shape |
| `periodicity_score` | Cycle detection post-transient |
| `compression_ratio` | Compressibility via zlib (proxy for regularity) |

Each metric has a documented definition, expected range, and known limitations. See [docs/methodology.md](docs/methodology.md).

### Test suite — 119 tests, all passing
- Rule encoding correctness (spot checks for Rules 0, 30, 90, 110, 255)
- Simulator output shape, dtype, binary-value guarantees
- Determinism of seeded random initial conditions
- Metric key completeness and value ranges
- Known behavioral corner cases

### Governance layer — complete
- [Prompt template v2.0](prompts/hypothesis-review.md) — structures the LLM submission with explicit epistemic constraints, known limitations, and output format requirements
- [JSON schema](schemas/hypothesis_response.schema.json) — validates every LLM response at intake (falsifiability fields, metric name enum, confidence level, test plan)
- [Hypothesis quality checklist](docs/hypothesis-quality-checklist.md) — hard blocking criteria (no unverified citations, no causal claims from a single run, must name specific metric and rule, must state direction)

### First LLM review session — complete
On 2026-06-18, the top 10 rules by behavioral interest were submitted independently to two models:

- **Claude Opus 4.8 Max** — 3 hypotheses, schema-conformant
- **ChatGPT o3** — 6 hypotheses, schema-conformant (one schema violation caught and corrected at intake)

**Key result:** Both models independently identified the same structural pattern — 5 near-identical pairs among the 10 rules (59/115, 25/67, 97/41, 83/27, 107/121), with matching metrics to 3–5 decimal places. This corresponds to known ECA reflection-equivalence classes. Neither model cited literature. Both produced falsifiable hypotheses with specific rules, metrics, and predicted directions.

This is a **methodology validation**, not a discovery. The result was expected from known ECA theory. The finding is that the governance layer worked: both models stayed within the epistemic constraints.

Full analysis in [Research Note 001](docs/research-notes/001-first-hypothesis-review-comparison.md). Publication positioning in [Research Note 002](docs/research-notes/002-publication-positioning.md).

---

## What Is Not Done

These are the gaps between current state and any external publication:

| Gap | Why it matters |
|---|---|
| Follow-up experiments not executed | All hypotheses are still `proposed` — none confirmed or refuted |
| Baseline comparison not run | No evidence that governed > unstructured prompting yet |
| Negative controls not designed | Cannot rule out spurious grouping without deliberate dissimilar batches |
| Only one batch, one session | One session is not enough to claim the workflow is reliable |
| Periodic boundary not implemented | Blocks one of the six current hypotheses from being testable |
| No `pyproject.toml` / pinned versions | Reproducibility package incomplete |
| Hypothesis status updates pending | JSON artifacts need `confirmed`/`refuted`/`inconclusive` added |

The project follows an explicit publication ladder (internal notes → GitHub Release → Zenodo DOI → preprint). We are at stage 1. The near-term goal is to complete at least one full execution cycle — run the follow-up experiments, update hypothesis statuses, and write Research Note 003.

---

## How to Run

### Prerequisites

```bash
pip install numpy jupyter pytest
```

Python 3.11+ required. No other dependencies. No API keys. No external credentials.

### Notebook

```bash
jupyter notebook notebooks/001_ca_rule_space_exploration.ipynb
```

Use **Kernel → Restart & Run All** for a clean run. The notebook runs fully offline.

### Tests

```bash
pytest tests/
```

All 119 tests should pass in under 2 seconds.

---

## Project Structure

```
cellauto-lab/
├── README.md
├── PUBLICATION_CHECKLIST.md        Pre-publication sign-off checklist
│
├── src/cellauto_lab/               Core Python library
│   ├── rules.py                    Wolfram rule encoding (0–255)
│   ├── simulator.py                ECA simulator (vectorized NumPy)
│   ├── metrics.py                  7 behavioral metrics
│   └── reporting.py               Structured experiment summaries
│
├── notebooks/
│   └── 001_ca_rule_space_exploration.ipynb
│
├── tests/                          119 pytest tests, all passing
│
├── docs/
│   ├── research-question.md        Scope, motivation, success criteria
│   ├── methodology.md              Simulation design and metric definitions
│   ├── references.md               Annotated bibliography (17 references)
│   ├── ai-hypothesis-loop.md       v2 workflow design (8 stages, manual)
│   ├── hypothesis-quality-checklist.md
│   └── research-notes/
│       ├── 001-first-hypothesis-review-comparison.md
│       └── 002-publication-positioning.md
│
├── prompts/
│   └── hypothesis-review.md        LLM submission prompt template (v2.0)
│
├── schemas/
│   └── hypothesis_response.schema.json   JSON Schema for LLM responses
│
├── hypotheses/                     LLM response artifacts (versioned, labeled)
│   ├── review_20260618_001.json    Claude Opus 4.8 Max — session 1
│   ├── review_20260618_eca01.json  ChatGPT o3 — session 1
│   └── review_20260618_comparison.md
│
└── examples/
    └── hypothesis_response_example.json   Annotated example (not research data)
```

---

## Known Limitations

- **Boundary condition:** `fixed_zero` only — periodic boundary not implemented
- **Grid size:** 100 × 200 default — finite-size effects not quantified
- **Entropy metric:** row-level density only — misses spatial block structure
- **Periodicity score:** may detect boundary-induced cycles, not intrinsic periodicity
- **Single run per configuration** — no multi-seed distributions yet
- **Manual LLM loop** — no API integration; submission is copy-paste by design (v2); automation planned for v3 after validation
- **One session completed** — results are preliminary and should not be interpreted as statistically reliable

---

## Contributing

This is an open research workspace. The artifacts — prompt template, JSON schema, quality checklist, experiment summaries — are designed to be reusable and adaptable.

If you want to follow the investigation as it progresses, watch this repository. Research Notes are the primary trail of decisions and findings.

If you find an issue with the simulation, metrics, or governance logic, open an issue.

---

## References

See [docs/references.md](docs/references.md) for the full annotated bibliography.

Key foundational references:

- Wolfram, S. "Statistical mechanics of cellular automata." *Reviews of Modern Physics*, 1983.
- Cook, M. "Universality in Elementary Cellular Automata." *Complex Systems*, 2004.
- Langton, C. "Computation at the edge of chaos." *Physica D*, 1990.
