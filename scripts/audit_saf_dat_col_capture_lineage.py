#!/usr/bin/env python3
"""CL11: original April 2019 saf_dat_col capture lineage and 2023 archive census.

Research purpose: assess whether the Apr 16 UTF-16 saved browser text
preserves any non-whitespace characters that are absent from the Apr 14
raw-curl page. It is NOT a 2019 BACKUP file or raw BMP/JPEG recovery.

Offline fixture mode needs stdlib and no external data. Full reproduction
requires the Apr 16 original from publicly archived 2019 Discord file and
(optionally) original Jan 2023 collected Terminal41 zip. Both checks use
Git raw blob hashes; no guessed code, 108-symbol CE stream or decoded text.
"""
from __future__ import annotations
import argparse
from hashlib import sha1
import json
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"data"/"conjecture-lab-saf-dat-col-original-captures-2026-10-08.json"
MIRROR=ROOT/"archive"/"external"/"twinysam-inside-arg"/"terminal41.link"
SRC={
 "apr14":("349b818fce618ef55c404bedfb602b1d03f29a48",1986163),
 "apr16":("6ca8c90711a54944850fdaf94a0ead1fab887686",2053806),
 "jan2023zip":("4f8958bd45a0e8874483b33e46e56a6a3b37a2f1",1605024),
}
def git_sha(data):
    return sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def checked(path,kind):
    data=Path(path).read_bytes()
    assert (git_sha(data),len(data))==SRC[kind],(kind,len(data),git_sha(data))
    return data
def audit_captures(a,b):
    a=a.decode("utf-8-sig")
    b=b.decode("utf-16")
    assert a.count("\ufffd")==b.count("\ufffd")==1900
    a_parts=["".join(x.split()) for x in a.split("\ufffd")]
    b_parts=["".join(x.split()) for x in b.split("\ufffd")]
    assert len(a_parts)==len(b_parts)==1901
    exact=sum(x==y for x,y in zip(a_parts,b_parts))
    subseq=0
    different=[]
    for i,(x,y) in enumerate(zip(a_parts,b_parts)):
        if x!=y:
            different.append({"replacement_segment_index":i,
                              "normalized_apr14_chars":len(x),
                              "normalized_apr16_chars":len(y),
                              "removed_nonwhitespace_chars":len(x)-len(y)})
        pos=0
        for ch in y:
            pos=x.find(ch,pos)
            if pos<0: break
            pos+=1
        else: subseq+=1
    return {
       "april14_decoded_chars":len(a),
       "april16_decoded_chars":len(b),
       "replacement_character_count_each":1900,
       "same_order_replacement_bounded_segments":1901,
       "identical_normalized_segments":exact,
       "subsequence_normalized_segments":subseq,
       "different_segments":different,
    }
def audit_zip(raw):
    with ZipFile(__import__("io").BytesIO(raw)) as z:
        files=sorted(info.filename for info in z.infolist() if not info.is_dir())
        expected=ROOT/"archive"/"external"/"twinysam-inside-arg"/"terminal41.link"
        missing=[]; divergent=[]; same=[]
        for name in files:
            local=expected/name
            if not local.is_file(): missing.append(name);continue
            b=z.read(name)
            c=local.read_bytes()
            if b==c: same.append(name)
            else: divergent.append({"path":name,"zip_sha1":git_sha(b),"mirror_sha1":git_sha(c)})
        return {
         "archived_regular_files":len(files),
         "archived_uncompressed_bytes":sum(z.getinfo(name).file_size for name in files),
         "same_bytes_as_mirror":len(same),
         "no_corresponding_current_mirror_file":missing,
         "different_content":divergent,
         "contains_explicit_backup_filename":any("BACKUP" in n.upper() for n in files),
        }
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--apr16",type=Path,
         help="Apr 16 2019 original UTF-16 Discord attachment, not original BACKUP file")
    p.add_argument("--jan2023zip",type=Path,
         help="Jan 25 2023 community-compiled Terminal41 pages ZIP")
    p.add_argument("--summary-json",type=Path)
    args=p.parse_args()
    d=json.loads(FIXTURE.read_text(encoding="utf8"))
    assert d["source_git_blobs"]=={
         k:{"sha1":v[0],"bytes":v[1]} for k,v in SRC.items()
    }
    assert d["april16_is_authored_backup"] is False
    assert d["contains_new_nonwhitespace_codepoints_in_april16"] is False
    assert d["corrected_payload_original_bytes"]==0
    orig=checked(MIRROR/"dat"/"saf_dat_col.html","apr14")
    output={"fixture_verified":True,"original_apr14_git_blob_sha":git_sha(orig)}
    if args.apr16:
        result=audit_captures(orig,checked(args.apr16,"apr16"))
        assert result==d["capture_comparison"],(result,d["capture_comparison"])
        output["capture"]=result
    if args.jan2023zip:
        result=audit_zip(checked(args.jan2023zip,"jan2023zip"))
        assert result==d["archive_zip_comparison"],(result,d["archive_zip_comparison"])
        output["archive"]=result
    if args.summary_json:args.summary_json.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps(output,indent=2))
if __name__=="__main__":
    main()
