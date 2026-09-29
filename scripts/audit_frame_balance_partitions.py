#!/usr/bin/env python3
"""Experiment 271: exhaust all 3+3+3 frame-balance partitions.

Experiment 257 showed that balancing the three depth-frame weights inside each
physical quarter recovers exactly the canonical 14 exact-POS3 states from the
832-state optional-pulse recursive closure. Experiment 258 proved that six
pairwise frame-weight equalities are cardinality-minimal in the full equality
family, but did not ask whether the quarter grouping itself is special.

A partition of the nine (q,d) frames into three unlabeled triples requires
exactly six independent equalities to make each triple internally equal.
There are 280 such partitions.

This experiment exhausts all 280 and asks which partitions recover exactly the
14 no-missing-pulse states. No terminal payload or solved ternary lattice is
used to rank the partitions.
"""

from __future__ import annotations

from itertools import combinations

from audit_primary_balance_minimality import closure_survivors
from audit_primary_frame_balance import frame_weights


NATURAL_QUARTERS = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
)

NATURAL_DEPTHS = (
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
)


def partitions_into_triples():
    """Yield each unlabeled 3+3+3 partition exactly once."""
    items = tuple(range(9))
    first = items[0]
    rest = set(items[1:])

    for mates in combinations(sorted(rest), 2):
        group1 = tuple(sorted((first,) + mates))
        remaining1 = rest - set(mates)

        anchor2 = min(remaining1)
        pool2 = sorted(remaining1 - {anchor2})
        for mates2 in combinations(pool2, 2):
            group2 = tuple(sorted((anchor2,) + mates2))
            remaining2 = tuple(sorted(remaining1 - set(group2)))
            group3 = remaining2
            yield tuple(sorted((group1, group2, group3)))


def balanced(weights, partition):
    return all(len({weights[i] for i in group}) == 1 for group in partition)


def manhattan_cost(partition):
    """Geometry cost on the native 3x3 (q,d) frame lattice."""
    total = 0
    for group in partition:
        for a, b in combinations(group, 2):
            qa, da = divmod(a, 3)
            qb, db = divmod(b, 3)
            total += abs(qa - qb) + abs(da - db)
    return total





def connected_group(group):
    points = {divmod(index, 3) for index in group}
    seen = {next(iter(points))}
    changed = True
    while changed:
        changed = False
        for row, col in tuple(seen):
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                neighbor = (row + dr, col + dc)
                if neighbor in points and neighbor not in seen:
                    seen.add(neighbor)
                    changed = True
    return seen == points


def straight_group(group):
    points = [divmod(index, 3) for index in group]
    return (
        len({row for row, _col in points}) == 1
        or len({col for _row, col in points}) == 1
    )


def main() -> None:
    survivors = closure_survivors()
    assert len(survivors) == 832

    canonical = [(payload, missing) for payload, missing in survivors if missing == 0]
    assert len(canonical) == 14

    partitions = list(partitions_into_triples())
    assert len(partitions) == 280
    assert len(set(partitions)) == 280

    records = []
    for partition in partitions:
        selected = [
            (payload, missing)
            for payload, missing in survivors
            if balanced(frame_weights(payload), partition)
        ]
        exact = (
            len(selected) == 14
            and all(missing == 0 for _payload, missing in selected)
        )
        records.append(
            (partition, len(selected), exact, manhattan_cost(partition))
        )

    natural = tuple(sorted(NATURAL_QUARTERS))
    depths = tuple(sorted(NATURAL_DEPTHS))

    natural_record = next(record for record in records if record[0] == natural)
    assert natural_record[1] == 14
    assert natural_record[2] is True

    exact = [record for record in records if record[2]]
    best_count = min(record[1] for record in records)
    best = [record for record in records if record[1] == best_count]

    assert best_count == 14
    assert len(exact) == 90
    assert len(best) == 90

    min_geometry = min(record[3] for record in exact)
    simple_exact = [record for record in exact if record[3] == min_geometry]
    assert min_geometry == 12
    assert len(simple_exact) == 5

    connected_exact = [
        record
        for record in exact
        if all(connected_group(group) for group in record[0])
    ]
    assert len(connected_exact) == 5

    straight_partitions = [
        record
        for record in records
        if all(straight_group(group) for group in record[0])
    ]
    assert len(straight_partitions) == 2
    assert {record[0] for record in straight_partitions} == {natural, depths}

    straight_exact = [record for record in straight_partitions if record[2]]
    assert len(straight_exact) == 1
    assert straight_exact[0][0] == natural
    assert next(record for record in records if record[0] == depths)[1] == 50

    print("Experiment 271")
    print("3+3+3 frame partitions:", len(partitions))
    print("minimum survivor count:", best_count)
    print("partitions attaining minimum:", len(best))
    print("partitions recovering exact 14-state POS3 family:", len(exact))
    print("natural quarter partition:", natural_record)
    depth_record = next(record for record in records if record[0] == depths)
    print("depth-column partition:", depth_record)

    print("minimum geometry cost among exact partitions:", min_geometry)
    print("exact partitions at minimum geometry cost:", len(simple_exact))
    print("connected exact partitions:", len(connected_exact))
    print("straight-axis partitions:", len(straight_partitions))
    print("straight-axis exact partitions:", len(straight_exact))
    for partition, count, _is_exact, cost in simple_exact:
        print(" ", partition, "states=", count, "geometry=", cost)

    print("RESULT: abstract balance is non-unique: 90/280 partitions recover 14 states")
    print("RESULT: only five exact partitions attain minimum geometry / full connectivity")
    print("RESULT: of the two straight parallel-axis partitions, only physical quarters recover 14 states")
    print("RESULT: depth columns retain 50 states")

    print("RESULT DATA: exact partitions")
    for partition, count, _is_exact, cost in exact:
        print(" ", partition, "states=", count, "geometry=", cost)


if __name__ == "__main__":
    main()
