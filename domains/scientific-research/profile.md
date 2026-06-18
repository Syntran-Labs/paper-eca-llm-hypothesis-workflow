# Domain Pack: scientific-research

Recommended path: `domains/scientific-research/profile.md`

## Purpose

This domain pack defines how SYNTRAN AIEOS should support scientific and research-oriented workflows.

It provides operating rules for hypothesis generation, experiment design, evidence handling, reproducibility, literature grounding, and AI-assisted research interpretation.

This domain is especially relevant for projects where Claude Code or another LLM helps explore a problem space, such as `cellauto-lab`.

The goal is not to make the AI a scientific authority. The goal is to make AI-assisted research more structured, auditable, falsifiable, and reproducible.

---

## Use This Domain When

Use `scientific-research` when the task involves:

- exploratory research
- hypothesis generation
- experiment planning
- simulation studies
- literature-grounded reasoning
- AI-assisted scientific discovery
- automated or semi-automated experiment loops
- evaluating evidence quality
- separating observation from interpretation
- writing research notes, experiment reports, and limitations

---

## Do Not Use This Domain For

Do not use this domain to:

- claim scientific discovery without validation
- replace peer review
- fabricate citations
- infer causality from correlation without evidence
- turn exploratory simulation into real-world claim
- make medical, financial, or safety-critical decisions without domain review
- let an LLM silently decide research conclusions

For implementation work, pair with `develop`. For data validation, pair with `data-ai-testing` and the `data-quality-test` skill.

---

## Core Research Principles

### 1. Separate Observation From Interpretation

Observations are things directly measured or computed.

Interpretations are explanations or meaning assigned to observations.

Bad:

```text
Rule 110 is intelligent.
```

Better:

```text
Rule 110 produced persistent localized structures under this initial condition. This is consistent with known complex behavior, but this run alone does not prove universality.
```

### 2. Every Hypothesis Must Be Falsifiable

A useful hypothesis must specify what result would count against it.

Bad:

```text
This rule is interesting.
```

Better:

```text
If Rule X belongs to the same behavioral region as Rule Y, then under random initial conditions it should show similar activity_mean and compression_ratio distributions across 20 seeded runs. If not, the similarity hypothesis is weakened.
```

### 3. Reproducibility Is Part Of The Result

A research result is incomplete unless another run can reproduce the evidence.

Minimum reproducibility metadata:

```yaml
experiment_id: string
timestamp_utc: string
code_version: string|null
notebook_name: string
python_version: string
package_versions: object
random_seed: int|null
input_parameters: object
output_artifacts: [paths]
```

### 4. Metrics Are Evidence, Not Truth

Metrics guide interpretation but do not replace thinking.

Every metric should document:

- what it measures
- why it is relevant
- failure modes
- expected range
- known blind spots

### 5. LLM Output Is A Research Artifact

LLM-generated analysis should be stored as an artifact, not treated as ground truth.

Recommended storage:

```yaml
llm_model: string
prompt_version: string
input_summary_hash: string
output_text: string
claims: [claim_objects]
uncertainties: [strings]
recommended_next_experiments: [experiment_specs]
```

---

## Research Object Model

Use this object model for experiments and reports.

### Research Question

```yaml
research_question:
  id: string
  question: string
  motivation: string
  scope: string
  out_of_scope: [strings]
```

### Hypothesis

```yaml
hypothesis:
  id: string
  statement: string
  rationale: string
  predicted_observations: [strings]
  falsification_criteria: [strings]
  confidence: 0-100
  status: proposed|tested|weakened|supported|rejected|inconclusive
```

### Experiment

```yaml
experiment:
  id: string
  objective: string
  hypothesis_ids: [strings]
  parameters: object
  controlled_variables: [strings]
  changed_variables: [strings]
  procedure: [steps]
  expected_outputs: [strings]
  reproducibility_metadata: object
```

### Evidence

```yaml
evidence:
  id: string
  experiment_id: string
  artifact_paths: [strings]
  metrics: object
  observations: [strings]
  limitations: [strings]
```

### Interpretation

