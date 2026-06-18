"""Wolfram elementary cellular automaton rule encoding.

This module is responsible for converting a Wolfram rule number (0–255) into a
transition table that maps every possible 3-cell neighborhood to its binary output.

Role in the workflow:
    ``rules.py`` is the foundational layer. It is called by ``simulator.py`` to
    build the per-step lookup table and is also exposed directly for inspection
    and explanatory displays in the notebook.

Assumptions:
    - Rules are elementary cellular automata: one-dimensional, binary states, radius 1.
    - The canonical Wolfram encoding is used throughout: neighborhood index
      ``i = left*4 + center*2 + right``; bit ``i`` of the rule number determines
      the output for that neighborhood.
    - No external dependencies. Pure Python. Offline.
"""

from __future__ import annotations

# Canonical Wolfram neighborhood ordering: (1,1,1) has index 7 (highest bit)
# down to (0,0,0) with index 0 (lowest bit). This order matches the Wolfram
# Atlas convention and is used in explanatory notebook displays.
NEIGHBORHOODS: tuple[tuple[int, int, int], ...] = (
    (1, 1, 1),
    (1, 1, 0),
    (1, 0, 1),
    (1, 0, 0),
    (0, 1, 1),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 0),
)


def validate_rule(rule_number: int) -> int:
    """Validate that a Wolfram rule number is an integer in [0, 255].

    Args:
        rule_number: Wolfram elementary cellular automaton rule identifier.
            Expected to be a Python ``int`` in the range 0 to 255 inclusive.

    Returns:
        The validated ``rule_number`` unchanged, allowing use in chained calls.

    Raises:
        TypeError: If ``rule_number`` is not a Python ``int``.
        ValueError: If ``rule_number`` is outside the range [0, 255].

    Notes:
        Elementary cellular automata have 2^3 = 8 possible binary neighborhoods.
        Each neighborhood maps to one binary output, giving 2^8 = 256 possible
        rules, numbered 0 through 255.
    """
    if not isinstance(rule_number, int):
        raise TypeError(
            f"Rule number must be an int, got {type(rule_number).__name__}"
        )
    if not (0 <= rule_number <= 255):
        raise ValueError(
            f"Rule number must be in range 0–255, got {rule_number}"
        )
    return rule_number


def rule_table(rule_number: int) -> dict[tuple[int, int, int], int]:
    """Convert a Wolfram rule number to its complete transition table.

    The transition table maps each of the 8 possible 3-cell neighborhoods to a
    binary output (0 or 1) as specified by the Wolfram encoding.

    Args:
        rule_number: Wolfram rule identifier in [0, 255].

    Returns:
        A dictionary with exactly 8 entries. Keys are ``(left, center, right)``
        tuples with values in ``{0, 1}``. Values are the binary outputs for each
        neighborhood under this rule.

    Raises:
        TypeError: If ``rule_number`` is not an integer.
        ValueError: If ``rule_number`` is outside [0, 255].

    Notes:
        Wolfram encoding: the neighborhood ``(left, center, right)`` has integer
        index ``i = left*4 + center*2 + right``. Bit ``i`` of the rule number
        (i.e., ``(rule_number >> i) & 1``) gives the output for that neighborhood.

        Example — Rule 110 = 01101110 in binary:
            - (1,1,1) → index 7, bit 7 = 0
            - (1,1,0) → index 6, bit 6 = 1
            - (0,0,0) → index 0, bit 0 = 0
    """
    validate_rule(rule_number)
    return {
        neighborhood: (rule_number >> (left * 4 + center * 2 + right)) & 1
        for neighborhood in NEIGHBORHOODS
        for left, center, right in [neighborhood]
    }


def neighborhood_ordering() -> tuple[tuple[int, int, int], ...]:
    """Return the canonical Wolfram neighborhood ordering.

    Returns:
        A tuple of 8 ``(left, center, right)`` triples, ordered from
        ``(1, 1, 1)`` (index 7) down to ``(0, 0, 0)`` (index 0). This ordering
        matches the Wolfram Atlas convention and is used in notebook displays.

    Notes:
        The ordering runs from highest binary index to lowest — from the
        neighborhood that contributes the most-significant bit of the rule number
        to the one that contributes the least-significant bit.
    """
    return NEIGHBORHOODS
