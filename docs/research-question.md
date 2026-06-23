# Research Question

**Repository:** `paper-eca-llm-hypothesis-workflow`
**Status:** Active
**Date:** 2026-06-17

---

## Primary Research Question

> Can an LLM-assisted workflow systematically explore the 256 elementary cellular automaton (ECA) rules, measure emergent behavioral properties, generate structured experiment summaries, and support falsifiable hypothesis generation — while maintaining reproducibility, auditability, and honest epistemic standards?

---

## Motivation

Elementary cellular automata (ECAs) are one of the simplest known systems capable of producing complex emergent behavior from local rules. Wolfram's classification of the 256 ECA rules into four behavioral classes (fixed, periodic, chaotic, complex) was done primarily through visual inspection and informal analysis.

This project asks whether a structured, LLM-assisted computational workflow can:

1. Reproduce and extend that classification using quantitative metrics
2. Generate falsifiable hypotheses about rule behavior
3. Identify candidate rules for deeper investigation
4. Do this in a reproducible, auditable way that separates observation from interpretation

The broader question is methodological: can LLM-assisted scientific exploration be made rigorous enough to be trustworthy, even in a domain as well-understood as ECAs?

---

## Scope

**In scope:**

- One-dimensional binary elementary cellular automata (radius 1, 2 states)
- Wolfram rules 0–255
- Behavioral measurement via quantitative metrics
- Structured experiment summaries
- LLM-assisted hypothesis proposal (placeholder in v1)
- Reproducibility infrastructure

**Out of scope:**

- Two-dimensional or higher-dimensional cellular automata
- Continuous-state cellular automata
- Formal mathematical proofs of universality or undecidability
- Claims requiring empirical validation outside simulation
- Production or deployment applications

---

## Success Criteria for v1

All v1 criteria met as of 2026-06-18.

- [x] All 256 rules are simulated under identical conditions
- [x] A minimum of 7 behavioral metrics are computed for each rule
- [x] Metrics are reproducible given the same parameters and seed
- [x] Structured summaries separate observation from interpretation
- [x] Known reference rules (0, 30, 90, 110, 184, 255) produce expected visual patterns
- [x] The notebook runs fully offline without external credentials
- [x] No LLM calls are embedded in the notebook

---

## Epistemological Constraints

All results from this project are:

- Contingent on the simulation parameters (grid size, step count, initial condition, boundary condition)
- Proxies for behavioral properties, not formal proofs
- Sensitive to the choice of metrics and their definitions
- Subject to finite-size effects and boundary artifacts

No result from this project should be stated as a mathematical claim without a formal proof external to the simulation.

---

## Next Questions (Post v1)

After the baseline infrastructure is established, candidate follow-on questions include:

1. Do LLM-assigned behavioral classifications agree with Wolfram's informal classes?
2. Which metrics are most predictive of perceived complexity?
3. Do nearby rules (by Hamming distance in their binary encoding) tend to have similar behavior?
4. How sensitive is behavior to initial condition for each rule?
5. Which rules are most interesting candidates for LLM-guided deeper exploration?
