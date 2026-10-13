# Does one Collector's Edition sticker encode an individually usable input?

*12 October 2026. DISCOVER/DEVELOP; independent source/observation census, not a decoded CE credential.*

## Hypothesis family

The owner-accessibility suggestion admits two importantly distinct endgames:

1. **Collaborative global puzzle, individually usable shared output:** owners contribute to reconstruction of a repeating foreground, which yields a common web/game/physical instruction. One owner is **not** expected to solve 108 positions alone.
2. **Each individual sticker as a credential or local instruction:** sticker number plus symbol and one of nine background artworks could be entered into a common service, or point at a local physical/game target. Owners could use their own sticker without seeing the rest.

Neither is assumed to be Playdead's intention. This experiment quantifies information available to one purchaser **before** assigning a receiver, and tests how much physical evidence supports the current H108 repetition premise.

## Source and true owner-local information

Use the canonical **84 physically recorded serials**, not 84 distinct bits. The currently reported raw symbol is one of slash/dash/dot; the three-digit serial and one A–I background tile are the other visible metadata.

The background class rotates deterministically with the serial's **modulo-nine residue**. In all records with an independently reported image class, the image agrees with that cycle. **043 and 427 lack independently observed image-class confirmation**, so the code can only *infer* G for 043 and D for 427 from the observed class rule. Both are marked as **inferred, not observed** in the machine-readable output.

Thus, conditional on the cyclic image assignment, one sticker's *class identity* adds no independent information beyond its serial. The class imagery itself can still carry collective information or serve as an authored visual instruction. The foreground mark contributes at most a binary choice **given a zone** (slash/dash for residues 1–81 and slash/dot for 82–108), conditional on the accepted 108-position serial registration.

There are exactly **9 × 3 = 27** possible class/glyph token types, of which **24** are represented by the 84 known serials. The three unobserved token types are **A-dot, C-dot, F-dot**; this is NOT proof those tokens were never produced. The body/tail one-minority and one-slash models permit them at missing tail serials. A per-owner mechanism demanding a unique input from a production run of hundreds must use the serial or other information rather than just the 27 possible class/glyph tokens. No premise of cryptographically secure access is imposed.

## Test: is 108 uniquely compelling across short candidate periods?

Independently compute pairwise repeat conflicts under every **candidate serial period p = 1..216**, allowing the repeated symbol or the joint (symbol, inferred image class) to match. For each candidate, count observed serials that collide modulo p, how many repeated observations they add, and whether **any** colliding pair contradicts.

| Candidate p | Extra agreeing symbol observations | Symbol conflicts | Joint class/symbol conflicts | Interpretation |
| --- | ---: | ---: | ---: | --- |
| **108** | **18** | **0** | **0** | Strongest directly supported matching cycle in tested window |
| **197** | 6 | 0 | **6** | Accidental symbol compatibility for six collisions; contradicts actual nine-tile repetition |
| **216** | 8 | 0 | 0 | Natural harmonic (2×108), fewer repeated confirmations |

**Only those three candidate periods have zero observed symbol contradictions among p=1..216 with at least one repeated collision.** Requiring the *joint* class/glyph repeat leaves only 108 and 216. Periods with no repeated collisions are excluded from this table because such models have **zero test evidence**, not a positive compatibility win. Period 108 is already part of the community's established carrier description; this is a new **bounded, observation-only comparative census**, not a discovery of a previously unknown period.

Across the actual 108-cycle grouping: 84 serial observations → **66 unique residues**, with **16 repeated residue groups** supplying **18 extra matching serials**. Group sizes are 38 singles, 14 doubles and two triples *within the 72 observed primary-sector serial entries*. No repeated tail residue was independently observed.

### Fixed-period label-shuffle check

Condition **in advance** on p=108, the 72 physical primary-sector entries, their 44 slashes/28 dashes, and their serial positions. Under the narrow null of assigning 44 slash marks uniformly across these 72 entries without replacement, all modulo-108 repeated groups would be monochromatic with exact probability:

\[
\frac{[x^{44}](1+x)^{38}(1+x^2)^{14}(1+x^3)^2}{\binom{72}{44}}
=\frac{440079448381568}{75553695443676829680}
\approx 5.8247243341\times10^{-6}.
\]

