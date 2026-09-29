#!/usr/bin/env python3
"""One-shot Discord server text archive using an authorized bot account.

Uses only the Python standard library and Discord's HTTPS API. The bot token is
read from DISCORD_BOT_TOKEN and is never written to the export.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
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


def anonymous_alias(user_id: str, salt: bytes) -> str:
    digest = hashlib.sha256(salt + user_id.encode("utf-8")).hexdigest()[:10]
    return f"poster-{digest}"


def sanitize_user(user: dict, salt: bytes) -> dict:
    user_id = str(user.get("id") or "unknown")
    alias = anonymous_alias(user_id, salt)
    return {
        "id": alias,
        "username": alias,
        "global_name": None,
        "discriminator": "0",
        "avatar": None,
        "bot": bool(user.get("bot", False)),
        "system": bool(user.get("system", False)),
    }


def anonymize_message(value, salt: bytes):
    """Remove Discord user identity metadata before an export is serialized."""
    if isinstance(value, list):
        return [anonymize_message(item, salt) for item in value]
    if not isinstance(value, dict):
        return value

    out = {}
    for key, item in value.items():
        if key in {"author", "user"} and isinstance(item, dict):
            out[key] = sanitize_user(item, salt)
        elif key == "member" and isinstance(item, dict):
            # Guild membership metadata can itself be identifying and is not
            # needed for the puzzle archive.
            out[key] = {"anonymized": True}
        elif key == "mentions" and isinstance(item, list):
            out[key] = [
                sanitize_user(mention, salt) if isinstance(mention, dict) else mention
                for mention in item
            ]
        else:
            out[key] = anonymize_message(item, salt)
    return out


def replace_user_mentions(value, aliases: dict[str, str]):
    """Replace Discord <@snowflake> tokens in strings with anonymous aliases."""
    if isinstance(value, str):
        for user_id, alias in aliases.items():
            value = value.replace(f"<@{user_id}>", f"@{alias}")
            value = value.replace(f"<@!{user_id}>", f"@{alias}")
        return value
    if isinstance(value, list):
        return [replace_user_mentions(item, aliases) for item in value]
    if isinstance(value, dict):
        return {key: replace_user_mentions(item, aliases) for key, item in value.items()}
    return value


def collect_user_ids(value, found: set[str]) -> None:
    if isinstance(value, list):
        for item in value:
            collect_user_ids(item, found)
        return
    if not isinstance(value, dict):
        return
    for key, item in value.items():
        if key in {"author", "user"} and isinstance(item, dict) and item.get("id"):
            found.add(str(item["id"]))
        elif key == "mentions" and isinstance(item, list):
            for mention in item:
                if isinstance(mention, dict) and mention.get("id"):
                    found.add(str(mention["id"]))
        collect_user_ids(item, found)


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
    parser.add_argument(
        "--channel-name",
        action="append",
        default=[],
        help="Restrict export to one or more exact channel/thread names.",
    )
    parser.add_argument("--download-attachments", action="store_true")
    parser.add_argument(
        "--anonymize-authors",
        action="store_true",
        help="Pseudonymize poster/user identity metadata before writing export files.",
    )
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

    wanted_ids = set(args.channel_id)
    wanted_names = set(args.channel_name)
    if wanted_names:
        available_names = {str(c.get("name") or "") for c in by_id.values()}
        missing_names = sorted(wanted_names - available_names)
        if missing_names:
            raise SystemExit(
                "Requested channel/thread name(s) not visible to bot: "
                + ", ".join(missing_names)
            )

    selected = [
        c for cid, c in by_id.items()
        if (not wanted_ids and not wanted_names)
        or cid in wanted_ids
        or str(c.get("name") or "") in wanted_names
    ]
    selected.sort(key=lambda c: (int(c.get("position", 0)), str(c.get("id"))))

    anonymization_salt = secrets.token_bytes(32) if args.anonymize_authors else None

    manifest = {
        "schema_version": 1,
        "authors_anonymized": bool(args.anonymize_authors),
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

        export_messages = messages
        if anonymization_salt is not None:
            user_ids: set[str] = set()
            collect_user_ids(messages, user_ids)
            aliases = {
                user_id: anonymous_alias(user_id, anonymization_salt)
                for user_id in user_ids
            }
            export_messages = anonymize_message(messages, anonymization_salt)
            export_messages = replace_user_mentions(export_messages, aliases)

        out = {
            "schema_version": 1,
            "authors_anonymized": bool(args.anonymize_authors),
            "guild_id": str(guild.get("id")),
            "guild_name": guild.get("name"),
            "channel": channel,
            "messages": export_messages,
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
