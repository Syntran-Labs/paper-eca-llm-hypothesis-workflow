# Hypothesis Quality Checklist

**Repository:** `paper-eca-llm-hypothesis-workflow`
**Status:** Active — used during Stage 6 of the Manual AI Hypothesis Loop
**See also:** `docs/ai-hypothesis-loop.md`, `schemas/hypothesis_response.schema.json`

---

## Purpose

This checklist is applied by the human reviewer to each hypothesis in an LLM-generated response before assigning a status of `accepted_for_testing`, `rejected`, or `inconclusive`.

A hypothesis that fails any **blocking** criterion must be rejected. Failures on **advisory** criteria should be noted but do not automatically require rejection — they may be acceptable with caveats.

Record the checklist result and any rejection reasons in the hypothesis record before updating its status.

---

## Blocking Criteria

A hypothesis fails if any of the following are true. Reject without exception.

### 1. Falsifiability

- [ ] **The hypothesis is falsifiable by a concrete simulation.**
  The follow-up experiment must be runnable with the existing `cellauto_lab.simulate()` function using parameters that differ from the baseline in a specific, named way. A hypothesis like "Rule 30 is interesting" or "complex rules behave differently" cannot be tested and must be rejected.

### 2. Metric specificity

- [ ] **The hypothesis names at least one specific metric by its exact name.**
  Acceptable metric names: `density_mean`, `density_final`, `transition_count`, `activity_score`, `entropy_score`, `periodicity_score`, `compression_ratio`. Vague labels like "complexity", "regularity", or "chaos" that are not mapped to a named metric are not acceptable.

### 3. Rule specificity

- [ ] **The hypothesis names at least one specific rule number.**
  "Rules with high entropy" or "chaotic rules" are not specific enough. The hypothesis must say "Rule 30" or "Rules 30 and 110".

### 4. Predicted direction

- [ ] **The hypothesis states a direction or a bound for the expected result.**
  "compression_ratio will change" is not a prediction. "compression_ratio will remain above 0.80" or "periodicity_score will decrease" is a prediction.

### 5. Test plan completeness

- [ ] **The test plan names the specific parameter change and its value.**
  "Run a longer simulation" is not a test plan. "Run simulate(30, n_cells=500, n_steps=200, initial_condition='single_seed')" is a test plan.

### 6. No invented citations

- [ ] **The hypothesis does not cite external literature that cannot be verified.**
  Any citation not present in `docs/references.md` is unverifiable in this repository. Reject if the hypothesis depends on an external citation to establish its premise.

### 7. No causality from a single run

- [ ] **The hypothesis does not make a causal claim based on a single simulation run.**
  "Rule 30 generates true randomness" is a causal claim from finite simulation evidence. Acceptable formulation: "Rule 30 produces metric values consistent with high unpredictability under these parameters."

---

## Advisory Criteria

These do not automatically reject a hypothesis, but failures should be recorded and may affect the confidence rating or require the reviewer to add a caveat.

### 8. Evidence basis

- [ ] **The observation_basis field quotes or paraphrases specific metric values from the submitted summaries.**
  A hypothesis grounded in actual measured values is more credible than one grounded in a general characterization.

### 9. Confidence calibration

- [ ] **The confidence level is justified given the evidence base.**
  `high` confidence on a single 100-cell, single-seed run is almost never justified. If the LLM returned `high` for a speculative hypothesis, downgrade it to `medium` or `low` before accepting.

  | Evidence base | Maximum justified confidence |
  |---|---|
  | Single run, single initial condition | low |
  | Multiple seeds, same parameters | medium |
  | Multiple initial conditions confirmed | medium |
  | Replicated across grid sizes | high |

### 10. Risk of overclaiming statement

- [ ] **The risk_of_overclaiming field acknowledges at least one of: finite-size effects, boundary artifacts, transient behavior, or single-initial-condition limitation.**
  A hypothesis that claims no risks is more likely to be overconfident than genuinely robust.

### 11. Separation of observation and interpretation

- [ ] **The observation_basis field contains only directly measured values, not interpretations.**
  The observation_basis should read as: "Rule X showed metric Y = Z." It should not read as: "Rule X showed metric Y = Z, which proves it is class IV."

### 12. Metrics-to-compare completeness

- [ ] **The metrics_to_compare list includes the metric the hypothesis predicts will change.**
  If the hypothesis predicts compression_ratio will decrease, compression_ratio must be in metrics_to_compare. A list that omits the key metric is a sign the test plan is incomplete.

### 13. No hallucinated behavior

- [ ] **The hypothesis does not describe behavior that contradicts the submitted observation fields.**
  If the observation field for Rule 30 reports periodicity_score=0.0 and the hypothesis claims "Rule 30 exhibits periodic behavior", the hypothesis is inconsistent with the evidence and should be rejected.

---

## Review Record Template

After applying this checklist, record the result for each hypothesis:

```
Hypothesis ID: <hypothesis_id>
Rule(s): <rule_ids>
Reviewer: <name or initials>
Review date: YYYY-MM-DD

Blocking criteria:
  [ ] Falsifiable
  [ ] Metric specificity
  [ ] Rule specificity
  [ ] Predicted direction
  [ ] Test plan completeness
  [ ] No invented citations
  [ ] No single-run causality

Advisory criteria:
  [ ] Evidence basis adequate
  [ ] Confidence calibrated
  [ ] Risk of overclaiming acknowledged
  [ ] Observation/interpretation separated
  [ ] Metrics-to-compare complete
  [ ] No hallucinated behavior

Decision: [ ] accepted_for_testing  [ ] rejected  [ ] inconclusive
Rejection reason (if rejected): <free text>
Caveats (if accepted with advisory failures): <free text>
```

---

## Common Rejection Patterns

The following failure modes appear frequently in LLM-generated hypotheses. Watch for them.

| Pattern | Why it fails | Example |
|---|---|---|
| Vague behavioral label | Not a named metric | "Rule 110 is complex" |
| Turing completeness claim | Mathematical theorem, not a simulation result | "Rule 110 is Turing complete therefore its compression_ratio must be high" |
| Wolfram class assignment | Not derived from the submitted metrics | "This is a Class III rule" (without citing a metric threshold) |
| Invented Wolfram citation | Cannot be verified in this repository | "As shown by Wolfram (2002), Rule 30 is pseudo-random" |
| Hedged non-prediction | Not falsifiable | "Rule 90 may or may not show different behavior under random IC" |
| Overclaiming from entropy | Entropy score is a proxy, not a proof | "entropy_score = 3.29 proves Rule 30 is maximally complex" |
| Missing parameter in test plan | Test plan is incomplete | "Run a larger grid" (no specific n_cells value) |
