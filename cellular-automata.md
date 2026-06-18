# Domain Pack: cellular-automata

Recommended path: `domains/cellular-automata/profile.md`

## Purpose

This domain pack provides the working knowledge needed to design, implement, test, and interpret one-dimensional cellular automata experiments inside SYNTRAN AIEOS.

It is intended for projects such as `syntran-ca-lab`, where Claude Code is used as a governed implementation partner to build reproducible simulations, extract metrics, generate visual artifacts, and support AI-assisted exploration of cellular automata rule spaces.

This domain is not a proof system. It supports exploratory research, reproducible computation, and hypothesis generation.

---

## Use This Domain When

Use `cellular-automata` when the task involves:

- one-dimensional cellular automata
- elementary cellular automata, also called ECA
- Wolfram rules `0-255`
- binary cell states
- local update rules
- rule-space exploration
- emergent behavior
- order, chaos, periodicity, and complexity classification
- simulation metrics
- visualization of space-time diagrams
- AI-guided search over discrete rule systems

---

## Do Not Use This Domain For

Do not use this domain as the primary source for:

- general machine learning model training
- arbitrary agent-based simulation
- physical traffic modeling beyond simple CA analogies
- scientific claims that require empirical validation outside simulation
- proof of universality unless a formal proof is explicitly provided
- production decision systems

For AI-generated hypotheses, pair this domain with `scientific-research`.

---

## Core Definitions

### Cellular Automaton

A cellular automaton is a discrete dynamical system composed of cells. Each cell has a state. Time evolves in discrete steps. At every step, each cell updates according to a local transition rule that depends on nearby cells.

### One-Dimensional Cellular Automaton

A one-dimensional CA is a line of cells updated over time. The full simulation history is usually visualized as a two-dimensional space-time diagram:

- horizontal axis: cell position
- vertical axis: time step
- pixel color: cell state

### Elementary Cellular Automaton

An elementary cellular automaton has:

- one spatial dimension
- binary states: `0` or `1`
- radius `1`
- neighborhood of three cells: `(left, center, right)`
- synchronous update across all cells

There are `2^3 = 8` possible local neighborhoods and `2^8 = 256` possible rules.

### Wolfram Rule Number

The eight neighborhoods are ordered as:

```text
111 110 101 100 011 010 001 000
```

A rule specifies the next center-cell state for each neighborhood. The output bits form an 8-bit binary number. That number is the Wolfram rule ID.

Example:

```text
Rule 110 = 01101110

111 -> 0
110 -> 1
101 -> 1
100 -> 0
011 -> 1
010 -> 1
001 -> 1
000 -> 0
```

---

## Canonical MVP Parameters

Use these defaults unless the project profile says otherwise:

```yaml
ca_type: elementary_cellular_automaton
n_cells: 100
n_steps: 200
states: [0, 1]
radius: 1
boundary_condition: fixed_zero
initial_conditions:
  - single_seed
  - random_seeded
rule_range: 0-255
random_seed_required: true
output_artifacts:
  - space_time_matrix
  - png_visualization
  - metrics_json
  - summary_markdown
```

### Boundary Conditions

Supported boundary conditions should be declared explicitly:

| Boundary condition | Meaning | MVP status |
|---|---|---|
| `fixed_zero` | out-of-range cells are treated as `0` | preferred v1 default |
| `periodic` | first and last cells wrap around | useful for finite-ring experiments |
| `fixed_copy` | edge cells preserve previous value or copy nearest valid cell | optional |

Do not compare experiments using different boundary conditions unless the report clearly states the difference.

---

## Known Reference Rules

These rules are useful for smoke tests, visual sanity checks, and explanatory examples.

| Rule | Expected behavior | Why it matters |
|---:|---|---|
| `0` | all cells become `0` | validates extinction behavior |
| `30` | apparent chaos from simple seed | standard example of simple rule producing complex-looking behavior |
| `90` | nested XOR / Sierpinski-like triangle | validates structured self-similarity |
| `110` | complex localized structures; universal computation known from Cook's proof | validates complex regime handling |
| `184` | particle/traffic-like behavior | useful for flow analogies |
| `255` | all cells become `1` | validates saturation behavior |

Caution: do not claim a simulation of Rule 110 proves universality. Universality is a formal result requiring a specific construction, not a visual impression.

---

## Behavioral Classes

Use these labels as working categories, not formal proof categories:

| Label | Informal meaning | Typical evidence |
|---|---|---|
| `extinct` | pattern dies out | final density near 0 |
| `saturated` | pattern fills with 1s | final density near 1 |
| `fixed` | reaches stable state | activity near 0 after transient |
| `periodic` | repeats over time | detected repeated rows or cycles |
| `nested` | self-similar or triangular structure | predictable geometric pattern |
| `chaotic` | high activity and low obvious repetition | high entropy, weak compression |
| `complex` | mixture of regular background and localized structures | medium entropy, persistent particles, nontrivial compression |
| `ambiguous` | evidence is insufficient or conflicting | metrics disagree or depend strongly on initial condition |

