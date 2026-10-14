# CE receiver follow-up: four banks of 128 and website command-like input

*12 October 2026. DISCOVER / DEVELOP. Conditional representation experiment and historical input-grammar clue, **no discovered CE consumer**.*

This supplements [the purchaser/receiver and classword census](ce-purchaser-receiver-and-classword-audit-2026-10-12.md). The directly linked damaged CE webpage contains the historically recovered text **128 UNSOLVED** (see [Experiment 478](experiment-478-source-native-consumer-affordances.md) and source-repair Experiments 413–423). That does **not** establish the page's pixel dimensions, a 128-element lookup table, or the interpretation of the sticker foreground.

## Four banks of 128 as an explicit rival

The earlier exact test rejects placing all nine **unmodified nine-bit class words directly** into a single 128- or 256-element table. One distinct *invented* alternative is a banked receiver: each nine-bit unsigned value v specifies **bank = floor(v/128)** in 0–3 and **offset = v modulo 128** in 0–127. That supplies a 2+7-bit coordinate and always fits in a four-bank array by construction. Whether original Playdead content supplies four 128-entry banks is the crucial outside question.

We enumerated **all 18 conditional 81-mark body completions**, without selecting any output, under four simple global conventions: original/reversed word order × slash-as-one/dash-as-one. The nine banks assigned to A–I stay fixed across the 18 bodies in every convention, because the high-order pair is determined by already fixed serial-frame rows:

| Word direction | One-bit glyph | Banks for A B C D E F G H I | Bank counts (0,1,2,3) |
| --- | --- | --- | --- |
| Forward | Slash | **2 2 0 1 2 3 2 1 2** | 1,2,5,1 |
| Forward | Dash | 1 1 3 2 1 0 1 2 1 | 1,5,2,1 |
| Reversed | Slash | 1 1 1 3 3 3 2 2 2 | 0,3,3,3 |
| Reversed | Dash | 2 2 2 0 0 0 1 1 1 | 3,3,3,0 |

In each convention, nine full 9-bit words remain distinct for every 18-body completion. The four earlier invariant class words, in forward/slash=1 representation, correspond to these fixed bank/offset pairs:

| Class | Nine-bit integer | Bank | Offset |
| --- | ---: | ---: | ---: |
| B | 382 | 2 | 126 |
| C | 58 | 0 | 58 |
| F | 407 | 3 | 23 |
| H | 129 | 1 | 1 |

**Why this is an interesting test but weak evidence:** 512 = 4×128 is an identity, not a discovered decoder. Every nine-bit value has a bank and offset, and the stable bank vector merely reflects the first two / last two frames already fixed in the physical corpus. One orientation even produces the attractive three groups of three banks, but that alternative was inspected after the fact and offers no independent confirmation.

The preserved Terminal41 print-status material names **four schemes** (PLANET, LIFE, PROBE and CONDISCON); that is an authentic four-way system, not an established four-bank *128-address* consumer. We must locate a first-party artifact with **four independently addressable 128-item regions**, a codebook, or source-defined bank ordering before using bank positions to select sticker completions.

Reproduce independently, no extra packages:

    python scripts/audit_ce_banked_128.py --output /tmp/ce-banked128.json

Full source-neutral output: [data/ce-banked-128-2026-10-12.json](../data/ce-banked-128-2026-10-12.json); [script](../scripts/audit_ce_banked_128.py). The four interpretations, all nine 7-bit offset sets and collision status are preserved. An independent JavaScript computation regenerated the artifact from the classword census; the Python script was also executed locally against the physical CSV fixture. No page/image bytes are silently transformed.

## Another historical possibility: the website field may have accepted commands

A directly contemporary [June 4, 2018 Steam discussion](https://steamcommunity.com/app/304430/discussions/0/359543951720753445/?ctp=53) contains more than accounts of accepted printer phrases. Participants discuss the Playdead website's input and a screenshot of a **console-like interface**. One first-person report says they typed **connect** into the purported email field; another viewer referred specifically to the displayed *Connect*. The same discussion reports a **comms overload / timed cooldown** screen after excessive input attempts, as well as a client-printed conditional result and two POSTs to prepare.php and index.php.

This is a distinct *question to test*: Was the 2018 input only a passphrase validator, or did it also implement **commands / transitions / printable echo**? The archived text does **not** establish that connect was accepted as a secret, that it changed a server state, or that this interface remained live at CE release. The screenshot link and request/response data need to be recovered before claiming it is anything more than visually echoing user-provided text. The [existing original-transport audit](experiment-480-original-print-transport.md) remains the base reference.

**Safe concrete follow-up:**

1. Acquire 2018–2020 archived original website JavaScript at the historically cited path www.playdead.com/js/dist.js, without pushing any modern guesses to a live server.
2. Identify how the page displays raw field text, recognized commands, incorrect input, cooldown and accepted printer phrases. Model stateful versus stateless branches from actual code, not from roleplayed terminal aesthetics.
3. Search for preserved original HTML fragments/HAR captures that distinguish *Connect*, a random string, and known accepted phrases, with timestamps and content hashes.
4. Only then, if an independently specified input language is found, apply candidate sticker-derived strings or command sequences; the 108 original symbols might specify actions rather than letters.

**Status:** the exact banked-128 transform is fully computed but lacks a native receiver. The command-input reading has first-person contemporary testimony but **no authenticated request/response or source code to confirm distinct server command behavior**. Both are investigable without acquiring any new stickers.
