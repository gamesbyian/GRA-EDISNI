#!/usr/bin/env python3
"""Rank public CE search-result JSONL for human review, without asserting ownership."""
import argparse, csv, json, re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
POSITIVE = [
 (r"(?i)\\b(?:my|mine|i bought|i got|i own|i received|i have|unboxed|selling my|sold my)\\b",4,"first_person_english"),
 (r"(?:届いた|購入した|買いました|持っています|開封した|買った|到着した)",4,"first_person_japanese"),
 (r"(?:我买了|我買了|收到了|收到貨|我有一套|開箱)",4,"first_person_chinese"),
 (r"(?:comprei|recebi|chegou aqui|eu tenho|vendi|vendo meu)",4,"first_person_portuguese"),
 (r"(?:lo compré|me llegó|tengo la edición|la vendí|vendo mi)",4,"first_person_spanish"),
 (r"(?:je l'ai acheté|je l'ai reçu|j'ai reçu|je possède|je vends)",4,"first_person_french"),
 (r"(?:habe ich gekauft|ist angekommen|ich besitze|verkaufe meine)",4,"first_person_german"),
 (r"(?:купил|купила|получил|получила|у меня есть|продаю)",4,"first_person_russian"),
 (r"(?i)(?:/|\\-|\\.)\\s?0?[0-9]{2,3}\\b",3,"potential_serial_requires_visual_confirmation"),
 (r"(?i)(?:sticker|label|serial|numbered|number|номер|シール|貼紙|编号|編號|etiqueta|Aufkleber|autocollant)",2,"number_or_label_discussion"),
 (r"(?i)(?:huddle|realdoll|iam8bit|playdead)",1,"ce_product_anchor")
]
NEGATIVE=[(r"(?i)(?:giveaway|concept art|soundtrack only|ps4 physical game only)",-2,"possibly_not_ce")]
def normalized(url):
    p=urlsplit(url.strip())
    if p.scheme not in ("https","http") or not p.netloc:return ""
    path=p.path.rstrip("/") or "/"
    query=urlencode(sorted((k,v) for k,v in parse_qsl(p.query) if k not in ("utm_source","utm_medium","utm_campaign","fbclid","gclid")))
    return urlunsplit((p.scheme.lower(),p.netloc.lower().removeprefix("www."),path,query,""))
def score(record):
    text=" ".join(str(record.get(k,"")) for k in ("title","snippet","description","text"))
    reasons=[];points=0
    for pattern,weight,reason in POSITIVE+NEGATIVE:
        if re.search(pattern,text):
            points+=weight;reasons.append(reason)
    return points,reasons
def triage(records,known_urls):
    grouped={}
    for row in records:
        url=normalized(str(row.get("url") or row.get("source_url") or ""))
        if not url:continue
        points,reasons=score(row)
        item=grouped.setdefault(url,{"url":url,"score":-999,"reason_codes":[],"original_title":"","original_excerpt":"","source_records":0,"canonical_url_match":url in known_urls,"status":"unverified_public_lead","new_confirmed_stickers":0})
        item["source_records"]+=1
        if points>item["score"]:
            item.update(score=points,reason_codes=reasons,original_title=str(row.get("title",""))[:250],original_excerpt=str(row.get("snippet") or row.get("text") or "")[:600])
    return sorted(grouped.values(),key=lambda r:(-r["score"],r["canonical_url_match"],r["url"]))
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--input",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    p.add_argument("--known-urls",type=Path)
    a=p.parse_args()
    known=set()
    if a.known_urls:
        for line in a.known_urls.read_text(encoding="utf-8").splitlines():
            for url in re.findall(r"https?://[^\\s<>\\])]+",line):
                known.add(normalized(url))
    records=[json.loads(x) for x in a.input.read_text(encoding="utf-8").splitlines() if x.strip()]
    out=triage(records,known)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text("".join(json.dumps(x,ensure_ascii=False)+"\\n" for x in out),encoding="utf-8")
    print(json.dumps({"input_records":len(records),"unique_source_urls":len(out),"unverified_candidates":sum(not x["canonical_url_match"] for x in out),"new_confirmed_stickers":0}))
if __name__=="__main__":main()
