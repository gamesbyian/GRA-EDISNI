# Archival / manufacturing evidence lane

_Status: working memo, independent of the active recursion branch._

## Purpose

This lane asks a different question from the closed-corpus mechanical work:

> Can surviving production history identify who authored, generated, printed, applied, or fulfilled the numbered symbol/image stickers?

The goal is independent evidence about the sticker mechanism. Generic facts about collector's-edition manufacturing do not count.

## Publicly established production chronology

### 1. The Collector's Edition was announced before its contents were revealed

On 2018-03-06, iam8bit announced the edition as a collaboration among iam8bit, Playdead, and RealDoll. Contemporary coverage records:

- preorder opening: 2018-03-08;
- timed preorder cutoff: 2018-06-08;
- intended worldwide shipping;
- the contents deliberately withheld;
- expected delivery originally around Q1 2019.

Sources:

- PlayStation LifeStyle, 2018-03-06: https://www.playstationlifestyle.net/2018/03/06/iam8bit-announces-inside-collectors-edition/
- PCGamesN, 2018-03-06: https://www.pcgamesn.com/inside/inside-collectors-edition-realdoll-iam8bit
- TechSpot, contemporary coverage: https://www.techspot.com/news/73601-inside-375-collector-edition-features-item-sex-doll.html

This matters because the preorder window ended roughly eighteen months before fulfillment. Any sticker-generation artifact could therefore plausibly live in either the early design period or the much later production/fulfillment period.

### 2. Production quantity appears to have been demand-determined, not a fixed public edition size

Contemporary owner discussion records that the edition was a timed release: the number produced was understood to be whatever quantity was ordered before the June 8 cutoff. The exact total was not publicly announced.

A later iam8bit waitlist email, reproduced publicly in April 2020, says the edition had sold out "nearly two years ago" and that a "super duper limited quantity" had become available again.

Sources:

- Reddit owner thread, 2019-11-27 onward: https://www.reddit.com/r/PlaydeadsInside/comments/e2m8ty/inside_collectors_edition_update/
- Cheap Ass Gamer reproduction of iam8bit waitlist email, 2020-04: https://www.cheapassgamer.com/threads/official-collectors-edition-compilation-xi-2020.371308/page-17

Implication: sticker serials are unlikely to be ordinary printed edition numbers such as "123/500". The known serials can instead belong to a larger authored address/code space whose population need not equal the number of CEs sold.

### 3. RealDoll's documented role is specifically the silicone Huddle

iam8bit's current product page describes the CE as an iam8bit / Playdead / RealDoll collaboration and specifically attributes the silicone Huddle production to RealDoll.

In a 2022 interview, iam8bit founders Jon M. Gibson and Amanda White describe the genesis in unusually concrete terms. The silicone-object idea began at iam8bit; contacts in the fetish/leather world referred them onward; iam8bit then worked with a San Diego manufacturer capable of controlling silicone skin tone, density, and movement. Gibson says iam8bit could visit the facilities and tracked that fabrication process.

Sources:

- iam8bit product page: https://www.iam8bit.com/products/inside-collector-s-edition
- TheSixthAxis interview with Jon M. Gibson and Amanda White, 2022-06-19: https://www.thesixthaxis.com/2022/06/19/interview-iam8bit-founders-on-publishing-day-of-the-devs-and-that-inside-collectors-edition/
- Kotaku reveal, 2019-12-12: https://kotaku.com/the-contents-of-the-secret-375-inside-collector-s-edit-1840398301

**Important negative inference:** nothing in the public descriptions found so far attributes the sticker, serial numbering, printed art, box assembly, or fulfillment logic to RealDoll. RealDoll is therefore a lower-priority sticker-code lead than iam8bit and Playdead unless packaging evidence connects the sticker physically to RealDoll's production step.

### 4. iam8bit and Playdead describe the project as unusually close and collaborative

The current iam8bit product description says Playdead and iam8bit collaborated "very closely" and "very quietly." In the 2022 founders interview, Gibson again describes the project as highly collaborative with Playdead.

The public evidence therefore does **not** support treating iam8bit as a mere distributor. Either Playdead or iam8bit, or both together, could plausibly have designed the sticker mechanism.

Source:

- https://www.iam8bit.com/products/inside-collector-s-edition
- https://www.thesixthaxis.com/2022/06/19/interview-iam8bit-founders-on-publishing-day-of-the-devs-and-that-inside-collectors-edition/

### 5. The ordinary PS4 physical edition is a useful control object

iam8bit separately sold an INSIDE PS4 physical edition, publicly described as a limited edition of 2,000 with a fold-out poster. Its product page explicitly says it arose alongside the quietly developed Collector's Edition.

Source:

- https://www.iam8bit.com/products/inside-ps4-physical-game

High-value comparison question:

> Which CE printed components are shared with the ordinary 2,000-copy physical edition, and which are CE-only?

If the game case, disc, or poster are identical while the coded sticker exists only on CE packaging, then the sticker was likely introduced in the CE-specific assembly/fulfillment chain rather than the ordinary game-manufacturing chain.

### 6. The coded sticker is documented as a seal on the wrapping

