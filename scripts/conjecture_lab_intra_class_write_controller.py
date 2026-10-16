#!/usr/bin/env python3
"""CL-OPS-03: fixed 3-bit per-class controller / one-site write audit.

DISCOVER, not a decoded CE stream. Raw observations only. Tail is interpreted
conditionally as one slash in each class's three tail positions; no missing
symbols are filled in the evidence ledger. Computes the *minimum observed
contradictions*, not probabilities of a model being the intended solution.
"""
import argparse
import csv
import itertools
import json
import random
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASSES = "IABCDEFGH"  # modulo-9 columns in zero-anchored community master
PERMS = tuple(itertools.permutations(range(3)))
SCHEDULES = ((0, 0), (1, 0), (0, 1), (1, 1))
MODELS = tuple(itertools.product(PERMS, (0, 1), SCHEDULES))


def load_master():
    obj = json.loads((ROOT / "data/discord-community-master-108.json").read_text())
    cells = list("".join(obj["rows_12x9"]))
    assert len(cells) == 108
    observations = list(csv.DictReader((ROOT / "data/observations.csv").open(newline="")))
    for row in observations:
        idx = int(row["residue"]) % 108
        assert cells[idx] in (" ", row["symbol"])
        cells[idx] = row["symbol"]
    master = "".join(cells)
    assert len(observations) == 84
    assert (master.count("/"), master.count("-"), master.count("."), master.count(" ")) == (36, 22, 8, 42)
    assert master[103] == "." and master[45] == " "
    assert all(c in "/- " for c in master[:81])
    assert all(c in "/. " for c in master[81:])
    return master


def source_classes(master):
    result = []
    for cls in range(9):
        known = dash = 0
        for k in range(9):
            symbol = master[cls + 9 * k]
            if symbol != " ":
                known |= 1 << k
                if symbol == "-":
                    dash |= 1 << k
        options = tuple(
            depth for depth in range(3)
            if all(
                master[cls + 9 * (9 + d)] in (" ", "/" if d == depth else ".")
                for d in range(3)
            )
        )
        assert options, (cls, master)
        result.append((known, dash, options))
    return result


def step(bits, perm, complement, selected, mutate):
    out = [bits[perm[i]] ^ complement for i in range(3)]
    if mutate:
        out[selected] ^= 1
    return out


@lru_cache(None)
def emitted(model, selector):
    perm, complement, mutations = model
    result = []
    for seed in itertools.product((0, 1), repeat=3):
        states = [list(seed)]
        for t in range(2):
            states.append(step(states[-1], perm, complement, selector, mutations[t]))
        flat = states[0] + states[1] + states[2]
        result.append(sum(bit << k for k, bit in enumerate(flat)))
    return tuple(result)


def error(mask, dash, predicted):
    return (mask & (dash ^ predicted)).bit_count()


def class_best(known, dash, options, model):
    return min(
        (error(known, dash, word), selector, word)
        for selector in options for word in emitted(model, selector)
    )


def score(classes, model):
    return sum(class_best(mask, dash, options, model)[0]
               for mask, dash, options in classes)


def best_fit(master):
    classes = source_classes(master)
    return min((score(classes, model), model) for model in MODELS)


def physical_errors(master, model):
    details = []
    for cls, (mask, dash, opts) in enumerate(source_classes(master)):
        cost, selector, witness = class_best(mask, dash, opts, model)
        bad = [cls + 9 * k for k in range(9)
               if (mask & (dash ^ witness) & (1 << k))]
        details.append({
            "class": CLASSES[cls],
            "source_index_mod_9": cls,
            "tail_selector_options": list(opts),
            "fitted_tail_selector": selector,
            "contradictions": cost,
            "contradictory_residues": bad,
            "observed_triples": [
                "".join(master[cls + 9 * (3 * q + d)] for d in range(3))
                for q in range(3)
            ],
        })
    return details


def shuffled(master, rng, scheme):
    arr = list(master)
    if scheme == "class":
        groups = [[j + 9 * k for k in range(9)] for j in range(9)]
    elif scheme == "frame":
        groups = [list(range(9 * k, 9 * (k + 1))) for k in range(9)]
    elif scheme == "trio":
        groups = [[j + 9 * (3 * q + d) for d in range(3)]
                  for j in range(9) for q in range(3)]
    else:
        raise ValueError(scheme)
    for group in groups:
        positions = [i for i in group if arr[i] != " "]
        values = [arr[i] for i in positions]
        rng.shuffle(values)
        for position, value in zip(positions, values):
            arr[position] = value
    return "".join(arr)


