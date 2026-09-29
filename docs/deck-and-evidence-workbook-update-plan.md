# Deck + Evidence Workbook Update Plan

_Status: implementation plan, drafted 2026-09-29 against `main` through Experiment 291 plus live PR #31 (Experiment 293), live PR #32 (Experiments 292, 294, 295), and live PR #34 (Experiments 296–297)._

## Purpose

Update the public-facing presentation and its single supporting evidence workbook so that they reflect the modern mechanical crack without losing the deck's existing narrative clarity, design language, density, or voice.

The current deck is not merely structurally good; its existing visual design is the baseline to preserve. The update should look like an extension of the same deck, not a redesign. Its typography, spacing, restrained palette, section dividers, callout style, diagram language, density, detail level, and conversational-but-careful tone should be reused wherever possible. Existing slides should not be reformatted, rewritten, or visually modernized unless correctness or the insertion of genuinely new evidence requires it.

Its early story of sparse stickers -> H108 -> ternary geometry -> selector/routing machine remains useful. The largest substantive problem is that later research has changed the epistemic status of several claims:

- exact primary POS3 is a preferred physical authoring grammar, but not the only parent that recovers the canonical 14-state machine;
- globally shared Q4 slash polarity is no longer a functional premise;
- the canonical transducer has physical completion gauges that must not be confused with hidden machine states;
- the two recursive address substitutions, route shell, and terminal `100` are much better derived than the current deck shows;
- the raw-constraint reconstruction `216 -> 20 -> 14 -> 100` and the broad Q4 inverse searches are now stronger anti-overfitting evidence than several older bounded-family rarity results;
- the closed-corpus mechanical crack is substantially complete, while the semantic/external-consumer question remains unresolved.

The update should preserve the public deck's "show the mystery becoming machinery" arc and avoid turning it into a research log.

## Baseline artifacts

Current archived artifacts:

- `archive/drive/INSIDE_Collector_Edition_Sticker_Mystery_What_I_found_and_what_it_might_mean.pptx`
- `archive/drive/INSIDE_Sticker_Mystery_Supplementary_Evidence.csv` — legacy evidence export; preserve as an archive, but do not maintain a second spreadsheet deliverable
- `archive/drive/INSIDE_Sticker_Mystery_Verification_Pack.xlsx` — the format to carry forward

The deck contains 44 slides including section dividers and appendix. The older evidence files are effectively frozen around Experiment 194. The refreshed evidence product should be **one XLSX workbook only**.

## Update principles

1. **Treat the existing deck as the design specification.** Preserve its typography, palette, spacing, grid, recurring shapes, section dividers, callouts, line weights, diagram style, and visual rhythm. Reuse existing slide elements whenever possible instead of inventing new ones.
2. **Do not change an existing slide merely because it could be redesigned.** Make the smallest visual and textual change that restores correctness or creates room for genuinely new evidence.
3. **Match the existing density, detail, and tone.** New slides should feel neither more academic and crowded nor more sparse and promotional than their neighbors. If one new idea cannot fit at the deck's established density, give it another slide rather than shrinking type or compressing prose.
4. Prefer one visual claim per slide, consistent with the current deck's pacing.
5. Distinguish:
   - raw observation;
   - local reconstruction;
   - model-class selection;
   - machine-derived consequence;
   - physical gauge;
   - observer/readout;
   - semantic hypothesis.
6. Do not use color alone to encode state. Every color-coded distinction also gets a label, icon, border style, position, or shape.
7. Do not imply that 224 or 336 complete masters are 224 or 336 machine states. The functional hidden-state family remains 14 states; the larger counts arise from physical completion gauges.
8. Do not present the all-slash Q4 surface as functionally forced. Present it as the preferred physical gauge representative, with independent simplicity/balance support.
9. Keep `100` as the mechanically reconstructed fixed terminal. Do not revive plaintext/lore speculation.
10. Use cubes only where the data are genuinely cubic or where a cube is an exact state-space diagram. Cubes should explain structure, not serve as decoration.
11. Preserve the deck's voice. Prefer editing only the specific sentence, caption, number, or diagram whose meaning has changed over rewriting a slide wholesale.

## Visual language and accessibility

The current deck's actual palette and components take precedence over any generic redesign guidance below. Sample colors, fonts, border weights, icon treatment, and recurring layout geometry from the existing deck and extend them. Introduce a new visual convention only where the existing system has no suitable equivalent.

Retain the deck's subdued dark/light neutral palette. For any genuinely new categorical accents, use a color-blind-safe set with high luminance separation, roughly:

- deep blue for observed / carrier facts;
- amber for inferred authoring grammar;
- blue-green for derived machine behavior;
- muted purple for gauge freedom;
- neutral gray for quarantined or non-causal alternatives.

