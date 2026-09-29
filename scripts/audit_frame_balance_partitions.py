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

    print("Experiment 271")
    print("3+3+3 frame partitions:", len(partitions))
    print("minimum survivor count:", best_count)
    print("partitions attaining minimum:", len(best))
    print("partitions recovering exact 14-state POS3 family:", len(exact))
    print("natural quarter partition:", natural_record)
    depth_record = next(record for record in records if record[0] == depths)
    print("depth-column partition:", depth_record)

    if exact:
        min_geometry = min(record[3] for record in exact)
        simple_exact = [record for record in exact if record[3] == min_geometry]
        print("minimum geometry cost among exact partitions:", min_geometry)
        print("exact partitions at minimum geometry cost:", len(simple_exact))
        for partition, count, _is_exact, cost in simple_exact:
            print(" ", partition, "states=", count, "geometry=", cost)

    print("RESULT DATA: exact partitions")
    for partition, count, _is_exact, cost in exact:
        print(" ", partition, "states=", count, "geometry=", cost)


if __name__ == "__main__":
    main()
