#!/usr/bin/env python3
"""DISCOVER/DEVELOP: 128-character CE sticker output and JPEG-row consumer audit.

All tests are offline; no Steam codes or guessed credentials are submitted.
Uses canonically preserved physical sticker observations and historical source
fixtures. Missing sticker marks are never presented as discoveries.

Run: python scripts/conjecture_lab_128_output_consumer.py
"""
import csv
import hashlib
import itertools
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
H108 = 108
OUTPUT = 128
NATIVE = "IABCDEFGH"
ABC = "ABCDEFGHI"


def load_sources():
    with (ROOT / "data/observations.csv").open(newline="") as stream:
        lines = list(csv.DictReader(stream))
    known = {}
    for record in lines:
        index, symbol = int(record["residue"]), record["symbol"]
        assert 1 <= index <= 108 and symbol in "./-"
        assert index not in known or known[index] == symbol
        known[index] = symbol
        # Apparent primary and tail alphabets are OBSERVED, not filled in.
        if index <= 81:
            assert symbol in "/-"
        else:
            assert symbol in "/."
    assert len(lines) == 84 and len(known) == 66
    footer = json.loads(
        (ROOT / "data/experiment-413-414-534brn-footer-128.json").read_text()
    )
    mcu = json.loads(
        (ROOT / "data/experiment-416-128-mcu-uniqueness.json").read_text()
    )
    assert footer["footer"]["decoded_message"] == "128 UNSOLVED"
    assert footer["footer"]["raw_dot_run_lengths"] == [8, 2, 1]
    assert footer["jpeg_header"]["dimension_range"] == [128, 255]
    assert mcu["sof_sampling"]["mcu_pixel_size"] == [16, 16]
    assert mcu["dimension_domain"] == {"width": [128, 255], "height": [128, 255]}
    return known


def periodic_window(known, start=0, length=OUTPUT):
    """Source-order cyclical transcription with no new decoder assumption."""
    return tuple(
        (index, known.get(index))
        for index in (((start + i) % H108) + 1 for i in range(length))
    )


def q4_depths(known):
    """Conditional: exactly one slash per three-depth A-I tail column."""
    classes = {}
    for j, klass in enumerate(ABC):
        cells = tuple(82 + j + 9 * k for k in range(3))
        options = tuple(
            depth for depth in range(3)
            if all(
                pos not in known
                or ((known[pos] == "/") == (k == depth))
                for k, pos in enumerate(cells)
            )
        )
        assert options, (klass, cells)
        classes[klass] = options
    assert tuple(classes.values()) == (
        (0, 1, 2), (2,), (0, 1, 2),
        (1,), (0,), (1,), (0, 2), (2,), (2,)
    )
    return classes


def index_candidates(classes, order=NATIVE):
    """Nine Q4 trits -> integer. %128 is an INVENTED row-address rule."""
    addresses = {}
    for depths in itertools.product(*(classes[c] for c in order)):
        index = 0
        for digit in depths:
            index = 3 * index + digit
        addresses["".join(map(str, depths))] = index
    assert len(addresses) == 18
    return addresses


def synthetic_hash_lengths(known):
    """Demonstrate information-expanding presentation without creating a guess.

    108 known-or-filled bit positions -> SHA-512 digest displayed as 128
    lowercase hex characters. Filling missing positions with 0/1 is a test
    vector ONLY, not an inferred sticker completion or Steam candidate.
    """
    outputs = []
    for default in (0, 1):
        binary = "".join(
            str(int(known[residue] == "/") if residue in known else default)
            for residue in range(1, H108 + 1)
        )
        assert len(binary) == H108
        output = hashlib.sha512(binary.encode("ascii")).hexdigest()
        assert len(output) == OUTPUT
        assert all(c in "0123456789abcdef" for c in output)
        outputs.append(output)
    assert outputs[0] != outputs[1]
    return {"input_length_bits": H108,
            "displayed_hex_characters": OUTPUT,
            "synthetic_distinct_digests": len(set(outputs)),
            "raw_unobserved_bits": H108 - len(known)}


def jpeg_mcu(width, height):
    return math.ceil(width / 16) * math.ceil(height / 16)


