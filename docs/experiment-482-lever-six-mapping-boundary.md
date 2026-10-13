# Experiment 482: the secret-ending code cannot fit any native sector-alphabet reading

_Status: completed bounded extension to Experiments 3, 342, 343, 401 and 479; 12 October 2026. Research mode: **VALIDATE**, conditional on the observed 81/27 alphabet sectors._

## Motivation and provenance

The actual INSIDE alternate-ending bunker lever accepts a 14-move musical phrase. Contemporary 2016 walkthroughs record the conventional start as:

\`\`\`text
U U R L R R R U U U R L L L
UURLRRRUUURLLL
\`\`\`

Sources: [Prima Games (2016)](https://primagames.com/tips/inside-game-how-unlock-secret-ending), [Shacknews (2016)](https://www.shacknews.com/article/95640/inside-how-to-get-the-secret-ending). The recording is a loop and several cyclic starts are documented: [GameFAQs player discussion](https://gamefaqs.gamespot.com/boards/191607-inside/79113965).

A much stronger CE-specific lead than arbitrary substitution already exists in the project's historical material. The **2020 and 2021 sleeve/lever discussions** independently associated the cover's dot/left, dash/right and slash/top glyphs with the in-game lever. See [Experiments 342](experiment-342-sticker-lever-cue.md) and [343](experiment-343-lever-lineage-boundary.md). Under that geometric mapping, the conventional phrase is \`//-.---///-...\`, with dot=\`.\`, dash=\`-\`, slash=\`/\`.

Experiment 343 had already shown that **no rotation or reversal of that phrase** fits a contiguous H108 window under the historical symbol mapping. Experiment 342 tested all six symbol assignments for the unrotated forward and reverse sequences, but had not combined **all mappings and all rotations** with the sector-alphabet boundary. This note closes that modest remaining sensitivity gap, without reopening the historical negative.

## Frozen search space

We preserve the documented ordinary in-game password and test only **direct consecutive reads** of the 108-period serial-ordered sticker cycle. No position permutation, isolated 14-of-108 selection, guessed second password, extra lever mechanic, or completion-model state is fitted.

- **Input phrase:** \`UURLRRRUUURLLL\` (five U, five R, four L).
- **Bijective direction-to-symbol assignment:** all 3! = 6 maps onto \`/\`, \`-\`, \`.\`.
- **Phrase orientation:** 14 cyclic rotations of the forward phrase and 14 of its reverse (28 distinct strings).
- **Sticker start:** all 108 positions of the circular H108 tape.
- **Carrier sectors:** residues 1–81 permit \`/\` or \`-\`; 82–108 permit \`/\` or \`.\`.

This evaluates **6 × 28 × 108 = 18,144** typed placements.

### Results

| Test | Result |
| --- | ---: |
| Mapping assignments | 6 |
| Distinct forward/reversed rotational password variants | 28 |
| Candidate placements per assignment | 3,024 |
| Total typed candidate placements | **18,144** |
| Typed-compatible placements | **0** |

**The zero is mathematical under the sector premise, not a statistical shortage of observed stickers.**

### A short proof that avoids brute-force dependence

Under any of the six mappings, one direction maps to slash, the glyph common to both sticker sectors. The *other two* directions map to dot and dash, each confined to a **different** sector.

Delete the slash-mapped direction from the cyclic lever password. For **every choice** of which direction is slash, the remaining two direction types have four alternating circular runs. Every possible linear rotation or reversal consequently retains **at least three changes** between those two types.

But a window of length 14 can cross **at most one** boundary between the 81-position slash/dash sector and the 27-position slash/dot sector, because the shorter sector itself has length 27. It therefore permits **at most one** alternation between dash and dot. Three required exceeds one available. No missing-symbol completion *respecting that sector model* can fix this.

The exhaustive script independently checks the whole finite search space and asserts the proof's run-count invariant.

## What the negative does and does not establish

**Ruled out, given the established sector model:** embedding the *already-known* 14-move original bunker password as any 14 **consecutive** H108 serial residues, under **any** one-to-one symbol mapping, forward/backward, with arbitrary cyclic origin.

**Not ruled out:** a different intended lever command, a registered nonconsecutive selection/readout, external permutation, a change of carrier geometry, or a downstream consumer that borrows lever-style symbol semantics. The known normal lever password is already functional and is not evidence of a *new* 14-move interface.

**Epistemic qualification:** no one has photographed all 108 distinct residues. The 81/27 *alphabet exclusion for unknown cells* is a plausible and repeatedly observed carrier rule, but still extrapolates from 66 physically observed residues. This is a **conditional structural impossibility**, not an unconditional theorem about every physically unobserved sticker. A newly verified dot in residues 1–81 or dash in 82–108 would invalidate the sector premise and require reconsideration.

Historical work [Experiment 401](experiment-401-digit-index-lever-historical-replay.md) also tested a different nine-command proposal against surviving 2023 brute-force lever streams, and [479](experiment-479-classword-lever-consumer.md) excluded two natural twelve-position A–I class-word readings of the original known password. Those negative results are **related, not new independent confirmations** of this experiment.

## Reproduce

\`\`\`bash
python scripts/audit_lever_six_mapping_rotations.py
\`\`\`

The script uses only the standard library and the fixed input/sector rule, with no dependency on the incumbent ternary machine, guessed missing stickers or model completion. Machine-readable expected snapshot: \`data/experiment-482-lever-six-mappings.json\`.

**Next evidence trigger:** a source-authenticated clue fixing a nonconsecutive readout/order, a new physical out-of-sector mark, or an independently demonstrated new lever input consumer. Do not use arbitrary symbol reassignments or rotations as an excuse to resume unfalsifiable substring searches.