Never use red-versus-green as a semantic pair. Use solid versus outline, filled versus hollow, labels, or line style as redundant encodings.

For cubes:

- use orthographic/isometric wireframes rather than perspective-heavy glossy 3D;
- keep front/back/depth labels explicit;
- label axes directly (`q`, `d`, `j`, or gauge bits);
- when showing selected cells, add small glyphs or numbers in addition to color;
- avoid more than 2–4 cubes on one slide unless they are tiny small multiples.

---

# Slide-by-slide plan

The recommendation below preserves the existing slide IDs where possible. New inserts use letter suffixes so implementation does not require renumbering the entire deck.

| Existing slide | Decision | Planned change | Neighbor / transition notes |
|---|---|---|---|
| Title | KEEP | No substantive change. Optionally update subtitle to "A closed-corpus mechanical crack, with the semantic endpoint still open." only if the closing slides adopt the same wording. | Must still feel like an invitation into a mystery rather than a solved-paper title. |
| 01 • THE MYSTERY | KEEP | Keep as-is. | Still the cleanest cold open. |
| 02 • COMMUNITY FOUNDATION | KEEP | Keep as-is. | No need to burden the opening with modern caveats. |
| 03 • PUBLIC RECORD | LIGHT EDIT | Keep the community-archaeology story. Replace any implication that fresh owner finds are the critical path with a small note that the current investigation proceeds closed-corpus. | Makes slide 04's "missing-data problem" explicitly historical. |
| 04 • THE OLD BOTTLENECK | LIGHT EDIT | Preserve the old-question/new-question pivot. Add one final line: "That question is now answerable without assuming another sticker will ever surface." | Leads naturally into the first-break divider. |
| Divider: The first break | KEEP | Keep. | No change. |
| 05 • CORPUS | KEEP | Keep 82 / 65 / 108 and 60.2%. These remain current. | None. |
| 06 • NORMALIZATION | KEEP | Keep. | None. |
| 06A • HUMAN CLUES | KEEP | Keep. It does useful narrative work and inoculates later formalism against looking purely machine-invented. | None. |
| 07 • BREAKTHROUGH | KEEP | Keep H108 evidence. | None. |
| 07A • REPEATS YOU CAN POINT TO | KEEP | Keep concrete repeats. | None. |
| 08 • H108 | TARGETED VISUAL ENHANCEMENT | Preserve the slide's existing composition and typography, but extend its "three views" treatment with a translation diagram: 12×9 strip -> four 27-cell quarters -> **four 3×3×3 cubes**. Use the deck's existing line/label language for the wireframes. Show one quarter enlarged with axes `d × row × column` / `d × j`, and annotate that the cube is a coordinate system, not semantic proof. | This is the first major "people love cubes" opportunity and is mathematically exact. It should feel like one more view added to the existing slide, not a visual reboot. Slide 09 immediately supplies the epistemic brake. |
| 09 • EPISTEMIC GUARDRAIL | KEEP | Keep. Slightly update the ladder so "mechanistic" now includes "raw reconstruction + gauge quotient", while "semantic" remains open. | Important immediately after the cube visual so dimensional elegance is not oversold. |
| 09A • LETTER-LIKE GHOSTS | KEEP / TRIM | Keep the human-recognition history but reduce copy by ~15–20%. Retain MIL / MIX / MISS / XML as cautionary artifacts. | The next divider can then decisively pivot away from glyph-reading. |
| Divider: The geometry starts behaving like machinery | KEEP | Keep. | None. |
| 10 • PRIMARY LATTICE | MODIFY | Keep the compact lattice, but change the footer from "tiny family of legal states" to "preferred exact-POS3 physical representative." Add a small gauge footnote: the transition machine cannot distinguish two unobserved pulse relocations found later. Do not explain the full gauge here. | Sets up new 10A instead of overloading this slide. |
| **10A • HOW MUCH THE RAW MARKS ALREADY FORCE** | **NEW** | Show 9 small primary frames. Mark 8/9 frame polarities as directly forced under POS3, and show 25/27 trits forced once the derived staircase is applied. Add the 34-residue minimum verification witness as a compact "34 of 54 observed primary residues are sufficient" callout. Mention that Experiment 293 provides a weaker composite parent that still collapses to the same 14 exact-POS3 states. | Insert between 10 and 11. Adjust slide 11's opening from "One quarter behaves..." to "The other quarter supplies the selector that acts on this lattice." |
| 11 • Q4 SELECTOR | SUBSTANTIAL REWRITE | Present Q4 first as an **abstract ternary depth selector** `S(j)`, physically represented by exceptional depth in a slash/dot stack. Use one 3-cell vertical stack plus a tiny 3×3 artwork map. State that the all-slash form is the preferred printed gauge, not a functional axiom. | Avoid saying "one slash in every stack" as though global polarity were required by the transition. |
| **11A • THE Q4 GAUGE CUBE** | **NEW** | Literal **3-bit cube** for the Experiment-260 Q4 polarity gauge bits A, C, F+I. Label cube vertices by polarity masks. Highlight the `F+I=0` face containing `0, A, C, A+C` as the route-capable family left by Experiment 292. Show that A/C are unobserved physical gauges. Show the all-slash origin with a subtle "preferred authoring representative" halo, supported by local homogeneity + 3:2:1 whole-master balance. | Excellent exact cube use. This slide replaces several paragraphs of caveat with a visual. Slide 12 then explains the shared positional primitive. |
| 12 • A SECOND CONSTRAINT | REPLACE CONTENT / RETITLE | Retitle to **ONE POSITIONAL PRIMITIVE, TWO JOBS**. Side-by-side: primary column POS3 and Q4 depth-stack POS3. Both encode a ternary value as the position of an exceptional member. Retain the historical "one dash per column" observation as a small inset, not the headline. | This makes the shared code concept explicit before control logic. |
| 13 • THE CONTROL RELATION | KEEP / LIGHT EDIT | Keep the request/grant table. Add one small caption: "This relation now emerges from raw-compatible closure; it is not supplied as a lookup table." | Prepares the audience for stronger derivation slides later. |
| 14 • REINDEX | MODIFY | Keep `q=2-p`, but change the framing from "simplest wiring" to "the route orientation eventually becomes uniquely recoverable." Avoid making 210 sound like a premise. | Slide 15 supplies the stronger derivation. |
| 15 • ROUTE TABLE | MAJOR EDIT | Keep `102 / 012 / 120` and S3 note. Add a small 27-candidate mini-grid: one q-indexed word chosen from each of 3 functional families gives 27 possibilities; requiring three distinct permutations leaves exactly one route shell. | This integrates Experiment 278 and makes the route less "chosen because elegant." |
| 16 • ENDPOINT | MODIFY | Preserve the derangement / loopless characterization, but explicitly call it a certificate of the terminal rather than the reason the machine is allowed to terminate there. | Follow with new 16B. |
| **16B • FIXED POINT, NOT A PHASE** | **NEW** | Visualize the broader nonlinear recursion result: two branches `100 -> 100 -> 100`; two siblings `102 -> 100 -> 102 -> ...`. Use two simple state strips, not a dense graph. Headline: "100 is the stable terminal; 102 is one phase of a two-cycle." | Makes Experiments 279/284 legible and strengthens the endpoint before the human direct construction. |
| 16A • THE DIAGONAL KEPT COMING BACK | KEEP | Keep. | If 16B is inserted, order should be 16, 16B, 16A only if narrative prefers formal proof before human payoff; otherwise use 16, 16A, 16B. Preferred order: 16, 16A, 16B, 17. |
| 17 • DIRECT CONSTRUCTION | KEEP / LIGHT EDIT | Keep the 1/5/9 + Q4 short path. Add "This remains the shortest visual endpoint proof, even though deeper searches now justify why these operations are allowed." | Good bridge to canonicalization. |
| 18 • CANONICALIZATION | KEEP / LIGHT EDIT | Keep the aliasing explanation. Add one label distinguishing **state canonicalization** from **physical completion gauge** so "different physical states" cannot be mistaken for the later gauge-bit issue. | Prepares slide 19. |
| 19 • STATE COMPRESSION | REWORK | Keep the staged quotient idea, but show two parallel lanes: **functional information** (`14 -> 7 -> 5 -> 3 -> 1`) and **physical completion choice** (preferred 14 masters vs gauge-expanded equivalent masters). Explicitly state that gauge multiplicity does not add computational states. | This is where 56/224/336 counts can be introduced carefully, if at all. Use only the exact-transducer 16 physical settings / 224 masters in main deck; put broader 336 nearby family in appendix/workbook. |
| **19B • FOUR BITS, FOURTEEN STATES** | **NEW** | Use **two ordinary cubes** side by side, one for `G=0` and one for `G=1`. Cube axes are `X,Y,Z`. In each cube, show all 8 Boolean vertices but hollow/cross out `011`; the remaining 7 + 7 = 14 physical states. This is an exact and intuitive visualization of the Horn constraint `Y AND Z -> X`. | Another high-value cube slide. Place after state compression and before thermometer/observer material. |
| 19A • THREE HUMAN-LEGIBLE STATES | KEEP | Keep the 100→110→111 thermometer code, but make clear it is a recoding of route state, not another independent discovery. | Works after 19B. |
| 20 • TWO INTERFACES | MODIFY | Keep causal-path vs observer distinction. Replace any old "14 distinct readouts survive" wording with language aligned to current observer theorem: the frozen observer recovers the four-bit hidden state while transition logic quotients it. | End of mechanism section. |
| Divider: Is this just an ornate story? | KEEP | Keep. | Stronger than ever because the next section now has better hostile tests. |
| 21 • HOSTILE COMPARISON | LIGHT EDIT | Keep the 746,496 older nearby-machine cage, but label it explicitly as an early bounded sibling-family stress test. Add a compact modern adversarial callout from Experiments 296–297: local recursion exceptions can preserve `100`, the exact 14 masters, or even 20 states, but the reversible route layer rejects those stronger-looking siblings; canonical uniquely maximizes retention among route-capable zero/one/two-cell first-pass variants. | This updates the hostile-test story without adding another experiment-specific slide. Do not let the older MDL cage remain the strongest-looking uniqueness evidence. |
| 22 • COMPRESSION | LIGHT EDIT | Keep the 24 / 746,496 / 1:31,104 / ~14.9 bits result as MDL bookkeeping. Add a footer: "Useful, but later raw-space reconstruction is a stronger argument." | Leads to new 22A. |
| **22A • START WITH RAW CONSTRAINTS, NOT THE SOLVED MACHINE** | **NEW** | Large funnel / Sankey-style count reduction: `6 primary payloads × 36 Q4 selectors = 216` -> first-pass POS3 -> `20` -> selector reuse -> `14` -> every survivor terminal `100`. Include three checkmarks: Boolean implementation, native `x/y/p/g` implementation, raw enumerator all emit the exact same 14 complete masters. | One of the most important new slides. This should visually supersede the older MDL result without deleting it. |
| **22B • RECOVER Q4 WITHOUT FEEDING IT Q4** | **NEW** | Summarize Experiments 294/295. Start from `3^9 = 19,683` abstract ternary selector fields × `C(9,3)=84` possible 3-position control cores. No observed Q4 cell values, expected core, route words, state count, or target terminal supplied. Recursive closure + reversible-route criterion recovers the physical A/D/G core, real scaffold modulo C gauge, 7-state compatibility relation, route shell, terminal 100. Then a small second panel: held-out Q4 marks plus either equal-row-weight or cyclic codebook symmetry recover the one-slash physical code `/.., ./. , ../`. | This is the modern anti-circularity showpiece. Could use a small **3×3×3 cube** inset to depict a ternary selector/codebook, but keep the main visual as a search funnel so the cube does not obscure the count argument. |
| 23 • A CLEANER RARITY RESULT | KEEP / LIGHT EDIT | Keep selector-universe 19,683 / 3,375 / 8 / 1 result, but frame it as a separate direct-selector fact, not as the global uniqueness proof. | It now works as corroboration after 22A/22B. |
| 24 • EVIDENCE ANATOMY | KEEP | Keep 12 load-bearing / 53 sentries. | None. |
| 25 • MUTATION TEST | KEEP | Keep. | None. |
| 26 • HUMAN-SCALE SOLVE | MODIFY | Update beyond "20 logical cells." Retain the 20-cell short endpoint witness and 43-cell staged witness, but add a third line: 34-residue minimum raw-primary verification witness. Make clear these answer different questions. | Sets up 26A. |
| **26A • A PLAUSIBLE PAPER-AND-PENCIL PATH** | **NEW** | Show a 6–8 step horizontal path: H108 -> 12 A–I rows -> 9+3 alphabet split -> physical-column POS3 -> Q4 depth selector -> try four literal coordinate copies -> only `(q,S)` is selector-sensitive and q-preserving -> reuse S on remaining q -> `20 -> 14 -> 100`. Add a small sidebar: Experiment 293 shows exact source POS3 can also emerge from a weaker composite grammar, but that route is less human-simple. | This incorporates Experiments 248, 259–265, 290–291, 293 without turning them into separate slides. |
| 27 • DIFFERENT KINDS OF FUTURE STICKER | REWRITE | Retitle **WHAT A NEW STICKER WOULD STILL TELL US**. Remove the obsolete claim that residues 82 and 93 are universal falsifiers across every surviving machine: A/C are now known physical-polarity gauges. Distinguish observations that resolve hidden route/state variables from observations that only choose a printed gauge representative. Emphasize that no future sticker is required for the mechanical crack. | This is a required correctness change after PR #32. |
| 27A • A USEFUL SMELL TEST | KEEP | Keep. It remains an excellent communication heuristic. | None. |
| Divider: What survived, and what did not | KEEP | Keep. | None. |
| 28 • FALSE LEADS | KEEP | Keep. If space is needed, shorten one or two rows but retain semantic quarantines. | None. |
| 29 • WHAT I THINK I KNOW NOW | MAJOR REWRITE | New headline: **THE CLOSED-CORPUS MECHANICAL CRACK IS SUBSTANTIALLY COMPLETE**. Strong takeaways: H108 carrier; shared positional primitive; raw reconstruction to 14 states; abstract Q4 and route shell recovered under bounded broad searches; `100` fixed terminal; observer reads the hidden state. Separate "preferred physical authoring choices" (exact POS3 gauge origin, all-slash Q4 gauge origin) from "functional machine." | This is the synthesis slide the current deck is missing. |
| 30 • WHAT IT MIGHT MEAN | REPLACE | Retitle **WHAT 100 IS, AND WHAT IT ISN'T**. Left: mechanically established properties (frame 9, normalized 100, raw ---//////, invariant fixed terminal, derangement certificate). Right: not established (plaintext, URL, lore phrase, known ARG consumer). One final line: an external clue could still tell us how to consume the terminal. | This closes the internal semantic branch without claiming the ARG itself is solved. |
| 31 • WHERE THE MYSTERY STANDS | REWRITE | Progress ladder should now show **mechanical decode / transducer** essentially complete, with **external semantic consumer** as a separate unresolved branch rather than one more step on the same ladder. | Avoid "decoded" as a binary single axis. |
| 32 • WHY THIS MATTERS | MODIFY | New central contrast: "The community already had enough data to recover the machine." New stickers are validation/gauge resolution; the critical path is no longer collection. | Stronger ending than the old "may already have enough." |
| APPENDIX • SOURCES & SCOPE | MAJOR UPDATE | Replace stale "Experiments 140–150 + Engines A–C" line. Cite repo state through 291 plus the merged/latest applicable 292–297 results at implementation time. Add `machine-spec.json`, theorem graph, proof-pack, raw enumerator, and three-way implementation equivalence as supporting sources. State clearly which claims come from unmerged PRs if the deck is built before merge. | Last implementation step should re-check this slide against actual merged state. |

