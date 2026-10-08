#!/usr/bin/env python3
"""Experiments 480-481: typed provenance assertions for original printer and poster.

No network requests, no remote POSTs, no copyrighted images downloaded.
These check the recorded evidence/chronology for internal consistency;
they do not replace verifying external original source bytes.
"""
from pathlib import Path
from urllib.parse import urlsplit
import json
import re

ROOT = Path(__file__).resolve().parents[1]


def read(relative):
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def audit_printer():
    d = read("data/experiment-480-original-printer-transport.json")
    assert d["experiment"] == 480 and d["schema_version"] == 1
    sources = {s["id"]: s for s in d["sources"]}
    assert set(sources) == {"steam-2018", "game-detectives",
                            "xbox-wire", "CE-chronology"}
    assert sources["steam-2018"]["date"] < sources["xbox-wire"]["date"] < sources["CE-chronology"]["date"]
    receiver = d["historically_reported_receiver"]
    assert "print button" in receiver["user_trigger"].lower()
    req = receiver["observed_requests"]
    assert [(x["method"],x["path"]) for x in req] == [
        ("POST", "/print/prepare.php"), ("POST", "/print/index.php")]
    for item in req:
        assert set(item["fields_reported"]) == {"email", "id", "check", "url"}
        assert item["status"]
    assert "window.print()" in receiver["browser_print"]
    classes = [x["case"] for x in receiver["response_classes"]]
    assert classes == [
        "empty", "nonempty_bad", "first_accepted",
        "second_accepted", "third_accepted"
    ]
    assert set(receiver["accepted_original_puzzle_phrases"]) == {
        "NEWPLANETDISCOVERED",
        "MULTIPLEPROBESDISPATCHED", "LIFEDETECTED"}
    assert "PDF" in " ".join(receiver["cautions"])
    assert not all(d["source_bytes_recovered"].values())
    assert len(d["recovery_priority"]) == 4
    # Important temporal/causal distinction: browser printing is an
    # observed client action; no server PDF bytes are asserted.
    assert d["source_bytes_recovered"]["original_printout_pdf"] is False
    return {
        "historical_witnesses": len(sources),
        "documented_POST_paths": [x["path"] for x in req],
        "response_classes": classes,
        "known_accepted_code_classes":len(receiver["accepted_original_puzzle_phrases"]),
        "original_server_response_bytes_available":False,
        "CE_specific_receiver_confirmed":False,
        "evidence_class":"source-verified externally; fixture-consistency-checked here",
    }


def audit_poster():
    d = read("data/experiment-481-poster-cross-edition-gallery.json")
    assert d["experiment"] == 481 and d["schema_version"] == 1
    ce = d["product_pages"]["CE"]
    standalone = d["product_pages"]["standalone"]
    assert ce["url"] != standalone["url"]
    assert "inside-collector-s-edition" in ce["url"]
    assert "inside-ps4-physical-game" in standalone["url"]
    assert "InsideCE_Lifestyle_00014" in ce["shown_gallery_asset"]
    assert "InsideCE_Lifestyle_00014" in standalone["shown_gallery_asset"]
    for listing in (ce,standalone):
        assert urlsplit(listing["url"]).hostname == "www.iam8bit.com"
        assert urlsplit(listing["shown_gallery_asset"]).hostname == "www.iam8bit.com"
    reuse = d["same_scene_evidence"]
    assert reuse["source_filename_stem"] == "InsideCE_Lifestyle_00014"
    assert "promotional source-image reuse" in reuse["confidence"]
    assert d["poster_front_as_pictured"]["rough_sketch_count"] == 9
    assert d["poster_front_as_pictured"]["complete_reverse_side_inspected"] is False
    assert d["poster_front_as_pictured"]["exact_label_mapping"] is False
    assert "Unknown" not in d["comparison_control"]["unavailable_externals"]
    assert len(d["comparison_control"]["unavailable_externals"]) >= 3
    prior=d["historical_prior_editions"]
    assert len(prior)==1
    assert prior[0]["source_class"].startswith("collector catalog")
    assert prior[0]["reported_release_date"] < "2019-12-01"
    assert "same poster design" in prior[0]["scope"]
    return {
        "official_product_pages":2,
        "same_promo_scene_source_stem":reuse["source_filename_stem"],
        "visually_reported_3_by_3_sketches":True,
        "identical_physical_sheet_confirmed":False,
        "A_I_foreground_receiver_confirmed":False,
        "evidence_class":"publisher source URLs and visible photo compared externally",
    }


def main():
    print(json.dumps({"printer":audit_printer(),"poster":audit_poster()},indent=2))


if __name__ == "__main__":
    main()
