# Non-destructive imaging leads for sealed INSIDE Collector's Editions

This note is about one narrow problem: there are still sealed Collector's Editions whose sticker cannot be read without disturbing the packaging. Could somebody look inside non-destructively?

I am not involved in the Discord or the existing ARG work. I went looking for people and facilities who might be technically able, geographically convenient, or simply interested enough to try. I am posting the leads rather than volunteering to contact owners or labs myself.

## What has to be recovered

The useful result is modest: the sticker needs to reveal a three-digit serial number and one of three large foreground marks (`/`, `-`, or `.`). A clean photographic image would be nice, but it is not necessary if the number and mark can be classified confidently.

That distinction matters. Some imaging methods may be able to distinguish enough ink, foil, relief, adhesive, or layer structure to classify the sticker without producing anything that looks like a normal photograph.

## Approximate size of the sealed CE

There does not appear to be a published exterior-size specification, so this is a working estimate from photographs using a standard PS4 case as a scale reference.

PS4 case reference: **190 × 135 × 14 mm**

Estimated Collector's Edition exterior: **about 320 × 235 × 235 mm**, with roughly **±10–15 mm uncertainty per dimension**.

A reasonable broader range is **315–330 mm wide × 225–240 mm high × 225–240 mm deep**.

This estimate should not be treated as a manufacturer measurement. It is good enough to rule some scanners in or out, but anybody arranging a scan should first get the real L × W × H from the owner.

One CT-specific wrinkle: scanners often rotate the sample. A 320 × 235 mm rectangle has a diagonal of about 397 mm, and even a 235 × 235 mm cross-section has a diagonal around 332 mm. A scanner advertised for a 300 mm maximum sample diameter may therefore still be too small.

## Known sealed-copy targets

The community ledger is the source of truth here:
https://github.com/twinysam/INSIDE-ARG/blob/master/stickers.md

### Shaxai (U47)
The ledger records that Reddit user Shaxai owns **two sealed Collector's Editions**. Current location is unresolved.

This is probably the highest-value owner lead because one cooperative owner could potentially yield two previously inaccessible stickers.

### Robert Borg (U17)
The ledger records that Robert Borg eventually acquired his friend's CE and has kept it unopened.

Working geography for logistics: **Malta**. That is only useful at country level; no finer location is needed.

### Other historical sealed copies
The ledger also contains sealed-copy provenance where the present owner is unknown or the chain has moved on, including U04 and U31. These may become useful if the current owner can be identified through ordinary community contact, but they are less immediately actionable.

## Industrial X-ray / CT leads

### Industrial Inspection & Consulting, Norton Shores, Michigan
**Why this one matters:** they have already done essentially the same class of experiment on collectibles.

They have used industrial CT to inspect unopened Pokémon packs and boxes, extracting card features from small density differences. They also advertise CT authentication of sealed collectibles and electronics.

Contact: `sales@industrialinspection.com`  
Phone: +1 231-246-8473

Sources:
- https://industrialinspection.com/2024/06/26/ct-scanning-unopened-pokemon-cards/
- https://industrialinspection.com/collectibles-ct-scan-authentication-services/
- https://industrialinspection.com/detecting-fake-sealed-nintendo-game-cartridges-using-ct-scanning/

This is probably the strongest "we already know this company likes weird sealed collectibles" lead.

### Scott Johnston / Lumafield, US
Scott Johnston is Lumafield's co-founder and Head of Engineering. Adam Savage and Tested have repeatedly brought unusual objects to Lumafield for CT scanning, including giant vacuum tubes, workshop curiosities, film props, and MythBusters' Buster.

Lumafield has facilities in San Francisco and Cambridge, Massachusetts.

Sources:
- https://www.lumafield.com/article/ct-scans-vacuum-tubes-tested-adam-savage
- https://www.lumafield.com/article/journalistic-storytelling-with-industrial-ct
- https://www.lumafield.com/contact

This feels like a good personality/outreach fit even apart from the hardware: they have an established habit of scanning interesting objects because the question is fun.

### Logan Hsu / Baylor OiVM Core, Houston
Logan Hsu is Co-Director of Baylor College of Medicine's Optical Imaging & Vital Microscopy Core and works with its microCT imaging pipeline. His institutional bio also explicitly says he enjoys playing video games with his kids.