## Deck length, density, and pacing

There is **no target slide count**.

The seven proposed inserts below are content recommendations, not a quota:

- 10A raw-primary forcing
- 11A Q4 gauge cube
- 16B fixed terminal vs 2-cycle
- 19B fourteen states as twin cubes
- 22A raw 216→20→14 reconstruction
- 22B broad Q4 inverse recovery
- 26A plausible human path

During implementation, preserve the existing deck's standard of density and pacing. If a proposed insert can be absorbed cleanly into an adjacent slide **without making that slide visibly denser, smaller-typed, or more technical than its neighbors**, do so. If an existing slide now needs two distinct visual claims to stay correct, split it rather than compress it. Conversely, do not add a slide merely because an experiment exists.

The deck may grow or shrink as needed. Slide count is subordinate to continuity, legibility, and the existing deck's tone.

Slides 22A and 22B contain central new evidence and should remain prominent somewhere in the main narrative even if their exact boundaries change.

## Cube inventory

Use cubes in exactly these places unless later layout testing suggests otherwise:

1. **Slide 08:** four 3×3×3 quarter cubes. This is literal H108 geometry.
2. **Slide 11A:** Q4 three-bit polarity **gauge cube**. Experiment 292 naturally selects one face.
3. **Slide 19B:** two Boolean state cubes for G=0/G=1, each missing forbidden vertex 011.
4. Optional small inset on **22B:** one 3×3×3 ternary codebook/selector cube if it helps explain exceptional depth. Do not force it if the search funnel is clearer.

