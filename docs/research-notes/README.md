# Research Notes

**Repository:** `cellauto-lab`
**Maintained by:** SYNTRAN Labs
**Workflow:** SYNTRAN AIEOS

---

## What Research Notes Are

Research Notes are structured documents that record observations, comparisons, decisions, and open questions at specific points in the project timeline.

Each note is a snapshot. It records what was known, what was found, and what remains untested at the time of writing. Notes do not get rewritten as new evidence arrives — they get superseded by later notes or updated with a dated addendum.

Research Notes serve as the audit trail that connects raw simulation artifacts, LLM-generated hypothesis files, and any eventual publication.

---

## What Research Notes Are Not

Research Notes are not:

- **Papers or preprints.** A note documents a step in the process. It does not claim a finding.
- **Conclusions.** A note records observations. Conclusions require executed experiments, multiple replications, and comparison against known literature.
- **LLM summaries.** Notes are written by the human operator and reviewed before being committed. LLM contributions appear as artifacts referenced from notes, not as the notes themselves.
- **Permanent truth.** Notes can be superseded when new evidence changes the picture. Superseded notes are kept with a `superseded` label; they are not deleted.

---

## Relationship to Other Artifacts

| Artifact | Role | Where stored |
|---|---|---|
| Simulation grid | Raw output from `simulate()` | Produced by notebook, not committed |
| Metrics JSON | Computed behavioral metrics | Produced by notebook |
| Experiment summary | Structured `experiment_summary()` output | Produced by notebook |
| Hypothesis review JSON | LLM-generated response to prompt | `hypotheses/` |
| Comparison markdown | Human reviewer analysis of LLM outputs | `hypotheses/` |
| Research Note | Synthesis document referencing the above | `docs/research-notes/` |
| Future paper | Synthesis of validated Research Notes | Not yet |

---

## Status Labels

Every Research Note carries one of the following status labels:

| Status | Meaning |
|---|---|
| `draft` | Written but not reviewed by a second reader or tested against experiments |
| `reviewed` | Reviewed by at least one other person; contents agreed upon |
| `experiment-pending` | Describes hypotheses that have not yet been executed |
| `experiment-tested` | At least one hypothesis in the note has been executed and the result recorded |
| `superseded` | Replaced by a later note; kept for traceability |

A note can carry compound status, e.g. `draft — experiment-pending`.

---

## Numbering Convention

Notes are numbered sequentially: `001`, `002`, `003`, etc. Numbers are never reused. Gaps are acceptable if a planned note was abandoned — document the abandonment in the index below rather than renumbering.

File format: `NNN-short-slug.md`

Example: `001-first-hypothesis-review-comparison.md`

---

## Discovery Rule

**A Research Note must not claim discovery of new scientific findings unless:**

1. The relevant hypothesis has been executed as a simulation experiment with stored output artifacts.
2. The result has been compared against existing literature in `docs/references.md`.
3. An alternative explanation has been considered and explicitly addressed.
4. The note has been reviewed by a second reader.

Until all four conditions are met, findings must be framed as hypotheses, preliminary observations, or methodological signals — not discoveries.

---

## Current Notes

| # | Title | Status | Description |
|---|---|---|---|
| [001](001-first-hypothesis-review-comparison.md) | First LLM Hypothesis Review Comparison | `draft — experiment-pending` | Compares ChatGPT o3 and Claude Opus 4.8 responses to the first ECA hypothesis review prompt; documents shared findings, structural differences, and next experiments |
| [002](002-publication-positioning.md) | Publication Positioning | `draft — planning` | Documents the publication strategy decision: methodology paper, not an ECA findings paper |
