# Experiment 483: recover and audit the authentic original Playdead printer-button JavaScript

**Date:** 16 October 2026. **Mode:** VALIDATE for byte-authenticated preserved client-side code; DEVELOP for any conclusion about lost server-side behavior or a possible CE continuation. **Inputs:** existing historical web archives only, **no sticker searches or owner contact**. This supersedes the previous *client-byte-unavailable* statement in [Experiment 480](../experiment-480-original-print-transport.md) without supplying the missing PHP/server response.

## Recovery, as actually performed

The [4 June 2018 Steam witness](https://steamcommunity.com/app/304430/discussions/0/359543951720753445?ctp=53) explicitly identified `http://www.playdead.com/js/dist.js` and quoted a success callback. The project already knew that report. This experiment directly recovered byte-bearing archive sources, rather than extrapolating the protocol from those comments.

1. [First read-only archive run](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38980599410) queried Wayback availability/CDX, Arquivo.pt and three Common Crawl index windows. It recovered a **2016-07-25 Wayback raw JavaScript** at [the preserved replay](https://web.archive.org/web/20160725224658id_/http://playdead.com/js/dist.js), **740,120 bytes**, SHA-256 `fc42ccefccf5a3c23cabdabbf7f61144b535bf1beb4f89e8d7b6f53866795690`. Its inline source map has **seven modules and no printer code**. This is a historical *negative control*, not the desired 2018 script.
2. [Second archive run](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38981035661) found **21 Arquivo.pt version-history entries**, including **2018-07-19**, **2019-03-27**, **2019-09-23**, **2019-11-23**, 2020 and 2021. Archived captures in 2018–2021 carry the same Arquivo index digest `GJNK47W44Z3L4HKY2YYBM4VSRJLX7C2P`. However, direct `/wayback/TIMESTAMP/…` replays returned **8,178-byte Arquivo viewer HTML**. Those responses were **not source recovery**, and were not treated as the client.
3. Inspection of that HTML exposed its true `replay_iframe` URL ending in `TIMESTAMPmp_/https://playdead.com/js/dist.js`. A dedicated [third archive run](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38981304970) requested this **exact source-backed archive URL**, its `id_` raw-replay form, and documented no-frame alternative, without contacting Playdead.
4. The **2018-07-19** and **2019-03-27** raw `id_` versions are **byte-identical**: **723,075 bytes**, SHA-256 **`892e795393531f93bb485c8382b52a13d35423b7251c7399d5a7ef5c7b912587`**. The archived `mp_` versions are **727,206 bytes**, SHA-256 `b345195c058007e0ee10fdbbd6…`, with archive replay injection. Keep these *rewritten* captures separate from raw source. The first original raw archive URL is [2018-07-19](https://arquivo.pt/wayback/20180719141035id_/https://playdead.com/js/dist.js); independent later raw replay is [2019-03-27](https://arquivo.pt/wayback/20190327172747id_/https://playdead.com/js/dist.js).

The original source replay bytes and metadata are preserved in the third run's **30-day GitHub Actions artifact**. The full third-party website bundle is deliberately **not redistributed verbatim inside the public research repo**. The archive source URL, capture timestamps, exact SHA-256, runtime behavior, source-map discrepancy and the offline/optional-local verification procedure are permanently recorded in [machine-readable evidence](../data/experiment-483-original-printer-client.json) and [the reproducer](../scripts/audit_archived_playdead_printer_483.py).

## Executable client-side printer state machine

Only the **raw 2018/2019 compiled client** is treated as the implementation. Its `printCheck()` function reads the element `#mce-EMAIL` and generates/preserves a browser-local `id` if one is not yet present in `localStorage`. The GUID helper constructs a pseudo-random UUID-like value using `Math.random()`, **not** a CE sticker serial or a person-facing login identity.

| Situation | Actual requests emitted by the compiled client | Observable client action |
|---|---|---|
| Empty input | **1 POST:** `/print/prepare.php` with `in,id,check,url` | Locally render *no message received*, call browser print |
| Nonempty input, check response is literal string `false` | **2 POSTs:** prepare, then `/print/index.php` **check mode** with `in,id,check,url` | Locally render *incorrect message received*, call browser print |
| Nonempty input, check response **is not** literal `false` | **3 POSTs:** prepare, check-mode index, then **content-mode** `/print/index.php` with only `in,id` | Insert second response into `#print-content`, apply success print styling, call `window.print()` |

Exact client details that materially refine Experiment 480:

- The posted field is **`in`**, taking its value from the field that looked like an email subscription box. It is **not** literally named `email` in this compiled JavaScript. The 2018 eyewitness described its *role* as email and noticed `id`, `check`, and `url`; recovered source gives exact wire keys.
- In check mode, **`check` is the literal string `'true'`**, `url` is **`window.location.pathname`**, and the persistent identifier is **`localStorage.getItem('id')`**.
- On a client-side recognized input, the **second** `index.php` POST intentionally drops both `check` and `url`, retaining only `in,id`. This separates validation from retrieval in a way a generic “printer button invokes a PDF” summary misses.
- **`prepare.php` is launched but not awaited** before the check POST. The client has no special delay or completion dependency there; server ordering, state changes or races are **not** reconstructible from this code alone.
- The compiled condition for the locally empty case is simple nonempty-string checking. An arbitrary nonempty value is **not** deemed valid by the client itself: it asks the server, and only a first response equal to the string `false` is treated as rejection.
- The original uses **browser `window.print()`** after locally inserting returned HTML. There is **no evidence here that the server returned a PDF** with PDF HTTP headers, nor that a fourth CE credential was accepted.

The `window.location.pathname` parameter is particularly worth preserving as a **potential routing discriminator**. It establishes that the server received the source page's path during the *check* request, so checks *could* theoretically depend on the page. It does **not** show that any pathway actually did, and no CE-specific path or submitted value is supplied by this source.

## Critical source-map mismatch: do not silently interpret source maps as executable code

The recovered raw JavaScript embeds an inline **source map with eight entries** including `3_print.js` (3,100 source characters). Unlike the seven-module **2016** source map, this includes a printer module.

However, the source map's `sourcesContent` is demonstrably **not equivalent to the 2018/2019 compiled `printCheck()`**:

| Behavior | Executable bundled JavaScript | Embedded `3_print.js` source-map text |
|---|---|---|
| `prepare.php` POST | **present** | **absent** |
| Send `url=window.location.pathname` | **present** | **absent** |
| Nonempty gate | **input != empty string** | regex rejects whitespace |
| First `index.php` check + second content retrieval | **present** | present |

Consequently the source map is a **versioned or stale-source artifact** relative to this compiled build. It might preserve an older development stage, but source map assembly/packaging could also create such divergence; we cannot assign it a precise authoring chronology from these bytes. **Executable source controls the request semantics.**

The discrepancy itself provides a useful version-history clue: a simple code-diff between archived builds could isolate precisely when preflight preparation and path-sensitive check parameters were added. The 2016 historical negative and the 2018/2019 byte-identical positives define a bounded interval, not a uniquely known development date.

## What was and was not solved

**Newly established:** original client bytes; actual request keys and stage order; persistent pseudo-random browser ID; local vs server print response class; documented client source-map mismatch; dated, byte-identical 2018/2019 captures. This repairs a genuine missing-source limitation in Experiment 480.

**Still unresolved:** no `/print/prepare.php` or `/print/index.php` server PHP, raw accepted-response HTML/HAR, server-side field schema beyond what the client sends, cookies, path-condition processing, or CE-era fourth/new credential has been recovered. A page route or output that resembles 108 sticker marks is not a validated receiver.

**Next bounded non-sticker experiment:** reconstruct the original Playdead site page paths/layout and obtain a historically captured successful `index.php` **response** or source-side PHP behavior, preferably differentiating check-mode `{in,id,check,url}` from content-mode `{in,id}`. A recovered post-December-2019 page may establish whether any site-specific CE operation was ever advertised, but no such operation is known today. Do not POST guessed passwords to a live Playdead domain.

## Reproduce

```bash
python scripts/audit_archived_playdead_printer_483.py
python scripts/audit_archived_playdead_printer_483.py --source path/to/2018-raw-id-replay.js
```

The first mode checks the committed summary and protocol contract offline. The second verifies SHA-256, size, raw compiled behavior, inline source-map module count, and the exact source-map mismatch against authentic downloaded archived bytes. Both source captures were separately checked locally against the same original SHA-256. No extra physical symbols are filled or inferred.
