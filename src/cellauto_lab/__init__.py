"""cellauto-lab: Elementary cellular automaton research workspace.

This package provides the core Python library for the ``cellauto-lab`` project —
a SYNTRAN Labs incubation workspace for exploring one-dimensional elementary
cellular automata (ECA) using a notebook-first, LLM-ready workflow.

Package architecture:
    - ``rules``: Wolfram rule encoding — validates rule numbers and converts them
      to 8-entry transition tables using the canonical Wolfram bit convention.
    - ``simulator``: Vectorized ECA simulation — produces a full space-time grid
      as a NumPy ``uint8`` array using a fixed-zero boundary condition.
    - ``metrics``: Behavioral metric extraction — computes seven quantitative
      signals (density, activity, entropy, periodicity, compression) from a
      simulation grid.
    - ``reporting``: Structured summary generation — builds experiment records
      with explicit observation/metrics/placeholder separation, ready for LLM
      review under SYNTRAN AIEOS governance.

All modules are offline, dependency-light (NumPy + standard library), and make
no external API or LLM calls.
"""

from cellauto_lab.rules import neighborhood_ordering, rule_table, validate_rule
from cellauto_lab.simulator import initial_state, simulate
from cellauto_lab.metrics import compute_metrics
from cellauto_lab.reporting import experiment_summary, summaries_to_json

__all__ = [
    "rule_table",
    "validate_rule",
    "neighborhood_ordering",
    "simulate",
    "initial_state",
    "compute_metrics",
    "experiment_summary",
    "summaries_to_json",
]
