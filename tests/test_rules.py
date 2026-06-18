"""Tests for cellauto_lab.rules."""

import pytest
from cellauto_lab.rules import validate_rule, rule_table, neighborhood_ordering, NEIGHBORHOODS


class TestValidateRule:
    def test_valid_lower_bound(self):
        assert validate_rule(0) == 0

    def test_valid_upper_bound(self):
        assert validate_rule(255) == 255

    def test_valid_midrange(self):
        assert validate_rule(110) == 110

    def test_invalid_below_zero(self):
        with pytest.raises(ValueError):
            validate_rule(-1)

    def test_invalid_above_255(self):
        with pytest.raises(ValueError):
            validate_rule(256)

    def test_invalid_type_float(self):
        with pytest.raises(TypeError):
            validate_rule(1.5)  # type: ignore[arg-type]

    def test_invalid_type_string(self):
        with pytest.raises(TypeError):
            validate_rule("30")  # type: ignore[arg-type]


class TestRuleTable:
    def test_table_has_eight_entries(self):
        assert len(rule_table(110)) == 8

    def test_keys_are_three_tuples(self):
        for key in rule_table(30):
            assert isinstance(key, tuple)
            assert len(key) == 3

    def test_keys_contain_binary_values(self):
        for key in rule_table(90):
            assert all(v in (0, 1) for v in key)

    def test_values_are_binary(self):
        for value in rule_table(90).values():
            assert value in (0, 1)

    def test_rule_0_all_outputs_zero(self):
        table = rule_table(0)
        assert all(v == 0 for v in table.values())

    def test_rule_255_all_outputs_one(self):
        table = rule_table(255)
        assert all(v == 1 for v in table.values())

    def test_rule_110_known_spot_checks(self):
        # Rule 110 = 01101110 in binary
        table = rule_table(110)
        assert table[(1, 1, 1)] == 0  # index 7, bit 7 of 110 = 0
        assert table[(1, 1, 0)] == 1  # index 6, bit 6 of 110 = 1
        assert table[(1, 0, 1)] == 1  # index 5, bit 5 of 110 = 1
        assert table[(1, 0, 0)] == 0  # index 4, bit 4 of 110 = 0
        assert table[(0, 1, 1)] == 1  # index 3, bit 3 of 110 = 1
        assert table[(0, 1, 0)] == 1  # index 2, bit 2 of 110 = 1
        assert table[(0, 0, 1)] == 1  # index 1, bit 1 of 110 = 1
        assert table[(0, 0, 0)] == 0  # index 0, bit 0 of 110 = 0

    def test_rule_30_known_spot_checks(self):
        # Rule 30 = 00011110 in binary
        table = rule_table(30)
        assert table[(1, 1, 1)] == 0  # bit 7 = 0
        assert table[(1, 0, 0)] == 1  # bit 4 = 1
        assert table[(0, 1, 1)] == 1  # bit 3 = 1
        assert table[(0, 0, 0)] == 0  # bit 0 = 0


class TestNeighborhoodOrdering:
    def test_ordering_has_eight_elements(self):
        assert len(neighborhood_ordering()) == 8

    def test_first_is_111(self):
        assert neighborhood_ordering()[0] == (1, 1, 1)

    def test_last_is_000(self):
        assert neighborhood_ordering()[-1] == (0, 0, 0)

    def test_all_entries_are_binary_triples(self):
        for nbhd in neighborhood_ordering():
            assert len(nbhd) == 3
            assert all(v in (0, 1) for v in nbhd)

    def test_matches_constant(self):
        assert neighborhood_ordering() == NEIGHBORHOODS
