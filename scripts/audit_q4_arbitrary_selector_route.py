#!/usr/bin/env python3
"""Experiment 294: recover Q4 function without a target terminal or core location.

This is a modern strengthening of the older broad Q4 inverse searches.

Parent space:
  * six raw-compatible primary POS3 payloads;
  * every abstract ternary Q4 selector map, 3^9 = 19,683 maps;
  * every one of the C(9,3) = 84 choices of three Q4 positions as a possible
    variable control core.

No raw Q4 slash/dot observations, shared polarity, expected Q4 scaffold,
expected A/D/G core location, expected control words, expected state count,
expected terminal payload, or expected route shell is used as a filter.

For every primary-payload / selector pair:
  1. require all three first-pass regenerated surfaces to be valid POS3;
  2. require the second-pass surface to be valid POS3.

Then, for each possible three-position core, group the surviving pairs by:
  * the fixed values on the other six selector positions; and
  * their common second-pass terminal word.

A group is route-capable only if its distinct first-pass functional families
number exactly three and one q-indexed output can be chosen from each so that
all three chosen words are distinct permutations of 0,1,2 (Experiment 278's
independently derived route criterion).

Goal:
  ask whether operation closure + reversible routing recover the functional Q4
  selector, including the physical location of its variable core, without
  supplying terminal 100 or the old A/D/G single-defect grammar.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from itertools import combinations, product

from enumerate_raw_machine import (
    SERIAL_ORDER,
    compact_primary_signature,
    decode_dash_pos3,
    enumerate_primary_payloads,
    first_pass_surface,
    load_rows,
    primary_column_candidates,
    terminal_surface,
)


def is_permutation(word: str) -> bool:
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def route_shells(families):
    families = tuple(sorted(families))
    if len(families) != 3:
        return []

    result = []
    for choices in product(range(3), repeat=3):
        routes = tuple(families[i][choices[i]] for i in range(3))
        if not all(is_permutation(route) for route in routes):
            continue
        if len(set(routes)) != 3:
            continue
        result.append((choices, routes))
    return result


def selector_dict(values):
    return dict(enumerate(values))


def word_at(values, indices):
    return "".join(str(values[index]) for index in indices)


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    assert len(payloads) == 6

    first_count = 0
    final = []

    for values in product(range(3), repeat=9):
        selector = selector_dict(values)
        for payload in payloads:
            first = tuple(
                decode_dash_pos3(first_pass_surface(payload, selector, q))
                for q in range(3)
            )
            if None in first:
                continue
            first_count += 1

            terminal = decode_dash_pos3(terminal_surface(payload, selector))
            if terminal is None:
                continue

            final.append(
                (
                    values,
                    compact_primary_signature(payload),
                    first,
                    terminal,
                )
            )

    assert 3**9 == 19683
    assert first_count == 288
    assert len(final) == 208

    terminal_counts = Counter(record[3] for record in final)
    assert terminal_counts == Counter(
        {
            "102": 84,
            "112": 72,
            "100": 28,
            "110": 24,
        }
    )

    winners = []
    all_indices = tuple(range(9))

    for core_indices in combinations(all_indices, 3):
        core_set = set(core_indices)
        scaffold_indices = tuple(
            index for index in all_indices if index not in core_set
        )

        groups = defaultdict(list)
        for record in final:
            values, _payload_signature, _first, terminal = record
            scaffold = word_at(values, scaffold_indices)
            groups[(scaffold, terminal)].append(record)

        for (scaffold, terminal), records in groups.items():
            families = {record[2] for record in records}
            shells = route_shells(families)
            if not shells:
                continue
            winners.append(
                (
                    core_indices,
                    scaffold_indices,
                    scaffold,
                    terminal,
                    records,
                    families,
                    shells,
                )
            )

    # Across every possible location of a three-cell variable core, only the
    # physical A/D/G centre lane supports a three-family reversible route.
    assert len(winners) == 2
    assert {
        "".join(SERIAL_ORDER[index] for index in winner[0])
        for winner in winners
    } == {"ADG"}

    # In SERIAL_ORDER with A/D/G removed, scaffold coordinates are B,C,E,F,H,I.
    expected_scaffold_indices = tuple(
        SERIAL_ORDER.index(letter) for letter in "BCEFHI"
    )
    assert all(winner[1] == expected_scaffold_indices for winner in winners)

    # The two winners are exactly the known C gauge representatives:
    # B=2, C={0,2}, E=0, F=1, H=2, I=2.
    assert {winner[2] for winner in winners} == {"200122", "220122"}
    assert {winner[3] for winner in winners} == {"100"}

    expected_families = {
        ("102", "002", "120"),
        ("102", "012", "100"),
        ("102", "022", "100"),
    }
    expected_shell = [
        ((2, 1, 0), ("120", "012", "102")),
    ]

    for (
        core_indices,
        _scaffold_indices,
        _scaffold,
        terminal,
        records,
        families,
        shells,
    ) in winners:
        assert terminal == "100"
        assert len(records) == 7
        assert families == expected_families
        assert shells == expected_shell

        core_words = {
            word_at(record[0], core_indices)
            for record in records
        }
        assert core_words == {"110", "220", "212"}

        # All six raw-compatible primary x/y payloads participate. The seventh
        # state is the familiar contention case where x=2,y=2 admits two cores.
        payload_signatures = {record[1] for record in records}
        assert payload_signatures == {
            (x, y)
            for x in (1, 2)
            for y in (0, 1, 2)
        }

        compatibility = defaultdict(set)
        for record in records:
            compatibility[word_at(record[0], core_indices)].add(record[1])
        assert compatibility == {
            "110": {(1, 2), (2, 2)},
            "220": {(1, 0), (1, 1)},
            "212": {(2, 0), (2, 1), (2, 2)},
        }

    print("Experiment 294")
    print("arbitrary ternary Q4 selectors:", 3**9)
    print("raw-compatible primary payloads:", len(payloads))
    print("first-pass POS3-closed pairs:", first_count)
    print("second-pass POS3-closed pairs:", len(final))
    print("second-pass terminal distribution:", dict(terminal_counts))
    print("possible three-position core locations:", len(tuple(combinations(range(9), 3))))
    print("route-capable scaffold/terminal groups:", len(winners))
    for winner in winners:
        core_indices, scaffold_indices, scaffold, terminal, records, families, shells = winner
        core_letters = "".join(SERIAL_ORDER[index] for index in core_indices)
        scaffold_letters = "".join(
            SERIAL_ORDER[index] for index in scaffold_indices
        )
        core_words = sorted(
            {
                word_at(record[0], core_indices)
                for record in records
            }
        )
        print(
            " ",
            f"core={core_letters}",
            f"{scaffold_letters}={scaffold}",
            f"terminal={terminal}",
            f"states={len(records)}",
            f"cores={core_words}",
            f"families={sorted(families)}",
            f"shells={shells}",
        )

    print("RESULT: only A/D/G can serve as the variable three-cell Q4 control core")
    print("RESULT: the route criterion uniquely recovers the real scaffold modulo C gauge")
    print("RESULT: cores 110/220/212 and the seven-state compatibility relation emerge")
    print("RESULT: terminal 100 and route shell 120/012/102 emerge without being targets")
    print("RESULT: no raw Q4 symbol observations or shared-polarity premise are required")


if __name__ == "__main__":
    main()
