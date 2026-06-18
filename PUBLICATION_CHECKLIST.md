# Publication Checklist

**Repository:** `cellauto-lab`
**Status:** Incubation — private research workspace

This checklist must be completed before any results from this project are shared externally, published, or presented.

---

## 1. Reproducibility

- [ ] All experiments use explicit, recorded parameters
- [ ] Random seeds are fixed and recorded in all outputs
- [ ] Notebook runs clean from restart (Kernel → Restart & Run All)
- [ ] No hidden notebook state contaminates results
- [ ] All output files are regeneratable from source
- [ ] Python version and package versions are recorded

---

## 2. Code Quality

- [ ] All tests pass: `pytest tests/`
- [ ] No hardcoded paths or secrets in source
- [ ] Rule encoding verified against known-value spot checks
- [ ] Simulation output shapes verified
- [ ] Metrics return expected keys and value ranges

---

## 3. Epistemic Honesty

- [ ] All behavioral classifications are labeled as **tentative**
- [ ] Observations and interpretations are clearly separated in all outputs
- [ ] No universality or complexity claims are made from visual inspection alone
- [ ] Interest scores and ranking are documented as heuristics, not ground truth
- [ ] Finite-size effects and boundary artifacts are acknowledged in methodology

---

## 4. Metric Validity

- [ ] Each metric has a documented definition, expected range, and limitation
- [ ] `compression_ratio` is presented as a proxy, not a proof of complexity
- [ ] `periodicity_score` acknowledges that finite-grid cycles may be boundary artifacts
- [ ] `entropy_score` is row-level only; spatial block structure may be missed
- [ ] No metric is used outside its documented scope

---

## 5. Literature and Attribution

- [ ] All cited references include title, author, year, and DOI or verified URL
- [ ] Source quality labels are attached to each reference
- [ ] No citations are fabricated or unverified
- [ ] Claims based on literature are traceable to specific sources

---

## 6. AI-Assisted Content

- [ ] All LLM-generated content is marked as such
- [ ] LLM hypotheses are stored as artifacts, not conclusions
- [ ] Prompt versions are recorded alongside LLM outputs
- [ ] No LLM output is treated as a mathematical or empirical proof
- [ ] Human operator has reviewed and approved all published interpretations

---

## 7. Security and Privacy

- [ ] No secrets, API keys, or credentials appear in source or outputs
- [ ] `.env` is in `.gitignore`
- [ ] `.claude/` is in `.gitignore`
- [ ] No personal data is included in research artifacts

---

## 8. Scope Declaration

- [ ] The publication clearly states: private incubation research, not peer-reviewed
- [ ] The publication clearly states: simulation-only, no empirical claims
- [ ] Limitations section is present and complete
- [ ] Next steps are framed as open questions, not conclusions

---

## Sign-Off

| Item | Reviewer | Date |
|---|---|---|
| Reproducibility | | |
| Code quality | | |
| Epistemic honesty | | |
| Metric validity | | |
| Literature | | |
| AI content review | | |
| Security | | |
| Scope declaration | | |
