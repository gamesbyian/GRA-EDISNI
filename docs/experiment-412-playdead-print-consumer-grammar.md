# Experiment 412 — historical Playdead answer consumer has no useful client-side grammar

_Status: completed source audit, 4 Oct 2026._

Experiment 411 showed that the preserved Terminal41 snapshot itself contains no typed input widgets.

The historical ARG **did** have a genuine answer consumer elsewhere: the Playdead print/subscription interface.

The original client JavaScript has now been vendored into this repository and audited directly.

## Protocol

The browser reads:

```js
$('#mce-EMAIL').val()
```

and preserves a browser-local GUID.

For a nonblank value it first POSTs:

```
/print/index.php

in    = user input
id    = persistent GUID
check = true
```

If the server does not return literal `false`, the client POSTs the same input and GUID again without the check flag and inserts the returned content into the print page.

So this is unquestionably a real hidden-answer consumer.

## Client-side grammar

The important negative is what the script **does not** validate.

There is no client-side:

- expected length;
- numeric-only rule;
- alphabet;
- ternary alphabet;
- nine-character requirement;
- phrase structure;
- checksum;
- coordinate syntax.

The only gate is effectively “not blank / whitespace.”

Correctness lives entirely on the server.

## Consequence

This historical mechanism strongly supports two architectural priors already useful to the sticker project:

1. Playdead used opaque server-side answer validation;
2. progression could be associated with a persistent per-client identifier.

But it gives us **no independent format cue** for deciding whether a future sticker answer should be:

- `112/012/120`;
- `100`;
- `--/--/-/-`;
- one of Experiment 410's nine-digit strings;
- plaintext;
- or something else.

That distinction prevents a very tempting circular move:

> “the old site accepted arbitrary text, therefore any derived sticker string is a plausible answer.”

The consumer architecture is licensed. The answer syntax is not.

## Repository consequence

The exact historical JavaScript is now preserved at:

`archive/external/playdead-unofficial-exports/assets/print-b58746938d8d0071.txt`

so future endpoint/consumer claims can be tested against source rather than recollection.

## Reopening trigger

A sticker-output representation should be paired to an answer endpoint only if another artifact independently supplies:

- the endpoint;
- the expected field or syntax;
- or a direct continuation cue from the CE material.

Do not spray frozen candidate strings into historical endpoints.