def controls(master, replicates, seed=20261014):
    observed, _ = best_fit(master)
    out = {}
    for scheme, shift in (("class", 1), ("frame", 2), ("trio", 3)):
        rng = random.Random(seed + shift)
        histogram = Counter()
        for _ in range(replicates):
            randomized = shuffled(master, rng, scheme)
            value, _ = best_fit(randomized)
            histogram[value] += 1
        out[scheme] = {
            "draws": replicates,
            "observed_min_conflicts": observed,
            "controls_at_most_as_many_conflicts": sum(
                count for value, count in histogram.items() if value <= observed
            ),
            "frequency": {str(k): histogram[k] for k in sorted(histogram)},
        }
    return out


def self_test():
    assert len(MODELS) == 48
    original = load_master()
    assert len(source_classes(original)) == 9
    ways = 1
    for _, _, options in source_classes(original):
        ways *= len(options)
    assert ways == 18
    # Independent nine-bit brute force equivalence for all 48 programs
    # and all three selector commands.
    for model in MODELS:
        for selector in range(3):
            candidates = emitted(model, selector)
            assert len(candidates) == 8 and len(set(candidates)) == 8
            for seed in itertools.product((0, 1), repeat=3):
                states = [list(seed)]
                for mutate in model[2]:
                    states.append(step(states[-1], model[0], model[1],
                                       selector, mutate))
                witness = sum(
                    bit << index
                    for index, bit in enumerate(sum(states, []))
                )
                assert witness in candidates
    # Source-independent impossibility: class C has complete --- / /// / -/-;
    # a permutation plus global complement cannot break row uniformity.
    cls_c = 3
    assert physical_errors(original, best_fit(original)[1])[cls_c]["observed_triples"] == ["---", "///", "-/-"]
    best, model = best_fit(original)
    assert best == 4
    assert model == ((2, 0, 1), 0, (1, 1))
    bad = sorted(r for d in physical_errors(original, model)
                 for r in d["contradictory_residues"])
    assert bad == [12, 39, 51, 72]
    for scheme in ("class", "frame", "trio"):
        rng = random.Random(1337)
        draw = shuffled(original, rng, scheme)
        assert len(draw) == len(original)
        assert sorted(draw) == sorted(original)
        assert [c == " " for c in draw] == [c == " " for c in original]
        assert draw[81:] == original[81:]
    print("CL-OPS-03 self-test passed: exact one-hot census, model optimum, and physical witnesses")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--null-replicates", type=int, default=10000)
    parser.add_argument("--output")
    args = parser.parse_args()
    self_test()
    if args.test:
        return
    if args.null_replicates < 1:
        parser.error("--null-replicates must be >= 1")
    master = load_master()
    optimum, model = best_fit(master)
    result = {
        "mode": "DISCOVER", "script": "scripts/conjecture_lab_intra_class_write_controller.py",
        "physical_records": 84, "unique_residues": 66, "body_observed": 54,
        "tail_observed": 12, "conditional_one_slash_tail_vectors": 18,
        "model_count": len(MODELS),
        "model": "Each class has three 3-bit rows. Select one tail depth; apply the SAME globally selected coordinate permutation, optional global complement, and selected-bit XOR on transition 1 and/or transition 2. Initial 3 bits free separately for each class.",
        "optimum_conflicts": optimum,
        "best_model": {"permutation": list(model[0]), "global_complement": model[1],
                       "write_schedule": list(model[2])},
        "physical_violations": physical_errors(master, model),
        "randomization": "Labels at observed early-zone positions only, preserving the exact unknown-position mask and known symbol counts inside the named groups; tail held constant; 48-model selection rerun each time",
        "controls": controls(master, args.null_replicates),
        "interpretation": "Every one of the 48 fixed global programs is contradicted by existing physical observations. The minimum of 4 is exploratory closeness, not a valid parse or prospective prediction.",
    }
    print(f"CL-OPS-03: best program contradicts {optimum} physical body symbols")
    for scheme, stat in result["controls"].items():
        print(f"{scheme}: {stat['controls_at_most_as_many_conflicts']}/{stat['draws']} matched controls are as close or closer")
    if args.output:
        dest = Path(args.output)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(result, indent=2) + "\n")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
