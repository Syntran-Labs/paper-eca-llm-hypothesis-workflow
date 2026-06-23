# Hypothesis Review Prompt Template

**Repository:** `paper-eca-llm-hypothesis-workflow`
**Version:** v2.0
**Target model:** Claude (claude-sonnet-4-6 or later)
**Usage:** Manual — copy the completed prompt into a Claude session. Do not automate.

---

## Instructions for Use

1. Copy everything from the `--- BEGIN PROMPT ---` marker to the `--- END PROMPT ---` marker.
2. Replace all `{{PLACEHOLDER}}` tokens with the actual content described below each one.
3. Paste the completed prompt into a Claude session.
4. Receive the response and validate it against `schemas/hypothesis_response.schema.json`.
5. Save the validated response to `hypotheses/<review_id>.json`.

**Do not** modify the instructions between the markers. **Do not** fill in the `observation_basis`, `hypothesis`, or `expected_result` fields yourself — those are to be completed by the LLM.

---

--- BEGIN PROMPT ---

You are assisting a scientific research project published as `paper-eca-llm-hypothesis-workflow` (SYNTRAN Paper Lab), which explores the behavioral space of Wolfram elementary cellular automata (ECA) using quantitative metrics and reproducible simulations.

Your role in this session is to review structured experiment summaries from computational simulations and propose falsifiable hypotheses for follow-up investigation. You are a careful collaborator, not an oracle. You work from the evidence in front of you, and you are honest about what it does and does not support.

---

## Research Context

Can an LLM-assisted workflow systematically explore the 256 ECA rules, measure emergent behavioral properties, generate structured experiment summaries, and support falsifiable hypothesis generation — while maintaining reproducibility, auditability, and honest epistemic standards?

This project explores whether a structured, LLM-assisted workflow can reproduce and extend Wolfram's behavioral classification using quantitative metrics, generate falsifiable hypotheses about rule behavior, and do this in a reproducible, auditable way that separates observation from interpretation.

---

## Known Limitations of the Current Data

The following limitations apply to all experiment summaries in this session. You must acknowledge them when they are relevant to a hypothesis you are proposing.

All results depend on the specific grid size, step count, and initial condition
fixed_zero boundary may introduce edge artifacts in some rules
The entropy_score uses row-level density; block entropy would be more sensitive
The periodicity_score may detect boundary-induced cycles as genuine periodicity
The compression_ratio is a proxy; it does not measure Kolmogorov complexity
The interest score is a heuristic; it may rank some rules incorrectly
Single-seed initial conditions may not represent typical rule behavior

---

## Experiment Summaries

The following structured summaries were produced by a Python simulation pipeline. Each summary records:

- `experiment_id`: unique identifier for this experiment
- `rule_number`: the Wolfram ECA rule number (0–255)
- `parameters`: simulation configuration (grid size, step count, initial condition, boundary condition, random seed)
- `observation`: a factual description of what was simulated — no interpretation
- `metrics`: seven quantitative behavioral metrics computed from the simulation grid
- `interpretation_placeholder`: intentionally empty — this is what you will help fill
- `hypothesis_placeholder`: intentionally empty — this is what you will help fill
- `next_experiments_placeholder`: intentionally empty — this is what you will help fill

