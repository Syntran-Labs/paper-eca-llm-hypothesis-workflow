"""Tests for cellauto_lab package-level API exports."""

import cellauto_lab
from cellauto_lab import (
    compute_metrics,
    experiment_summary,
    initial_state,
    neighborhood_ordering,
    rule_table,
    simulate,
    summaries_to_json,
    validate_rule,
)

EXPECTED_ALL = {
    "rule_table",
    "validate_rule",
    "neighborhood_ordering",
    "simulate",
    "initial_state",
    "compute_metrics",
    "experiment_summary",
    "summaries_to_json",
}


class TestAllExports:
    def test_all_names_present_in_module(self):
        for name in cellauto_lab.__all__:
            assert hasattr(cellauto_lab, name), f"{name!r} missing from package"

    def test_all_list_is_complete(self):
        assert set(cellauto_lab.__all__) == EXPECTED_ALL

    def test_no_undeclared_exports_missing(self):
        for name in EXPECTED_ALL:
            assert name in cellauto_lab.__all__


class TestImportedCallables:
    def test_rule_table_is_callable(self):
        assert callable(rule_table)

    def test_validate_rule_is_callable(self):
        assert callable(validate_rule)

    def test_neighborhood_ordering_is_callable(self):
        assert callable(neighborhood_ordering)

    def test_simulate_is_callable(self):
        assert callable(simulate)

    def test_initial_state_is_callable(self):
        assert callable(initial_state)

    def test_compute_metrics_is_callable(self):
        assert callable(compute_metrics)

    def test_experiment_summary_is_callable(self):
        assert callable(experiment_summary)

    def test_summaries_to_json_is_callable(self):
        assert callable(summaries_to_json)


class TestPackageLevelFunctionality:
    def test_rule_table_returns_eight_entries(self):
        assert len(cellauto_lab.rule_table(110)) == 8

    def test_validate_rule_accepts_valid_number(self):
        assert cellauto_lab.validate_rule(30) == 30

    def test_neighborhood_ordering_returns_eight_triples(self):
        assert len(cellauto_lab.neighborhood_ordering()) == 8

    def test_simulate_returns_correct_shape(self):
        grid = cellauto_lab.simulate(30, n_cells=10, n_steps=5)
        assert grid.shape == (6, 10)

    def test_initial_state_returns_correct_shape(self):
        state = cellauto_lab.initial_state(20)
        assert state.shape == (20,)

    def test_compute_metrics_returns_dict(self):
        grid = cellauto_lab.simulate(30, n_cells=10, n_steps=5)
        assert isinstance(cellauto_lab.compute_metrics(grid), dict)

    def test_experiment_summary_returns_dict(self):
        grid = cellauto_lab.simulate(30, n_cells=10, n_steps=5)
        assert isinstance(cellauto_lab.experiment_summary(30, grid), dict)

    def test_summaries_to_json_returns_string(self):
        assert isinstance(cellauto_lab.summaries_to_json([]), str)

    def test_package_imports_are_same_objects_as_module_imports(self):
        import cellauto_lab.rules as rules_mod
        import cellauto_lab.simulator as sim_mod
        import cellauto_lab.metrics as metrics_mod
        import cellauto_lab.reporting as reporting_mod

        assert cellauto_lab.rule_table is rules_mod.rule_table
        assert cellauto_lab.simulate is sim_mod.simulate
        assert cellauto_lab.compute_metrics is metrics_mod.compute_metrics
        assert cellauto_lab.experiment_summary is reporting_mod.experiment_summary