The community's long-running INSIDE-ARG documentation states that the stickers **seal the wrapping** of the Collector's Edition. That is a highly useful manufacturing fact because it places the coded label at or near the **final packaging stage**, downstream of the fabrication of individual contents.

Source:

- twinysam/INSIDE-ARG public documentation, Collector's Edition Stickers section: https://github.com/twinysam/INSIDE-ARG

Manufacturing implication:

- a sticker applied to exterior wrapping is unlikely to have been part of RealDoll's silicone fabrication process;
- the most plausible application points become final box assembly, shrink/wrap sealing, warehouse kitting, or fulfillment preparation;
- the sticker printer and the final pack-out operation may therefore have been the same vendor or tightly coupled vendors.

This gives a concrete provenance test: locate photos/video of an **unwrapped but not yet finally sealed** CE during production. If coded stickers are absent at that stage, the application point can be localized even further.

## Responsibility map

Current public evidence supports this working split:

| Function | Best-supported actor | Confidence | Sticker relevance |
|---|---|---:|---|
| Game/IP and ARG design context | Playdead | high | very high |
| Collector's-edition concept / production management | iam8bit + Playdead | high | very high |
| Silicone Huddle fabrication | RealDoll / San Diego fabrication operation | high | low unless sticker was applied there |
| PS4 physical-game publishing / sale | iam8bit | high | medium as control chain |
| Premium box / foam / printed inserts | unknown supplier(s) | unresolved | high |
| Coded-sticker artwork/master generation | unknown | unresolved | highest |
| Sticker printing | unknown | unresolved | highest |
| Sticker application / final wrapping or box assembly | unknown | unresolved | highest; community documentation places sticker on wrapping |
| Final CE fulfillment | likely iam8bit-managed, exact vendor unresolved | medium | high |

## Records worth finding

Priority records are now more specific than "find production information":

1. **Sticker source file**: Illustrator/PDF/InDesign/CSV/variable-data-print file.
2. **Sticker imposition sheet or print proof**: could reveal total serial range, repeated 108-cycle structure, ordering, or unused variants.
3. **Variable-data or numbering spreadsheet/script**: potentially the cleanest explanation of serial ↔ symbol ↔ image generation.
4. **Packaging BOM / vendor purchase order**: identifies the sticker printer and assembly vendor.
5. **Assembly instructions**: establishes when and where each sticker was applied.
6. **Fulfillment pick/pack worksheet**: could reveal whether sticker identity was tied to order number or randomized.
7. **Preproduction samples / approval photos**: may expose serials outside the public owner corpus.
8. **Ordinary-PS4-vs-CE component BOM**: isolates where the coded sticker entered the chain.

## People / organizations to prioritize

### Tier A: direct design / production memory

- **Amanda White, iam8bit co-founder** — described the CE's genesis firsthand in 2022.
- **Jon M. Gibson, iam8bit co-founder** — described iam8bit's facility visits, production tracking, and close Playdead collaboration firsthand.
- **Relevant Playdead producer / art / ARG personnel from 2018–2019** — exact individual still to identify from credits and public employment history.
- **iam8bit production/operations staff from 2018–2019** — especially whoever sourced premium packaging and managed final assembly.

Questions should be artifact-oriented rather than puzzle-oriented:

- Who supplied the small numbered symbol/image stickers?
- Were they generated from a spreadsheet/script or supplied as finished art?
- Who physically applied them?
- Does the source/imposition/proof still exist?
- Was the serial range equal to the CE production count, or was it drawn from a larger sequence?

### Tier B: vendors who may retain job records

- premium rigid-box / foam-inlay supplier;
- label/sticker printer;
- final assembly or fulfillment house;
- ordinary PS4 physical-edition printer/packager, as a control.

### Tier C: RealDoll

RealDoll remains worth one narrowly framed question:

> Did sealed Huddle units leave your facility already bearing any numbered sticker or coded paper label, or were those added after your production step?

A "no" would be useful because it removes an entire manufacturing branch.

## New discriminators enabled by archival evidence

These are concrete observations that would materially test the current machine rather than merely decorate its history:

- **Full print sheet order** could confirm H108 periodicity and whether serials were contiguous.
- **Unused labels** could expose residues not represented among sold CEs.
- **Source formula/script** could independently confirm the 108 carrier and 14-state family.
- **Quantity ordered from printer** could distinguish CE sales count from sticker code-space size.
- **Application order** could reveal whether sticker serials were deliberately assigned to units or effectively shuffled.
- **Printer variable-data setup** could show whether number, glyph, and image tile were generated jointly from a table.
- **CE-only component comparison** could localize authorship to Playdead/iam8bit rather than Sony's ordinary PS4 manufacturing chain.

## Current conclusion

The archival lane should now focus on **iam8bit/Playdead packaging and assembly records**, not on RealDoll's silicone fabrication process.

The most valuable single artifact is no longer "another sticker." It is a surviving **sticker production source**: an imposition sheet, variable-data file, spreadsheet, script, print proof, or vendor job record.

That artifact could independently answer questions the closed public corpus cannot: total generated serial range, whether the H108 cycle was intentional, how variants were selected, and whether the coded stickers were authored as one algorithmic production object.
