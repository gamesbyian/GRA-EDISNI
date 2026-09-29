#!/usr/bin/env python3
"""One-shot Discord server text archive using an authorized bot account.

Uses only the Python standard library and Discord's HTTPS API. The bot token is
read from DISCORD_BOT_TOKEN and is never written to the export.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import time
import urllib.error
import urllib.parse
import urllib.request

API = "https://discord.com/api/v10"
USER_AGENT = "GRA-EDISNI-one-shot-discord-archive/1.0"


def api_get(path: str, token: str, params: dict[str, str | int] | None = None):
    url = API + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bot {token}",
            "User-Agent": USER_AGENT,
        },
    )
    while True:
        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                body = response.read()
                return json.loads(body) if body else None
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            if exc.code == 429:
                try:
                    retry_after = float(json.loads(body).get("retry_after", 1))
                except Exception:
                    retry_after = 1.0
                time.sleep(max(retry_after, 0.25))
                continue
            raise RuntimeError(f"Discord API {exc.code} for {url}: {body}") from exc


def safe_name(value: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in "-_." else "_" for c in value)
    return cleaned.strip("._") or "unnamed"


def list_channels(guild_id: str, token: str):
    channels = api_get(f"/guilds/{guild_id}/channels", token) or []
    # Discord text-capable channel types relevant to archival.
    text_types = {0, 5, 10, 11, 12, 15, 16}
    return [c for c in channels if c.get("type") in text_types]


def list_active_threads(guild_id: str, token: str):
    data = api_get(f"/guilds/{guild_id}/threads/active", token) or {}
    return data.get("threads", [])


def list_archived_threads(channel_id: str, token: str):
    # Public archived threads. Private archived threads require extra membership
    # semantics and are deliberately not swept by this minimal archival tool.
    out = []
    before = None
    while True:
        params = {"limit": 100}
        if before:
            params["before"] = before
        data = api_get(
            f"/channels/{channel_id}/threads/archived/public",
            token,
            params=params,
        ) or {}
        batch = data.get("threads", [])
        out.extend(batch)
        if not data.get("has_more") or not batch:
            break
        before = batch[-1].get("thread_metadata", {}).get("archive_timestamp")
        if not before:
            break
    return out


def fetch_messages(channel_id: str, token: str):
    messages = []
    before = None
    while True:
        params = {"limit": 100}
        if before:
            params["before"] = before
        batch = api_get(f"/channels/{channel_id}/messages", token, params=params) or []
        if not batch:
            break
        messages.extend(batch)
        before = batch[-1]["id"]
        if len(batch) < 100:
            break
    messages.reverse()
    return messages


def download_attachment(url: str, destination: pathlib.Path):
    destination.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            destination.write_bytes(response.read())
        return None
    except Exception as exc:
        return str(exc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--guild-id", required=True)
    parser.add_argument("--output", default="discord-export")
    parser.add_argument(
        "--channel-id",
        action="append",
        default=[],
        help="Restrict export to one or more channel/thread IDs.",
    )
    parser.add_argument("--download-attachments", action="store_true")
    parser.add_argument(
        "--include-archived-public-threads",
        action="store_true",
        help="Also enumerate archived public threads under accessible text/forum channels.",
    )
    args = parser.parse_args()

    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        raise SystemExit("DISCORD_BOT_TOKEN is required")

    root = pathlib.Path(args.output)
    root.mkdir(parents=True, exist_ok=True)

    guild = api_get(f"/guilds/{args.guild_id}", token)
    channels = list_channels(args.guild_id, token)
    active_threads = list_active_threads(args.guild_id, token)

    by_id = {str(c["id"]): c for c in channels + active_threads}

    if args.include_archived_public_threads:
        for channel in list(channels):
            if channel.get("type") not in {0, 5, 15, 16}:
                continue
            try:
                for thread in list_archived_threads(str(channel["id"]), token):
                    by_id.setdefault(str(thread["id"]), thread)
            except RuntimeError as exc:
                print(f"warning: archived threads for {channel['id']}: {exc}")

    wanted = set(args.channel_id)
    selected = [
        c for cid, c in by_id.items()
        if not wanted or cid in wanted
    ]
    selected.sort(key=lambda c: (int(c.get("position", 0)), str(c.get("id"))))

    manifest = {
        "schema_version": 1,
        "guild": {
            "id": str(guild.get("id")),
            "name": guild.get("name"),
        },
        "exported_channel_count": 0,
        "exported_message_count": 0,
        "channels": [],
    }

    for channel in selected:
        cid = str(channel["id"])
        name = channel.get("name") or cid
        try:
            messages = fetch_messages(cid, token)
        except RuntimeError as exc:
            print(f"skip {cid} #{name}: {exc}")
            continue

        record = {
            "id": cid,
            "name": name,
            "type": channel.get("type"),
            "parent_id": channel.get("parent_id"),
            "message_count": len(messages),
        }
        manifest["channels"].append(record)
        manifest["exported_channel_count"] += 1
        manifest["exported_message_count"] += len(messages)

        out = {
            "schema_version": 1,
            "guild_id": str(guild.get("id")),
            "guild_name": guild.get("name"),
            "channel": channel,
            "messages": messages,
        }
        file_path = root / "channels" / f"{safe_name(name)}--{cid}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"{cid} #{name}: {len(messages)} messages")

        if args.download_attachments:
            for message in messages:
                mid = str(message["id"])
                for attachment in message.get("attachments", []):
                    aid = str(attachment.get("id", "attachment"))
                    filename = safe_name(attachment.get("filename") or aid)
                    destination = root / "attachments" / cid / mid / f"{aid}--{filename}"
                    error = download_attachment(attachment["url"], destination)
                    if error:
                        print(f"warning: attachment {aid}: {error}")

    (root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"exported {manifest['exported_message_count']} messages from "
        f"{manifest['exported_channel_count']} channels"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
