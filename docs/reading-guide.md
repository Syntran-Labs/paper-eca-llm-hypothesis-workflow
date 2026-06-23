# Reading Guide for Data Scientists

**Repository:** `paper-eca-llm-hypothesis-workflow` · **SYNTRAN Paper Lab** · Early Incubation  
**Audience:** Data Scientists, ML Engineers, AI researchers, and technical reviewers entering this repository for the first time  
**Purpose:** A recommended reading order that moves you from high-level orientation to technical audit, with notes on what each document covers and what not to overinterpret.

---

## What You Are Looking At

This is a methods-research repository. The central question is:

> **Can an LLM-assisted scientific workflow generate falsifiable, non-overclaiming hypotheses — reproducibly?**

Elementary cellular automata (ECA) — Wolfram's 256 one-dimensional binary rules — are the testbed. Because ECA behavioral ground truth is well established, it is immediately visible when an LLM overclaims, hallucinates structure, or produces an unfalsifiable hypothesis. The ECA domain was chosen for its auditability, not because new ECA results are expected.

The repository is at **Early Incubation** stage. One complete hypothesis loop cycle (propose → validate → test → record results) has been run. The infrastructure is complete; the evidence base for the central methods claim is preliminary and is documented as such.

---

## Recommended Reading Order

### 1. [README.md](../README.md)

**Why first.** This is the single-page orientation to the whole project. It explains the research question, why ECA is the right testbed, what the SYNTRAN AIEOS governance layer does, what is complete, and what gaps remain before any external publication step.

**What you will learn:**
- The research question and its motivation
- The seven behavioral metrics at a glance
- What the governance layer enforces (separate storage of observations and interpretations, schema-validated LLM output, quality checklist, immutable human decision record)
- Current state: 256 rules simulated, 7 metrics per rule, 119 tests passing, one LLM session with two models, first follow-up experiment cycle complete
- Explicit gaps: no baseline comparison, no negative controls, one session, one batch

**Note.** The "What Is Done" section describes infrastructure readiness, not publication readiness. These are distinct.

---

### 2. [docs/research-question.md](research-question.md)

**Why second.** The README gives you the question in one sentence. This document gives you the scope, the epistemological constraints, and the v1 success criteria that gate all downstream claims.

**What you will learn:**
- The full research question with scope boundaries (1D binary ECA only; no proofs; no deployment; no claims outside simulation)
- The epistemological constraints that apply to every result: parameter-contingent, proxy-based, not formal proofs
- Which v1 success criteria were met (all, as of 2026-06-18)
- Candidate follow-on questions — illustrative, not committed work

**Note.** "Next Questions" at the end of this document is a list of open directions, not a roadmap.

---

### 3. [docs/methodology.md](methodology.md)

**Why third.** Before reading any simulation output or hypothesis, you need the exact definitions of simulation parameters and metrics. This document is the authoritative reference.

**What you will learn:**
- Default grid configuration: `n_cells=100`, `n_steps=200`, `fixed_zero` boundary, `single_seed` initial condition, `random_seed=42`
- How Wolfram rule encoding works (neighborhood indexing from `111` to `000`)
- All seven metrics: definition, what each measures, and — critically — what each does not measure (the "Interpretation Limit" column)
- The 11-step experiment loop from configuration through hypothesis review
- The structured summary format: which fields are factual (`observation`) and which are intentionally empty (`interpretation_placeholder`, `hypothesis_placeholder`)
- Documented metric limitations: entropy is row-level only; periodicity score may detect boundary artifacts; compression ratio is a proxy for regularity, not a measure of Kolmogorov complexity

**Note.** Read the "Interpretation Limit" column for every metric before drawing any conclusion from a metric value. Each limit is load-bearing.

---

### 4. [notebooks/001_ca_rule_space_exploration.ipynb](../notebooks/001_ca_rule_space_exploration.ipynb)

**Why fourth.** With the methodology in hand, run the notebook. You will see the full simulation pipeline execute — all 256 rules ranked, structured summaries generated, and the data that was submitted to the first LLM session produced.

**What you will learn:**
- What the simulation output looks like in practice (metric tables, ranked DataFrames, visualizations for selected rules)
- How the heuristic interest score ranks rules and what "top 10 rules" means operationally
- What the `ai_hypothesis_loop_inputs` object looks like before serialization
- The exact JSON that was pasted into the LLM prompt in session 1

**How to run:** `pip install -e ".[dev]"` then `jupyter notebook notebooks/001_ca_rule_space_exploration.ipynb`. Use **Kernel → Restart & Run All**. Fully offline. No API keys.

**Note.** The interest score is a heuristic combining activity, entropy, and compressibility. The top-ranked rules are not objectively "the most important rules" — a different heuristic would produce a different ranking.

---

### 5. [docs/ai-hypothesis-loop.md](ai-hypothesis-loop.md)

**Why fifth.** This document describes the 8-stage governed loop that converts simulation output into testable hypotheses and compares predictions against observed results.

