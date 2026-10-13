#!/usr/bin/env python3
"""Exact four-bank x 128-site interpretation of nine-bit class words.

DISCOVER/DEVELOP only. Splitting nine bits into 2+7 is mathematically
tautological, not evidence that any original artifact used four banks.
"""
import argparse
import itertools
import json
from pathlib import Path

from audit_ce_classword_receivers import (
    CLASSES, class_word, decode_word, frame_options, read_stickers,
)


def audit(path):
    observations, known = read_stickers(path)
    frames = [frame_options(known, k) for k in range(9)]
    bodies = [''.join(parts) for parts in itertools.product(*frames)]
    interpretations = {}
    for reversed_word, one in itertools.product((False, True), ('/', '-')):
        address_vectors = [tuple(decode_word(class_word(b, c), one, reversed_word)
                                 for c in range(9)) for b in bodies]
        bank_patterns = sorted({tuple(v // 128 for v in vector)
                                for vector in address_vectors})
        low7 = {
            letter: sorted({vector[c] % 128 for vector in address_vectors})
            for c, letter in enumerate(CLASSES)
        }
        name = f'reverse{int(reversed_word)}_one{one}'
        interpretations[name] = {
            'bank_patterns': bank_patterns,
            'bank_pattern_count': len(bank_patterns),
            'bank_counts': [{str(n): list(bank).count(n) for n in range(4)}
                            for bank in bank_patterns],
            'seven_bit_offsets': low7,
            'distinct_nine_addresses_per_body': all(len(set(vec)) == 9
                                                     for vec in address_vectors),
        }
    return {'corpus_records': len(observations), 'distinct_residues': len(known),
            'conditional_bodies': len(bodies), 'interpretations': interpretations,
            'status': 'DISCOVER_DEVELOP_banked_128_is_tautological_split'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--observations', default='data/observations.csv')
    parser.add_argument('--output')
    opts = parser.parse_args()
    result = audit(opts.observations)
    assert (result['corpus_records'], result['distinct_residues'],
            result['conditional_bodies']) == (84, 66, 18)
    assert all(t['bank_pattern_count'] == 1 for t in result['interpretations'].values())
    assert result['interpretations']['reverse0_one/']['bank_patterns'] == [(
        2, 2, 0, 1, 2, 3, 2, 1, 2)]
    assert all(t['distinct_nine_addresses_per_body']
               for t in result['interpretations'].values())
    output = json.dumps(result, sort_keys=True, indent=2) + '\n'
    if opts.output:
        Path(opts.output).write_text(output, encoding='utf-8')
    else:
        print(output, end='')


if __name__ == '__main__':
    main()
