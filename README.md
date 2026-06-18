# cellauto-lab

**Status:** Incubation — private research workspace  
**Project:** SYNTRAN Labs  
**Workflow:** SYNTRAN AIEOS

---

## What Is This?

`cellauto-lab` is a Python/Jupyter research workspace for exploring one-dimensional elementary cellular automata (ECA) — 256 simple rules studied by Stephen Wolfram and others, capable of producing surprisingly complex emergent behavior.

The project is a testbed for a specific methodological question: can an LLM-assisted computational workflow explore a well-understood discrete system in a way that is reproducible, auditable, and epistemically honest?

This is not production software. It is exploratory research infrastructure at an early incubation stage.

---

## Research Question

> Can an LLM-assisted workflow systematically explore the 256 elementary cellular automaton rules, measure emergent behavioral properties, generate structured experiment summaries, and support falsifiable hypothesis generation — while maintaining reproducibility, auditability, and honest epistemic standards?

See [docs/research-question.md](docs/research-question.md) for full scope and success criteria.

---

## Why Cellular Automata?

Elementary cellular automata are ideal for this kind of methodological study because:

1. **The ground truth is known.** Wolfram's four behavioral classes are well-established, giving a reference point for evaluating LLM-assisted classification.
2. **The rule space is finite and small.** All 256 rules can be exhaustively simulated in seconds.
3. **Behavior is visually striking.** Space-time diagrams make patterns immediately interpretable, which helps detect when an LLM overclaims or confabulates.
4. **The domain has known hard problems.** Rule 110's universality is a formal result, not a visual impression — a good test of whether the workflow maintains epistemic discipline.

---

## Why SYNTRAN AIEOS?

This project follows [SYNTRAN AIEOS](https://syntran.io) workflow conventions because:

- Observations and interpretations are stored separately, preventing silent conflation
- All LLM-generated content is marked as such and stored as artifacts, not conclusions
- Human operator authority is explicit: the LLM proposes, the human decides
- Every experiment is governed by pre-declared parameters, seeds, and metadata
- Reproducibility is treated as part of the result, not an afterthought

See [docs/methodology.md](docs/methodology.md) for the full methodology.

---

## How To Run the Notebook

### Prerequisites

```bash
pip install numpy pandas matplotlib jupyter
```

Python 3.11+ is required. No other dependencies.

### Run

```bash
# From the project root
jupyter notebook notebooks/001_ca_rule_space_exploration.ipynb
```

Or with JupyterLab:

```bash
jupyter lab notebooks/001_ca_rule_space_exploration.ipynb
```

The notebook runs fully offline. No internet connection or external credentials are required.

After opening, use **Kernel → Restart & Run All** to ensure a clean run from scratch.

---

## How To Run Tests

```bash
# From the project root
pip install pytest
pytest tests/
```

Tests cover:
- Rule encoding correctness (including known-value spot checks for Rules 30, 90, 110)
- Simulator output shape, dtype, and binary-value guarantees
- Determinism of seeded random initial conditions
- Metric key completeness and value ranges
- Known behavioral corner cases (Rule 0 extinction, Rule 255 saturation)

---

## Project Structure

```
cellauto-lab/
├── README.md
├── .gitignore
├── PUBLICATION_CHECKLIST.md
│
├── domains/                         # Project-local domain packs (SYNTRAN AIEOS)
│   ├── cellular-automata/
│   │   └── profile.md
│   └── scientific-research/
│       └── profile.md
│
├── src/
│   └── cellauto_lab/               # Core Python library
│       ├── __init__.py
│       ├── rules.py                # Wolfram rule encoding
│       ├── simulator.py            # ECA simulator (vectorized)
│       ├── metrics.py              # Behavioral metrics
│       └── reporting.py           # Structured experiment summaries
│
├── notebooks/
│   └── 001_ca_rule_space_exploration.ipynb
│
├── tests/
│   ├── test_rules.py
│   ├── test_simulator.py
│   └── test_metrics.py
│
└── docs/
    ├── research-question.md
    ├── methodology.md
    └── references.md
```

---

## Current Status and Limitations

**What works in v1:**
- Full simulation of all 256 Wolfram ECA rules
- Seven behavioral metrics computed per rule
- Space-time diagram visualization for any rule
- Structured experiment summaries with explicit placeholders for LLM review
- Pytest test suite for core functionality

**Known limitations:**
- Boundary condition: `fixed_zero` only (periodic boundary not yet implemented)
- Initial condition: `single_seed` or `random` (no structured periodic seeds yet)
- Grid size: 100 cells, 200 steps by default (fixed; configurable in-notebook)
- Entropy metric: row-level density only; misses spatial block structure
- Periodicity detection: may pick up boundary-induced cycles
- No LLM integration in v1 — all interpretation fields are placeholders
- Results are sensitive to grid size and step count; finite-size effects are not quantified

---

## Next Steps

The intended progression after v1:

1. **LLM hypothesis review** — Pass structured summaries to a SYNTRAN AIEOS agent for tentative behavioral classification and hypothesis generation.
2. **Initial condition sensitivity** — Run selected rules under multiple random seeds and compare metric distributions.
3. **Boundary sensitivity** — Compare `fixed_zero` vs. `periodic` for candidate rules.
4. **Rule neighborhood search** — Study Hamming-distance neighbors in the rule-number space.
5. **Data quality validation** — Add schema validation for experiment output artifacts.

See [PUBLICATION_CHECKLIST.md](PUBLICATION_CHECKLIST.md) before sharing any results externally.

---

## References

See [docs/references.md](docs/references.md) for the full reference list with source quality labels.

Key foundational references:

- Wolfram, S. "Statistical mechanics of cellular automata," *Reviews of Modern Physics*, 1983.
- Cook, M. "Universality in Elementary Cellular Automata," *Complex Systems*, 2004.
- Langton, C. "Computation at the edge of chaos," *Physica D*, 1990.
