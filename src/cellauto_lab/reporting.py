"""Structured experiment summaries for later LLM review.

This module produces machine-readable experiment summaries that deliberately
separate factual content (observation, metrics) from unfilled placeholders
(interpretation, hypothesis, next experiments). The separation enforces the
``scientific-research`` domain principle: do not conflate what was measured with
what it means.

Role in the workflow:
    ``reporting.py`` is the final step of the v1 pipeline. The notebook calls
    ``experiment_summary()`` for selected rules after simulation and metric
    extraction are complete. The resulting summaries are designed to be passed
    verbatim to an LLM in a future, governed workflow step without further
    preprocessing.

Assumptions:
    - No LLM calls are made in this module. All interpretation fields are empty
      strings or empty lists — explicit placeholders, not absent fields.
    - Timestamps use UTC to avoid timezone ambiguity in experiment metadata.
    - The ``parameters`` dict is expected to contain ``initial_condition``,
      ``random_seed``, ``boundary_condition``, ``n_cells``, and ``n_steps``.
      Missing keys fall back to safe defaults.
    - No external dependencies beyond the standard library and ``metrics.py``.
      Offline.
"""

from __future__ import annotations

import datetime
import json
from typing import Any

import numpy as np

from cellauto_lab.metrics import compute_metrics


def experiment_summary(
    rule_number: int,
    grid: np.ndarray,
    parameters: dict[str, Any] | None = None,
    observation_notes: str = "",
) -> dict[str, Any]:
    """Generate a structured experiment summary suitable for later LLM review.

    Produces a dictionary that separates factual, computed content from
    explicitly empty placeholder fields. The placeholder fields are not to be
    filled by the caller; they are reserved for an LLM agent in a governed,
    separate workflow step.

    Args:
        rule_number: Wolfram rule identifier (0–255). Used in the experiment ID
            and included in the parameters block.
        grid: Simulation output from ``simulate()``. Shape
            ``(n_steps + 1, n_cells)``, dtype ``uint8``.
        parameters: Optional dictionary of experiment parameters. Recognized
            keys: ``initial_condition`` (str), ``random_seed`` (int or None),
            ``boundary_condition`` (str), ``n_cells`` (int), ``n_steps`` (int).
            Missing keys use safe defaults. Pass ``None`` to accept all defaults.
        observation_notes: Optional free-text string of additional factual
            observations to append to the ``observation`` field. Must describe
            only what was measured or computed, not interpretation.

    Returns:
        A dictionary with the following structure:

        - ``experiment_id`` (str): Human-readable identifier such as
          ``"rule_030_single_seed"``.
        - ``timestamp_utc`` (str): ISO 8601 UTC timestamp of summary generation.
        - ``rule_number`` (int): The Wolfram rule number.
        - ``parameters`` (dict): Recorded experiment parameters for reproducibility.
        - ``observation`` (str): Factual description of what was simulated.
          Contains only directly measurable facts: rule number, step count, cell
          count, initial condition, boundary condition, and optional caller notes.
        - ``metrics`` (dict): Output of ``compute_metrics(grid)``.
        - ``interpretation_placeholder`` (str): Empty string. Reserved for LLM.
        - ``hypothesis_placeholder`` (str): Empty string. Reserved for LLM.
        - ``next_experiments_placeholder`` (list): Empty list. Reserved for LLM.

    Notes:
        The three placeholder fields are intentionally empty, not absent. An LLM
        reviewing this summary should populate them based solely on the recorded
        ``observation`` and ``metrics``, without fabricating claims that go beyond
        the evidence. The ``scientific-research`` domain pack governs what content
        is appropriate for each placeholder field.

        The ``observation`` field is always strictly factual. It never contains
        interpretation or causal claims — those belong in ``interpretation_placeholder``
        after LLM review.
    """
    metrics = compute_metrics(grid)
    n_rows, n_cells = grid.shape
    n_steps = n_rows - 1

    params = parameters or {}
    initial_condition = params.get("initial_condition", "unknown")
    random_seed = params.get("random_seed", None)
    boundary_condition = params.get("boundary_condition", "fixed_zero")

    # Build the observation field from verifiable facts only.
    # Observation and interpretation must remain in separate output fields.
    obs_parts = [
        f"Rule {rule_number} simulated for {n_steps} steps over {n_cells} cells.",
        f"Initial condition: {initial_condition}.",
        f"Boundary condition: {boundary_condition}.",
    ]
    if random_seed is not None:
        obs_parts.append(f"Random seed: {random_seed}.")
    if observation_notes:
        obs_parts.append(observation_notes)

    return {
        "experiment_id": f"rule_{rule_number:03d}_{initial_condition}",
        "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
        "rule_number": rule_number,
        "parameters": {
            "n_cells": n_cells,
            "n_steps": n_steps,
            "initial_condition": initial_condition,
            "random_seed": random_seed,
            "boundary_condition": boundary_condition,
        },
        "observation": " ".join(obs_parts),
        "metrics": metrics,
        # Placeholder fields are deliberately empty. Reserved for LLM-assisted
        # analysis in a governed future workflow step.
        "interpretation_placeholder": "",
        "hypothesis_placeholder": "",
        "next_experiments_placeholder": [],
    }


def summaries_to_json(summaries: list[dict[str, Any]], indent: int = 2) -> str:
    """Serialize a list of experiment summaries to a formatted JSON string.

    Args:
        summaries: List of summary dictionaries produced by
            ``experiment_summary()``.
        indent: Number of spaces used for JSON indentation. Default 2.

    Returns:
        A UTF-8 compatible JSON string representing the list of summaries.
        Suitable for writing to a file or passing as an LLM prompt context block.
    """
    return json.dumps(summaries, indent=indent)