def run():
    known = load_sources()

    transcriptions = []
    for phase in range(H108):
        window = periodic_window(known, phase)
        assert len(window) == OUTPUT
        assert len({index for index, _ in window}) == H108
        assert all(window[i][0] == window[i + H108][0] for i in range(20))
        assert all(window[i][1] == window[i + H108][1] for i in range(20))
        duplicates_known = sum(window[i][1] is not None for i in range(20))
        transcriptions.append(duplicates_known)
    starting = periodic_window(known)
    assert [i for i, _ in starting[-20:]] == list(range(1, 21))
    assert sum(mark is not None for _, mark in starting) == 66 + transcriptions[0]

    # At most 108 distinct information-bearing bit positions are present
    # in a 128-position literal cyclic window. 20 positions are copies.
    assert 128 - 108 == 20
    max_raw_bits = H108
    assert max_raw_bits < 128
    assert max_raw_bits < (128 * 4)  # hex digit alphabet
    assert max_raw_bits < (128 * 8)  # 128 unconstrained 8-bit ASCII bytes

    depths = q4_depths(known)
    native = index_candidates(depths)
    alphabetical = index_candidates(depths, ABC)
    assert len(native) == len(alphabetical) == 18
    assert min(native.values()) > 127  # Native 9-trit number is NOT a direct 0..127 row.
    native_rows = tuple(sorted({value % 128 for value in native.values()}))
    assert len(native_rows) == 18  # modulo row selection is one-to-one HERE, not necessarily always.
    assert native_rows == (
        0, 5, 17, 23, 32, 38, 44, 50, 56,
        62, 71, 77, 89, 94, 95, 110, 112, 127
    )

    # JPEG structure: the damaged image dimensions are *not* uniquely known.
    assert jpeg_mcu(128, 128) == 64
    assert jpeg_mcu(128, 129) == jpeg_mcu(129, 128) == 72
    assert jpeg_mcu(129, 129) == 81
    for width in range(128, 256):
        for height in range(128, 256):
            if jpeg_mcu(width, height) == 64:
                assert (width, height) == (128, 128)

    synthetic = synthetic_hash_lengths(known)
    summary = {
        "status": "DISCOVER/DEVELOP, not a decoded CE password",
        "physical_records": 84,
        "unique_known_residues": 66,
        "unknown_residues": 42,
        "source_period": H108,
        "candidate_output_characters": OUTPUT,
        "literal_cyclic": {
            "number_of_start_phases": H108,
            "forced_equal_character_pairs_for_every_phase": 20,
            "first20_equal_last20_if_start_at_residue1": True,
            "distinct_source_cells_per_window": H108,
            "known_positions_repeated_range": [
                min(transcriptions), max(transcriptions)
            ],
            "known_positions_repeated_phase0": transcriptions[0],
            "unique_unobserved_positions_per_window": 42,
        },
        "sha512_hex_example_ONLY": synthetic,
        "conditional_q4_native_image_row": {
            "physical_class_order": NATIVE,
            "q4_conditional_selections": 18,
            "straight_base3_address_range": [
                min(native.values()), max(native.values())
            ],
            "straight_base3_0_to_127_rows": 0,
            "invented_modulo_128_candidate_rows": list(native_rows),
            "candidate_row_count": len(native_rows),
            "alphabetical_order_alternative_count": len(alphabetical)
        },
        "damaged_jpeg": {
            "footer": "128 UNSOLVED",
            "verified_dimension_domain_each": [128, 255],
            "128_by_128_if_exactly_64_mcus": True,
            "mcu_count_128_square": 64,
            "mcu_count_128_by_129": 72,
            "mcu_count_129_square": 81,
            "image_pixels_if_128_square": 16384,
            "original_128_pixel_rows_available": False
        },
        "remaining_unsupported_bridges": [
            "128 means password length (rather than dimensions)",
            "a Steam beta branch for the CE exists",
            "Steam's beta-password UI/server accepts exactly 128 characters",
            "SHA-512, modulo-128 row addressing or cycle transcription is intended",
            "the original image is exactly 128x128 and has recoverable row pixels"
        ],
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    run()