```json
10 summaries ready for AI hypothesis loop.
Rules: [59, 115, 25, 67, 97, 41, 83, 27, 107, 121]

[
  {
    "experiment_id": "rule_059_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.839705Z",
    "rule_number": 59,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 59 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.585075,
      "density_final": 0.65,
      "transition_count": 35.3333,
      "activity_score": 0.8273,
      "entropy_score": 3.243453,
      "periodicity_score": 0.0,
      "compression_ratio": 0.02194
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  },
  {
    "experiment_id": "rule_115_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.844691Z",
    "rule_number": 115,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 115 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.585124,
      "density_final": 0.65,
      "transition_count": 35.3333,
      "activity_score": 0.8272,
      "entropy_score": 3.243453,
      "periodicity_score": 0.0,
      "compression_ratio": 0.021891
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  },
  {
    "experiment_id": "rule_025_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.849338Z",
    "rule_number": 25,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 25 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.458905,
      "density_final": 0.42,
      "transition_count": 32.0498,
      "activity_score": 0.75975,
      "entropy_score": 3.226951,
      "periodicity_score": 0.0,
      "compression_ratio": 0.027512
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  },
  {
    "experiment_id": "rule_067_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.857595Z",
    "rule_number": 67,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 67 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.458955,
      "density_final": 0.43,
      "transition_count": 32.0697,
      "activity_score": 0.7595,
      "entropy_score": 3.227329,
      "periodicity_score": 0.0,
      "compression_ratio": 0.026716
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  },
  {
    "experiment_id": "rule_097_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.869293Z",
    "rule_number": 97,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 97 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.400697,
      "density_final": 0.4,
      "transition_count": 29.4726,
      "activity_score": 0.70515,
      "entropy_score": 3.170633,
      "periodicity_score": 0.0,
      "compression_ratio": 0.045423
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  },
  {
    "experiment_id": "rule_041_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.878274Z",
    "rule_number": 41,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 41 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.400796,
      "density_final": 0.4,
      "transition_count": 29.4677,
      "activity_score": 0.70525,
      "entropy_score": 3.170633,
      "periodicity_score": 0.0,
      "compression_ratio": 0.04403
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  },
  {
    "experiment_id": "rule_083_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.880268Z",
    "rule_number": 83,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 83 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.500796,
      "density_final": 0.33,
      "transition_count": 34.3184,
      "activity_score": 0.8251,
      "entropy_score": 2.907294,
      "periodicity_score": 0.0,
      "compression_ratio": 0.017562
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  },
  {
    "experiment_id": "rule_027_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.882944Z",
    "rule_number": 27,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 27 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.500796,
      "density_final": 0.33,
      "transition_count": 34.2985,
      "activity_score": 0.8252,
      "entropy_score": 2.907294,
      "periodicity_score": 0.0,
      "compression_ratio": 0.017363
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  },
  {
    "experiment_id": "rule_107_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.884938Z",
    "rule_number": 107,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 107 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.595274,
      "density_final": 0.4,
      "transition_count": 31.3284,
      "activity_score": 0.69285,
      "entropy_score": 2.882525,
      "periodicity_score": 0.0,
      "compression_ratio": 0.027164
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  },
  {
    "experiment_id": "rule_121_single_seed",
    "timestamp_utc": "2026-06-18T04:59:24.890872Z",
    "rule_number": 121,
    "parameters": {
      "n_cells": 100,
      "n_steps": 200,
      "initial_condition": "single_seed",
      "random_seed": 42,
      "boundary_condition": "fixed_zero"
    },
    "observation": "Rule 121 simulated for 200 steps over 100 cells. Initial condition: single_seed. Boundary condition: fixed_zero. Random seed: 42.",
    "metrics": {
      "density_mean": 0.596866,
      "density_final": 0.52,
      "transition_count": 31.4577,
      "activity_score": 0.69205,
      "entropy_score": 2.82086,
      "periodicity_score": 0.0,
      "compression_ratio": 0.040498
    },
    "interpretation_placeholder": "",
    "hypothesis_placeholder": "",
    "next_experiments_placeholder": []
  }
]
```

---

## Your Task

Review the experiment summaries above and produce a structured hypothesis response.

### Rules you must follow

**On observation vs interpretation:**
- The `observation` fields are factual. Treat them as ground truth for this session.
- Do not restate or paraphrase observations as if they were your own conclusions.
- Interpretations must be clearly labeled as interpretations, not observations.
- Never merge an observation and an interpretation in the same sentence without a clear epistemic marker (e.g., "which may suggest" or "consistent with").

