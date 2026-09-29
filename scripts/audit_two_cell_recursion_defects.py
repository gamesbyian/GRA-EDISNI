#!/usr/bin/env python3
"""Experiment 307: exhaust up-to-two-cell first-pass recursion defects.

Experiment 306 found:
  * no single first-pass depth defect preserves the exact canonical transducer;
  * one A+1 defect retains 16 states and terminal 100 but destroys the clean
    three-class reversible route layer.

This experiment asks whether two local first-pass exceptions can rescue a
credible sibling.

Parent operation:
    canonical first pass (q, S(j), j)

Defect grammar:
    at zero, one, or two distinct physical A-I cells, replace depth S(j) with
    S(j)+delta mod 3 for delta in {1,2}.

Configuration count:
    1 canonical
    + 9*2 single-cell
    + C(9,2)*2^2 two-cell
    = 163.

The second pass remains canonical.

Filters:
    first-pass three surfaces and second-pass terminal must decode as POS3.

Model-selection check:
    derive the set of distinct first-pass functional families for each
    surviving configuration. A route-capable configuration must have exactly
    three functional families and admit one q-indexed ternary permutation from
    each such that all three selected route words are distinct.

No expected state count, terminal, route words, or canonical master set is used
as a filter.
"""

from __future__ import annotations

from collections import Counter
from itertools import combinations, product

from enumerate_raw_machine import (
    PHYSICAL_LAYOUT,
    SERIAL_ORDER,
    decode_dash_pos3,
    enumerate_primary_payloads,
    enumerate_selectors,
    frame_symbol,
    generate_master,
    load_rows,
    primary_column_candidates,
    q4_selector_candidates,
    selector_at_physical_cell,
    terminal_surface,
)


def first_surface(payload, selector, external_q, offsets):
    return tuple(
        tuple(
            frame_symbol(
                payload,
                external_q,
                (
                    selector_at_physical_cell(selector, row, col)
                    + offsets.get(SERIAL_ORDER.index(PHYSICAL_LAYOUT[row][col]), 0)
                ) % 3,
                row,
                col,
            )
            for col in range(3)
        )
        for row in range(3)
    )


def evaluate(raw, offsets):
    final = []
    for payload, selector in raw:
        first = tuple(
            decode_dash_pos3(first_surface(payload, selector, q, offsets))
            for q in range(3)
        )
        if None in first:
            continue
        terminal = decode_dash_pos3(terminal_surface(payload, selector))
        if terminal is None:
            continue
        final.append((payload, selector, first, terminal))
    return final


def machine_key(item):
    payload, selector = item[:2]
    return (
        tuple(sorted(payload.items())),
        tuple(sorted(selector.items())),
    )


def is_permutation(word):
    return len(word) == 3 and set(word) == {"0", "1", "2"}


def route_shells(families):
    families = tuple(sorted(families))
    if len(families) != 3:
        return []

    result = []
    for choices in product(range(3), repeat=3):
        routes = tuple(
            families[index][choices[index]]
            for index in range(3)
        )
        if not all(is_permutation(word) for word in routes):
            continue
        if len(set(routes)) != 3:
            continue
        result.append((choices, routes))
    return result


def label(offsets):
    if not offsets:
        return "canonical"
    return "+".join(
        f"{SERIAL_ORDER[j]}{delta}"
        for j, delta in sorted(offsets.items())
    )


def configurations():
    yield {}
    for j in range(9):
        for delta in (1, 2):
            yield {j: delta}
    for j1, j2 in combinations(range(9), 2):
        for d1, d2 in product((1, 2), repeat=2):
            yield {j1: d1, j2: d2}


