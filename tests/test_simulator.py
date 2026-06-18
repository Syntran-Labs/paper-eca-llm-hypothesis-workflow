"""Tests for cellauto_lab.simulator."""

import numpy as np
import pytest
from cellauto_lab.simulator import simulate, initial_state


class TestInitialState:
    def test_single_seed_shape(self):
        state = initial_state(100, "single_seed")
        assert state.shape == (100,)

    def test_single_seed_has_one_active_cell(self):
        state = initial_state(100, "single_seed")
        assert state.sum() == 1

    def test_single_seed_center_position(self):
        state = initial_state(100, "single_seed")
        assert state[50] == 1

    def test_single_seed_dtype(self):
        state = initial_state(100, "single_seed")
        assert state.dtype == np.uint8

    def test_random_shape(self):
        state = initial_state(100, "random", random_seed=42)
        assert state.shape == (100,)

    def test_random_binary_values(self):
        state = initial_state(100, "random", random_seed=42)
        assert set(np.unique(state)).issubset({0, 1})

    def test_random_deterministic_with_seed(self):
        a = initial_state(100, "random", random_seed=42)
        b = initial_state(100, "random", random_seed=42)
        assert np.array_equal(a, b)

    def test_random_differs_across_seeds(self):
        a = initial_state(100, "random", random_seed=1)
        b = initial_state(100, "random", random_seed=2)
        assert not np.array_equal(a, b)

    def test_unknown_condition_raises(self):
        with pytest.raises(ValueError):
            initial_state(100, "unknown")


class TestSimulate:
    def test_output_shape_default(self):
        grid = simulate(30)
        assert grid.shape == (201, 100)  # n_steps + 1 rows, n_cells cols

    def test_output_shape_custom(self):
        grid = simulate(110, n_cells=50, n_steps=100)
        assert grid.shape == (101, 50)

    def test_output_dtype(self):
        grid = simulate(30)
        assert grid.dtype == np.uint8

    def test_output_binary_only(self):
        grid = simulate(30)
        assert set(np.unique(grid)).issubset({0, 1})

    def test_rule_0_extinction(self):
        # Rule 0 maps every neighborhood to 0; grid is all-zero after step 1.
        grid = simulate(0, n_steps=10)
        assert grid[-1].sum() == 0

    def test_rule_255_saturation(self):
        # Rule 255 maps every neighborhood to 1; grid is all-one after step 1.
        grid = simulate(255, n_cells=100, n_steps=10)
        assert grid[-1].sum() == 100

    def test_rule_90_symmetric_single_seed(self):
        # Rule 90 with a single seed produces a symmetric pattern.
        grid = simulate(90, n_cells=101, n_steps=50)
        center = 50
        for row in grid:
            assert np.array_equal(row[:center], row[center + 1:][::-1])

    def test_random_initial_deterministic(self):
        a = simulate(30, initial_condition="random", random_seed=42)
        b = simulate(30, initial_condition="random", random_seed=42)
        assert np.array_equal(a, b)

    def test_random_initial_differs_across_seeds(self):
        a = simulate(30, initial_condition="random", random_seed=42)
        b = simulate(30, initial_condition="random", random_seed=99)
        assert not np.array_equal(a, b)

    def test_invalid_rule_raises(self):
        with pytest.raises(ValueError):
            simulate(256)

    def test_invalid_initial_condition_raises(self):
        with pytest.raises(ValueError):
            simulate(30, initial_condition="invalid")

    def test_row_zero_is_initial_state(self):
        grid = simulate(110, n_cells=20, n_steps=5)
        expected = initial_state(20, "single_seed")
        assert np.array_equal(grid[0], expected)
