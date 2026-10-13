#!/usr/bin/env python3
"""Observation-only Playdead design-grammar pilots; DISCOVER, not a CE decoder.

Uses exactly data/observations.csv. No filled-in H108 master, POS3 or U5
predictions. Outputs a fixed-geometry temporal negative and exact 27->81
controller truth-table baselines. Python standard library only.
"""
import argparse
import csv
import itertools
import json
from pathlib import Path


def physical(path):
    with open(path, newline="", encoding="utf-8") as handle:
        records = list(csv.DictReader(handle))
    observed = ["?"] * 108
    seen = {}
    for r in records:
        index = int(r["residue"]) - 1
        symbol = r["symbol"]
        assert 0 <= index < 108 and symbol in ("/", "-", ".")
        assert int(r["serial"]) % 108 == index + 1 or (index == 107 and int(r["serial"]) % 108 == 0)
        assert index not in seen or seen[index] == symbol
        seen[index] = symbol
        observed[index] = symbol
    assert len(records) == 84 and len(seen) == 66
    assert all(s in ("/", "-", "?") for s in observed[:81])
    assert all(s in ("/", ".", "?") for s in observed[81:])
    return observed, records


def maps_d4():
    maps = []
    for t in range(8):
        m = []
        for idx in range(9):
            x, y = idx % 3, idx // 3
            if t >= 4:
                x = 2 - x
            for _ in range(t % 4):
                x, y = 2 - y, x
            m.append(y * 3 + x)
        maps.append(m)
    assert len({tuple(x) for x in maps}) == 8
    return maps


def temporal_scores(frames):
    scores = []
    for t, remap in enumerate(maps_d4()):
        for invert in (0, 1):
            match = mismatch = compared = 0
            for left, right in zip(frames[:8], frames[1:9]):
                for j in range(9):
                    a, b = left[j], right[remap[j]]
                    if "?" in (a, b):
                        continue
                    compared += 1
                    if (a == b) != bool(invert):
                        match += 1
                    else:
                        mismatch += 1
            scores.append(dict(transform=t, invert=invert, match=match,
                               mismatch=mismatch, comparable=compared))
    return sorted(scores, key=lambda x: (-x["match"], x["mismatch"]))


class LCG:
    def __init__(self, seed=0x7A5B8321):
        self.seed = seed

    def rand(self):
        self.seed = (self.seed * 1664525 + 1013904223) & 0xFFFFFFFF
        return self.seed / 4294967296

    def shuff(self, arr):
        # Fisher-Yates matching the frozen JS pilot seed and draw order.
        for j in range(len(arr) - 1, 0, -1):
            k = int(self.rand() * (j + 1))
            arr[j], arr[k] = arr[k], arr[j]


def temporal_test(observed, n=5000):
    frames = [observed[i * 9:(i + 1) * 9] for i in range(12)]
    # The null draw order includes all 12 physical frames even though the
    # D4 temporal comparison uses only the nine slash/dash body frames.
    actual = temporal_scores(frames)
    best, identity = actual[0], next(
        x for x in actual if x["transform"] == 0 and x["invert"] == 0)
    rand = LCG()
    null_best = []
    null_identity = []
    for _ in range(n):
        shuffled = []
        for f in frames:
            payload = [s for s in f if s != "?"]
            rand.shuff(payload)
            k = iter(payload)
            shuffled.append([next(k) if s != "?" else "?" for s in f])
        ss = temporal_scores(shuffled)
        null_best.append(ss[0]["match"])
        null_identity.append(next(
            x["match"] for x in ss
            if x["transform"] == 0 and x["invert"] == 0))
    result = {
        "kind": "observation_only_temporal_d4",
        "body_frames": 9,
        "transitions": 8,
        "transform_family": "8 D4 symmetries * 2 optional global bit complements",
        "best": best,
        "identity": identity,
        "null": {
            "n": n,
            "seed": "0x7A5B8321",
            "preserved": "observed mask and slash/dash count in each frame",
            "best_ge_observed": sum(x >= best["match"] for x in null_best),
            "best_mean_matches": sum(null_best) / n,
            "identity_ge_observed": sum(
                x >= identity["match"] for x in null_identity),
            "identity_mean_matches": sum(null_identity) / n,
        },
    }
    return result


def triple_indices(layout, k):
    if layout == "consecutive":
        return (3 * k, 3 * k + 1, 3 * k + 2)
    if layout == "planes27":
        return (k, k + 27, k + 54)
    assert layout == "within27"
    q, j = divmod(k, 9)
    return (27 * q + j, 27 * q + 9 + j, 27 * q + 18 + j)


