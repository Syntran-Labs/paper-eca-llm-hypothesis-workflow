"""Behavioral metrics for elementary cellular automaton simulation outputs.

This module extracts quantitative behavioral signals from a simulation grid
produced by ``simulator.py``. Seven metrics together describe the density,
activity, temporal regularity, spatial complexity, and compressibility of an
ECA run.

Role in the workflow:
    ``metrics.py`` sits between the simulator and the reporting layer. The
    notebook calls ``compute_metrics()`` for every rule in the 256-rule sweep
    to populate the comparison DataFrame and to generate structured summaries.

Assumptions:
    - The input grid has dtype ``uint8`` with values strictly in ``{0, 1}``.
    - The grid shape is ``(n_steps + 1, n_cells)`` with at least two rows.
    - All metrics are proxies. They guide interpretation; they do not replace it.
      See ``docs/methodology.md`` for per-metric definitions and known blind spots.
    - No external dependencies beyond NumPy and the standard library ``zlib``.
      Offline. Deterministic for a given grid.
"""

from __future__ import annotations

import zlib

import numpy as np


def compute_metrics(grid: np.ndarray) -> dict[str, float]:
    """Compute standard behavioral metrics from an ECA simulation grid.

    Calculates seven metrics that characterize different aspects of a simulation:
    density over time, final density, spatial transitions, temporal activity,
    row-density entropy, temporal periodicity, and compression complexity.

    Args:
        grid: A two-dimensional array of shape ``(n_steps + 1, n_cells)`` with
            dtype ``uint8`` and values in ``{0, 1}``. Row 0 is the initial state;
            subsequent rows are successive time steps from ``simulate()``.

    Returns:
        A dictionary with exactly seven ``float`` keys, all rounded for stable
        JSON serialization:

        - ``density_mean``: Average fraction of cells equal to 1 across all rows.
        - ``density_final``: Fraction of cells equal to 1 in the last row.
        - ``transition_count``: Mean number of adjacent-cell state changes per row.
        - ``activity_score``: Mean fraction of cells that differ between consecutive rows.
        - ``entropy_score``: Shannon entropy of the per-row density distribution.
        - ``periodicity_score``: Fraction of consecutive identical rows after transient.
        - ``compression_ratio``: zlib-compressed size divided by raw byte size.

    Notes:
        **density_mean / density_final**: Distinguishes trivially extinct rules
        (density ≈ 0) and saturated rules (density ≈ 1) from everything else.

        **transition_count**: Counts horizontal boundary crossings per row by
        taking absolute differences between adjacent cells. High counts suggest
        fragmented or chaotic spatial structure; low counts suggest large uniform
        regions. Casting to ``int8`` before ``diff`` prevents uint8 wrap-around
        (e.g., 0 − 1 = 255 in uint8, not −1).

        **activity_score**: Averages the fraction of cells that change state
        between each pair of consecutive rows. A rule that reaches a fixed point
        quickly will have low activity, but the score includes the transient phase.

        **entropy_score**: Uses a 10-bin histogram of per-row densities over
        [0.0, 1.0]. Captures whether row densities are concentrated (low entropy)
        or spread across many values (high entropy). Does not capture spatial
        block structure within rows.

        **periodicity_score**: After skipping an initial transient of
        ``min(50, n_steps // 4)`` rows, checks what fraction of consecutive row
        pairs are byte-identical. Score of 1.0 means every pair was identical
        (fixed point). Beware: finite grids can produce apparent periodicity that
        is a boundary artifact rather than intrinsic rule behavior.

        **compression_ratio**: Serializes the grid to bytes (C-contiguous,
        row-major) and compresses with ``zlib`` at maximum effort. Highly regular
        grids compress well (low ratio); complex or chaotic grids resist
        compression (ratio approaching 1.0). This is a proxy for descriptive
        complexity, not Kolmogorov complexity.
    """
    n_rows, n_cells = grid.shape
    n_steps = n_rows - 1

    density_mean = float(grid.mean())
    density_final = float(grid[-1].mean())

    # Cast to int8 before diff to avoid uint8 underflow (0 - 1 = 255 in uint8).
    diffs = np.diff(grid.astype(np.int8), axis=1)
    transition_count = float(np.abs(diffs).sum(axis=1).mean())

    if n_steps > 0:
        activity_score = float((grid[1:] != grid[:-1]).mean())
    else:
        activity_score = 0.0

    # Row-density entropy: how uniformly spread are the per-row 1-fractions?
    # The right edge of the last bin is inclusive in numpy.histogram, so
    # density=1.0 is correctly captured without a separate bin.
    row_densities = grid.mean(axis=1)
    hist, _ = np.histogram(row_densities, bins=10, range=(0.0, 1.0))
    total = float(hist.sum())
    if total > 0:
        probs = hist[hist > 0].astype(float) / total
        entropy_score = float(-np.sum(probs * np.log2(probs)))
    else:
        entropy_score = 0.0

    # Skip an initial transient before checking for periodicity.
    # The window is capped at 50 rows to avoid consuming most of a short
    # simulation; for longer simulations it is n_steps // 4.
    transient = min(50, n_steps // 4)
    tail = grid[transient:]
    if len(tail) > 1:
        row_hashes = [hash(row.tobytes()) for row in tail]
        matches = sum(
            1 for i in range(1, len(row_hashes)) if row_hashes[i] == row_hashes[i - 1]
        )
        periodicity_score = matches / (len(row_hashes) - 1)
    else:
        periodicity_score = 0.0

    # Serialize the grid in C-contiguous row-major order (NumPy default for
    # tobytes()) and compress. Consistent byte ordering is required for
    # reproducible compression ratios across platforms.
    raw_bytes = grid.tobytes()
    compressed = zlib.compress(raw_bytes, level=9)
    compression_ratio = len(compressed) / max(len(raw_bytes), 1)

    return {
        "density_mean": round(density_mean, 6),
        "density_final": round(density_final, 6),
        "transition_count": round(transition_count, 4),
        "activity_score": round(activity_score, 6),
        "entropy_score": round(entropy_score, 6),
        "periodicity_score": round(periodicity_score, 6),
        "compression_ratio": round(compression_ratio, 6),
    }
