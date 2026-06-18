"""One-dimensional elementary cellular automaton simulator.

This module runs deterministic, vectorized simulations of Wolfram elementary
cellular automata (ECA) over a fixed-size binary grid.

Role in the workflow:
    ``simulator.py`` is the core execution engine. It is called by the notebook
    for both the smoke-test set and the full 256-rule sweep. Its output — a
    two-dimensional NumPy array — is the raw material consumed by ``metrics.py``
    and ``reporting.py``.

Assumptions:
    - Grid is one-dimensional with binary cell states (0 or 1).
    - Boundary condition is ``fixed_zero``: cells outside the grid are treated as 0.
      This is the v1 default; periodic boundary is not yet implemented.
    - The NumPy random generator (``default_rng``) is used for reproducible random
      initial conditions. The same seed produces the same initial state across runs
      on the same platform and NumPy version.
    - No external dependencies beyond NumPy. Offline.
"""

from __future__ import annotations

import numpy as np

from cellauto_lab.rules import validate_rule


def initial_state(
    n_cells: int,
    condition: str = "single_seed",
    random_seed: int = 42,
) -> np.ndarray:
    """Create an initial cell state array for a cellular automaton simulation.

    Args:
        n_cells: Number of cells in the one-dimensional grid. Must be positive.
        condition: Initialization strategy. ``"single_seed"`` places a single
            active cell (state 1) at the center index ``n_cells // 2``, with all
            other cells set to 0. ``"random"`` fills the grid with independent
            uniform binary values using the given RNG seed.
        random_seed: Integer seed for the NumPy random generator. Used only when
            ``condition`` is ``"random"``. The same seed produces identical output
            across runs on the same platform and NumPy version.

    Returns:
        A one-dimensional ``np.ndarray`` of shape ``(n_cells,)`` with dtype
        ``uint8``. All values are in ``{0, 1}``.

    Raises:
        ValueError: If ``condition`` is not ``"single_seed"`` or ``"random"``.

    Notes:
        The ``"single_seed"`` condition is the standard starting point for
        visualizing rule symmetry and for reproducible sweeps across all 256
        rules. The ``"random"`` condition is useful for testing sensitivity to
        initial conditions, but the seed must be recorded in experiment metadata
        to keep the run reproducible.
    """
    if condition == "single_seed":
        state = np.zeros(n_cells, dtype=np.uint8)
        state[n_cells // 2] = 1
        return state
    if condition == "random":
        rng = np.random.default_rng(random_seed)
        return rng.integers(0, 2, size=n_cells, dtype=np.uint8)
    raise ValueError(
        f"Unknown initial_condition: {condition!r}. Use 'single_seed' or 'random'."
    )


def simulate(
    rule_number: int,
    n_cells: int = 100,
    n_steps: int = 200,
    initial_condition: str = "single_seed",
    random_seed: int = 42,
) -> np.ndarray:
    """Simulate an elementary cellular automaton and return its full history.

    Applies the Wolfram rule to a binary grid for ``n_steps`` discrete time
    steps, recording every generation. The simulation is fully deterministic
    given fixed parameters and seed.

    Boundary condition: ``fixed_zero`` — cells immediately outside the left and
    right edges are treated as permanently 0. This may introduce edge artifacts
    for rules that are sensitive to boundary state.

    Args:
        rule_number: Wolfram rule identifier in [0, 255]. Determines the
            transition function applied at every cell at every time step.
        n_cells: Width of the grid in cells. Default 100.
        n_steps: Number of time steps to simulate. Default 200. The returned
            array has ``n_steps + 1`` rows, including the initial state at row 0.
        initial_condition: Starting state strategy. ``"single_seed"`` or
            ``"random"``. See ``initial_state()`` for details.
        random_seed: RNG seed passed to ``initial_state()`` when
            ``initial_condition`` is ``"random"``. Ignored for ``"single_seed"``.

    Returns:
        A two-dimensional ``np.ndarray`` of shape ``(n_steps + 1, n_cells)``
        with dtype ``uint8``. Row 0 is the initial state; row ``t + 1`` is the
        state after applying the rule to row ``t``.

    Raises:
        TypeError: If ``rule_number`` is not an integer.
        ValueError: If ``rule_number`` is outside [0, 255], or if
            ``initial_condition`` is not a recognized value.

    Notes:
        The inner loop is vectorized: at each step, every cell's 3-cell
        neighborhood is encoded as an integer index (0–7) and looked up
        simultaneously in a precomputed array, avoiding a Python-level per-cell
        loop.

        Reproducibility: given identical arguments, ``simulate()`` always
        produces the same output. For ``"random"`` initial conditions, the
        ``random_seed`` must be recorded in experiment metadata.
    """
    validate_rule(rule_number)

    # Precompute a length-8 lookup array: lookup[i] = output bit for the
    # neighborhood whose index is i = left*4 + center*2 + right.
    # This avoids a Python-level dict lookup on every cell at every step.
    lookup = np.array(
        [(rule_number >> i) & 1 for i in range(8)],
        dtype=np.uint8,
    )

    grid = np.zeros((n_steps + 1, n_cells), dtype=np.uint8)
    grid[0] = initial_state(n_cells, initial_condition, random_seed)

    for t in range(n_steps):
        row = grid[t]
        # Pad with one zero on each side to implement the fixed_zero boundary:
        # out-of-bound cells are always treated as state 0.
        padded = np.pad(row, 1, mode="constant", constant_values=0)
        left = padded[:-2]
        center = padded[1:-1]
        right = padded[2:]
        # Encode each cell's neighborhood as a 3-bit integer in [0, 7],
        # then look up the output bit for all cells simultaneously.
        indices = left * 4 + center * 2 + right
        grid[t + 1] = lookup[indices]

    return grid
