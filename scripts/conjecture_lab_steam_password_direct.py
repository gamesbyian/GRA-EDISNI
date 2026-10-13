#!/usr/bin/env python3
"""Exploratory direct sticker-to-passphrase compatibility audit.

No password is tested with Steam or any third-party service.
This script uses ONLY observed residues; all others remain unknown.
Raw serial order is one invented bridge, not a verified CE readout.
Run: python scripts/conjecture_lab_steam_password_direct.py
"""
import csv
import itertools
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SYM = "./-"  # bijections of digit 0,1,2 to physical symbol; all six tested
TARGETS = ("NEWPLANETDISCOVERED", "LIFEDETECTED", "534BRN9653F9J8MMD")
FAMILIES = tuple(
    (width, encoding)
    for width in (3, 4, 5, 6)
    for encoding in ("A0", "A1", "ASCII", "ALNUM0")
    if not (encoding == "ASCII" and width < 5)
    and not (encoding == "ALNUM0" and width < 4)
)


def observations():
    with (REPO / "data" / "observations.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 84, "Review census change; rerun with revised documentation"
    mapping = {}
    for row in rows:
        residue = int(row["residue"])
        symbol = row["symbol"]
        assert 1 <= residue <= 108 and symbol in SYM
        assert residue not in mapping or mapping[residue] == symbol
        mapping[residue] = symbol
    assert len(mapping) == 66, "Review unique-residue count"
    return mapping


def number(character, encoding):
    if encoding in ("A0", "A1"):
        if not ("A" <= character <= "Z"):
            return None
        return ord(character) - ord("A") + (encoding == "A1")
    if encoding == "ASCII":
        return ord(character)
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return alphabet.index(character) if character in alphabet else None


def trits(value, width):
    if value is None or not (0 <= value < 3 ** width):
        return None
    return tuple((value // 3 ** power) % 3 for power in range(width - 1, -1, -1))


def render(target, width, encoding, digit_symbols):
    result = []
    for ch in target:
        symbols = trits(number(ch, encoding), width)
        if symbols is None:
            return None
        result.extend(digit_symbols[digit] for digit in symbols)
    return result


def compare(pattern, observed, start, forward):
    mismatches = 0
    checked = 0
    for index, expected in enumerate(pattern):
        residue = (start + index + 1) if forward else (108 - start - index)
        actual = observed.get(residue)
        if actual is not None:
            checked += 1
            mismatches += actual != expected
    return mismatches, checked


def audit(observed, target):
    rows = []
    for width, encoding in FAMILIES:
        if width * len(target) > 108:
            continue
        trials = []
        for digit_symbols in itertools.permutations(SYM):
            pattern = render(target, width, encoding, digit_symbols)
            if pattern is None:
                continue
            for forward in (True, False):
                for start in range(109 - len(pattern)):
                    mismatches, checked = compare(pattern, observed, start, forward)
                    trials.append((mismatches, -checked, forward, "".join(digit_symbols), start))
        if not trials:
            continue
        trials.sort()
        best = trials[0]
        rows.append({
            "encoding": f"{width}:{encoding}",
            "tested": len(trials),
            "exact": sum(row[0] == 0 for row in trials),
            "best_conflicts": best[0],
            "best_known_positions": -best[1],
            "best_read_order": "forward" if best[2] else "reverse",
            "best_0_based_start": best[4],
            "best_digit_symbol_order": best[3],
        })
    return rows


def positive_control():
    """Synthetic encoded target has zero conflicts despite unknown positions."""
    word = "LIFEDETECTED"
    word_symbols = render(word, 5, "A0", (".", "/", "-"))
    observed = {i + 1: word_symbols[i] for i in range(0, len(word_symbols), 2)}
    conflicts, checked = compare(word_symbols, observed, 0, True)
    assert (conflicts, checked) == (0, 30)
    changed = dict(observed)
    changed[1] = next(sym for sym in SYM if sym != changed[1])
    assert compare(word_symbols, changed, 0, True)[0] == 1


def main():
    positive_control()
    observed = observations()
    print(f"Current observed corpus: {len(observed)}/108 unique residues (84 physical observations)")
    print("All unknown cells remain unconstrained. Encoding choices and targets are exploratory.")
    for target in TARGETS:
        rows = audit(observed, target)
        print(f"\nTARGET {target}:")
        for row in rows:
            print(f"  {row['encoding']:9s} trials={row['tested']:3d} exact={row['exact']:2d}"
                  f" best_conflicts={row['best_conflicts']:2d}/{row['best_known_positions']:2d}"
                  f" order={row['best_read_order']:7s}"
                  f" start={row['best_0_based_start']:2d}"
                  f" trit_map={row['best_digit_symbol_order']}")
    print("\nThese results test ONLY contiguous, fixed-width, ordinary base-3 mappings")
    print("of literal historical strings. No contradiction generalizes to other readouts.")


if __name__ == "__main__":
    main()