Do not use labels as final truth. Treat them as hypotheses about observed behavior under declared conditions.

---

## Required Metrics

Each experiment should produce a machine-readable metrics record.

Recommended schema:

```yaml
rule_id: int
n_cells: int
n_steps: int
boundary_condition: string
initial_condition: string
random_seed: int|null
density_mean: float
density_final: float
activity_mean: float
transition_count_mean: float
entropy_mean: float
period_detected: bool
period_length: int|null
compression_ratio: float
symmetry_score: float|null
classification_candidate: string
```

### density_mean

Average fraction of cells equal to `1` across the full simulation.

### density_final

Fraction of cells equal to `1` at the final time step.

### activity_mean

Average fraction of cells that change between consecutive time steps.

### transition_count_mean

Average number of horizontal state transitions within each row.

Example:

```text
0001110100 has 3 horizontal transitions
```

### entropy_mean

Approximate binary Shannon entropy of row densities or local block frequencies.

Caution: row-density entropy alone can miss spatial structure. Prefer block entropy when classifying complexity.

### period_detected

Whether a repeated row or repeated recent state sequence is detected after a transient window.

Caution: finite grids can create artificial cycles. Report transient length and detection window.

### compression_ratio

Approximate complexity signal from compressing the space-time matrix serialized as bytes.

Interpretation:

- very compressible: regular, repetitive, or empty
- poorly compressible: irregular or chaotic-looking
- intermediate: potentially structured complexity

Caution: compression is a proxy, not a proof of algorithmic complexity.

### symmetry_score

Optional measure of left/right similarity around the center. Useful for single-seed experiments.

---

## Recommended Experiment Types

### 1. Smoke Test Set

Run:

```text
0, 30, 90, 110, 184, 255
```

Purpose:

- verify rule encoding
- verify visualization
- verify metrics
- provide known reference outputs

### 2. Full ECA Sweep

Run all rules `0-255` under the same conditions.

Purpose:

- create baseline atlas
- compare metric distributions
- identify candidate rules for deeper exploration

### 3. Initial-Condition Sensitivity

For selected rules, compare:

- single center seed
- random seed with fixed RNG seed
- random seed over multiple RNG seeds
- structured periodic seed

Purpose:

- detect whether behavior depends on initial condition
- avoid overclaiming from single-seed visuals

### 4. Boundary Sensitivity

Compare `fixed_zero` and `periodic` boundaries.

Purpose:

- detect finite-size artifacts
- understand whether observed periodicity is boundary-induced

### 5. Rule Neighborhood Search

Compare rules with nearby binary encodings or Hamming-distance neighbors.

Purpose:

- study rule-space locality
- support AI-guided exploration

---

## AI-Guided Rule Exploration

An LLM may be used to propose rule exploration strategies, but it must not be treated as a source of truth.

Allowed LLM roles:

- summarize metric results
- classify observed behavior tentatively
- propose candidate rules for follow-up
- compare hypotheses
- identify contradictions in reports
- generate reproducible experiment plans

Disallowed LLM roles:

- declaring mathematical proof from visual output
- fabricating paper references
- changing metrics without stating rationale
- silently ignoring contradictory results
- treating a single run as conclusive

### Hypothesis Format

Every LLM-generated hypothesis must be falsifiable:

```yaml
hypothesis_id: string
rule_ids: [int]
observations: [facts_only]
metrics_used: [metric_names]
interpretation: string
confidence: 0-100
prediction: string
falsification_test: string
next_experiments: [experiment_specs]
```

---

## Recommended SYNTRAN Invocations

### Architecture design

```text
/synw-agent-architect
/synw-skill-develop

Relevant domains:
- cellular-automata
- scientific-research

Task:
Design the SYNTRAN CA-Lab notebook architecture for exploring elementary cellular automata.

Constraints:
- Jupyter Notebook first.
- 100 binary cells.
- Wolfram rules 0-255.
- Python 3.11+, NumPy, pandas, matplotlib.
- No external CA libraries in v1.
- Separate observation from interpretation.
```

### Simulation implementation

```text
/synw-agent-python-engineer
/synw-skill-develop

Relevant domains:
- cellular-automata

Task:
Implement the ECA rule encoder, simulator, visualization helper, and metrics extractor.

Constraints:
- Python 3.11+.
- Type hints preferred.
- No hardcoded output paths.
- No new dependencies beyond NumPy, pandas, matplotlib.
- Include smoke tests for rules 0, 30, 90, 110, 184, and 255.
```

### Metric validation

```text
/synw-agent-data-quality-tester
/synw-skill-data-quality-test

Relevant domains:
- cellular-automata
- data-ai-testing

Task:
Design validation checks for CA simulation outputs and metrics JSON files.

Constraints:
- Read-only checks.
- Validate schema, value ranges, reproducibility metadata, and missing fields.
```