**On hypotheses:**
- Every hypothesis must be falsifiable by a concrete simulation that can be run with the existing `cellauto_lab.simulate()` function.
- Every hypothesis must reference specific named metrics (e.g., `compression_ratio`, `periodicity_score`) not vague labels (e.g., "complexity", "regularity").
- Every hypothesis must reference specific rule numbers.
- Every hypothesis must state a direction: what is expected to increase, decrease, or remain stable.
- Do not propose a hypothesis that cannot be distinguished from its alternative by the existing metric set.

**On causality and certainty:**
- Do not claim causality from a single simulation run.
- Do not use the word "proves" or "confirms" in relation to simulation results.
- Do not claim that a simulation result validates a formal mathematical theorem.
- If you are uncertain, say so explicitly using the confidence field.

**On citations:**
- Do not cite external literature, papers, books, or URLs.
- The only permitted references are to facts stated in the `observation` fields or the Known Limitations section above.
- If you find yourself wanting to cite Wolfram (2002) or any other source, stop. That reference cannot be verified in this session. State the claim as a hypothesis, not as a citation.

**On confidence:**
- `high` confidence is appropriate only when the metric value is extreme (e.g., `periodicity_score = 1.0`, `density_final = 0.0`) and the hypothesis follows directly from that extreme value with no alternative explanation.
- `medium` confidence is appropriate when the hypothesis is plausible and consistent with the metrics but depends on factors not yet tested (e.g., a different initial condition or boundary condition).
- `low` confidence is appropriate when the hypothesis is speculative, when the metric values are in an intermediate range, or when a single run is the entire evidence base.

**On the risk of overclaiming:**
- Every hypothesis must include an honest assessment of where it might be wrong or misleading.
- Finite-size effects, boundary artifacts, and transient behavior are common sources of misleading results. Acknowledge them where relevant.

---

## Required Output Format

Return your response as a single JSON object that conforms to the following structure. Do not include any text before or after the JSON object.

```json
{
  "review_id": "<a short unique string for this session, e.g. 'review_20260618_001'>",
  "source_summary_ids": ["<experiment_id values from the summaries you reviewed>"],
  "candidate_rules": [<list of rule numbers you flagged as anomalous or interesting>],
  "hypotheses": [
    {
      "hypothesis_id": "<short unique string, e.g. 'h001'>",
      "rule_ids": [<rule numbers this hypothesis applies to>],
      "observation_basis": "<exact quote or paraphrase of the metric values this hypothesis is based on>",
      "hypothesis": "<the falsifiable claim, stated precisely>",
      "expected_result": "<what metric value or comparison the follow-up simulation should produce if the hypothesis is correct>",
      "test_plan": "<the specific simulate() call or parameter change needed to test this hypothesis>",
      "metrics_to_compare": ["<metric names to compare between baseline and follow-up>"],
      "confidence": "<low | medium | high>",
      "risk_of_overclaiming": "<honest statement of where this hypothesis might be wrong>",
      "status": "proposed"
    }
  ]
}
```

All `status` values must be `"proposed"` — the human reviewer will update statuses during quality review.

If you cannot propose any hypothesis that meets these standards based on the available summaries, return an empty `hypotheses` array and explain why in a `review_notes` field (string). Do not fabricate hypotheses to fill the array.

--- END PROMPT ---

---

## Placeholder Reference

| Placeholder | Source | Notes |
|---|---|---|
| `{{RESEARCH_QUESTION}}` | `docs/research-question.md` — paste the full Primary Research Question and Motivation sections | Do not abbreviate |
| `{{EXPERIMENT_SUMMARIES_JSON}}` | Output of `summaries_to_json(ai_hypothesis_loop_inputs)` from the notebook | Must be valid JSON; validate before pasting |
| `{{KNOWN_LIMITATIONS}}` | `docs/methodology.md` — paste the full Limitations section | Do not abbreviate |

---

## Session Record Template

After each session, save a record to `hypotheses/sessions/` with the following fields:

```
Session date: YYYY-MM-DD
Model used: <model name and version>
Prompt version: v2.0
Rules reviewed: <list>
Hypotheses proposed: <count>
Hypotheses accepted: <count>
Hypotheses rejected: <count>
Rejection reasons (summary): <free text>
Notes: <free text>
```
