# Q4 roles for an exploratory nine-frame receiver (12 October 2026)

**Mode: DISCOVER/DEVELOP.** All output conventions below are invented hypotheses, not CE decoding claims. The purpose is to *try* concrete output-producing rules even when no independent clue endorses them. Reproduction: `python scripts/conjecture_lab_q4_roles.py`. It reads the canonical 84 physical observations at 66 distinct foreground residues; the other 42 stay unresolved.

## The shared primary assumption

Read residues 1–81 as nine consecutive 3x3 frames. In each frame, each vertical 1-4-7/2-5-8/3-6-9 triplet has exactly one minority symbol; encode the minority's 0-based position as a trit. Three trits give one base-27 integer. Examine alphabetical conventions 0=A through 25=Z (A0), or 1=A through 26=Z (A1); values outside these intervals are omitted from *alphabetic-only* output counts. Different column orders, mirrored frames and a space as the 27th symbol are separate untested alternatives.

The final 27 symbols are read by the separately hypothesized *exactly one slash at one of three depths* in each of nine depth stacks (82+j, 91+j, 100+j for j=0..8). Current physical marks allow 18 slash-position sequences. This Q4 rule is conditional, not confirmed.

## Three competing, concrete Q4 roles

1. **Suffix:** The first 81 positions yield nine independent letters; Q4's nine depth-index trits yield three more. Under A0 the primary has 77,760 alphabetic nine-character outputs and the suffix eight alphabetic outputs, for **622,080** joint 12-letter outputs. Under A1 the corresponding numbers are **57,024 × 18 = 1,026,432**. This high degeneracy is not a proposed password list. Under A0 the suffix middle is K, and under A1 it is J, *conditional on exactly this grouping and alphabet*. The A1 body ninth character F is only forced if zero is **discarded** rather than interpreted as a space.
2. **Selector:** Let the Q4 depth trit for frame j choose one of its three POS3 column digits. Nine selected trits, regrouped by threes, give **54 compatible three-letter strings** under either A0 or A1 in the ordinary column order. A0 allowed letter sets by output position: `DEFMNOVWX / SU / GPY`. A1: `CDELMNUVW / RT / FOX`. This model uses Q4 as an *addressing/control layer*, not extra symbols appended to a message.
3. **Rotation:** Let the Q4 depth index for frame j cyclically rotate its three POS3 column digits before interpreting its letter. Under ordinary frame and column order this yields **1,399,680** possible nine-letter strings under A0, and **855,360** under A1. It broadens rather than sharpens the literal-word search.

All counts reflect compatible symbolic completions with no imputation of missing physical observations. Independence of frame and Q4 choices is assumed only within these toy operators.

## Exploratory dictionary test and matched null

Using **CMUDICT 1.1.3** (13,124 ASCII alphabetic nine-character entries after normalization and deduplication), the direct-body and Q4-rotation readers were tested with A0/A1, six common column permutations, and 16 unique 3x3 frame orders obtained from the symmetries of serial A–I and the hypothesized printed-art layout I/A/B;C/D/E;F/G/H.

- **Unrotated**: 0 dictionary matches.
- **Q4-rotated**: exactly one dictionary entry, `GOLIGHTLY`, with A0, column permutation (1,2,0), and frame indices (8,5,2,7,4,1,6,3,0). The entry is also a surname, so do not interpret it as an instruction without independent support.
- **250 shuffled-frame nulls**, deterministic NumPy RNG seed 20261012, repeating the same layout/alphabet/column search: 134 runs yielded 0 hits, 88 yielded 1, 22 yielded 2, four yielded 3, and two yielded 4. Thus **116/250 (46.4%)** had at least one match. Observed = 1 is unremarkable under this test.

The shuffle control tests the limited word-recognition claim after trying many arrangements, not whether this is the actual CE grammar. The wordlist experiment is exploratory and was selected after seeing the attractive output; it is not a validation p-value. The script above covers the pure positional arithmetic; the dictionary test currently needs CMUDICT 1.1.3 and NumPy to replay, and is not a CI check.

## Research disposition

Keep **suffix, selector, rotation** as rival versioned conjectures. The selector is economical and creates the *smallest* readout class, but small output space alone is not evidence. Next: inspect whether artifact geometry or historic ARG operator examples prefer any Q4 role; consider explicit 27th-character separator and nonalphabetic instructions; use any future new sticker only as independent falsification, not as the essential route. No Steam password was tested, and no hidden branch is established.