Avoid turning the 4-bit state into a fake 4D cube projection. Two ordinary 3D cubes are cleaner and exact.

---

# Spreadsheet / evidence-pack redesign

## Overall decision

Maintain **one spreadsheet artifact only: XLSX**.

The refreshed `INSIDE_Sticker_Mystery_Verification_Pack.xlsx` becomes the single supporting evidence workbook for both human browsing and structured evidence records. It should absorb all useful rows and fields from the old supplementary CSV into an `EVIDENCE RECORDS` sheet and extend them through the current research frontier.

The existing `INSIDE_Sticker_Mystery_Supplementary_Evidence.csv` should remain in the archive unchanged as historical provenance, but it should **not** be updated, presented as a parallel current deliverable, or treated as a second canonical spreadsheet.

The workbook should be generated from canonical repo data where practical rather than manually diverging. If a script ever needs CSV as an interchange format, it may derive a temporary CSV from the workbook/repo data during a build or analysis step, but no second maintained spreadsheet artifact should result.

## Workbook visual system

Use a restrained, slide-compatible system:

- off-white / very light gray sheet background;
- dark charcoal text;
- dark navy title bars;
- pale blue for observed facts;
- pale amber for supplied/model-class assumptions;
- pale blue-green for derived results;
- pale purple for gauge / representation freedom;
- neutral gray for historical/quarantined material;
- no saturated traffic-light red/green;
- status also encoded with text and/or symbols, never color alone.