def functions():
    return [
        ("XOR", lambda z: z[0] ^ z[1] ^ z[2]),
        ("MAJ", lambda z: int(sum(z) >= 2)),
        ("OR", lambda z: int(any(z))),
        ("AND", lambda z: int(all(z))),
        ("EXACT1", lambda z: int(sum(z) == 1)),
        ("ALL_SAME", lambda z: int(z[0] == z[1] == z[2])),
        ("FIRST", lambda z: z[0]),
        ("MIDDLE", lambda z: z[1]),
        ("LAST", lambda z: z[2]),
    ]


LAYOUTS = ("consecutive", "planes27", "within27")


def control_counts(body, tail):
    counts = []
    for layout in LAYOUTS:
        cases = []
        for k in range(27):
            values = [body[j] for j in triple_indices(layout, k)]
            if tail[k] == "?" or "?" in values:
                continue
            cases.append(([int(v == "/") for v in values],
                          int(tail[k] == "/"), k + 1))
        match = {}
        for name, func in functions():
            match[name] = sum(func(a) == b for a, b, _ in cases)
        counts.append({
            "layout": layout,
            "complete_cases": len(cases),
            "case_indices": [k for _, _, k in cases],
            "match": match,
            "best": max(match.values()),
        })
    return counts


def controller_test(observed):
    body, tail = observed[:81], observed[81:]
    known = [i for i, v in enumerate(tail) if v != "?"]
    slashes = sum(tail[i] == "/" for i in known)
    actual = control_counts(body, tail)
    nulls = []
    for slash_slots in itertools.combinations(known, slashes):
        permuted = ["?"] * 27
        for i in known:
            permuted[i] = "."
        for i in slash_slots:
            permuted[i] = "/"
        nulls.append(control_counts(body, permuted))
    best_actual = max(r["best"] for r in actual)
    return {
        "kind": "fixed_81_body_vs_27_tail_boolean_controller",
        "slash_code": "1=/; 0=- for body, 0=. for tail",
        "families": actual,
        "tail_known": len(known),
        "tail_slashes": slashes,
        "null": {
            "type": "exact tail-label permutations preserving observed positions and slash count",
            "n": len(nulls),
            "best_across_27_models_ge_observed": sum(
                max(t["best"] for t in n) >= best_actual for n in nulls),
            "planes27_best_ge_observed": sum(
                n[1]["best"] >= actual[1]["best"] for n in nulls),
            "best_xor_ge_observed": sum(
                max(t["match"]["XOR"] for t in n) >=
                max(t["match"]["XOR"] for t in actual)
                for n in nulls),
            "perfect_fit_in_any": sum(
                any(t["best"] == t["complete_cases"] for t in n)
                for n in nulls),
        },
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations", default="data/observations.csv")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    observed, records = physical(Path(args.observations))
    temporal = temporal_test(observed)
    controller = controller_test(observed)
    assert temporal["best"]["match"] == 19
    assert temporal["best"]["comparable"] == 33
    assert temporal["null"]["best_ge_observed"] == 4818
    assert temporal["null"]["identity_ge_observed"] == 4483
    assert [(x["complete_cases"], x["best"], x["match"]["XOR"])
            for x in controller["families"]] == [(3, 2, 1), (5, 4, 2), (4, 3, 1)]
    assert controller["null"]["n"] == 495
    assert controller["null"]["best_across_27_models_ge_observed"] == 351
    assert controller["null"]["planes27_best_ge_observed"] == 271
    assert controller["null"]["perfect_fit_in_any"] == 326
    output = {
        "status": "DISCOVER negative pilots, not foreground decoder",
        "source": str(args.observations),
        "records": len(records),
        "unique_residues": sum(v != "?" for v in observed),
        "temporal": temporal,
        "controller": controller,
    }
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print("Physical corpus:", output["records"], "records,",
              output["unique_residues"], "unique H108 positions")
        print("D4/global invert best:", temporal["best"],
              "| matched null >= observed:",
              temporal["null"]["best_ge_observed"], "/ 5000")
        for row in controller["families"]:
            print(row["layout"], "complete", row["complete_cases"],
                  "best", row["best"], "XOR", row["match"]["XOR"])
        print("Controller exact matched null >= global best:",
              controller["null"]["best_across_27_models_ge_observed"], "/ 495")


if __name__ == "__main__":
    main()