```yaml
interpretation:
  id: string
  evidence_ids: [strings]
  claims: [strings]
  confidence: 0-100
  alternative_explanations: [strings]
  next_tests: [strings]
```

---

## AI-Assisted Research Loop

Recommended loop:

```text
Research Question
        ↓
Prior Context / Literature
        ↓
Hypothesis Generation
        ↓
Experiment Design
        ↓
Execution
        ↓
Metric Extraction
        ↓
Evidence Review
        ↓
Hypothesis Update
        ↓
Next Experiment Selection
```

The LLM may assist at each step, but it must expose reasoning outputs as reviewable artifacts.

### Required Loop Discipline

Before execution:

```text
[ ] Research question is stated.
[ ] Hypothesis is falsifiable.
[ ] Variables are identified.
[ ] Inputs and outputs are defined.
[ ] Reproducibility metadata is planned.
[ ] Risks and limitations are declared.
```

After execution:

```text
[ ] Raw outputs are saved.
[ ] Metrics are saved.
[ ] Observations are separated from interpretation.
[ ] Hypothesis status is updated.
[ ] Alternative explanations are listed.
[ ] Next experiment is justified.
```

---

## Literature Grounding Rules

When using literature:

1. Prefer primary sources: papers, proceedings, official documentation, author pages.
2. Use secondary sources only for orientation.
3. Every cited paper must include at least title, author, year, and URL or DOI.
4. Do not cite a paper that was not actually checked.
5. Do not fabricate DOI, venue, author names, or claims.
6. Distinguish between peer-reviewed, preprint, blog, documentation, and news.
7. When sources disagree, surface the disagreement.
8. When a claim is outside available evidence, mark it as speculation.

### Source Quality Labels

Use these labels in research notes:

| Label | Meaning |
|---|---|
| `primary-peer-reviewed` | journal/conference paper or official proceedings |
| `primary-preprint` | arXiv or similar preprint by authors |
| `primary-official` | official project, lab, or vendor page |
| `secondary-reference` | encyclopedia or curated reference |
| `secondary-news` | journalism or media report |
| `unverified` | not yet checked directly |

---

## AI Research Risk Register

| Risk | Severity | Mitigation |
|---|---:|---|
| LLM fabricates citations | High | Require DOI/URL and source-quality label |
| LLM overstates simulation result | High | Separate observation, interpretation, and proof |
| Hidden notebook state affects results | Medium | Require restart-and-run-all validation |
| Prompt contamination affects hypothesis generation | Medium | Version prompts and store model outputs |
| Confirmation bias in next-experiment selection | Medium | Include random baseline and negative controls |
| Metric gaming by the exploration loop | Medium | Define metrics before exploration round |
| False novelty claim | High | Compare against literature before claiming novelty |
| Non-deterministic model output | Medium | Store prompt, model name, temperature, and output |
| Excessive autonomy | High | Keep human approval over conclusions and project direction |

---

## Recommended Roles For Research Projects

### Architect Agent

Use for:

- research architecture
- experiment pipeline design
- decomposition of simulation, metrics, and reporting layers
- tradeoff analysis

### Python Engineer

Use for:

- implementation of simulations
- notebooks
- metrics code
- artifact generation
- local reproducibility scripts

### Data Quality Tester

Use for:

- metric validation
- artifact schema validation
- output consistency checks
- AI output structure validation

### Technical Writer

Use for:

- research notes
- README files
- experiment reports
- limitations sections
- literature summaries

### Security Reviewer

Use for:

- prompt-injection risks
- external API risks
- data exposure risks
- secret handling risks
- research artifact governance

### Test Strategy Lead

Use for:

- validation strategy
- test matrix
- quality gates
- acceptance criteria for research infrastructure

---

## Recommended SYNTRAN Invocations

### Research architecture

```text
/synw-agent-architect
/synw-skill-develop

Relevant domains:
- scientific-research
- cellular-automata

Task:
Design a reproducible notebook-first research architecture for cellauto-lab.

Constraints:
- Human remains final authority.
- AI hypotheses must be falsifiable.
- No claims of discovery without evidence.
- All experiment artifacts must be reproducible.
```

### Research documentation