def main() -> None:
    rows = load_rows()
    payloads = list(enumerate_primary_payloads(primary_column_candidates(rows)))
    selectors = list(enumerate_selectors(q4_selector_candidates(rows)))
    raw = [(payload, selector) for payload in payloads for selector in selectors]
    assert len(raw) == 216

    configs = list(configurations())
    assert len(configs) == 163

    results = []
    for offsets in configs:
        final = evaluate(raw, offsets)
        families = {item[2] for item in final}
        terminals = Counter(item[3] for item in final)
        results.append({
            "offsets": offsets,
            "label": label(offsets),
            "final": final,
            "states": len(final),
            "terminals": terminals,
            "families": families,
            "shells": route_shells(families),
        })

    distribution = Counter(
        (result["states"], len(result["terminals"]))
        for result in results
    )
    assert distribution == Counter({
        (0, 0): 128,
        (2, 1): 2,
        (3, 1): 2,
        (4, 1): 5,
        (5, 1): 4,
        (6, 1): 3,
        (7, 1): 2,
        (8, 1): 3,
        (10, 1): 2,
        (12, 1): 3,
        (14, 1): 4,
        (16, 1): 2,
        (18, 1): 1,
        (20, 1): 2,
    })

    canonical = next(result for result in results if not result["offsets"])
    assert canonical["states"] == 14
    assert canonical["terminals"] == Counter({"100": 14})
    assert canonical["shells"] == [
        ((2, 1, 0), ("120", "012", "102")),
    ]
    canonical_keys = {machine_key(item) for item in canonical["final"]}
    canonical_masters = {
        generate_master(item[0], item[1])
        for item in canonical["final"]
    }
    assert len(canonical_masters) == 14

    # Three two-cell siblings preserve the exact 14 physical machines and
    # terminal 100 while changing the intermediate first-pass families.
    exact_siblings = []
    for result in results:
        if not result["offsets"]:
            continue
        keys = {machine_key(item) for item in result["final"]}
        if keys == canonical_keys and result["terminals"] == Counter({"100": 14}):
            exact_siblings.append(result)

    assert {result["label"] for result in exact_siblings} == {
        "B1+H1",
        "B2+H2",
        "F2+I1",
    }
    assert all(not result["shells"] for result in exact_siblings)

    expected_sibling_families = {
        "B1+H1": {
            ("102", "002", "122"),
            ("102", "012", "102"),
            ("102", "022", "102"),
        },
        "B2+H2": {
            ("100", "002", "122"),
            ("100", "012", "102"),
            ("100", "022", "102"),
        },
        "F2+I1": {
            ("102", "202", "120"),
            ("102", "212", "100"),
            ("102", "222", "100"),
        },
    }
    for result in exact_siblings:
        assert result["families"] == expected_sibling_families[result["label"]]

    # Only canonical plus the two single-C defects support a full three-route
    # reversible shell anywhere in the entire 163-configuration family.
    route_capable = [result for result in results if result["shells"]]
    assert {result["label"] for result in route_capable} == {
        "canonical",
        "C1",
        "C2",
    }
    assert {
        result["label"]: result["states"]
        for result in route_capable
    } == {
        "canonical": 14,
        "C1": 7,
        "C2": 7,
    }
    assert all(
        result["shells"] == [((2, 1, 0), ("120", "012", "102"))]
        for result in route_capable
    )

    # Thus canonical uniquely maximizes raw-state retention among every
    # route-capable zero/one/two-cell operation in the tested family.
    assert canonical["states"] == max(
        result["states"]
        for result in route_capable
    )

    # Several local-defect siblings retain more than 14 states, but none are
    # route-capable. The strongest retain 20 and remain terminal 100.
    maximum = max(result["states"] for result in results)
    assert maximum == 20
    max_siblings = [
        result for result in results
        if result["states"] == maximum
    ]
    assert {result["label"] for result in max_siblings} == {
        "A1+D1",
        "A1+D2",
    }
    assert all(result["terminals"] == Counter({"100": 20}) for result in max_siblings)
    assert all(not result["shells"] for result in max_siblings)

    print("Experiment 307")
    print("zero/one/two-cell first-pass configurations:", len(results))
    print("outcome distribution (states, terminal cardinality):")
    for key in sorted(distribution):
        print(" ", key, "->", distribution[key])
    print("exact 14-master siblings:", sorted(result["label"] for result in exact_siblings))
    print("route-capable configurations:")
    for result in route_capable:
        print(
            " ",
            result["label"],
            "states=",
            result["states"],
            "shell=",
            result["shells"][0],
        )
    print("maximum-retention configurations:", sorted(result["label"] for result in max_siblings))
    print("maximum retained states:", maximum)
    print("RESULT: three two-cell defects preserve the exact 14 masters but all destroy the route shell")
    print("RESULT: canonical uniquely maximizes retention among route-capable configurations")
    print("RESULT: the 20-state local siblings preserve terminal 100 only by losing reversible routing")
    print("RESULT: the route layer remains the discriminator as local exception freedom grows")


if __name__ == "__main__":
    main()
