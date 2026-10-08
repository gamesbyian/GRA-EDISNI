#!/usr/bin/env python3
"""Experiment 476: source-native receiving artifact and typed-input gates.

Fail loudly if the supported mirror's printed 22-slot interface, four
breach schemes, original CE path, or 84/66 foreground snapshot changes.

This audits preserved source files and explicit candidate projection
types. It does NOT prove missing backend software never existed, nor
solve any foreground code.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import json
import re

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "data/experiment-476-source-native-consumer-affordances.json"
MIRROR = ROOT / "archive/external/twinysam-inside-arg/terminal41.link"
VALID_IDS = {
    "secret_ending_lever", "playdead_printer_website_subscription_box",
    "terminal41_printer_four_schemes",
    "terminal41_viewgate_22_placeholder",
    "terminal41_saf_seven_fields", "ce_background_terminal41_path",
    "damaged_ce_jpeg", "terminal41_shutdown_nine_redirects",
    "ce_reversible_cover", "original_2016_secretmap",
    "original_switch_joycon_printer", "original_pc_acorn_life",
    "ce_art_card_set", "ce_foldout_poster", "ce_premium_spot_varnish_box"
}


def source(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def verify_viewgate():
    result = []
    for filename in ("comms_main_viewgate.html",
                     "comms_main_viewgate_002.html"):
        content = source(MIRROR / filename)
        hits = re.findall(r"Input:\[\s*((?:_\s*)+)\]", content)
        assert len(hits) == 1, (filename, len(hits))
        slots = hits[0].count("_")
        assert slots == 22, (filename, slots)
        forbidden = [
            t for t in (r"<\s*form\b", r"<\s*input\b",
                        r"<\s*select\b", r"\bmaxlength\s*=")
            if re.search(t, content, flags=re.I)
        ]
        assert not forbidden, (filename, forbidden)
        result.append({
            "source_path":filename, "printed_underscore_positions":slots,
            "html_form_control_count":0, "verified_input_handler":False
        })
    return result


def verify_status():
    html = source(MIRROR / "sys/printreqstatus_SD.html")
    schemes = {
        str(n): re.findall(r"\[>\s*([A-Z]+)\s*<\]", html)
        for n in range(4)
    }
    expected = ("PLANET", "LIFE", "PROBE", "CONDISCON")
    for word in expected:
        assert word in html, word
    indexes = sorted(set(re.findall(r"schem\[(\d+)\]",html)))
    assert indexes == ["0","1","2","3"], indexes
    assert "print requirements obtained(b)" in html
    assert "print requirements applied(b)" in html
    return {"scheme_indexes":indexes, "named_breach_tags":expected,
            "fifth_scheme_in_preserved_status":False}


def verify_static_ce_page():
    html = source(MIRROR / "dat/534brn9653f9j8mmd/index.html")
    assert "JFIF" in html and "Exif" in html
    assert "pe^!02un" in html
    assert "........\n..\n." in html.replace("\r\n","\n")
    return {
        "known_static_path":"dat/534brn9653f9j8mmd",
        "contains_JFIF_and_Exif_like_text":True,
        "footer_literal":"pe^!02un",
        "footer_dot_line_lengths":[8,2,1],
        "does_not_supply_verified_sticker_key_or_form":True,
        "limitation":"Truncated/malformed binary-in-HTML text. Do not infer byte-complete decoding."
    }


def verify_saf_island():
    data = json.loads(source(ROOT / "data/endgame-saf-dat-island-2026-10-08.json"))
    field_lengths = [f["length"] for f in data["fields"]]
    assert field_lengths == [26,22,10,2,3,1,5]
    token = data["fields"][1]["value"]
    assert len(token) == 22
    bits = int(token,36).bit_length()
    assert bits == 111 and bits > 108
    assert data["viewgate_html_input_controls"] == 0
    return {
        "source_fields":field_lengths,
        "field_one_value":token,
        "direct_unsigned_base36_bit_length":bits,
        "raw_108_binary_capacity_bits":108,
        "direct_unsigned_conversion_feasible":False
    }


def verify_observed_split():
    lines = source(ROOT / "data/observations.csv").strip().splitlines()
    records, observed = len(lines)-1,{}
    for line in lines[1:]:
        fields=line.split(",")
        residue,symbol=int(fields[1]),fields[2]
        assert residue not in observed or observed[residue]==symbol
        observed[residue]=symbol
    assert records==84 and len(observed)==66
    assert len([r for r in observed if r<=81])==54
    assert len([r for r in observed if r>=82])==12
    assert {v for r,v in observed.items() if r<=81}=={"/","-"}
    assert {v for r,v in observed.items() if r>=82}=={"/","."}
    return {
        "physical_records":records,"unique_residues":len(observed),
        "known_primary":54,"known_tail":12,
        "primary_only_lever_commands":["U","R"],
        "tail_only_lever_commands":["U","L"]
    }


def possible_direct_lever_sequence():
    """
    Existing bunker sequence from the historical 2016 secret-orb solve.
    A 14-char contiguous word drawn from H108 must respect:
    primary sector -> only U/R, tail sector -> only U/L.
    Cyclic offsets of the 14-command PASSWORD, both orientations and all
    cyclic H108 start positions are tested as a **necessary** type check,
    not a new cipher search or a fresh code discovery.
    """
    normal = "UURLRRRUUURLLL"
    assert len(normal)==14 and set(normal)=={"U","R","L"}
    permitted = [{"U","R"}]*81 + [{"U","L"}]*27
    variants = [
        normal[k:]+normal[:k] for k in range(len(normal))
    ]
    rev=normal[::-1]
    variants.extend(rev[k:]+rev[:k] for k in range(len(rev)))
    placements = []
    for word in variants:
        for start in range(108):
            if all(ch in permitted[(start+i)%108]
                   for i,ch in enumerate(word)):
                placements.append((word,start))
    assert not placements
    # For all selected-primary-depth readings, there are zero L symbols
    # irrespective of which unknown sticker values are assigned.
    return {
        "known_password":normal,"password_length":len(normal),
        "cyclic_password_orientations_tested":len(variants),
        "h108_cyclic_starts":108,
        "type_compatible_14_command_direct_placements":0,
        "primary_selected_readout_directly_equivalent_to_password":False,
        "why":"Known command sequence requires both L and R; one binary sector never supplies both."
    }


def main():
    registry=json.loads(source(REGISTRY))
    assert registry["schema_version"]==1
    artifacts=registry["native_artifacts"]
    ids=[a["id"] for a in artifacts]
    assert len(ids)==len(set(ids))==len(VALID_IDS)
    assert set(ids)==VALID_IDS
    for a in artifacts:
        assert a["primary_source"]
        src=a["primary_source"]
        if src.startswith(("docs/","data/","archive/")):
            assert (ROOT/src).exists(),(a["id"],src)
        assert not a["demonstrated_receives_new_ce_value"],a["id"]
        assert a["next_independent_evidence"]

    for item_id in ("ce_art_card_set", "ce_foldout_poster",
                    "ce_premium_spot_varnish_box"):
        item = next(a for a in artifacts if a["id"] == item_id)
        assert item["primary_source"] == (
            "https://www.iam8bit.com/products/inside-collector-s-edition"
        )
        assert not item["demonstrated_receives_new_ce_value"]
        assert item["ce_bridge_status"] == "no_native_register_or_reader"

    asset=json.loads(source(ROOT/"data/original-game-asset-consumer-inventory-2026-10-08.json"))
    assert any(a["id"]=="SecretMap" for a in asset["entries"])
    report={
        "schema_version":1,"experiment":476,
        "artifact_total":len(artifacts),
        "verified_new_ce_value_receivers":sum(
            a["demonstrated_receives_new_ce_value"] for a in artifacts),
        "viewgate":verify_viewgate(),
        "status_schemes":verify_status(),
        "ce_page":verify_static_ce_page(),
        "saf_island":verify_saf_island(),
        "foreground":verify_observed_split(),
        "known_lever_direct_replay_type_check":
            possible_direct_lever_sequence(),
        "historical_secretmap":{
            "native_texture_bytes_available":False,
            "contemporary_report_of_fourteenth_mark":True,
            "fourteenth_mark_already_suggested_as_large_orb_in_2016":True,
            "original_primary_url":next(
                a["contemporary_primary_url"] for a in artifacts
                if a["id"]=="original_2016_secretmap"),
            "meaning":"Contemporaneous interpretation, not confirmed pixel-to-orb registration."
        },
        "limitations":[
            "Zero verified consumer means absent in examined materials, not impossible in lost game/server versions.",
            "Visual cover/map sites require unchanged native assets and fixed registration before sticker comparison.",
            "Simple type compatibility never upgrades a speculative interpretation into a Playdead-authorized reader.",
            "No manufactured missing symbols, aesthetic plaintext fitting, or arbitrary rotations."
        ]
    }
    print(json.dumps(report,indent=2))


if __name__=="__main__":
    main()
