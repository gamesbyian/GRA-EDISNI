# INSIDE ARG Verification Handoff — extracted text

Source filename supplied in chat: `INSIDE-ARG-Verification-Handoff (1).pdf`

This repository copy preserves the Files-system parsed text of the supplied seven-page PDF because the GitHub connector used for this ingest cannot transfer the original binary attachment directly. Treat it as an archival transcription, not a byte-identical PDF. Original attachment SHA-256 recorded at ingest: `f69227b630a5d014f0fb9eed3c9d294d409192e9e877bd14bbc6263ddae0dfb7`.

---

<PARSED TEXT FOR PAGE: 1 / 7>
INSIDE ARG
Investigation status and verification handoff
As of September 27, 2026, 10:02 p.m. EDT. PDF prepared September 27, 2026.
Status: The collector's-edition sticker data support a 108-position repeating symbol sequence. No
plaintext has been established. It remains unresolved whether the repetition serves a puzzle, reflects
manufacturing, or both.
Immediate obstacle: The community's labeled 3 x 3 background-image assembly has not been retrieved.
Its verified A-I placement is required before the proposed jigsaw-based symbol pictures can be assembled
without guessing.
The user reports independent reproduction of several findings. The external model's complete code and
outputs have not been inspected in this investigation. No unknown symbol has been filled to manufacture a
phrase, and no completed ARG solution is claimed.
1. Evidence and conventions
Primary dataset: the community repository maintained by twinysam, pinned to commit:
4de72d7c2f21bd9eb4144fda51281c84cbcb90c4
The snapshot contains 82 numbered sticker observations. The photographs and transcriptions were
collected by community contributors; this investigation analyzes that work and does not claim priority over
undocumented Discord findings. [1, 2]
Symbol Sticker observations
Slash / 47
Dash - 28
Dot . 7
- Cycle positions are one-based: position = ((sticker_number - 1) mod 108) + 1.
- Background letter = "ABCDEFGHI"[(sticker_number - 1) mod 9].
- A question mark means unknown and is never silently filled.
- Repeated stickers occupying one cycle position count once when describing the cycle.
2. The 108-position cycle
An exhaustive period scan from 1 through 300 found four contradiction-free periods: 108, 197, 216 and
254. The shortest is 108. The alternatives have fewer overlapping observations; 216 is also a multiple of
108.
The 82 observations fill 65 positions, leaving 43 unknowns. Fifteen positions have multiple observations,
producing 19 agreeing pairwise comparisons. Those comparisons are not independent: there are 17
observations beyond the first observation in each filled position.
INSIDE ARG | Verification handoff | 27 September 2026 1 / 7
<PARSED TEXT FOR PAGE: 2 / 7>
The corrected cycle, displayed as three rows of 36, is:
?/--/?/?/-?-/-/?/--/-?--?-??//-/???/
-///?//-?///??-?-??/-?//??/?//??/---
?--/?////???./??..?.??./..??/??????/
Position 44 is a known dash, supplied by sticker 476. Its photograph was inspected. A previously
supplied transcription incorrectly showed a question mark there.
Two exploratory randomization tests each used 100,000 trials and seed 20260927:
Null model Trials with any contradiction-free
period at or below 108
Shuffle symbols globally, preserving counts 0 / 100,000
Shuffle symbols within each background-image group 0 / 100,000
These results reject those particular random-assignment models. They do not establish a zero probability of
chance, prove an encoded message, or exclude manufacturing structure.
Further checks: removing sticker 597 still leaves 108 as the shortest fitting period. A November 2025
snapshot with 77 observations also yields 108. Removing all seven dot observations still leaves 108
as the shortest fitting period.
3. Dot clustering
Dot sticker Cycle position Background
193 85 D
413 89 H
306 90 I
92 92 B
95 95 E
97 97 G
206 98 H
All seven observed dots occupy distinct positions within 85-98, a 14-position window. Under the specified
null, seven positions are selected uniformly without replacement from 108.
Event Probability Approximately
Inside a particular 14-position window fixed beforehand 1.23085 x 10^-7 1 in 8,124,481
Inside any nonwrapping 14-position window 5.90807 x 10^-6 1 in 169,260
Inside any circular 14-position window 6.64658 x 10^-6 1 in 150,453
The circular calculation is P = 108 x C(13,6) / C(108,7), where C(n,k) is the binomial coefficient. The
denominator is 27,883,218,168. The circular numerator is 185,328; the nonwrapping numerator is 164,736.
INSIDE ARG | Verification handoff | 27 September 2026 2 / 7
INSIDE ARG / CURRENT FINDINGS AND OPEN QUESTIONS
<PARSED TEXT FOR PAGE: 3 / 7>
The circular result is appropriate for a cluster noticed after inspecting the cycle. It does not account for
every possible investigation-level selection effect, and should not be multiplied by the earlier permutation
results as though statistically independent.
Correction: positions 85-108 are not all dots. Positions 86, 96, 101 and 108 are known slashes.
4. Symbol distribution by background image
Each image owns 12 cycle positions. These counts are for distinct positions, not all 82 sticker observations.
Image Dash Slash Dot Unknown
A 3 1 0 8
B 1 8 1 2
C 5 4 0 3
D 2 3 1 6
E 2 4 1 5
F 2 6 0 4
G 1 3 1 7
H 4 2 2 4
I 2 5 1 4
Total 22 36 7 43
B is slash-dominated: 8 of 10 known positions. C is mildly dash-heavy: five dashes versus four slashes. The
dot-background multiset is B, D, E, G, H, H, I. These are descriptive counts; no separate significance test for
this association has been established.
5. Comparison against known printer strings
Sources: the community printer document and Game Detectives transcription. [3, 4] Each complete listed
string was slid over all 108 circular starting positions. Known symbols had to agree literally; only question
marks acted as wildcards. No reversal, substitution, insertion or row rearrangement was allowed.
Set Entries tested Compatible placements
PC long, 32 characters 32 0
PC short 9 34
Xbox long, 36 characters 36, including one duplicate 0
Xbox short 12 0
Of the 34 short-PC placements, 32 do not wrap and ten lie entirely within unknown positions. For example,
PC string --/. fits positions 3-6, currently --/?.
Supported conclusion: no documented full-length PC or Xbox line fits literally anywhere in the partial
cycle.
INSIDE ARG | Verification handoff | 27 September 2026 3 / 7
INSIDE ARG / CURRENT FINDINGS AND OPEN QUESTIONS
<PARSED TEXT FOR PAGE: 4 / 7>
Not established: that the sticker sequence is definitively new material rather than a transformed or
rearranged use of earlier material. Short-string compatibility is not a confirmed occurrence.
6. Binary comparisons against LIFEDETECTED
The exact target is uppercase LIFEDETECTED, containing 12 letters. Seven-bit ASCII uses 84 bits; five-bit
A=1 through Z=26 uses 60 bits. Bits are most-significant first. Both slash/dash polarities were tested. Dots
and question marks remained unconstrained.
Encoding and scan / = 1, - = 0: minimum
conflicts
/ = 0, - = 1: minimum
conflicts
Seven-bit, nonwrapping 18 18
Seven-bit, all circular offsets 16 14
Five-bit, nonwrapping 9 5
Five-bit, all circular offsets 9 5
The independently supplied 18/5 result is reproduced for a nonwrapping scan. Circular scanning lowers the
ASCII minimum to 14.
- Best circular ASCII alignment: starts at position 30, slash = 0; 14 conflicts, 28 agreements and 42
unconstrained positions.
- Best five-bit alignments: start at 45 or 55, slash = 0; each has five conflicts, 21 agreements and 34
unconstrained positions.
- Start 45 does not wrap. Its conflicting positions are 46, 47, 53, 70 and 71.
Neither encoding fits. Unknown values cannot eliminate hard conflicts.
7. Braille checks completed
For the straight three-row by 36-column layout, cells have two columns and three rows. Every nonwrapping
cell origin was tested. A reading is reported only when all six positions are known. Different alignments and
overlapping cells are not concatenated.
Mapping Fully determined result
Dots raised, unrotated Two blank cells and ⠄ (dot 3 only)
Dots raised, rotated 90 degrees
clockwise
Three blank cells
Dashes raised, rotated 90 degrees
clockwise
Isolated ⠃, ⠰ and ⠠
The dash mapping reflects the documented Xbox extraction more closely, but the sticker layout has no
established circular outline or interior mask. [3] These isolated patterns do not establish a message.
For this specific straight layout, positions 93, 54 and 61 would each complete a currently dot-bearing cell.
These priorities must not be represented as findings about the unassembled jigsaw layout.
INSIDE ARG | Verification handoff | 27 September 2026 4 / 7
INSIDE ARG / CURRENT FINDINGS AND OPEN QUESTIONS
<PARSED TEXT FOR PAGE: 5 / 7>
8. Jigsaw-tile experiment: prepared, not assembled
The community's labeled assembly is image 846shEE.jpg. [5] It could not be retrieved in the analysis
session. Linked historical Discord copies also failed. The actual nine-letter slot order has not been
verified.
The tile inputs were computed by taking positions letter_index + 9k, with A=1 through I=9 and k=0
through 11, in increasing order:
Tile Twelve symbols
A ?--?-/??????
B /?//////-?./
C ---///-/-???
D -/?-/???/.??
E /--/??/??/.?
F ?/-?/-///?/?
G /???/??-/?.?
H ?/-?--?-/..?
I /-?/??/-/.?/
Six block variants were generated: three wide by four tall, and four wide by three tall, each filled row-major,
by alternating-direction rows, or column-major. Row serpentine begins left-to-right on the top row and
reverses on alternate rows. Column-major proceeds top-to-bottom, then moves right.
Cells entirely within individual tiles were checked at 0, 90, 180 and 270 degrees. Every fully known
nonblank dot-as-raised cell found in that restricted test contained one raised point. No phrase was
established.
Not yet completed: placement of the nine blocks in community order; the six complete symbol pictures;
dash/slash continuity across boundaries; overall dot geometry; Braille cells crossing boundaries; and
ranking unknown positions for the strongest assembled-layout candidate.
Required input: the labeled image, or its nine letters in reading order from top-left to bottom-right. No
alphabetical arrangement has been substituted.
9. Manufacturing explanation
Standard 108-label sheets exist:
- SheetLabels SL716: 0.75-inch square labels, 108 per letter-size sheet. [6]
- Creative Label Concepts 9-12C_5034: 0.75-inch circles, explicitly nine across by twelve down. [7]
No public production specification was found connecting these products to iam8bit's INSIDE stickers.
Current product listings do not establish availability or use during the historical production run.
No explicit sticker measurement or original backing-sheet specification was found in the reviewed public
repository, sticker catalogue or research account. [1, 2, 8] Discord's complete history and private
correspondence were not searched.
INSIDE ARG | Verification handoff | 27 September 2026 5 / 7
INSIDE ARG / CURRENT FINDINGS AND OPEN QUESTIONS
<PARSED TEXT FOR PAGE: 6 / 7>
A repeated sheet of 108 fixed artworks with advancing serial numbers could produce the observed cycle.
Merely having 108 labels per sheet does not automatically produce such a cycle. Intentional puzzle content
and a repeated manufacturing template can coexist.
Unresolved: actual sticker dimensions, backing-sheet geometry, artwork placement and numbering
workflow. A measurement would test the specific 0.75-inch products; it would not alone exclude a larger
custom 108-up printing layout.
10. JPEG-page recovery
Target: the terminal41.link page at dat/534brn9653f9j8mmd/. [9]
The repository copy and public mirror were fetched and found identical: 16,922 bytes, with 2,047 literal
UTF-8 U+FFFD replacement characters. SHA-256:
d663d180f340b792e1bd4dbd8e8400e3b89da1c97af251b32d49735005273fa8
JPEG remnants and HTML-serialization artifacts support lossy text handling. They do not establish when or
where the damage occurred. Changing character encoding cannot uniquely restore information already
discarded by replacement decoding.
Wayback raw id_ requests using these timestamp selectors returned HTTP 404 archive error pages:
20200421000000
20200421064134
20211231000000
These are requested selectors, not recovered capture dates. Availability queries returned no snapshots for
the tested URL forms; one successful CDX prefix query returned an empty list. Other index attempts
encountered a 503 or timeout.
No original archived payload was recovered. The existing reproduction package contains 13 request
records and hashes for the 12 returned bodies. Error pages without U+FFFD are not successful JPEG
recoveries.
11. Missing evidence and next verification steps
The 43 unfilled cycle positions are:
1, 6, 8, 11, 16, 22, 25, 27, 28, 33, 34, 35,
41, 45, 49, 50, 52, 54, 55, 58, 61, 62, 64,
67, 68, 73, 77, 82, 83, 84, 87, 88, 91, 93,
94, 99, 100, 102, 103, 104, 105, 106, 107
The missing classes inside the observed dot window are 87, 88, 91, 93 and 94. Their values remain
unknown. For any missing position p, candidate sticker numbers are p+108k. The existing checklist lists
k=0 through 4; it does not assert that every candidate exists.
Recommended verification order:
1. Independently regenerate the cycle and counts from the pinned sticker catalogue.
2. Check the binary tests with explicit wraparound and polarity conventions.
3. Supply and verify the jigsaw's nine-letter arrangement.
4. Assemble all six block variants before choosing a preferred layout; record both favorable and
unfavorable results.
INSIDE ARG | Verification handoff | 27 September 2026 6 / 7
INSIDE ARG / CURRENT FINDINGS AND OPEN QUESTIONS
<PARSED TEXT FOR PAGE: 7 / 7>
5. Obtain fresh photographs testing already-filled dot predictions, particularly sticker 200, alongside
photographs filling unknown positions.
6. Obtain a ruler photograph, backing sheet or production template.
7. Seek an original HTTP/WARC payload or contemporary untouched copy of the JPEG page.
Branch Current stopping point
Jigsaw assembly Verified A-I slot order unavailable
Manufacturing explanation No measured sticker or documented production layout
JPEG recovery No intact original payload retrieved
Message extraction All tested readings lack a justified phrase
Discovery priority Complete Discord solving history not reviewed
12. Sources and companion evidence
[1] Community repository and pinned revision:
https://github.com/twinysam/INSIDE-ARG/tree/4de72d7c2f21bd9eb4144fda51281c84cbcb90c4
[2] Sticker catalogue: https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md
[3] Community printer research:
https://docs.google.com/document/d/1vlpah0LdCRpJe-OfhnkaiBIcmepGXust5BMbaFJGGt8/edit
[4] Game Detectives overview: https://wiki.gamedetectives.net/w/Inside_ARG
[5] Labeled jigsaw image, inaccessible during the analysis session: https://i.imgur.com/846shEE.jpg
[6] SheetLabels SL716: https://www.sheetlabels.com/labels/SL716
[7] Creative Label Concepts / BrownKraftLabels product 9-12C_5034: https://www.brownkraftlabels.com/items/white-high-glos
s-laser-labels/white-high-gloss-round-laser-labels/3-4-diameter-round-white-high-gloss-laser-label-sheet-br-usually-ships-same
-day-hg9-12c_5034-detail.htm
[8] Raezores research account: https://github.com/twinysam/INSIDE-ARG/blob/master/raezores-research.md
[9] Original JPEG-page target: http://terminal41.link/dat/534brn9653f9j8mmd/ ; preserved mirror:
http://534brn9653f9j8mmd.surge.sh/
Existing companion files, not embedded in this PDF:
- INSIDE-ARG-Investigation-2026-09-27.md
- INSIDE-ARG-Reproduction-2026-09-27.zip
- INSIDE-ARG-43-Position-Checklist.md
Version note: those companion files include the cycle, clustering, printer comparisons, straight-layout
Braille, archive attempts and checklist. The latest binary comparisons and preliminary tile checks are
documented in this PDF and have not been added to those older files.
Evidence standard: observations, computed results and hypotheses remain separate. No unknown
symbol has been assigned to make a phrase. No completed ARG solution or exclusive discovery is claimed.
INSIDE ARG | Verification handoff | 27 September 2026 7 / 7
INSIDE ARG / CURRENT FINDINGS AND OPEN QUESTIONS