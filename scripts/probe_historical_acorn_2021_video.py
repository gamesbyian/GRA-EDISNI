#!/usr/bin/env python3
"""Read-only bounded recovery of one SOURCE-LITERAL 2021 acorn overlay video.

The exact Discord CDN attachment URL comes from the archived #tldr
message dated 2021-06-25; neither URL nor file name is guessed.
Report all HTTP/MIME results even if no video is recovered. Do not
submit to the original game site, try private Discord APIs, or brute
force expired CDN query strings.
"""
import hashlib
import json
import pathlib
import urllib.error
import urllib.parse
import urllib.request

URL="https://cdn.discordapp.com/attachments/461275582970462209/857907060334919700/acorn.mp4"
MAX_SIZE=36*1024*1024
OUTPUT=pathlib.Path("archive_video_probe")
HOSTS={"cdn.discordapp.com","media.discordapp.net","cdn.discordapp.net"}

class LimitedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, url):
        p=urllib.parse.urlparse(url)
        if p.scheme!="https" or p.hostname not in HOSTS:
            raise ValueError(f"Non-source CDN redirect forbidden: {p.hostname}")
        return super().redirect_request(request,fp,code,msg,headers,url)

def run():
    OUTPUT.mkdir(parents=True,exist_ok=True)
    result={
       "source":"gamesbyian/playdead-unofficial-exports archived #tldr dated 2021-06-25",
       "source_original_url":URL,
       "source_discord_message":"https://discord.com/channels/460626942190813184/461275582970462209/852612048482336788",
       "retrieval_attempt":"one HTTP GET for the one literal known 2021 video, no guessing",
       "status":"not_attempted","video_authenticated":False,
       "original_2021_git_sha":None,
       "note":"Even recovered valid MP4 bytes could be a CDN rendition; only original 2021 source provenance attests claimed use."
    }
    request=urllib.request.Request(URL,headers={
       "User-Agent":"INSIDE historical source check/1.0",
       "Accept":"video/mp4,application/octet-stream"
    })
    try:
        with urllib.request.build_opener(LimitedRedirect()).open(request,timeout=35) as response:
            length=int(response.headers.get("Content-Length","0"))
            result["http_status"]=response.status
            result["response_content_type"]=response.headers.get("Content-Type")
            result["final_url_host"]=urllib.parse.urlparse(response.url).hostname
            if length>MAX_SIZE:
                raise ValueError("Video exceeds fixed 36 MB size cap")
            data=response.read(MAX_SIZE+1)
            if len(data)>MAX_SIZE:
                raise ValueError("Video exceeds fixed 36 MB size cap")
            is_mp4=(len(data)>=12 and data[4:8]==b"ftyp")
            result.update({"response_bytes":len(data),"mp4_ftyp_magic":is_mp4,
                           "sha256":hashlib.sha256(data).hexdigest()})
            if not is_mp4:
                result["status"]="non_mp4_response_rejected"
            else:
                out=OUTPUT/"acorn-2021-cdn-retrieved.mp4"
                out.write_bytes(data)
                result["status"]="retrieved_video_candidate"
                result["candidate_file"]=out.name
                result["video_authenticated"]=False
    except urllib.error.HTTPError as exc:
        result.update({"status":"http_unavailable","http_status":exc.code,
                       "reason":str(exc.reason)[:250]})
    except Exception as exc:
        result.update({"status":"request_failed","reason":str(exc)[:250]})
    (OUTPUT/"report.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,indent=2))
    return result

if __name__=="__main__":
    run()