```text
/synw-agent-technical-writer
/synw-skill-document

Relevant domains:
- scientific-research
- documentation

Task:
Write an explanation document for the research method used in cellauto-lab.

Constraints:
- Document type: Explanation.
- Audience: technical reader.
- Include research question, limitations, experiment loop, and source-quality rules.
```

### Data and AI output validation

```text
/synw-agent-data-quality-tester
/synw-skill-data-quality-test

Relevant domains:
- scientific-research
- data-ai-testing

Task:
Design validation checks for experiment metrics and LLM-generated hypothesis outputs.

Constraints:
- Read-only checks.
- Fail loudly on schema drift.
- Validate that every hypothesis includes falsification criteria.
```

### Security and integrity review

```text
/synw-agent-security-reviewer
/synw-skill-review

Relevant domains:
- scientific-research

Task:
Review the research workflow for prompt-injection, citation hallucination, reproducibility, and data exposure risks.

Constraints:
- No code changes.
- Produce findings with severity and mitigation.
```

---

## Research Report Template

```markdown
# Experiment Report: <experiment_id>

## Research Question

<question>

## Hypothesis

<statement>

## Falsification Criteria

<what would weaken or reject this hypothesis>

## Setup

- Code version:
- Notebook:
- Python version:
- Packages:
- Parameters:
- Random seed:

## Observations

Facts only.

## Metrics

| Metric | Value | Interpretation limit |
|---|---:|---|

## Interpretation

Tentative explanation.

## Alternative Explanations

- ...

## Conclusion

Supported / weakened / rejected / inconclusive.

## Next Experiment

<next test and why>

## References

<checked sources only>
```

---

## Public References

### Automated scientific discovery and robot scientists

1. Ross D. King et al., "The Automation of Science," *Science*, 324(5923), 85-89, 2009. DOI: https://doi.org/10.1126/science.1165620
2. A. Sparkes et al., "Towards Robot Scientists for autonomous scientific discovery," *Automated Experimentation*, 2, 1, 2010. https://pmc.ncbi.nlm.nih.gov/articles/PMC2813846/
3. Alexander H. Gower et al., "The Use of AI-Robotic Systems for Scientific Discovery," arXiv:2406.17835, 2024. https://arxiv.org/abs/2406.17835

### Equation discovery and symbolic scientific reasoning

4. Michael Schmidt and Hod Lipson, "Distilling Free-Form Natural Laws from Experimental Data," *Science*, 324(5923), 81-85, 2009. DOI: https://doi.org/10.1126/science.1165893
5. Stefan Kramer, Mattia Cerrato, Saso Dzeroski, and Ross King, "Automated Scientific Discovery: From Equation Discovery to Autonomous Discovery Systems," arXiv:2305.02251, 2023. https://arxiv.org/abs/2305.02251

### LLM and agentic scientific discovery

6. Chris Lu et al., "The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery," arXiv:2408.06292, 2024. https://arxiv.org/abs/2408.06292
7. Yutaro Yamada et al., "The AI Scientist-v2: Workshop-Level Automated Scientific Discovery via Agentic Tree Search," arXiv:2504.08066, 2025. https://arxiv.org/abs/2504.08066
8. Juraj Gottweis et al., "Towards an AI co-scientist," arXiv:2502.18864, 2025. https://arxiv.org/abs/2502.18864
9. Juraj Gottweis et al., "Accelerating scientific discovery with Co-Scientist," *Nature*, 2026. https://www.nature.com/articles/s41586-026-10644-y

### Critical framing

10. Use AI-assisted research systems as augmentation and acceleration tools. Do not treat them as replacements for empirical validation, peer review, domain expertise, or human scientific judgment.

---

## Notes For cellauto-lab

For the first cellauto-lab iteration, keep the AI role modest:

1. The notebook runs deterministic simulations.
2. Python extracts metrics.
3. The LLM reviews metrics and proposes hypotheses.
4. The next experiment is selected by the human operator.
5. Reports clearly mark all conclusions as tentative unless independently validated.

This keeps the project aligned with SYNTRAN AIEOS governance: human authority is final, AI actions are traceable, and sensitive claims are not made silently.
