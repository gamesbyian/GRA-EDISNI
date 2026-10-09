# Wow!-signal analogy for INSIDE transport inscriptions (2026-10-09)

**Research mode:** DISCOVER (Discord hypothesis), DEVELOP (assume a Big Ear-inspired inscription scheme), and one bounded VALIDATE test (the historically documented *exact* Big Ear output alphabet and a single-transit envelope). **Status (updated with archival screenshot and matched controls): the literal transcriptions violate Big Ear's zero notation and single-transit envelope. A post-hoc 0/O + 1/I alternative fits a single-peak envelope, but its apparent success is forced by the chosen alphabet ranks (26/26 matched controls) and is not evidence for radio astronomy. The scene screenshot montage is now archived, but original Unity texture bytes remain missing.** No claim about the CE foreground, Terminal41 receiver, or Project 3 link is established.

## Hypothesis and preselected corpus

A Discord participant suggested that `A10N7` might work like the 1977 Wow! printout `6EQUJ5` and noted the mapped 23. Fix the corpus from pre-existing 2016 discussion rather than retrieving attractive alphanumeric strings after applying the rule:

| Source | String | Provenance | Important dependence |
|---|---|---|---|
| Big Ear historical positive control | `6EQUJ5` | Jerry Ehman's first-party explanation (linked below) | External reference, not INSIDE |
| Station sign | `A10N7` | July 2016 original-game screen/texture investigation | `OTHER_TrainLetters_#888` is a contemporaneous *exporter label*, not authorial puzzle number |
| Wrecked train | `L08` | Same July 2016 thread | Reported on a *different train*, not independently recovered original bytes here |
| Laboratory text suffix | `B02` | Same July 2016 file/scene investigation | Suffix of longer `Fordsjh Gjfhdfdjfhd Ujhdfr B02`; do not pretend it is a standalone train label |

The repo already records these source distinctions in `data/original-game-asset-consumer-inventory-2026-10-08.json`; this card does not add physical observation.


## Recovered scene-image witness (new evidence intake)

The project's already mirrored `sashaok123/BigDusty_INSIDE_ARG_Map` map had **omitted its image files**. GitHub code search found a block expressly tagged `A10N7 / L08`. I recovered and preserved two actual image files from the public original map repository as **byte-identical Git blobs** (checked SHA equality), not AI recreations:

| Image | Repo evidence copy | Upstream original | Exact blob SHA | What it shows |
|---|---|---|---|---|
| `block_004.webp` | [A10N7 + L08 screenshot pair](../../archive/external/bigdusty/data/blocks/block_004.webp) | [BigDusty source](https://github.com/sashaok123/BigDusty_INSIDE_ARG_Map/blob/main/data/blocks/block_004.webp) | `b82846b2209c36176c36461aba508430086df63f` | Dark in-game transport-scene montage with both strings, explicitly **captioned by the 2026 map maker as A10N7 and L08**. |
| `block_009.webp` | [B02 lab label montage](../../archive/external/bigdusty/data/blocks/block_009.webp) | [BigDusty source](https://github.com/sashaok123/BigDusty_INSIDE_ARG_Map/blob/main/data/blocks/block_009.webp) | `7a425c2daa9a0d1a06b0f1d950543cb7d0ea7c16` | Lab-window/prop code `Fordsjh … B02`; map also labels a screenshot **“2014 Trailer”**. This trailer attribution is not yet independently frame-verified. |

**Image status:** authentic bytes of a **2026 community-produced montage**, not original lossless game textures, not independent confirmation of its own transcribed captions. Visual inspection confirms that a sign and another transport marking are depicted, but the crop is too small and dark to adjudicate whether their original glyphs are `1/I` and `0/O` by their strokes. The block's explicitly numeric captions and the repeated diegetic use of zero-padded `02`, `08` are evidence favoring a **label/ID** reading; a decisive typography comparison still requires better pixels.

The map's `B02` panel explicitly foregrounds its appearance in a reported 2014-era trailer, supplying a chronology-check target independent of the 2019 CE. Playdead's [official press assets](https://playdead.com/press/) include E3 2014 footage, which could validate or falsify the montage caption. No causal bridge to the third game follows from these images.


## Actual historical rule (not generic base 36)

Ehman explicitly describes one character per **12-second signal-strength reading** (10 seconds sampled, approximately 2 processing). The scale is integer-truncated, baseline/rms normalized: **blank means 0**, printed `1`–`9` mean 1–9, and letters `A`–`Z` mean 10–35. Thus `N = 23`; `L = 21`; `B = 11`. `0` was **not** a printed zero-strength character. No frequency, direction, or audio is recoverable from those characters alone. A literal `0` therefore excludes *exact unmodified reproduction* of the 1977 output convention, though a later artist could deliberately invent a modified convention.

The authentic positive control gives `[6,14,26,30,19,5]`: a single rise and fall consistent with the fixed antenna's beam transit.

The three INSIDE strings all include a literal zero. In a **deliberately non-authentic** character-0-tolerant reading:

| String | Intensities | Big Ear exact printout compatible? | Single nondecreasing-then-nonincreasing shape? |
|---|---|---|---|
| `6EQUJ5` | `6,14,26,30,19,5` | **yes** | **yes**, interior peak |
| `A10N7` | `10,1,0,23,7` | **no**, glyph zero | **no**, two separated highs |
| `L08` | `21,0,8` | **no**, glyph zero | **no**, valley |
| `B02` | `11,0,2` | **no**, glyph zero | **no**, valley |

**Strongest invariant:** `A10N7` has letter/digit pattern L-D-D-L-D. Under the Big Ear mapping *every letter is >=10 and every printed digit 1–9 is <=9*, so the two letter highs with intervening digit lows make a single-hump beam profile impossible **regardless of the specific letters or digits**. This does not exclude arbitrary variable/transient radio telemetry. `L08` and `B02` similarly fail a single-hump shape in the zero-tolerant comparison, but `B02` is not an independent transport reading.

Reproduce strictly and permissively, including checks that fail if the fixtures change:

```sh
python scripts/audit_wow_signal_inscriptions.py
```

This is a **structural applicability test**, not a calibrated significance test: only three selected candidate markings were observed, and no complete game-wide marking census was available. Assigning a p-value from a random alphabet would mistake ad hoc signs for random samples.

## A surprising exploratory escape hatch: are the zeros actually O?

**DISCOVER; selected after seeing the incompatible literals.** A `0` in poor-resolution or stylized typography could be uppercase `O`, and `1` could be uppercase `I`. Those are **alternative readings of an as-yet-unverified glyph image**, not permitted changes to a verified source transcription. Restrict the sensitivity search to only these substitutions (no arbitrary digit-to-letter conversion); the three strings have 2+1+1 ambiguous positions, so exactly **16 joint readings**.

| Reported transcription | Hypothetical glyph reading | Authentic Big Ear intensities | Single interior peak? |
|---|---|---|---|
| `A10N7` | **`AION7`** (`1→I`, `0→O`) | **10,18,24,23,7** | **yes** |
| `L08` | **`LO8`** (`0→O`) | **21,24,8** | **yes** |
| `B02` | **`BO2`** (`0→O`) | **11,24,2** | **yes** |

Exactly **1/16** of these narrow *joint glyph assignments* has all three authentic-printable, interior-peaked sequences. This is **not** a statistical p-value: the substitutions were selected in response to failure, the signs were not sampled randomly, and the three- and five-character sequences are not independent astronomical observations. In particular `LO8` and `BO2` are cheap successes: for a generic letter-`0`-digit label, changing 0 to O forces a middle intensity of 24, larger than *any* trailing digit 1–9; choosing a preceding letter A–O gives an automatic interior peak. `B02` is additionally extracted from a longer lab inscription.

**Critical matched-class control (subsequent audit): the seemingly elegant `AION7` hump is mathematically *automatic*.** Keep `A`, `O`, `N`, `7` fixed and replace the `I` with any of the alphabet's 26 letters. Every single `A?ON7` passes the one-interior-peak test (**26/26 exact enumeration**, confirmed by `scripts/audit_wow_signal_inscriptions.py`). Proof: `A=10` is the **minimum** letter value, `O=24` exceeds `N=23`, and all letter values exceed the final digit 7. For any intervening letter, the sequence must rise from A, peak at that letter or O, then descend through N to 7. The O/N near-plateau is determined by the preselected adjacent alphabetical letter identities in the alternative transcription, not independent source evidence.

`LO8` and `BO2` also pass trivially after replacing the zero with O=24: `L=21` and `B=11` are smaller than 24 while final digits 8 and 2 are smaller. Thus **the three curve matches add no discrimination over this narrow, after-the-fact interpretation**, despite exactly one of 16 jointly enumerated literal/glyph-confusion readings satisfying all tests. **1/16 describes the chosen *transcription repair* and must never be represented as a chance probability of a Wow! match.** The literal source-transcription `A10N7` still fails exactly, and we still need original pixels to determine if the speculative transcription is even plausible.

**Still-decisive acquisition target after recovering the low-resolution montage:** inspect an original-resolution image or byte-accurate texture for `A10N7` and the glyphs on `L08` and `B02`. If the scene fonts differentiate uppercase `O` from numeric `0` or uppercase `I` from `1`, this entire escape hatch can be closed or narrowed. Do not let a beautified typed replacement stand in for the actual sign pixels.

## Three rival conditional explanations

**R1: Exact Wow!/Big Ear homage.** If the designer meant characters as exact Big Ear data, `0` would have been a blank, and a steady off-axis point source crossing a fixed beam would make a single peak. This *fixed* implementation is contradicted on both counts. It is inaccurate to say this disproves all possible fictional radio telemetry.

**R2: Generic fictional radio data / scientific reference.** Keep the mapping but allow printed `0`, time-varying sources, nonstationary receivers, or deliberately scrambled readings. This remains logically possible, but introduces at least two unfixed departures (zero notation, source/time pattern). A receiving artifact requires an independent indication of frequency, sample interval, channel, ordering, celestial coordinate, modulation, or what to do next. Values alone contain no radio frequency and do not construct sound. The letter `N` yields 23 solely from the chosen alphabet mapping; the 23 observation is **derived from the proposed interpretation**, not an extra clue corroborating it.

**R3: Diegetic transport/sector/asset labels.** `L08` and `B02` follow letter + zero-padded two-digit ID conventions; `A10N7` could be a distinct concatenation of `A10` and `N7`, though this precise segmentation is **invented** until the typography/location is inspected. This model explains the literal printed zeros naturally; it predicts consistency with other nearby signs/props, variant material colors and train IDs. `B02` coming from lab text means a common cross-scene labeling convention itself is **unproven**.

**R4: 2016-era textual reading.** A contemporary August 2016 Steam participant remarked that `A10N7` resembles **ALONE**. Another July 2016 participant proposed `A = 10`, `N = 7`, and speculated `B = 02` as possible letter/number correspondences. Neither is evidence of authorial intent. They are worthwhile *historical alternatives* to preserve rather than backfitting one present-day decode.

**Project 3 bridge:** Playdead's own current recruitment copy calls its ongoing game a third-person science-fiction adventure in a remote corner of the universe. This supports the public *theme*, but supplies **no dating, 2016 intent, mechanics, frequency, or cross-game binding**. The INSIDE markings were publicly investigated in July 2016; no connection with Project 3 is demonstrated.

## Risky next checks and stopping rule

1. Recover the **actual shipped texture/screenshot** of `OTHER_TrainLetters`, with orientation and spacing, plus the separate `L08` scene and any adjacent labels. Exact byte sourcing remains an unclosed asset gap in the original-game intake. Is `A10N7` a single contiguous telemetry string, a sign with field dividers, or prop typography?
2. Build a genuinely **exhaustive** inventory of original game's short in-world alphanumeric labels with *scene*, *asset*, *glyph spacing*, and *dated source*. Include negative controls: clearly mundane object IDs, unrelated nonsense suffixes, known secret-solving strings. Do not claim the current three exemplars exhaust the game.
3. Ask whether any pre-2019, source-authenticated in-game/ARG object supplies an **independent astronomical cue** (telescope image, sky position, radio receiver, explicit frequency or 1420 MHz hydrogen-line cue, repeated 12-second cadence). A web search not returning such a cue is not proof of global absence.
4. Require a prospective prediction: given a uniquely identified radio-like context, freeze the decoder and predict the reading/function of a previously withheld authentic inscription, rather than retrospectively recognizing a pleasing value.
5. **Stop** using Big Ear shape matching on these three exact strings without new independent evidence. R2 may stay as a low-priority, explicitly speculative branch; do not force the sticker foreground into this alphabet.

## Sources

- First-person explanation of code values and timing: https://bigear.org/6equj5.htm
- First-person account of the observation: https://www.bigear.org/Wow30th/wow30th.htm
- July 2016 asset names, sign scenes, L08, and B02: https://steamcommunity.com/app/304430/discussions/0/365172547948628597/?ctp=2
- July 2016 proposed A=10, N=7 / B=02 interpretation: https://steamcommunity.com/app/304430/discussions/0/359543951708963220/
- August 2016 ALONE alternative: https://steamcommunity.com/app/304430/discussions/0/359543951720753445?ctp=7
- Current Playdead Project 3 description: https://playdead.breezy.hr/
- Repo fixture/provenance: `data/original-game-asset-consumer-inventory-2026-10-08.json`