### Scientific write-up

```text
/synw-agent-technical-writer
/synw-skill-document

Relevant domains:
- cellular-automata
- scientific-research
- documentation

Task:
Write an explanation document describing the CA-Lab experiment design and limitations.

Constraints:
- Audience: technical reader familiar with Python but not necessarily cellular automata.
- Do not overclaim scientific conclusions.
- Include references and limitations.
```

---

## Validation Checklist

Before accepting a CA experiment output:

```text
[ ] Rule number is between 0 and 255.
[ ] Rule table matches Wolfram encoding order.
[ ] Number of cells is recorded.
[ ] Number of steps is recorded.
[ ] Boundary condition is recorded.
[ ] Initial condition is recorded.
[ ] Random seed is recorded when randomness is used.
[ ] Space-time matrix shape is correct.
[ ] Metrics are within expected ranges.
[ ] Visualization matches matrix orientation.
[ ] Classification is labeled as tentative.
[ ] Hypotheses include falsification tests.
[ ] Sources are listed when claims reference known literature.
```

---

## Risk Register

| Risk | Severity | Mitigation |
|---|---:|---|
| Wrong Wolfram bit ordering | High | Test known rules and document neighborhood order |
| Overclaiming from visual patterns | High | Separate observation, interpretation, and proof |
| Boundary artifacts mistaken for intrinsic behavior | Medium | Compare `fixed_zero` vs `periodic` for selected rules |
| Single initial condition bias | Medium | Run multiple initial conditions for candidate rules |
| LLM hallucinated citations | High | Require public source URL or DOI for every reference |
| Metric proxy misuse | Medium | Explain metric limitations in every report |
| Non-reproducible random runs | Medium | Require RNG seed in output metadata |
| Notebook state contamination | Medium | Provide restart-and-run-all validation |

---

## Public References

### Foundational cellular automata

1. Stephen Wolfram, "Statistical mechanics of cellular automata," *Reviews of Modern Physics*, 55, 601-644, 1983. DOI: https://doi.org/10.1103/RevModPhys.55.601
2. Stephen Wolfram, *A New Kind of Science*, Wolfram Media, 2002. Public site: https://www.wolframscience.com/nks/
3. Wolfram MathWorld, "Elementary Cellular Automaton." https://mathworld.wolfram.com/ElementaryCellularAutomaton.html
4. Stanford Encyclopedia of Philosophy, "Cellular Automata." https://plato.stanford.edu/entries/cellular-automata/
5. Wolfram Atlas of Simple Programs, "Elementary Cellular Automata." https://atlas.wolfram.com/01/01/

### Rule 110 and computational universality

6. Matthew Cook, "Universality in Elementary Cellular Automata," *Complex Systems*, 15(1), 1-40, 2004. DOI: https://doi.org/10.25088/ComplexSystems.15.1.1
7. Matthew Cook, "A Concrete View of Rule 110 Computation," arXiv:0906.3248, 2009. https://arxiv.org/abs/0906.3248

### Edge of chaos and evolved cellular automata

8. Christopher G. Langton, "Computation at the edge of chaos: Phase transitions and emergent computation," *Physica D*, 42(1-3), 12-37, 1990. DOI: https://doi.org/10.1016/0167-2789(90)90064-V
9. Melanie Mitchell, Peter T. Hraber, and James P. Crutchfield, "Revisiting the Edge of Chaos: Evolving Cellular Automata to Perform Computations," arXiv:adap-org/9303003, 1993. https://arxiv.org/abs/adap-org/9303003
10. James P. Crutchfield, Melanie Mitchell, and Rajarshi Das, "The Evolutionary Design of Collective Computation in Cellular Automata," arXiv:adap-org/9809001, 1998. https://arxiv.org/abs/adap-org/9809001
11. Melanie Mitchell, "Evolving Cellular Automata with Genetic Algorithms: A Review of Recent Work." https://csc.ucdavis.edu/~evca/Papers/evca-review.html

### Classification and complexity

12. Genaro J. Martinez, "A Note on Elementary Cellular Automata Classification," arXiv:1306.5577, 2013. https://arxiv.org/abs/1306.5577
13. Pierre-Etienne Meunier, "Unraveling simplicity in elementary cellular automata," arXiv:1406.5306, 2014. https://arxiv.org/abs/1406.5306
14. Jurgen Riedel and Hector Zenil, "Rule Primality, Minimal Generating Sets, Turing-Universality and Causal Decomposition in Elementary Cellular Automata," arXiv:1802.08769, 2018. https://arxiv.org/abs/1802.08769

---

## Notes For SYNTRAN CA-Lab

This domain should be paired with:

- `scientific-research` for hypothesis discipline
- `data-ai-testing` for output validation
- `documentation` for notebooks, READMEs, and research notes
- `local-inference` only if private or offline inference becomes relevant

For v1, keep the implementation simple. Prefer a reliable notebook and reproducible metrics over premature orchestration.