Formatting:

- freeze panes on every tab with tables;
- enable filters on every data table;
- wrap long text;
- use consistent row heights;
- use thin neutral borders for data grids and heavier top borders for section starts;
- use monospace font only for symbols, payloads, formulas, and residue sets;
- use large title + one-sentence purpose at top of each sheet;
- keep raw IDs and experiment numbers visible so the workbook remains auditable.

## Recommended workbook tabs

### 1. START HERE

Purpose: a calm landing page.

Contents:

- title and last-updated experiment;
- four headline counts:
  - 82 physical stickers;
  - 65 occupied H108 residues;
  - 14 functional hidden states;
  - terminal 100;
- one compact architecture ribbon:
  `H108 -> POS3 -> selector -> 216 -> 20 -> 14 -> 3 -> 1`;
- evidence-status legend;
- "what is still unknown" box;
- hyperlinks to the key sheets.

Optional visual: a small wireframe 3×3×3 cube to echo the deck without turning Excel into a poster.

### 2. CLAIMS MAP

Replace the current challenge-question page with a richer table:

Columns:

- Claim ID
- Public claim
- Status
- Evidence class
- Direct support
- Key experiment(s)
- Reproduction script
- Main caveat
- Deck slide(s)
- Confidence / scope note

Use grouped sections:

- Carrier
- Primary
- Q4
- Recursion
- Routing
- Terminal
- Observer
- Gauge
- Semantic boundary

This becomes the fastest skeptical-reader audit surface.

### 3. EVIDENCE RECORDS

Absorb the full legacy supplementary-CSV schema into this workbook and extend it through the current experiment frontier. This sheet replaces the old CSV as the maintained flat evidence table.

Keep the existing columns but add:

- `claim_id`
- `module`
- `evidence_class`
- `gauge_scope`
- `supersedes_or_superseded_by`
- `repo_artifact`
- `deck_slide`

Use an Excel table with filters and alternating neutral row shading.

### 4. EXPERIMENT FRONTIER

Human-readable summary of Experiments 195 onward, especially 241 through the current implementation frontier.

Columns:

- Experiment
- Question
- Parent family
- What was supplied
- Search size
- Survivors
- Result
- What premise was weakened / closed
- Status
- Script

Highlight superseded Experiment 286 with strike-through and gray fill; point to 287.

### 5. RAW RECONSTRUCTION

Visual audit of Experiments 250–253:

- 6 primary payloads
- 36 preferred Q4 selectors
- 216 raw candidate machines
- 20 first-pass survivors
- 14 second-pass survivors
- 100 invariant terminal

Add compact tables for the 14 states and first-pass families.

A funnel chart is acceptable if visually restrained; otherwise use large count boxes with arrows.

### 6. PRIMARY STRUCTURE

Combine:

- compact lattice;
- 8/9 forced frame polarities;
- 25/27 forced trits;
- 34-residue minimum witness;
- rail-orientation audit;
- holdout result;
- primary two-bit physical gauge;
- transport costs 172/196/196/220;
- Experiment 293 weaker composite recovery.

Include a 2×2 gauge matrix for the two physical pulse-swap bits.

### 7. Q4 SELECTOR & GAUGES

This should be one of the most visual sheets.

Include:

- 3×3 A–I layout;
- selector-depth field;
- Q4 3-bit polarity gauge cube represented in 2D as cube vertices/edges;
- Experiment 292 surviving route-capable face `0/A/C/A+C`;
- all-slash physical-selection evidence from Experiments 270/281;
- Experiment 294 inverse recovery;
- Experiment 295 physical-codebook reconstruction;
- explicit note that A/C remain unobserved printed gauges absent the shared-codebook authoring premise.

### 8. ROUTING & TERMINAL

Include:

- request/grant table;
- q=2-p;
- route rows 102 / 012 / 120;
- 27-choice route-shell audit;
- fixed-point vs 102↔100 period-2 behavior;
- direct selector-universe counts;
- Experiments 296–297 as a hostile local-operation test: terminal agreement and raw-state retention alone admit attractive siblings, while route capability isolates canonical as the highest-retention member of the tested local-defect family;
- terminal representations: frame 9 / 100 / ---//////.

### 9. HIDDEN STATE & OBSERVER

Show:

- X,Y,Z,G definition;
- legality clause `YZ -> X`;
- 14 states;
- two 3D cube diagrams rendered as simple cell/vertex tables if actual 3D drawing in Excel becomes awkward;
- observer minima;
- latent residue register.

This is the spreadsheet counterpart of slide 19B.

### 10. WITNESSES & ROBUSTNESS