This is **NOT** an inferential probability of intended H108 coding:
- The period is being discussed because historical investigation *already* found it; testing p=108 after model selection violates preregistration.
- Manufacturing assignment and observed survivor/owner sampling are not uniform independent symbol labels.
- Both historical nine-tile periodicity and the actual 2019 sticker imagery are stronger authored-structure priors than this toy null.
- The comparison has not corrected for selecting the best period among 216 or beyond 216.

The calculation is still valuable: the 18 repeated symbol observations are not merely a loose visual impression, and the assumptions of the reference distribution are completely explicit.

## Consequences for a purchaser-access experiment

Once an entire repeating 108-symbol sequence is known, **serial modulo 108 predicts the foreground glyph** and **serial modulo 9 predicts background class**, under this model. For a proposed *single sticker input*, the serial is then the only distinct variable supplied by owners. A shared receiver may nonetheless consume the individual serial as a selector or claim token. This is not evidence that such a receiving system existed.

**Design three independent tests, without restricting any other solution:**

- **Global completion → common action:** test reconstructed 108/81/27/9-symbol payloads against independently established Playdead site, physical artwork and game mechanisms. The receiver may work for anyone and need no unique sticker.
- **Single sticker → action:** search genuine historical HTML, printed art and game handlers for a numeric serial slot, input pairing, row/column selector, per-copy response or unique short token. Distinguish a *real* serial-specific input from a supposed one invented solely to justify a single-owner solve.
- **Collaborative URL + per-owner serial:** the nine-part background already yielded a URL through pooled sticker images. Conditional experiment: perhaps it pointed to a shared receiver where a *personal* three-digit serial and its corresponding glyph were then useful. The archived **534brn** page is damaged/static and shows **no verified numerical input or original backend**. This two-stage hypothesis is an excellent explanation of usability *if* an actual receiver is recovered, not a finding.

## Third physical PS4 release: provenance control

Do not compare the CE disc only against iam8bit's standalone PS4 edition. A separately dated **September 2017 505 Games INSIDE + LIMBO PS4 release** included a poster and art card; its catalogued disc identifier is **CUSA-09304**, documented in the [Pratt Institute library catalog](https://cat.pratt.edu/record%3Db1699465), including disc-level identifiers. This is an earlier **comparison baseline**, not something CE purchasers themselves automatically received.

The **2019 CE's actual CUSA and disc bytes remain unverified**, as do the standalone 2019 disc's exact build identifiers. The [GameFAQs PS4 table](https://gamefaqs.gamespot.com/ps4/194097-inside/data) has a blank CE Product ID, while the independently catalogued 2016 US digital version uses CUSA-05297. None of these differences proves a hidden game build. Obtain actual disk/installer manifests and binary version hashes before comparing secrets, assets, or data layouts.

The [official iam8bit standalone PS4 listing](https://www.iam8bit.com/products/inside-ps4-physical-game) and [CE listing](https://www.iam8bit.com/products/inside-collector-s-edition) present similar disc label designs and nine-sketch poster imagery. Promotional photo reuse is not proof that shipped disc binaries, covers or poster sheets were identical.

## Reproducibility

Python standard-library only from repository root:

    python scripts/audit_ce_owner_local_channels.py --output /tmp/owner-local-ce.json
    python -m unittest discover -s tests -p 'test_ce_owner_local_channels.py' -v

Exact parsed result: [data/ce-owner-local-period-audit-2026-10-12.json](../data/ce-owner-local-period-audit-2026-10-12.json); [source script](../scripts/audit_ce_owner_local_channels.py); [tests](../tests/test_ce_owner_local_channels.py). The source physically observed class for 043 and 427 remains blank. Neither test imputes missing foreground symbols, reveals a private CE owner, supplies a password, or claims a working consumer.

**Result:** stronger empirical support for a shared periodic carrier, an explicit 27-token limit for serial-free owner-local inputs, and a clearly defined *collaborative lookup then per-owner serial* hypothesis. No new sticker or Playdead contact needed for further investigation.
