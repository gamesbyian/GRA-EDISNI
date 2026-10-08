# Experiment 466 — partial CE artwork as a route lookup against a known corpus

_Date: 8 October 2026. A bounded retrospective **identification** exercise, not a blind sticker decode or a reconstructed 2020 website index._

## Question

If a solver already has incomplete letters from the nine CE sticker **background** pieces, could *recognition among an externally supplied URL set* resolve the unreadable characters without an independent 21/21 image decode?

Experiment [465](experiment-465-background-url-discovery-provenance.md) identified the actual discovery channel from the original Discord export. On 21 April 2020 the URL was reportedly found while inspecting **Wayback / Internet Archive site maps**, then associated with a partially deciphered mosaic. Experiment 466 checks whether that type of noisy-string lookup is feasible using an independent, fixed, **retrospective** candidate corpus: the 74-page snapshot preserved in `data/terminal41-source-tree.json` (source tree SHA `4de72d7c2f21bd9eb4144fda51281c84cbcb90c4`, snapshot 29 Sep 2026).

The 2026 mirror is not the actual Wayback listing that the April-2020 user browsed. Neither that index's complete contents nor its exact historical enumeration order has been recovered. **Do not claim this is a faithful rerun of the original solve.**

## Method: fixed source set, fixed readouts

1. Read all **74 unique** paths from the current source manifest. Strip literal `terminal41.link/` prefix; strip terminal `/index.html` for a directory page, or terminal `.html`, `.txt` or `.png` from other file paths. No arbitrary character corrections or manual synonym tables.
2. Preserve three literal partial readings from the pinned Experiment-465 history, keeping their unequal provenance. No machine completions, symbol conversion, model-derived words, lexical scoring or image recognition.
3. Rank all paths by standard unit-cost Levenshtein edit distance from each **21-character** reading; tie-break lexicographically. Freeze the target path `dat/534brn9653f9j8mmd` and record the best alternative after withholding it from the candidate list.
4. Run `python scripts/audit_background_url_lookup_discrimination.py --summary`. It checks 74 unique paths, exact source tree, fixed candidate strings, distance and nearest-neighbor results. Dedicated CI preserves a full JSON record.

## Result

| Candidate's provenance | Partial string | Distance to true URL | Best *other* route distance | Margin |
|---|---|---:|---:|---:|
| March 20, 2020 linked reading | `uat/5345rn9653f9i8nmd` | **4** | **17** (`dat/breachlog`) | **13** |
| Closest *first-person* remembered pre-index reading | `dat/534brn9653f9i8rnd` | **3** | **15** (`dat/breachlog`) | **12** |
| Later README's unverified 19/21 reading | `dat/534brn9653f9i8nmd` | **2** | **15** (`dat/breachlog`) | **13** |

In this *particular 74-route mirror* the true URL ranks first with no ties on every historical candidate. It is also the only route within edit distance four of each partial reading. Removing the correct destination leaves a far more distant nearest candidate. This demonstrates **retrieval separation within a fixed codebook**, not the probability that a string arose by chance or proof a contemporary solver used Levenshtein distance.

The two most authoritative source events are (a) first-person original April-21 **site-index discovery** and (b) April-28/29 solver acknowledgment that the entire path was **not read from art beforehand**. The 19/21 retrospective candidate should not be upgraded to a contemporaneous primary-source reading merely because it makes the distance even smaller.

## What this teaches the larger ARG investigation

**A partial code can have an unambiguous practical destination when paired with an external dictionary.** That does **not** require all physical symbols to be recovered or a complete image manually deciphered. The original background → URL pairing was a genuine puzzle advance, even though external discovery contributed information.

The sticker **foreground** could theoretically work through a similar *source-anchored lookup* (e.g. an exact native slot, short command vocabulary, or historical page index). But this experiment supplies **no foreground-to-dictionary registration at all**. Testing every substring against every known artifact until one looks close would simply replay answer-assisted discovery without its historically independent constraints.

The useful design rule is: **first** establish a finite, source-native target list and a reproducible interpretation rule; **then** evaluate how strongly the physical foreground distinguishes candidates. Require the source to supply at least one additional registration cue (selection, order, layout, symbol legend, or input length) **before** treating a match as a foreground decoding clue.

## Falsification and limitations

- **Retrospective corpus bias:** 74 paths were preserved *after* 2020 and include the correct answer. We must not infer a likelihood under a random URL distribution from this ranked list.
- **Incomplete historical index:** Wayback's actual April-2020 listing may have contained additional candidates and different file naming; uniqueness among 74 survivors is not proof of uniqueness then.
- **Normalization choices:** Stripping file extensions/directory index is motivated by URL vs. file path semantics; it is specified in the test, not demonstrably the exact 2020 solver procedure.
- **Provenance:** March-20 partial string is source-linked, April-28 remembered variant is corroborated firsthand in original Discord export, and the “19/21” reading is retrospective-only.
- **Scope:** The index result does not imply the foreground symbols themselves encode `534brn`, an embedded image, a password or any recurrent selector.

### Next high-value independent evidence

Recover the exact April-2020 Wayback site-map output, or a pre-discovery 21-character foreground decoding instruction. The former would permit a historically valid candidate-set ranking; the latter might establish the missing foreground-to-reader link. Neither follows from the 74-route retrospective lookup alone.

**Conclusion:** This is an experimentally demonstrated **source-assisted error-resolution mechanism**, not a recovered additional INSIDE cipher or independent authorial proof of an intended URL edit-distance code.
