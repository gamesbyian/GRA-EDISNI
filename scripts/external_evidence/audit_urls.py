#!/usr/bin/env python3
"""Audit acquisition targets without downloading large media."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import ssl
import urllib.error
import urllib.request
from pathlib import Path


UA = "GRA-EDISNI-evidence-audit/1.0 (+https://github.com/gamesbyian/GRA-EDISNI)"


def load_sources(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))["sources"]


def classify(code: int | None, final_url: str | None, requested: str, error: str | None) -> str:
    if error:
        e = error.lower()
        if "429" in e:
            return "rate-limited"
        if "401" in e or "403" in e:
            return "login-required-or-forbidden"
        if "404" in e or "410" in e:
            return "removed-or-missing"
        return "network-error"
    if code in (401, 403):
        return "login-required-or-forbidden"
    if code in (404, 410):
        return "removed-or-missing"
    if code == 429:
        return "rate-limited"
    if final_url and final_url.rstrip("/") != requested.rstrip("/"):
        return "redirected"
    if code and 200 <= code < 400:
        return "live"
    return "unknown"


def probe(source: dict, timeout: int) -> dict:
    url = source["url"]
    result = {
        "id": source["id"],
        "kind": source["kind"],
        "requested_url": url,
        "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ssl.create_default_context()) as resp:
            result["status_code"] = resp.status
            result["final_url"] = resp.geturl()
            result["content_type"] = resp.headers.get("Content-Type")
            result["content_length"] = resp.headers.get("Content-Length")
            result["classification"] = classify(resp.status, resp.geturl(), url, None)
            return result
    except urllib.error.HTTPError as exc:
        # Some sites reject HEAD while serving GET. Retry a tiny ranged GET.
        if exc.code in (400, 403, 405):
            get_req = urllib.request.Request(
                url,
                method="GET",
                headers={"User-Agent": UA, "Range": "bytes=0-0"},
            )
            try:
                with urllib.request.urlopen(get_req, timeout=timeout) as resp:
                    result["status_code"] = resp.status
                    result["final_url"] = resp.geturl()
                    result["content_type"] = resp.headers.get("Content-Type")
                    result["classification"] = classify(resp.status, resp.geturl(), url, None)
                    return result
            except Exception as retry_exc:  # noqa: BLE001
                result["error"] = repr(retry_exc)
                result["classification"] = classify(None, None, url, result["error"])
                return result
        result["status_code"] = exc.code
        result["error"] = repr(exc)
        result["classification"] = classify(exc.code, None, url, result["error"])
        return result
    except Exception as exc:  # noqa: BLE001
        result["error"] = repr(exc)
        result["classification"] = classify(None, None, url, result["error"])
        return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=Path("data/external-acquisition-targets.json"))
    parser.add_argument("--output", type=Path, default=Path("evidence-work/url-audit.json"))
    parser.add_argument("--timeout", type=int, default=20)
    args = parser.parse_args()

    results = [probe(source, args.timeout) for source in load_sources(args.manifest)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "results": results,
            },
            indent=2,
            sort_keys=True,
        ) + "\n",
        encoding="utf-8",
    )

    counts: dict[str, int] = {}
    for item in results:
        counts[item["classification"]] = counts.get(item["classification"], 0) + 1
    print(json.dumps(counts, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