**What you will learn:**
- Why the loop is intentionally manual at v2 (governance risk, not a technical limitation — five specific risks are documented)
- The 8 stages: simulate → collect metrics → generate summaries → submit to LLM → receive hypotheses → review with checklist → convert to follow-up experiments → compare results
- What constitutes a good hypothesis (falsifiable, metric-specific, rule-specific, directional, honest about evidence base and confidence)
- What constitutes a bad hypothesis (vague label, causal claim from single run, invented citation, hedged non-prediction)
- The SYNTRAN AIEOS governance principle: the LLM proposes, the operator decides, the record is immutable

**Note.** The "Future Automation Path" section describes v3 plans. These are conditional on completing a validated baseline with the manual loop first.

---

### 6. [prompts/hypothesis-review.md](../prompts/hypothesis-review.md)

**Why sixth.** This is the actual prompt template used in every LLM session. Reading it lets you audit whether the governance constraints were enforced at the point of submission — before the model produced any output.

**What you will learn:**
- The exact epistemic constraints the model received: no external citations, no causality from single runs, no "proves", direction required, confidence calibration rules, risk of overclaiming required
- The required output format (JSON conforming to the schema you will read next)
- How the prompt is assembled from source documents (the placeholder reference table)
- The session record template for logging each submission

**Note.** The prompt template is a constraint, not a guarantee. The hypothesis files in `hypotheses/` are the evidence of how well the constraint held in practice.

---

### 7. [schemas/hypothesis_response.schema.json](../schemas/hypothesis_response.schema.json)

**Why seventh.** The JSON schema is the structural contract for every LLM response. Reading it alongside the prompt template tells you which fields are required, which values are enumerated, and what the schema was designed to prevent.

**What you will learn:**
- Required fields: `hypothesis_id`, `rule_ids`, `observation_basis`, `hypothesis`, `expected_result`, `test_plan`, `metrics_to_compare`, `confidence`, `risk_of_overclaiming`, `status`
- Enumerated values: `confidence` must be `low | medium | high`; `status` must be one of `proposed | accepted_for_testing | rejected | inconclusive | supported | partially_supported | refuted`
- What a schema violation looks like (one was caught at intake during session 1 — see Research Note 001)

**Note.** Schema conformance is necessary but not sufficient for hypothesis quality. A hypothesis can pass schema validation and still fail the quality checklist on falsifiability or confidence calibration.

---

### 8. [docs/hypothesis-quality-checklist.md](hypothesis-quality-checklist.md)

**Why eighth.** This is the human review layer applied after schema validation. It defines the hard blocking criteria (reject without exception) and advisory criteria (flag with caveats).

**What you will learn:**
- 7 blocking criteria: falsifiability, metric specificity by exact name, rule specificity by number, predicted direction or bound, test plan completeness (specific `simulate()` call), no unverifiable external citations, no causal claim from a single run
- 6 advisory criteria: evidence basis in observed values, confidence calibration table, risk of overclaiming acknowledgment, observation/interpretation separation, metrics-to-compare completeness, no hallucinated behavior
- The review record template
- Common rejection patterns: vague behavioral labels, Turing completeness claims, Wolfram class assignments without metric threshold, "as shown by Wolfram (2002)" when no such reference is verifiable in this repository

**Note.** The checklist structures the reviewer's judgment; it does not automate rejection decisions.

---

### 9. [hypotheses/](../hypotheses/)

**Why ninth.** With the prompt, schema, and checklist in mind, you can now audit the actual LLM responses from session 1 (2026-06-18) against the governance standards you have just read.

**What to read:**
- `review_20260618_001.json` — Claude Opus 4.8 Max: 3 hypotheses, schema-conformant
- `review_20260618_eca01.json` — ChatGPT 5.5 high thinking: 6 hypotheses, schema-conformant (one schema violation caught and corrected at intake)
- `review_20260618_comparison.md` — human reviewer's pre-analysis written before Research Note 001

**What you will learn:**
- How each model responded to the same prompt on the same data
- Whether the `confidence` and `risk_of_overclaiming` fields reflect the checklist calibration table
- Whether `observation_basis` fields contain only measured values or smuggle in interpretations
- Which hypotheses were accepted, which remain at `proposed`, and which were tested in the follow-up cycle

**Note.** Two models in one session on one batch of 10 rules is a data point about method behavior, not a benchmark of model capability.

---

### 10. [docs/research-notes/001-first-hypothesis-review-comparison.md](research-notes/001-first-hypothesis-review-comparison.md)

**Why tenth.** This is the primary analysis note for session 1. It documents what both models found, how their approaches differed, what the result says about the workflow, and what remains to be tested.

**What you will learn:**
- Both models independently identified the same five near-identical rule pairs (59/115, 25/67, 97/41, 83/27, 107/121), with matching metrics to 3–5 decimal places
- This corresponds to known ECA reflection-equivalence — it is a methodology sanity check, not a discovery
- How Claude Opus and ChatGPT 5.5 differed in hypothesis count, style, and confidence calibration
- The audit trail: what schema validation caught, what the checklist caught, and what was accepted for testing
- Which hypotheses were carried forward to the follow-up experiment cycle

