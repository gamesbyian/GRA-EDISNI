#!/usr/bin/env python3
"""Experiment 411: typed-input inventory of the archived Terminal41 snapshot."""

from pathlib import Path
import json, re

ROOT=Path(__file__).resolve().parents[1]
TREE=ROOT/"data"/"terminal41-source-tree.json"
VENDOR=ROOT/"archive"/"external"/"twinysam-inside-arg"
OUT=ROOT/"data"/"experiment-411-terminal41-input-grammar-inventory.json"

TAGS=("form","input","select","textarea","button")

def main():
    tree=json.loads(TREE.read_text(encoding="utf-8"))
    text_files=[f for f in tree["files"] if f["media_class"]=="text-or-unknown"]
    assert len(tree["files"])==74
    assert len(text_files)==73

    counts={tag:0 for tag in TAGS}
    files_with_tags=[]
    meta_refresh=0
    directory_indexes=0

    for item in text_files:
        path=VENDOR/item["path"]
        text=path.read_text(encoding="utf-8",errors="replace")
        local={}
        for tag in TAGS:
            n=len(re.findall(rf"<{tag}\b",text,re.I))
            counts[tag]+=n
            if n:
                local[tag]=n
        if local:
            files_with_tags.append({"path":item["path"],"tags":local})
        if re.search(r'http-equiv\s*=\s*["\']?refresh',text,re.I):
            meta_refresh+=1
        if re.search(r"<title>Index of /",text,re.I):
            directory_indexes+=1

    # The preserved static snapshot exposes navigation/state pages, not typed input widgets.
    assert counts["form"]==0
    assert counts["input"]==0
    assert counts["select"]==0
    assert counts["textarea"]==0

    result={
        "experiment":411,
        "source_tree_files":len(tree["files"]),
        "text_files_scanned":len(text_files),
        "html_tag_counts":counts,
        "files_with_input_like_tags":files_with_tags,
        "meta_refresh_file_count":meta_refresh,
        "directory_index_file_count":directory_indexes,
        "interpretation":(
            "The complete vendored Terminal41 text snapshot contains no forms, input fields, selects or textareas. "
            "It preserves routes, redirects and state pages but no typed nine-value/ternary/numeric consumer grammar. "
            "Therefore static Terminal41 pages cannot currently supply the missing downstream interface for E2, "
            "Experiment-398, or the 9+3 numeric surfaces."
        ),
        "scope":(
            "This is a statement about the preserved Terminal41 snapshot only. Historical Playdead-site JavaScript "
            "and subscription-box endpoints are separate evidence and did accept solver input."
        ),
    }
    OUT.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2))

if __name__=="__main__":
    main()