Contact:
- `loganh@bcm.edu`
- https://oivm.org/whoweare/

Caveat: Baylor's biomedical microCT hardware may be too small for the intact CE. This is still a potentially useful technical/referral contact.

### Alberta Industrial CT, Edmonton
The University of Alberta operates a Nikon XTH-225 ST large-cabinet CT system. Their public specification says it can hold samples up to about **30 cm wide × 35 cm high** in a single scan.

Source:
https://www.eas.ualberta.ca/aict/

This is near the estimated CE size, so exact dimensions and rotational clearance would have to be checked carefully.

### INGV Osservatorio Vesuviano, Naples
The Naples micro-CT lab operates a ZEISS Xradia 410 Versa.

Lab lead: Lucia Pappalardo  
Email: `lucia.pappalardo@ingv.it`

Source:
https://www.ov.ingv.it/index.php/laboratorio-di-microtomografia-ai-raggi-x

This is geographically interesting for the Malta copy. Published nominal sample limits for this class of instrument make the intact CE look borderline, not obviously compatible, so geometry should be confirmed before anybody moves a box.

## Terahertz leads

Terahertz imaging may be worth trying because THz radiation can penetrate many non-metallic materials and has been used to recover information from layered paper/art objects. It may or may not have enough contrast for these particular inks, but there are groups whose current research is very close to the problem.

### SapienzaTerahertz, Rome
**Massimo Petrarca** and **Candida Moffa** are especially interesting.

Their group has demonstrated THz multispectral imaging that reveals concealed text beneath layered mock-up materials. The lab works on non-invasive imaging of cultural-heritage materials and is open to multidisciplinary collaboration.

There is also an unusually useful Malta connection: Petrarca, Moffa and colleagues organized a session on terahertz applications for cultural heritage at the **University of Malta's Valletta Campus in October 2024**.

Contacts:
- `massimo.petrarca@uniroma1.it`
- `candida.moffa@uniroma1.it`

Sources:
- https://sapienzaterahertz.sbai.uniroma1.it/people/
- https://iris.uniroma1.it/handle/11573/1745328
- https://www.metroarcheo.com/ma2024/special-session-4

For Robert Borg's sealed copy in Malta, this is probably the most intriguing academic lead.

### TeraView, Cambridge, UK
TeraView explicitly offers **contract terahertz analysis**, including one-off exploratory jobs. Their examples include non-destructive scanning of letters, books and art, and material studies involving paper, plastics and wood.

Contact: `enquiries@teraview.com`

Sources:
- https://teraview.com/services/contract-terahertz-analysis/
- https://teraview.com/contact/

This may be the easiest THz route commercially because unusual one-off analysis is already part of what they sell.

## Suggested order of attack

If somebody in the community wants to pursue this, I would start with:

1. **Industrial Inspection & Consulting** for a blunt feasibility opinion. They already scan unopened collectibles and have spent time optimizing for tiny density differences.
2. **SapienzaTerahertz** for the Malta copy. Their hidden-text work is unusually relevant, and they already have a Malta academic connection.
3. **Lumafield / Scott Johnston** as the "interesting object, let's see what CT can do" lead.
4. **TeraView** for a commercial THz feasibility test.
5. Regional facilities such as INGV Naples or Alberta Industrial CT once actual box dimensions and owner logistics are known.

## Sensible first experiment

Before anybody ships a valuable sealed CE across a continent, test the modality on a **known loose sticker** or a realistic surrogate stack.

Questions worth answering first:

- Can the instrument distinguish the black printed serial from the sticker stock?
- Can it distinguish `/`, `-`, and `.`?
- Does the sticker use any pigment, foil, coating, relief or adhesive layer that provides stronger contrast than expected?
- How badly do the surrounding cardboard, plastic case, disc, figure and other CE contents interfere?
- Is a single 2D radiograph enough, or is CT / spectral imaging actually necessary?

If the answer is "yes, the known sticker is readable through representative packaging," then asking a sealed owner to participate becomes a much less speculative proposition.

## Boundaries / caveats

- This is a lead list, not a claim that any method will work.
- Exact CE dimensions should be measured before scanner compatibility is assumed.
- Owner locations should be kept at the coarse level needed for logistics.
- The community should decide which owners are appropriate to approach.
- I am contributing the research and leads here, not volunteering to contact owners, labs, or companies.