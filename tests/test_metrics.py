"""Tests for cellauto_lab.metrics."""

import numpy as np
import pytest
from cellauto_lab.simulator import simulate
from cellauto_lab.metrics import compute_metrics

EXPECTED_KEYS = {
    "density_mean",
    "density_final",
    "transition_count",
    "activity_score",
    "entropy_score",
    "periodicity_score",
    "compression_ratio",
}


class TestMetricKeys:
    def test_all_expected_keys_present(self):
        grid = simulate(30)
        result = compute_metrics(grid)
        assert EXPECTED_KEYS.issubset(result.keys())

    def test_no_unexpected_keys(self):
        grid = simulate(30)
        result = compute_metrics(grid)
        assert set(result.keys()) == EXPECTED_KEYS


class TestMetricRanges:
    def test_density_mean_in_unit_interval(self):
        assert 0.0 <= compute_metrics(simulate(30))["density_mean"] <= 1.0

    def test_density_final_in_unit_interval(self):
        assert 0.0 <= compute_metrics(simulate(110))["density_final"] <= 1.0

    def test_activity_score_in_unit_interval(self):
        assert 0.0 <= compute_metrics(simulate(90))["activity_score"] <= 1.0

    def test_periodicity_score_in_unit_interval(self):
        assert 0.0 <= compute_metrics(simulate(30))["periodicity_score"] <= 1.0

    def test_compression_ratio_positive(self):
        assert compute_metrics(simulate(30))["compression_ratio"] > 0.0

    def test_transition_count_non_negative(self):
        assert compute_metrics(simulate(30))["transition_count"] >= 0.0

    def test_entropy_score_non_negative(self):
        assert compute_metrics(simulate(30))["entropy_score"] >= 0.0


class TestKnownRuleBehavior:
    def test_rule_0_density_final_zero(self):
        # Rule 0 drives all cells to 0 after step 1.
        m = compute_metrics(simulate(0, n_steps=50))
        assert m["density_final"] == 0.0

    def test_rule_255_density_final_one(self):
        # Rule 255 drives all cells to 1 after step 1.
        m = compute_metrics(simulate(255, n_cells=100, n_steps=50))
        assert m["density_final"] == 1.0

    def test_rule_0_high_periodicity(self):
        # After the transient, rule 0 is a fixed point — all rows identical.
        m = compute_metrics(simulate(0, n_steps=100))
        assert m["periodicity_score"] > 0.9

    def test_rule_30_low_periodicity(self):
        # Rule 30 is chaotic; consecutive rows are rarely identical.
        m = compute_metrics(simulate(30))
        assert m["periodicity_score"] < 0.5


class TestReproducibility:
    def test_seeded_random_produces_identical_metrics(self):
        m_a = compute_metrics(simulate(30, initial_condition="random", random_seed=7))
        m_b = compute_metrics(simulate(30, initial_condition="random", random_seed=7))
        assert m_a == m_b

    def test_different_seeds_may_produce_different_metrics(self):
        m_a = compute_metrics(simulate(30, initial_condition="random", random_seed=7))
        m_b = compute_metrics(simulate(30, initial_condition="random", random_seed=8))
        # Not guaranteed to differ for all rules but almost certain for rule 30
        assert m_a != m_b


class TestEdgeCases:
    def test_all_zeros_grid_density_is_zero(self):
        grid = np.zeros((5, 20), dtype=np.uint8)
        m = compute_metrics(grid)
        assert m["density_mean"] == 0.0
        assert m["density_final"] == 0.0

    def test_all_zeros_grid_activity_is_zero(self):
        grid = np.zeros((5, 20), dtype=np.uint8)
        assert compute_metrics(grid)["activity_score"] == 0.0

    def test_all_zeros_grid_transition_count_is_zero(self):
        grid = np.zeros((5, 20), dtype=np.uint8)
        assert compute_metrics(grid)["transition_count"] == 0.0

    def test_all_zeros_grid_periodicity_is_one(self):
        # Every consecutive row pair is identical — fixed point.
        grid = np.zeros((10, 20), dtype=np.uint8)
        assert compute_metrics(grid)["periodicity_score"] == 1.0

    def test_all_ones_grid_density_is_one(self):
        grid = np.ones((5, 20), dtype=np.uint8)
        m = compute_metrics(grid)
        assert m["density_mean"] == 1.0
        assert m["density_final"] == 1.0

    def test_single_row_activity_score_is_zero(self):
        # n_steps=0 triggers the explicit zero branch in compute_metrics.
        grid = simulate(30, n_cells=50, n_steps=0)
        assert compute_metrics(grid)["activity_score"] == 0.0

    def test_single_row_periodicity_score_is_zero(self):
        # Tail has only one row; no consecutive pairs to compare.
        grid = simulate(30, n_cells=50, n_steps=0)
        assert compute_metrics(grid)["periodicity_score"] == 0.0

    def test_compression_ratio_uniform_grid_below_one(self):
        # A highly uniform grid should compress to a ratio well below 1.0.
        grid = np.zeros((50, 100), dtype=np.uint8)
        assert compute_metrics(grid)["compression_ratio"] < 0.5

    def test_metrics_values_are_floats(self):
        grid = simulate(110)
        m = compute_metrics(grid)
        for key, value in m.items():
            assert isinstance(value, float), f"{key} is not a float"
