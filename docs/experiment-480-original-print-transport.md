# Experiment 480: original Playdead printer-button transport and response grammar

*8 October 2026. Source archaeology, not a new sticker decode or a live input test.*

## What this audit newly establishes

The historically demonstrated Playdead puzzle receiver was more specific
than “enter text into a form and receive a PDF.” The contemporary
4 June 2018 Steam discussion contains both a copied **browser-side
JavaScript success path** and a firsthand network observation:

- Players typed a decoded message into what otherwise looked like an
  email-subscription field, then activated the site's separate
  **printer button**. That is not an ordinary mailing-list submit.
- The contemporary witness reports **two POSTs**, to
  `/print/prepare.php` and `/print/index.php`. The witness describes
  four transmitted values: `email`, `id`, `check`, and `url`.
  These are **witness-reported fields**, not preserved request bytes
  or a verified server-side schema.
- A saved excerpt of the successful client action posts to
  `/print/index.php`; returned `data` is inserted into the HTML
  element `#print-content`, and a delayed **`window.print()`**
  call opens the browser's printing machinery.
- The same witness observed an empty response from `prepare.php`
  and `false` from `index.php` during an **incorrect** attempt.
  No original successful response body has been recovered.

[Contemporaneous Steam discussion, 4 June 2018](https://steamcommunity.com/app/304430/discussions/0/359543951720753445/?ctp=53).

The [Xbox Wire report, 3 January 2019](https://news.xbox.com/en-us/2019/01/03/unsolved-secret-in-inside/)
describes the user-facing result as a **corrupted-image PDF**.
These accounts are compatible: at least one 2018 client path
rendered server-returned material in the browser and then printed it.
**Neither source proves that the original server itself returned
a PDF payload** with `Content-Type: application/pdf`. A saved PDF
might instead be the *client-side printed representation* of HTML.
This is a transport distinction with direct acquisition consequences.

## Response classes: preserve what was actually seen

The [Game Detectives chronology](https://wiki.gamedetectives.net/w/Inside_ARG#Printer_Button)
documents a genuinely conditional interface.

| Historical field/action situation | Observed or reported printed result | Evidence strength |
| --- | --- | --- |
| Empty input, press print | “no message received” | Community witnessed, 2018 |
| Unrecognized nonempty input, press print | “incorrect message received” | Community witnessed, 2018 |
| First accepted printer phrase | first successful factor message / noisy image | Community report; original response bytes missing |
| Another accepted printer phrase | second successful factor message / noisy image | Community report; original response bytes missing |
| Third historical accepted phrase | separate large artwork and spectrogram, leading onward to Terminal41 | Community report; original response bytes missing |
| Ordinary email sent separately | occasional mail/attached `printer.jpg` with rejection messages | June 2018 eyewitness account; not a print-button PDF |

The known historical accepted phrases include
`NEWPLANETDISCOVERED`,
`MULTIPLEPROBESDISPATCHED`, and
`LIFEDETECTED`. Game Detectives documents the latter as
**guessed and accepted on 13 April 2019**, not proven to be a
literal extraction of the PC/PS4 printer graphic.

The community reports that entering the known codes in any order
led to three different printouts. This does **not** establish whether
the server tracked state per session, globally, by distinct secret
categories, or through client cookies. No response headers, cookies,
HAR file, authoritative PHP code or actual success HTML remain in
this research corpus.

The original site's occasional emailed printer JPEGs must be
catalogued **separately** from material produced by the print button.
Treating both as “PDF responses” risks manufacturing false
continuity between unrelated output mechanisms.

## Chronology excludes an easy new CE password inference

The print button was documented in **June 2018**. The publisher
confirmed its operation in **January 2019**. All three known
accepted phrases were documented before the Collector's Edition
began shipping in **December 2019**. Thus a hypothetical CE output
cannot merely be asserted to be a fourth previously unreported
printer answer because Playdead once implemented such a mechanism.

The Terminal41 mirror's four indexed historical achievement
schemes are a *separate status layer*, not proof that exactly four
successful website-print PDFs existed. The printer's separate
email pathway and the static Viewgate placeholders are also
different interfaces.

## Retrieval effort and negative result

I checked the contemporary Steam witness, Game Detectives original
chronology, Microsoft's 2019 publisher report, and the existing
archived Terminal41 material. The former explicitly identifies
the original live JavaScript URL
`http://www.playdead.com/js/dist.js`.
Direct contemporary/replay-source retrieval through the available
web access did **not** yield usable original JS bytes, an original
HAR, or the `prepare.php`/`index.php` server implementations.
No historical accepted response fragment or byte-identical printed
PDF was acquired in this investigation.

The useful result is a **frozen retrieval target**, not claiming
to have recovered that data.

## Concrete, source-first next actions

1. Recover an archived `/js/dist.js` as actually served in
   **2018–2020**, recording capture date and SHA-256. Locate exact
   `_data` construction, error/success branches, path and print
   render logic; avoid treating the Steam observer's four field
   names as a complete schema.
2. Recover a browser HAR or **saved successful response fragment**
   from `/print/index.php`, with input class, cookies, date and
   content type. Compare empty, incorrect, and each of the three
   historically accepted phrases **without live POSTing guesses**.
3. Recover original printed image/PDF bytes and distinguish a
   browser-saved document from a response with server PDF headers.
   Do the same separately for the intermittent emailed
   `printer.jpg`.
4. If genuine dated CE-era records exist, look for an **additional
   accepted response branch or state**. Only if that is independently
   established should sticker-derived candidate plaintext be
   measured against its input grammar.

The [machine-readable evidence contract](../data/experiment-480-original-printer-transport.json)
freezes the witnesses, distinctions and missing files.

## Conclusion

**Real receiver:** confirmed before CE.
**Known action:** printer button, client POST(s), server content
then browser printing.
**Known output grammar:** empty / incorrect / multiple accepted
printouts, with state ordering not fully reconstructed.
**CE-specific reader or accepted input:** not verified.

The strongest new practical insight is to seek the **original
successful HTML fragment and browser print artifacts**, not only
a missing “server-generated PDF.” A source-anchored 108-symbol
foreground-to-request transformation remains unknown.
