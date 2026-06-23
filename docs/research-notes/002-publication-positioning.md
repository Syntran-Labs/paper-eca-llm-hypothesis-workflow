# Research Note 002: Publication Positioning

**Repository:** `paper-eca-llm-hypothesis-workflow`
**Date:** 2026-06-18
**Author:** Leonardo Sigales / SYNTRAN Labs
**Status:** `draft — planning`

---

## Summary

The first hypothesis review session (documented in [Research Note 001](001-first-hypothesis-review-comparison.md)) makes the publication positioning decision clear: this project should not be framed as a cellular automata findings paper at this stage, and possibly not at any stage.

The stronger and more honest positioning is a **methodology paper about governed, audit-first LLM-assisted hypothesis generation**, evaluated on a known computational system with verifiable ground truth.

This note records that decision, its rationale, the evidence still missing before any publication step is appropriate, and the near-term plan.

---

## What The Paper Is Not

Being explicit about what this project is not prevents scope creep and premature claims.

**Not a claim of new ECA theory.**
The behavioral properties of the 256 Wolfram rules are extensively documented. The five rule pairs identified in session 1 correspond to known reflection symmetry equivalence classes. Documenting that metrics of mirror-equivalent rules are similar is a methodology sanity check, not a discovery.

**Not a claim that an LLM discovered known symmetries.**
Both models recovered a metric pattern consistent with known ECA structure, working only from simulation metrics and without citing literature. This is an interesting signal about the method. It is not the same as saying the models discovered or proved anything.

**Not a claim of autonomous scientific discovery.**
The workflow requires a human operator at every stage: to run the notebook, to submit the prompt, to review the schema, to apply the quality checklist, to decide which hypotheses to execute, and to interpret the results. The LLM is a structured collaborator, not an autonomous agent.

**Not a general benchmark of model intelligence.**
ChatGPT 5.5 (high thinking) and Claude Opus 4.8 were compared on a single batch in one session. No statistically meaningful conclusions about relative capability can be drawn from this.

**Not a production AI system.**
`paper-eca-llm-hypothesis-workflow` is an incubation research workspace. It is not a deployed tool, a library for others to use, or a system with reliability guarantees.

---

## What The Paper Could Become

The honest framing of a future contribution is a **methods and reproducibility paper** with the following characteristics:

### Primary question

Does a governed, structured LLM workflow — with explicit schema validation, falsifiability requirements, epistemic constraints in the prompt, and human review checkpoints — produce measurably better hypothesis quality than unstructured LLM use on the same research task?

"Better" could be operationalized as: higher schema validity rate, higher falsifiability rate, lower overclaiming rate, higher follow-up experiment executability rate, and lower hallucinated citation rate.

### Why ECA is the right testbed

ECA is ideal for evaluating this question because:

1. Ground truth is verifiable — known behavioral classes and symmetry structure provide a baseline against which LLM output can be checked.
2. The rule space is finite and exhaustible — all 256 rules can be tested under identical conditions.
3. Overclaiming is detectable — an LLM claiming Rule 110 "proves" universality from a 200-step simulation is falsifiable immediately.
4. The domain is non-trivial but accessible — a technically literate reader can evaluate claims without specialized domain expertise.

### Candidate research contributions

1. A practical, fully reproducible workflow for LLM-assisted exploratory computation, with all artifacts committed to a version-controlled repository.
2. A documented artifact trail from simulation output → structured summary → prompt → LLM response → schema validation → human review → hypothesis execution → result recording.
3. A case study in epistemic discipline: separating observation, hypothesis, and interpretation at every stage with structured tooling.
4. A comparative analysis of governed vs less-governed prompting on the same task, measuring schema conformance, falsifiability, and overclaiming rates.
5. A reusable prompt template, JSON schema, and checklist that other researchers can adapt for governed LLM-assisted exploratory science.

---

## Evidence Still Missing

The project is not ready for any external publication step. The following evidence is required before that changes:

- **Executed follow-up experiments** — at minimum, Claude h001 and h003 (see [Research Note 001](001-first-hypothesis-review-comparison.md)). Results must be stored as artifacts and hypothesis statuses must be updated.
- **Hypothesis status updates** — all current hypotheses are `proposed`. At least one cycle of execution, status update, and result recording is needed to demonstrate the loop works end-to-end.
- **Baseline comparison** — a session run with an unstructured prompt (same summaries, no schema, no epistemic constraints) to measure what the governance layer actually changes.
- **Negative controls** — submit a batch of deliberately dissimilar rules and verify that the models do not spuriously group them.
- **Multiple independent batches** — the current result is from one batch of 10 rules. The methodology paper needs evidence from multiple sessions to claim the workflow is reliable.
- **Literature-grounded novelty check** — the observation about rule pairing needs to be checked against the ECA symmetry literature cited in [`docs/references.md`](../references.md) to confirm that it is indeed known, not a new finding.
- **Reproducibility package** — the repository needs to be in a state where a reader can clone it, run `pytest` and the notebook, and reproduce all artifacts referenced in the paper.

---

## Publication Ladder

Progress toward publication should follow this sequence. No step should be taken before the previous one is complete.

| Stage | Trigger condition | Notes |
|---|---|---|
| **1. Internal Research Notes** | Any new finding or decision | Current stage |
| **2. GitHub Discussions** | After at least one complete hypothesis execution cycle | For community feedback before any external commitment |
| **3. GitHub Release with artifacts** | After reproducibility package is complete and verified | Tag the repo; generate a DOI-eligible snapshot |
| **4. Zenodo archive** | After Release; only if the artifact package is coherent and complete | Provides a citable DOI for the methodology artifacts |
| **5. Preprint (arXiv or similar)** | After baseline comparison, negative controls, and multiple batches | Requires a meaningful results section, not just a workflow description |
| **6. Workshop or conference submission** | After preprint feedback; requires a complete evaluation section | Target: AI for Science workshops, reproducibility tracks, or methods venues |

Do not skip stages. A preprint submitted before the baseline comparison exists would be premature and difficult to defend.

---

## Near-Term Plan

### Today (already done)

- Saved and validated both LLM hypothesis review responses.
- Wrote the first Research Notes (this note and Note 001).
- Documented the comparison and the publication positioning decision.
- Preserved all artifacts with attribution and status labels.

### Next (this week)

- Execute Claude h001: re-run the batch at `n_cells=101` and record whether within-pair metric differences collapse.
- Execute Claude h003: re-run at `n_steps=201` and check density_final swing.
- Update hypothesis statuses in the JSON files.
- Write Research Note 003 recording the experiment results.

### After that

- Execute ChatGPT h003 (temporal stability at `n_steps=400`).
- Design and run the baseline comparison (unstructured prompt session).
- Submit the second rule batch for a second hypothesis review session.

---

## Gaps and Limitations

- This note is based on one session. The positioning decision could change if the workflow fails to produce executable hypotheses in subsequent sessions.
- The baseline comparison (governed vs ungoverned) is planned but not yet designed. The evaluation criteria need to be defined before the comparison is run, not after.
- The publication venues suggested (AI for Science workshops, reproducibility tracks) are provisional. Appropriate venues should be confirmed once the results section exists.

---

## Conclusion

The immediate deliverable is not a paper. The immediate deliverable is a transparent, reproducible research trail — executed experiments, stored artifacts, updated hypothesis statuses, and Research Notes documenting every decision — that can later become the evidence base for a serious methods contribution.

The project is on track. The governance layer worked as intended in session 1: both models produced schema-conformant, falsifiable output without overclaiming, and the human review step caught the one schema violation (missing `status` fields) before it was committed. That is the result to build on.