Bring together:

- 20-cell short witness;
- 43-cell staged witness;
- 34-residue raw-primary witness;
- single-deletion sensitivity;
- single- and double-mutation results;
- load-bearing vs sentry classification.

### 11. HUMAN SOLVE

A prose-light staged table:

- what the solver sees;
- what inference becomes available;
- what remains free;
- what test removes the freedom;
- hindsight classification.

Include Experiments 290–291 and the alternate Experiment-293 route as a side branch.

### 12. PREDICTIONS / FUTURE OBSERVATIONS

Replace the old flat "best missing sticker" story with categories:

- hidden-state discriminator;
- printed-gauge discriminator;
- architecture falsifier;
- historical frozen prediction.

Any prediction invalidated or weakened by gauge broadening must be clearly marked, not silently retained.

### 13. BOUNDARIES & QUARANTINE

Collect:

- H108 semantic caveat;
- coordinate-semantic caveat;
- MDL-not-probability caveat;
- gauge-versus-state caveat;
- no standard ECC claim;
- semantic endpoint caveat;
- XML/MIX/MISS/etc quarantine.

### 14. SOURCES & REPRODUCTION

Map each major result to:

- repo script;
- data file;
- canonical doc;
- PR / experiment;
- deck slide;
- workbook sheet.

This should make the evidence pack self-navigating.

## Spreadsheet charts / visualizations

Use only charts that clarify a concrete relationship:

- raw reconstruction count funnel;
- 4-setting primary gauge transport comparison;
- route fixed-point counts;
- mutation survival counts;
- historical witness availability over time;
- experiment frontier by module, if useful.

Do not add decorative pie charts.

## Legacy CSV retirement

Do not produce an updated CSV deliverable.

During workbook construction, ingest the useful legacy CSV content into the `EVIDENCE RECORDS` sheet, preserve source/provenance columns, then extend and clean the records there. Required content work includes:

- extend experiment coverage from 194 through the implementation frontier;
- add explicit gauge rows;
- revise Q4 prospective rows affected by A/C gauge freedom;
- add raw reconstruction and independent-implementation rows;
- add route-shell derivation and recursion fixed-point rows;
- add primary and Q4 physical-gauge rows;
- add Experiment 293 weaker-source-POS3 rows if merged;
- add Experiments 292/294/295 if merged;
- add Experiments 296–297 if merged, emphasizing that terminal agreement alone is weak and route structure remains discriminating;
- mark Experiment 286 superseded by 287;
- add `claim_id`, `module`, and `repo_artifact` columns.

Once incorporated, the old CSV remains only an archived snapshot of an earlier evidence pack.

---

# Implementation order

1. Reconcile/merge or explicitly pin the current research frontier. Before editing artifacts, check whether PR #31, #32, and #34 have merged or advanced.
2. Rebuild the XLSX as the **single maintained evidence spreadsheet**, importing the old CSV rows into `EVIDENCE RECORDS` and extending them from canonical repo state.
3. Validate the workbook's flat evidence sheet against the relevant repo data/scripts so the workbook does not become a manually forked truth source.
4. Update the deck narrative and slide order from the verified evidence pack, not from memory.
5. Render the deck to images/PDF and inspect every slide for overflow, contrast, and visual continuity.
6. Check all workbook sheets for clipped text, inaccessible color reliance, hidden columns, broken filters, and frozen-pane behavior.
7. Cross-check every headline number appearing in the deck against workbook cells or repo scripts.
8. Update appendix/source slide last.
9. Save versioned outputs and, if appropriate, overwrite the Drive copies only after visual QA.

## Freshness gate

At implementation time, repeat these checks:

- current `main` head;
- all open PRs touching `docs/current-state.md`, `docs/theorem-graph.md`, `data/machine-spec.json`, or new audit scripts;
- latest experiment number;
- whether PR #31 / Experiment 293 is merged;
- whether PR #32's 292/294/295 work is merged or has advanced;
- whether PR #34's 296/297 local-recursion-defect work is merged or has advanced;
- whether any new result changes:
  - functional state count;
  - physical gauge count;
  - Q4 route-capable gauge orbit;
  - terminal fixed-point claim;
  - raw reconstruction counts;
  - semantic stopping point.

If the frontier changes only by another bounded audit that reproduces the same model, update the verification pack and appendix but do not automatically add another deck slide.

---

# Plan review / self-audit

After drafting the slide plan, the following improvements were made deliberately:

1. **Do not just append 99 experiments.** The new deck is organized around changed epistemic status and stronger proof paths.
2. **Move the strongest new anti-circularity evidence into the main narrative.** Raw `216 -> 20 -> 14` and Q4-from-abstract-selector recovery deserve new slides; they should not be buried in appendix tables.
3. **Correct obsolete Q4 wording.** The deck must no longer imply globally shared slash polarity is functionally required.
4. **Correct future-sticker claims.** A/C residues can now distinguish printed gauge without falsifying the route machine.
5. **Separate state from gauge.** This prevents the new 56/224/336 master counts from confusing the audience about the 14-state machine.
6. **Use cubes where they carry exact meaning.** H108 quarter geometry, Q4 gauge cube, and twin hidden-state cubes are all real structures, not ornamental 3D.
7. **Keep the human story.** The direct diagonal construction, visual hunches, and failed letter readings remain because they explain discovery rather than merely proving correctness.
8. **Close the semantic branch more firmly.** The updated ending should say the machine is mechanically cracked while an external consumer remains unknown.
9. **Make the workbook the technical companion.** This lets the deck stay elegant while still exposing the modern theorem/ablation/gauge machinery to skeptical readers.
10. **One spreadsheet, one truth surface.** The XLSX should contain the flat evidence table as one sheet rather than maintaining a parallel updated CSV. The legacy CSV remains archive-only.

## Current repo-change review at plan completion

The plan was initially framed against `main` through Experiment 291 plus PRs 31–32. During review, PR #32 was found to have advanced beyond its title:

- Experiment 292 removes globally shared Q4 polarity as a functional premise;
- Experiment 294 searches all 19,683 abstract ternary selector fields and all 84 possible 3-cell control-core locations, recovering the functional Q4 structure and terminal under closure + reversible-route criteria without supplying the Q4 observations/core/terminal as targets;
- Experiment 295 reconstructs the exact one-slash physical Q4 codebook downstream from held-out Q4 marks under weaker shared-codebook symmetry families.

Those results materially improved the plan and are now explicitly represented in slides 11A and 22B and in the Q4 workbook sheet.

PR #31's Experiment 293 remains represented as a weaker composite source-POS3 recovery, but not promoted to the primary public discovery path because its five authoring regularities are less human-simple than direct POS3 recognition.

A second freshness pass then found PR #34 containing Experiments 296–297. These show that tiny cell-local recursion exceptions can preserve terminal `100`, preserve the exact 14 masters, or even retain 20 states, while destroying the reversible route layer. Across the 163 zero/one/two-cell first-pass configurations tested in Experiment 297, only canonical plus two damaged seven-state C variants remain route-capable, and canonical uniquely maximizes retained raw states among them. This strengthens the route criterion as an adversarial discriminator but **does not warrant another main-deck slide**. Incorporate it as a concise callout on slide 21 or 22A and in the workbook's Experiment Frontier / Routing & Terminal / Robustness sheets.

Final sanity conclusions:

- preserve the existing deck's design elements by default;
- preserve its density, level of detail, and tone rather than optimizing for a particular slide count;
- add visual complexity only where it carries new information;
- prefer adapting an existing component to inventing a new visual language;
- maintain one current spreadsheet artifact, the XLSX verification workbook;
- keep research-frontier churn mostly in the workbook/appendix unless it changes the public explanatory story.

Before artifact editing begins, re-run the freshness gate above.

---

## Implementation checkpoint — 2026-09-29

The plan has now been implemented on this branch.

Deliverables:

- `deliverables/INSIDE_Collector_Edition_Sticker_Mystery_v2.pptx`
- `deliverables/INSIDE_Sticker_Mystery_Verification_Pack_v2.xlsx`

Implementation notes:

- the deck grew from 44 to 51 slides, preserving the existing visual system while adding the planned raw-primary, Q4 gauge, terminal-dynamics, hidden-state, raw-reconstruction, Q4-inverse, and paper-and-pencil-path material;
- the workbook is now the single maintained spreadsheet supplement and contains 14 sheets, including START HERE, CLAIMS MAP, EVIDENCE RECORDS, EXPERIMENT FRONTIER, RAW RECONSTRUCTION, PRIMARY STRUCTURE, Q4 SELECTOR & GAUGES, ROUTING & TERMINAL, HIDDEN STATE, WITNESSES & ROBUSTNESS, HUMAN SOLVE, PREDICTIONS, BOUNDARIES, and SOURCES & REPRO;
- the legacy supplementary CSV remains archive-only; its useful rows were absorbed into EVIDENCE RECORDS rather than maintained as a second current spreadsheet;
- live PR results are explicitly labelled as provisional in the deck/workbook where relevant: PR #31 / Experiment 293, PR #32 / Experiments 292, 294–295, and PR #34 / Experiments 296–298;
- the updated deck was rendered and visually inspected after generation; the workbook received targeted table/error inspection plus rendered checks of the landing, Q4, claims/frontier surfaces;
- the temporary transfer workflow used while committing binary deliverables was removed after the artifacts landed.
