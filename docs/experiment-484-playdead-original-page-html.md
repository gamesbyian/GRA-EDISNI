# Experiment 484: recover the original Playdead printer button's HTML wiring

**16 October 2026. Research mode:** VALIDATE for dated **archive-served HTML bytes and DOM wiring**; DEVELOP for conjectures about missing 2018–2019 backend behavior and alternate page-specific inputs. **No new sticker search, no live Playdead POST, no owner outreach.**

This continues [Experiment 483](experiment-483-original-printer-client-runtime.md), which directly recovered the compiled `printCheck()` function from identical authentic July 2018 and March 2019 `js/dist.js` builds. It had no internal call site for the function. The missing piece was a contemporary page *loading* that source and calling the function from a real control.

## Acquisition and exact dates

A bounded [one-shot GitHub Actions archive query](https://github.com/gamesbyian/GRA-EDISNI/actions/runs/38982607776) requested eight `id_` archived HTML replays from `arquivo.pt` only: four original Playdead URL variants near two known 2018/2019 JavaScript capture timestamps. The provider returned all eight HTTP 200 responses and saved original response bytes plus JSON in a 30-day source artifact. Those eight responses represent **four distinct bodies**, **not eight independent historical observations**.

**Crucial provenance warning:** the archive *requested* timestamp need not equal the original timestamp it *returned*. The 2018 homepage query returned an actual **2019-03-27** replay. The `/inside/` queries returned **2025-10-09** redirect HTML, not an original 2018/2019 page. Always follow the **actual replay URL's timestamp**.

| Original path / actual source replay | Actual UTC capture | SHA-256 | Bytes | Printer UI |
|---|---|---|---:|---|
| [playdead.com homepage](https://arquivo.pt/wayback/20190327172702id_/https://playdead.com/) | **2019-03-27 17:27:02** | `dbb585bbb175c3288f1ee53322fc46ee277123a173a1cccfa022cc6b1a36fdeb` | 9,178 | **Full click binding, email field, print output area** |
| [Original INSIDE game page](https://arquivo.pt/wayback/20180719140951id_/http://playdead.com/games/inside/) | **2018-07-19 14:09:51** | `70e93a066974df4d4dd3f83ab25d48b0ec2598d3e9b4130f69bdcda8a142430c` | 18,795 | Print button bound, **no email field or output area** |
| [INSIDE page later state](https://arquivo.pt/wayback/20190405002453id_/https://playdead.com/games/inside/) | **2019-04-05 00:24:53** | `49885e820c7e5baeb995b327dc5ce9087e4e38c67bc0246c375e227b034aa591` | 18,856 | Same missing elements, script URL migrated HTTP→HTTPS |
| [`/inside/` redirect](https://arquivo.pt/wayback/20251009104855id_/https://playdead.com/inside/) | **2025-10-09** | `590a6fa8f40b371027cb3c8b70be6dcf9d4f46dda6cb9b5ead394d13780f4f4a` | 561 | Modern redirect only; **do not use as historical source** |

This direct byte-level source-capture record is pinned in [the Experiment 484 fixture](../data/experiment-484-playdead-original-page-html.json). No full third-party HTML is redistributed in this repository; source URLs, SHA-256 and precise DOM facts are durable.

## Independently verified original homepage call site

The original **March 2019 Playdead homepage** contains the exact native mark-up:

```html
<div class="print-button-wrapper" onclick="printCheck()">
```

It contains the real input element with `id="mce-EMAIL"`, `name="EMAIL"`, `type="email"`; an empty content container `id="print-content"`; and `<script src="https://playdead.com/js/dist.js">`, matching the recovered 2018–2019 script (Experiment 483). This is the first *fully source-grounded* evidence chain, in our repository, for **button → JavaScript function → input value → printer AJAX requests → printed output container**.

### The two deceptively similar submit paths are now proven distinct

On the same page the **ordinary newsletter subscription** is an HTML `<form>` with `id="mc-embedded-subscribe-form"` and an action at a third-party Mailchimp domain `playdead.us3.list-manage.com`, using its standard Submit control. That independently proves that the `#mce-EMAIL` field was a genuine email-subscription field.

The game ARG's **printer button** is a *different element*, a plain clickable wrapper calling `printCheck()`. It reuses the visible email field's typed text, but **does not submit the Mailchimp form**. Instead the original JavaScript submits `in,id,check,url` to Playdead's own `/print/prepare.php` and `/print/index.php`, followed conditionally by a content-mode `/print/index.php` with `in,id`. The native page and compiled client now independently complete one coherent **functional user-input-to-client-response architecture**, although the PHP reply implementation itself is lost.

This clears a genuine historical ambiguity from the original June 2018 community descriptions: *typing into an email-like field* is not the same as *submitting a newsletter signup*.

## A live architectural difference between two historical page types

The original **July 2018 `/games/inside/`** page has the same inline `onclick="printCheck()"` wrapper and loads the same script path, but **does not contain**:

- `id="mce-EMAIL"` (the specific field the compiled function queries),
- `id="print-content"` (the element receiving success content),
- or the homepage's `mc-embedded-subscribe-form` subscription form.

The April 2019 version of that game page has the same properties. On an otherwise unmodified detail page, plain jQuery `$('#mce-EMAIL').val()` resolves to **undefined** if the selector has no matched element. In that state the compiled strict test `s_input != ""` evaluates true, but the exact request encoding/server behavior needs its own source-specific test: do **not** silently assert a valid input, accepted server response, or a new page-specific secret merely from the button's presence.

The optional posted field `url=window.location.pathname` in the actual original client acquires a more concrete potential purpose: **the same button exists on at least two structurally different page templates**. Sending the page path could help the server select which page's request it was checking, but the PHP and original responses are still missing. Equally plausible ordinary explanations include analytics, auditing or scaffolding a shared navigation/header template. The *client* supplies the path; there is **no positive evidence here that the server acted on it or supported a CE feature**.

## Separation of historical and current sources

The requested timestamp for `/inside/` yielded a 2025 archived redirect, not 2018 input. We explicitly exclude this from original-player conclusions. For the 2018 game detail, the true returned replay date is 2018-07-19. For the homepage the true return date is 2019-03-27; an original July 2018 homepage has **not yet** been independently recovered here. The separate June 2018 first-person Steam witness establishes that a printer button existed earlier, but does not supply identical HTML bytes.

Original static client/HTML bytes, archived modern redirects, eyewitness network reports, old source-map `sourcesContent`, and unknown PHP are separate evidence levels. A DOM element's presence without its companion nodes is an interface problem, **not** automatically an ARG clue.

## Follow-on work with no new stickers

1. Recover an actual **June–December 2018 homepage** HTML capture, if archived, rather than treating the March 2019 homepage as contemporaneous with the June 2018 Steam witness. Look for the field/control structure and exact source script revision.
2. The now-proven **path-sensitive request metadata** warrants retrieving historically archived server responses (not submitting modern guesses) to determine if the original backend branched on `url`, browser `id`, or original input class.
3. If source pages with a distinct print content container exist, freeze the DOM and response contract **before** testing any claimed source-native foreground operation. Unrelated page/selector coincidences are insufficient.

**Result:** source-grounded print-button wiring and two-page template distinction, plus a provider-date correction. **Not** a decoded CE foreground; **not** another physical symbol; **not** evidence of a fifth Terminal41 scheme or a new post-2019 Playdead credential.
