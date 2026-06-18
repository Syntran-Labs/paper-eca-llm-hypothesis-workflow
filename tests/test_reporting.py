"""Tests for cellauto_lab.reporting."""

import datetime
import json

import numpy as np
import pytest

from cellauto_lab.metrics import compute_metrics
from cellauto_lab.reporting import experiment_summary, summaries_to_json
from cellauto_lab.simulator import simulate

SUMMARY_KEYS = {
    "experiment_id",
    "timestamp_utc",
    "rule_number",
    "parameters",
    "observation",
    "metrics",
    "interpretation_placeholder",
    "hypothesis_placeholder",
    "next_experiments_placeholder",
}

PARAMETER_KEYS = {
    "n_cells",
    "n_steps",
    "initial_condition",
    "random_seed",
    "boundary_condition",
}


@pytest.fixture
def sample_grid():
    return simulate(30, n_cells=50, n_steps=100)


class TestExperimentSummaryStructure:
    def test_all_expected_keys_present(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert SUMMARY_KEYS.issubset(result.keys())

    def test_no_unexpected_keys(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert set(result.keys()) == SUMMARY_KEYS

    def test_parameters_has_all_expected_keys(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert set(result["parameters"].keys()) == PARAMETER_KEYS


class TestExperimentSummaryValues:
    def test_rule_number_matches_input(self, sample_grid):
        result = experiment_summary(110, sample_grid)
        assert result["rule_number"] == 110

    def test_experiment_id_default_initial_condition(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert result["experiment_id"] == "rule_030_unknown"

    def test_experiment_id_with_custom_initial_condition(self, sample_grid):
        result = experiment_summary(30, sample_grid, parameters={"initial_condition": "single_seed"})
        assert result["experiment_id"] == "rule_030_single_seed"

    def test_experiment_id_pads_rule_to_three_digits(self, sample_grid):
        result = experiment_summary(5, sample_grid)
        assert result["experiment_id"].startswith("rule_005_")

    def test_timestamp_utc_ends_with_z(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert result["timestamp_utc"].endswith("Z")

    def test_timestamp_utc_parses_as_iso_8601(self, sample_grid):
        ts = experiment_summary(30, sample_grid)["timestamp_utc"]
        datetime.datetime.fromisoformat(ts.rstrip("Z"))

    def test_interpretation_placeholder_is_empty_string(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert result["interpretation_placeholder"] == ""

    def test_hypothesis_placeholder_is_empty_string(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert result["hypothesis_placeholder"] == ""

    def test_next_experiments_placeholder_is_empty_list(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert result["next_experiments_placeholder"] == []

    def test_metrics_match_compute_metrics(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert result["metrics"] == compute_metrics(sample_grid)

    def test_parameters_n_cells_derived_from_grid(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert result["parameters"]["n_cells"] == sample_grid.shape[1]

    def test_parameters_n_steps_derived_from_grid(self, sample_grid):
        result = experiment_summary(30, sample_grid)
        assert result["parameters"]["n_steps"] == sample_grid.shape[0] - 1


class TestExperimentSummaryParameters:
    def test_none_parameters_defaults_initial_condition_unknown(self, sample_grid):
        result = experiment_summary(30, sample_grid, parameters=None)
        assert result["parameters"]["initial_condition"] == "unknown"

    def test_none_parameters_defaults_random_seed_none(self, sample_grid):
        result = experiment_summary(30, sample_grid, parameters=None)
        assert result["parameters"]["random_seed"] is None

    def test_none_parameters_defaults_boundary_condition(self, sample_grid):
        result = experiment_summary(30, sample_grid, parameters=None)
        assert result["parameters"]["boundary_condition"] == "fixed_zero"

    def test_custom_initial_condition_recorded(self, sample_grid):
        params = {"initial_condition": "random", "random_seed": 42}
        result = experiment_summary(30, sample_grid, parameters=params)
        assert result["parameters"]["initial_condition"] == "random"
        assert result["parameters"]["random_seed"] == 42

    def test_random_seed_included_in_observation(self, sample_grid):
        result = experiment_summary(30, sample_grid, parameters={"random_seed": 99})
        assert "99" in result["observation"]

    def test_none_random_seed_absent_from_observation(self, sample_grid):
        result = experiment_summary(30, sample_grid, parameters=None)
        assert "Random seed" not in result["observation"]

    def test_observation_notes_appended_to_observation(self, sample_grid):
        notes = "Visual inspection shows diagonal stripes."
        result = experiment_summary(30, sample_grid, observation_notes=notes)
        assert notes in result["observation"]

    def test_empty_observation_notes_leaves_observation_unchanged(self, sample_grid):
        result_a = experiment_summary(30, sample_grid, observation_notes="")
        result_b = experiment_summary(30, sample_grid)
        assert result_a["observation"] == result_b["observation"]

    def test_observation_contains_rule_number(self, sample_grid):
        result = experiment_summary(110, sample_grid)
        assert "110" in result["observation"]

    def test_observation_contains_boundary_condition(self, sample_grid):
        result = experiment_summary(30, sample_grid, parameters={"boundary_condition": "fixed_zero"})
        assert "fixed_zero" in result["observation"]

    def test_observation_contains_step_count(self):
        grid = simulate(30, n_cells=20, n_steps=50)
        result = experiment_summary(30, grid)
        assert "50" in result["observation"]

    def test_observation_contains_cell_count(self):
        grid = simulate(30, n_cells=37, n_steps=10)
        result = experiment_summary(30, grid)
        assert "37" in result["observation"]


class TestSummariesToJson:
    def test_empty_list_returns_valid_json(self):
        output = summaries_to_json([])
        assert json.loads(output) == []

    def test_returns_string(self):
        assert isinstance(summaries_to_json([]), str)

    def test_single_summary_round_trips(self):
        grid = simulate(30, n_cells=20, n_steps=20)
        summary = experiment_summary(30, grid)
        parsed = json.loads(summaries_to_json([summary]))
        assert len(parsed) == 1
        assert parsed[0]["rule_number"] == 30

    def test_multiple_summaries_order_preserved(self):
        grid = simulate(30, n_cells=20, n_steps=20)
        summaries = [experiment_summary(r, grid) for r in [0, 30, 110]]
        parsed = json.loads(summaries_to_json(summaries))
        assert [p["rule_number"] for p in parsed] == [0, 30, 110]

    def test_default_indent_produces_multiline_output(self):
        grid = simulate(0, n_cells=5, n_steps=5)
        output = summaries_to_json([experiment_summary(0, grid)])
        assert "\n" in output

    def test_custom_indent_four_spaces(self):
        grid = simulate(0, n_cells=5, n_steps=5)
        output = summaries_to_json([experiment_summary(0, grid)], indent=4)
        assert "    " in output

    def test_placeholders_serialized_correctly(self):
        grid = simulate(0, n_cells=5, n_steps=5)
        parsed = json.loads(summaries_to_json([experiment_summary(0, grid)]))[0]
        assert parsed["interpretation_placeholder"] == ""
        assert parsed["hypothesis_placeholder"] == ""
        assert parsed["next_experiments_placeholder"] == []
