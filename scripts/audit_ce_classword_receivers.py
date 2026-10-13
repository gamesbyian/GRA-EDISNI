#!/usr/bin/env python3
"""Exact observed/class-word addressing census, independent of recursion.

DISCOVER/DEVELOP. No claim that the foreground is an address. Each
nine-cell primary frame conditionally has one minority glyph in
positions (1,4,7), (2,5,8), (3,6,9), with frame-local polarity.
"""
import argparse
import csv
import itertools
import json
import math
from pathlib import Path

CLASSES = 'ABCDEFGHI'
COMPLEMENT = {'/': '-', '-': '/'}


def read_stickers(path):
    rows = list(csv.DictReader(Path(path).open(encoding='utf-8', newline='')))
    by_residue = {}
    for row in rows:
        serial, residue = int(row['serial']), int(row['residue'])
        symbol = row['symbol']
        assert 1 <= residue <= 108 and residue == (serial - 1) % 108 + 1
        assert symbol in '/-.'
        assert (symbol in '/-' if residue <= 81 else symbol in '/.')
        if residue in by_residue:
            assert by_residue[residue] == symbol, (residue, symbol)
        by_residue[residue] = symbol
        claimed = row['image_class']
        if claimed:
            assert claimed == CLASSES[(residue - 1) % 9], (serial, claimed)
    return rows, by_residue


def frame_options(observed, frame_index):
    """Enumerate 2 * 3^3 patterns, requiring physical compatibility."""
    result = set()
    for minority in '/-':
        for row_choices in itertools.product(range(3), repeat=3):
            glyphs = [COMPLEMENT[minority]] * 9
            for col, row in enumerate(row_choices):
                glyphs[3 * row + col] = minority
            if all(observed.get(9 * frame_index + pos + 1, glyphs[pos]) == glyphs[pos]
                   for pos in range(9)):
                result.add(''.join(glyphs))
    return sorted(result)


def tail_options(observed, class_index):
    options = []
    for slash_row in range(3):
        glyphs = ['.'] * 3
        glyphs[slash_row] = '/'
        if all(observed.get(81 + 9 * row + class_index + 1, glyphs[row]) == glyphs[row]
               for row in range(3)):
            options.append(''.join(glyphs))
    return options


def class_word(body, class_index):
    return ''.join(body[9 * frame + class_index] for frame in range(9))


def decode_word(word, one='/', reverse=False):
    if reverse:
        word = word[::-1]
    return int(''.join('1' if glyph == one else '0' for glyph in word), 2)


def coverage_null(known_body, total=81):
    """Uniform fixed-size subset, NOT a model of sticker collection."""
    denominator = math.comb(total, known_body)
    return sum(((-1) ** (j + 1) * math.comb(9, j)
                * math.comb(total - 9 * j, known_body - 9 * j) / denominator)
               for j in range(1, min(9, known_body // 9) + 1))


def analyze(path):
    rows, known = read_stickers(path)
    frames = [frame_options(known, i) for i in range(9)]
    tails = [tail_options(known, i) for i in range(9)]
    assert all(frames) and all(tails)
    bodies = [''.join(chunks) for chunks in itertools.product(*frames)]
    raw = {}
    conditional = {}
    for i, name in enumerate(CLASSES):
        observed_word = ''.join(known.get(9 * f + i + 1, '?') for f in range(9))
        possibilities = {decode_word(''.join(bits))
                         for bits in itertools.product(
                             *[['/', '-'] if x == '?' else [x] for x in observed_word])}
        raw[name] = {'observed_word': observed_word,
                     'known': 9 - observed_word.count('?'),
                     'possible_count': len(possibilities),
                     'values': sorted(possibilities) if len(possibilities) <= 16 else None}
        values = sorted({decode_word(class_word(body, i)) for body in bodies})
        conditional[name] = {'values': values, 'possible_count': len(values)}
        assert set(values).issubset(possibilities)
    projections = {}
    for target_bits in (7, 8, 9):
        for reverse in (False, True):
            for one in ('/', '-'):
                addresses = [tuple(decode_word(class_word(b, i), one, reverse)
                                   for i in range(9)) for b in bodies]
                limit = 1 << target_bits
                fail_counts = [sum(v >= limit for v in row) for row in addresses]
                forced_fail = [CLASSES[i] for i in range(9)
                               if all(row[i] >= limit for row in addresses)]
                key = f'{target_bits}bits_reverse{int(reverse)}_one{one}'
                projections[key] = {'valid_full_vectors': fail_counts.count(0),
                                    'minimum_out_of_range': min(fail_counts),
                                    'always_out_of_range': forced_fail}
    return {
        'mode': 'DISCOVER_DEVELOP_conditional_no_receiver_claim',
        'observation_count': len(rows), 'distinct_residues': len(known),
        'body_observed': sum(r <= 81 for r in known),
        'tail_observed': sum(r > 81 for r in known),
        'frame_option_counts': list(map(len, frames)),
        'body_completions': len(bodies),
        'tail_option_counts': list(map(len, tails)),
        'tail_completions': math.prod(map(len, tails)),
        'raw_classes': raw, 'conditional_classes': conditional,
        'complete_raw_classes': [k for k, v in raw.items() if v['possible_count'] == 1],
        'complete_conditional_classes': [k for k, v in conditional.items()
                                         if v['possible_count'] == 1],
        'index_projection_tests': projections,
        'uniform_subset_null_p_at_least_one_complete_body_class': coverage_null(
            sum(r <= 81 for r in known)),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--observations', default='data/observations.csv')
    parser.add_argument('--output')
    args = parser.parse_args()
    result = analyze(args.observations)
    assert (result['observation_count'], result['distinct_residues']) == (84, 66)
    assert result['body_completions'] == 18
    assert result['tail_completions'] == 18
    assert result['complete_raw_classes'] == ['C']
    assert result['complete_conditional_classes'] == ['B', 'C', 'F', 'H']
    assert [result['conditional_classes'][x]['values'][0] for x in 'BCFH'] == [382, 58, 407, 129]
    assert all(x['valid_full_vectors'] == 0
               for k, x in result['index_projection_tests'].items()
               if not k.startswith('9bits'))
    serialized = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.output:
        Path(args.output).write_text(serialized, encoding='utf-8')
    else:
        print(serialized, end='')


if __name__ == '__main__':
    main()
