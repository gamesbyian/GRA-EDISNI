#!/usr/bin/env python3
"""CL09: verify historically photographed Terminal41 namespace exceeds mirror.

Both inputs local JSON, standard library. Assert pinned screenshot and
historic export provenance and the documented entries. Do NOT assert they
must remain absent: if archivists recover a page, status should improve,
not cause a failing test.
"""
from pathlib import Path
import json

BASE=Path(__file__).resolve().parents[1]
SOURCE=BASE/"data"/"terminal41-screenshot-index-gaps-2026-10-08.json"
MIRROR=BASE/"data"/"terminal41-source-tree.json"

def check():
    x=json.loads(SOURCE.read_text(encoding="utf8"))
    m=json.loads(MIRROR.read_text(encoding="utf8"))
    assert x["source"]["historical_public_discord_export"]["git_blob_sha"]=="1889cc948f86f5a4455de0d7310b15cdb1b88b5c"
    p=x["source"]["historical_screenshots"]
    assert len(p)==4 and [t["git_blob_sha"] for t in p]==[
      "48cdd698a5d9303609cd2659d020a0c31a52cffc",
      "e3d7287527a5482cb58a41837873f396e0c79ee7",
      "a56809a9856020489a87ff38d114ae4a67d83964",
      "95bb5aaec9a9f2da0966744fbc80b67f7f358c99"
    ]
    assert m["source_tree_sha"]=="4de72d7c2f21bd9eb4144fda51281c84cbcb90c4"
    assert len(m["files"])==m["count"]==74
    entries=x["directory_entries"]
    assert len(entries)==11
    paths=[e["path"] for e in entries]
    assert len(paths)==len(set(paths))
    all_terminal=sorted(int(p.split("/")[-2]) for p in paths if p.startswith("sys/terminate_terminal/"))
    assert all_terminal==[11,23,41,42,99]
    known=set(e["path"] for e in m["files"])
    prefix="terminal41.link/"
    known={k[len(prefix):] if k.startswith(prefix) else k for k in known}
    statuses=[]
    for e in entries:
        path=e["path"]
        hits=[k for k in known if k==path or (path.endswith("/") and k.startswith(path))]
        statuses.append({"path":path,"evidence":e["confidence"],
                         "currently_archived_files":len(hits)})
    missing=[e for e in statuses if not e["currently_archived_files"]]
    assert len(missing)==10,missing
    assert len([e for e in statuses if e["currently_archived_files"]])==1
    assert statuses[3]["path"]=="sys/terminate_terminal/41/"
    assert statuses[3]["currently_archived_files"]>0
    # The fixed Sep-29 mirror is pinned as a historical comparison, so the
    # 10/11 count is for that exact snapshot; it is not a ban on later rescue.
    print("CL09 PASS: 11 screenshot-attested directory/file targets, 10 absent in pinned 74-file mirror")
    print("CL09 PASS: five terminal-number directories include 11,23,41,42,99; only 41 mirrored")
    print("CL09 PASS: 4 original screenshot blob identities and exact original Discord source")
    return {"mirror_sha":m["source_tree_sha"],"source_index_entries":len(entries),
            "mirror_missing_count":len(missing),"still_unmirrored":missing}

if __name__=="__main__":
    check()