**Note.** The convergence result confirms that the governance layer worked — both models stayed within epistemic constraints. It does not mean the models "discovered" ECA symmetry independently.

---

### 11. [docs/research-notes/003-follow-up-experiments-results.md](research-notes/003-follow-up-experiments-results.md)

**Why eleventh.** This note records the outcomes of the three follow-up experiments run against accepted hypotheses. It is the first evidence layer: predictions compared against observed results.

**What you will learn:**
- Experiment A (Claude h001/h002, `n_cells=101`): **supported** — switching to an odd grid collapsed within-pair metric differences to zero, confirming the centering-artifact interpretation
- Experiment B (Claude h003, `n_steps=201`): **partially supported** — large density swings observed for rules 83/27/107/121; negligible for 59/115/25/67
- Experiment C (ChatGPT h003, `n_steps=400`): **supported** — rank ordering of rules 97/41/25/67 preserved at longer run; compression_ratio gap widened
- How hypothesis statuses were updated in the JSON artifacts

**Note.** Three experiments on one batch constitutes a proof-of-concept for the loop mechanism. "Supported" means the prediction held in this specific experiment — not that the hypothesis generalizes across the full 256-rule space or different parameter settings.

---

### 12. [docs/research-notes/002-publication-positioning.md](research-notes/002-publication-positioning.md)

**Why twelfth.** After seeing the evidence, read the publication positioning note to understand what the project claims this evidence supports — and what it explicitly rules out.

**What you will learn:**
- Why the target paper is a methods paper, not an ECA results paper
- The explicit "what this paper is not" list: not new ECA theory, not an LLM discovery claim, not autonomous science, not a model capability benchmark, not a production system
- The evidence gaps that remain before any external publication: baseline comparison (governed vs. unstructured prompting), negative controls, multiple sessions, multiple batches
- The publication ladder: internal notes → GitHub Release → Zenodo DOI → preprint. Current position: stage 1.

**Note.** This is a planning document. The publication ladder states gate conditions, not a timeline commitment.

---

### 13. [docs/references.md](references.md)

**Why thirteenth.** After reading the full research trail, consult the reference list to understand the intellectual foundation. This document is also the governance boundary for citations: any reference not in this list cannot be verified within a simulation session and must not appear in a hypothesis.

**What you will learn:**
- The 17 foundational references for ECA, complexity theory, and scientific reproducibility
- Why the project prohibits citing these sources inside hypotheses (they cannot be verified from within a session — they are background knowledge, not evidence)

---

### 14. [src/cellauto_lab/](../src/cellauto_lab/)

**Why fourteenth.** Now audit the implementation against the methodology you have read.

**What to read:**
- `rules.py` — Wolfram rule encoding; verify the neighborhood indexing matches the documentation
- `simulator.py` — ECA simulator; look for vectorized NumPy operations, `fixed_zero` boundary enforcement, and determinism of seeded random initial conditions
- `metrics.py` — all seven metrics; match each implementation to its definition and interpretation limit in `docs/methodology.md`
- `reporting.py` — structured summary generation; verify `observation` fields are purely factual and that all placeholder fields initialize to empty strings or empty lists
- `__init__.py` — public API surface

**Note.** Any discrepancy between the code and the methodology documentation is a bug worth filing as an issue.

---

### 15. [tests/](../tests/)

**Why last.** After reading the code, verify the test suite covers the behavioral guarantees the methodology documents.

**What to read:**
- `test_rules.py` — rule encoding correctness, spot checks for Rules 0, 30, 90, 110, 184, 255
- `test_simulator.py` — output shape, dtype, binary-value guarantee, determinism, boundary cases
- `test_metrics.py` — metric key completeness and value ranges for known behaviors
- `test_package_api.py` — public API contract
- `test_reporting.py` — structured summary structure and placeholder field state

**How to run:** `pytest tests/` — 119 tests, should pass in under 2 seconds.

**Note.** The test suite verifies code correctness. It does not validate that the metrics capture the behavioral properties they are intended to measure — that is the epistemological question the research is investigating.

---

## What You Have Covered

After completing this reading path you will have:

1. Understood the research question and why ECA is the right testbed for it
2. Learned the exact simulation parameters and metric definitions, including their documented limits
3. Traced the full governed hypothesis loop from simulation output to experiment outcome
4. Audited the actual LLM responses and the human review decisions against the governance standards
5. Understood what the current evidence supports and what gaps remain before any publication step
6. Verified that the implementation matches the documented methodology

The project is in Early Incubation. The infrastructure is complete and the first loop cycle is done. The central claim — that a governed LLM-assisted workflow produces better scientific hypotheses than unstructured prompting — has not yet been tested. That gap is documented explicitly in the README and in Research Note 002, and it is the reason for the current incubation status.
