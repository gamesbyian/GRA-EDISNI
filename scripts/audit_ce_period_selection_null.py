#!/usr/bin/env python3
"""Union-bound selection control for recurring CE foreground periods, 1..216.

Exact combinatorics under a deliberately artificial zone-preserving null.
Conditional null is not an inferential probability of Playdead design.
"""
import argparse
from collections import defaultdict
import csv
import itertools
import json
from math import comb
from pathlib import Path


def read_data(path):
    rows = list(csv.DictReader(Path(path).open(encoding="utf-8", newline="")))
    data = [(int(r["serial"]), int(r["residue"]), r["symbol"]) for r in rows]
    assert all((s - 1) % 108 + 1 == residue for s, residue, _ in data)
    assert all((v in "-/" if residue <= 81 else v in "/.")
               for _, residue, v in data)
    return data


def favorable(group_sizes, wanted_body, wanted_tail):
    """Coefficient of a bivariate polynomial; exact integer arithmetic.

    For group (b,t) containing both early and tail stickers, only '/' is
    a permitted common symbol, since their other alphabets differ.
    """
    dp = {(0, 0): 1}
    for b, t in group_sizes:
        if b and t:
            choices = [(b, t)]
        elif b:
            choices = [(0, 0), (b, 0)]
        else:
            choices = [(0, 0), (0, t)]
        new = {}
        for (x, y), ways in dp.items():
            for bx, ty in choices:
                key = (x + bx, y + ty)
                if key[0] <= wanted_body and key[1] <= wanted_tail:
                    new[key] = new.get(key, 0) + ways
        dp = new
        if not dp:
            return 0
    return dp.get((wanted_body, wanted_tail), 0)


def audit(path, maximum=None, min_support=18):
    data = read_data(path)
    observable_max = max(s for s, _, _ in data) - min(s for s, _, _ in data)
    if maximum is None:
        maximum = observable_max
    body = [r for r in data if r[1] <= 81]
    tail = [r for r in data if r[1] > 81]
    slash_body = sum(s == "/" for _, _, s in body)
    slash_tail = sum(s == "/" for _, _, s in tail)
    denominator = comb(len(body), slash_body) * comb(len(tail), slash_tail)
    eligible = 0
    positive = []
    total_favorable = 0
    for period in range(1, maximum + 1):
        groups = defaultdict(list)
        for serial, residue, _ in data:
            groups[(serial - 1) % period].append(residue <= 81)
        extra = len(data) - len(groups)
        if extra < min_support:
            continue
        eligible += 1
        sizes = [(sum(g), len(g) - sum(g)) for g in groups.values()]
        count = favorable(sizes, slash_body, slash_tail)
        total_favorable += count
        if count:
            positive.append({
                "period": period, "repeat_excess": extra,
                "favorable_assignments": count,
                "fixed_period_null_probability": count / denominator,
            })
    return {
        "mode": "DISCOVER_DEVELOP_zone_preserving_label_shuffle_union_bound",
        "physical_observations": len(data),
        "body_entries": len(body), "tail_entries": len(tail),
        "body_slashes": slash_body, "tail_slashes": slash_tail,
        "period_range": [1, maximum], "maximum_observable_period": observable_max,
        "minimum_repeat_support": min_support,
        "eligible_periods": eligible, "nonzero_null_periods": len(positive),
        "denominator": denominator, "union_bound_numerator": total_favorable,
        "union_bound_upper_probability": total_favorable / denominator,
        "candidate_nulls": positive,
    }


def small_oracle():
    """Check bivariate count against brute force on synthetic tiny groups."""
    groups = [(2, 0), (1, 1), (0, 2), (1, 0)]
    for b_slash in range(5):
        for t_slash in range(4):
            expected = 0
            # Explicit groupwise choice oracle, independent of DP recurrence.
            allowed = [[(0, 0), (2, 0)], [(1, 1)],
                       [(0, 0), (0, 2)], [(0, 0), (1, 0)]]
            for combo in itertools.product(*allowed):
                expected += int((sum(x for x, _ in combo),
                                 sum(y for _, y in combo)) == (b_slash, t_slash))
            assert favorable(groups, b_slash, t_slash) == expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--observations", default="data/observations.csv")
    parser.add_argument("--max-period", type=int, default=None)
    parser.add_argument("--min-support", type=int, default=18)
    parser.add_argument("--output")
    args = parser.parse_args()
    small_oracle()
    result = audit(args.observations, args.max_period, args.min_support)
    if (args.max_period is None and args.min_support == 18):
        assert result["maximum_observable_period"] == 595
        assert result["period_range"] == [1, 595]
        assert (result["eligible_periods"], result["nonzero_null_periods"]) == (137, 27)
        assert result["denominator"] == 37399079244620030691600
        assert result["union_bound_numerator"] == 377822188953098255
        assert next(v for v in result["candidate_nulls"] if v["period"] == 108
                    )["favorable_assignments"] == 217839326948876160
    output = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
