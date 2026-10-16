#!/usr/bin/env python3
"""CL-OPS-03 leave-one-image-class-out selection audit (DISCOVER)."""
import argparse
import json
import random
from collections import Counter
from pathlib import Path

import conjecture_lab_intra_class_write_controller as exp


def holdout(master):
    classes = exp.source_classes(master)
    # Source observations for each class are converted to an exact minimum
    # number of contradictions under each of the 48 global program families.
    losses = [
        [exp.class_best(mask, dash, options, model)[0]
         for mask, dash, options in classes]
        for model in exp.MODELS
    ]
    total = 0
    details = []
    for withheld in range(9):
        # Choose the least contradictory program using ONLY the other classes.
        # On ties, choose the lexicographically first fixed program, as declared.
        candidate = min(
            (sum(row) - row[withheld], model_index)
            for model_index, row in enumerate(losses)
        )
        training, chosen_index = candidate
        mismatch = losses[chosen_index][withheld]
        total += mismatch
        details.append({
            "class": exp.CLASSES[withheld],
            "train_minimum_conflicts": training,
            "held_out_conflicts": mismatch,
            "selected_model": {
                "permutation": list(exp.MODELS[chosen_index][0]),
                "global_complement": exp.MODELS[chosen_index][1],
                "write_schedule": list(exp.MODELS[chosen_index][2]),
            }
        })
    return total, details


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--null-replicates", type=int, default=10000)
    p.add_argument("--test", action="store_true")
    p.add_argument("--output")
    args = p.parse_args()
    exp.self_test()
    original = exp.load_master()
    total, details = holdout(original)
    assert total == 5
    assert {x["class"]: x["held_out_conflicts"] for x in details} == {
        "I": 1, "A": 0, "B": 0, "C": 2, "D": 0, "E": 1,
        "F": 1, "G": 0, "H": 0
    }
    if args.test:
        print("CL-OPS-03 leave-one-class-out self-test passed")
        return
    if args.null_replicates < 1:
        p.error("--null-replicates must be positive")
    null = {}
    for scheme, seed in (("class", 20261016), ("frame", 20261017),
                         ("trio", 20261018)):
        rng = random.Random(seed)
        histogram = Counter()
        for _ in range(args.null_replicates):
            draw = exp.shuffled(original, rng, scheme)
            value, _ = holdout(draw)
            histogram[value] += 1
        null[scheme] = {
            "draws": args.null_replicates,
            "null_at_most_five": sum(v for k, v in histogram.items() if k <= 5),
            "histogram": {str(k): histogram[k] for k in sorted(histogram)},
        }
        print(scheme, null[scheme]["null_at_most_five"],
              "/", args.null_replicates)
    result = {
        "mode": "DISCOVER",
        "holdout": "Each image class's 9 body positions withheld wholesale; select best shared program from the other eight classes, then score a best local seed/selector in held-out class.",
        "model_count": 48,
        "observed_heldout_conflicts": total,
        "folds": details,
        "null": null,
        "interpretation": "Partial near-fit conditional on post-hoc choice of grammar; every complete model remains physically impossible. Not independent prospective validation.",
    }
    if args.output:
        dst = Path(args.output)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(json.dumps(result, indent=2) + "\n")
    else:
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
