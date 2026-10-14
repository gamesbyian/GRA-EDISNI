#!/usr/bin/env python3
"""Offline public CE lead ranking. Review queue, never evidence confirmation.

Accepts original-search JSONL (url/title/description/text) and existing
Brave index executor JSONL (matches array). Never fetches websites or contacts
individuals. Scores claims, not people; no private identity resolution.
"""
from __future__ import annotations
import argparse
import csv
import json
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

POSITIVE = (
    (r"\b(?:my|mine|i bought|i got|i own|i received|i have|unboxed|selling my|sold my)\b", 4, "first_person_en"),
    (r"(?:届いた|購入した|買いました|持っています|開封した|買った|到着した)", 4, "first_person_ja"),
    (r"(?:我买了|我買了|收到了|收到貨|我有一套|開箱)", 4, "first_person_zh"),
    (r"(?:comprei|recebi|chegou aqui|eu tenho|vendi|vendo meu)", 4, "first_person_pt"),
    (r"(?:lo compré|me llegó|tengo la edición|la vendí|vendo mi)", 4, "first_person_es"),
    (r"(?:je l'ai acheté|je l'ai reçu|j'ai reçu|je possède|je vends)", 4, "first_person_fr"),
    (r"(?:habe ich gekauft|ist angekommen|ich besitze|verkaufe meine)", 4, "first_person_de"),
    (r"(?:купил|купила|получил|получила|у меня есть|продаю)", 4, "first_person_ru"),
    (r"(?:/|-|\.)\s?0?[0-9]{2,3}\b", 2, "numeric_candidate_not_serial_proof"),
    (r"(?:sticker|label|serial|numbered|number|номер|シール|貼紙|编号|編號|etiqueta|Aufkleber|autocollant)", 2, "number_label_mentioned"),
    (r"(?:huddle|realdoll|iam8bit|playdead)", 2, "ce_anchor"),
)
NEGATIVE = ((r"(?:soundtrack only|ps4 physical game only|flight simulator|larian)", -4, "possible_unrelated_or_standalone"),)
TRACKING = {"utm_source","utm_medium","utm_campaign","utm_content","utm_term","fbclid","gclid"}

def normalize_url(url: str) -> str:
    try:
        p = urlsplit(url.strip())
        if p.scheme.lower() not in ("http", "https") or not p.hostname:
            return ""
        host = p.hostname.lower()
        if host in ("reddit.com", "www.reddit.com", "old.reddit.com",
                    "new.reddit.com", "sh.reddit.com"):
            match = re.search(r"/comments/([a-z0-9]+)(?:/|$)", p.path, re.I)
            if match:
                thread_id = match.group(1).lower()
                remainder = [piece for piece in p.path[match.end():].split("/") if piece]
                comment_id = ""
                if len(remainder) >= 2 and remainder[0].lower() == "comment":
                    comment_id = remainder[1].lower()
                elif len(remainder) >= 2 and re.fullmatch(r"[a-z0-9]+", remainder[1], re.I):
                    comment_id = remainder[1].lower()
                return ("https://reddit.com/comments/" + thread_id +
                        ("/comment/" + comment_id if comment_id else ""))
        query = urlencode(sorted((k,v) for k,v in parse_qsl(p.query,keep_blank_values=True)
                                 if k.lower() not in TRACKING))
        return urlunsplit(("https",p.netloc.lower().removeprefix("www."),
                           p.path.rstrip("/") or "/",query,""))
    except ValueError:
        return ""

def score(row: dict) -> tuple[int,list[str]]:
    text = " ".join(str(row.get(k) or "") for k in ("title","snippet","description","text"))
    pts, reasons = 0, []
    for pattern,weight,name in POSITIVE+NEGATIVE:
        if re.search(pattern,text,re.IGNORECASE):
            pts += weight
            reasons.append(name)
    return pts, reasons

def iter_hits(records):
    for row in records:
        if not isinstance(row,dict):
            continue
        if "matches" in row:
            if row.get("status") != "index_search_success":
                continue
            if not isinstance(row["matches"],list):
                continue
            for hit in row["matches"]:
                if isinstance(hit,dict):
                    yield hit
        else:
            yield row

def load_known_source_crosswalk(path: Path) -> dict[str, dict]:
    """Human-reviewed exact source URL relations, never heuristic owner matching."""
    required = {"source_url", "canonical_record", "source_relation",
                "evidence_note", "review_status"}
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("Malformed known-source crosswalk header")
        result = {}
        for row in reader:
            url = normalize_url(row["source_url"])
            if not url or url in result:
                raise ValueError("Invalid or duplicate crosswalk source URL")
            if not row["canonical_record"] or not row["review_status"]:
                raise ValueError("Missing explicit source review context")
            result[url] = row
        return result

def triage(records, known_urls, known_source_crosswalk=None):
    known = {normalize_url(x) for x in known_urls}
    crosswalk = known_source_crosswalk or {}
    grouped = {}
    for hit in iter_hits(records):
        url = normalize_url(str(hit.get("url") or hit.get("source_url") or ""))
        if not url:
            continue
        points,reasons=score(hit)
        link = crosswalk.get(url)
        item=grouped.setdefault(url,{
            "url":url,"score":-999,"reason_codes":[],
            "original_title":"","original_excerpt":"","source_records":0,
            "canonical_url_match":url in known,
            "crosswalk_record":link["canonical_record"] if link else "",
            "crosswalk_relation":link["source_relation"] if link else "",
            "crosswalk_review_status":link["review_status"] if link else "",
            "status":"existing_case_context_review" if link else "unverified_public_lead",
            "new_confirmed_stickers":0,
        })
        item["source_records"]+=1
        if points > item["score"]:
            item.update(score=points,reason_codes=reasons,
                        original_title=str(hit.get("title") or "")[:250],
                        original_excerpt=str(hit.get("snippet") or hit.get("description") or hit.get("text") or "")[:600])
    return sorted(grouped.values(),key=lambda r:(
        bool(r["crosswalk_record"]) or r["canonical_url_match"],
        -r["score"], r["url"]))

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--known-urls",type=Path)
    p.add_argument("--known-source-crosswalk",type=Path,
                   help="Curated exact-URL canonical owner/sticker reconciliation TSV")
    a=p.parse_args()
    known=[]
    if a.known_urls:
        known=re.findall(r'https?://[^\s<>\])"]+',a.known_urls.read_text(encoding="utf-8"))
    records=[json.loads(x) for x in a.input.read_text(encoding="utf-8").splitlines() if x.strip()]
    crosswalk=(load_known_source_crosswalk(a.known_source_crosswalk)
               if a.known_source_crosswalk else {})
    out=triage(records,known,crosswalk)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text("".join(json.dumps(x,ensure_ascii=False)+"\n" for x in out),encoding="utf-8")
    print(json.dumps({"input_records":len(records),"unique_source_urls":len(out),
                      "unverified_candidates":sum(not x["canonical_url_match"] and not x["crosswalk_record"] for x in out),
                      "known_case_source_matches":sum(bool(x["crosswalk_record"]) for x in out),
                      "new_confirmed_stickers":0}))
if __name__=="__main__":
    main()
