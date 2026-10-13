#!/usr/bin/env python3
"""Optional localhost-only snapshot of INSIDE's live runtime via InsideDevTool.

Standard-library MCP-over-HTTP client. Default path only calls tools advertised
readOnlyHint=true. --with-logic explicitly opts into four FIXED "command"
queries; the upstream API classifies command as non-read-only, although these
specific queries are inspection-oriented. No game files or outputs enter Git.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import http.client
import json
from pathlib import Path
import sys

UPSTREAM = "RedMatterGG/InsideDevTool"
PINNED_REVISION = "bdc3bbd7d61f1eb77f9e01200493c14c5ac2650a"
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
SAFE_CALLS = frozenset({"game_state", "find_objects", "inspect", "fsm_find", "log"})
FIXED_LOGIC_COMMANDS = (
    "gamecode",
    "logic PrintingPaperEasterEgg",
    "logic SecretJoystick",
    "logic shared secret",
)
SNAPSHOT_CALLS = (
    ("game_state", {}),
    ("find_objects", {"query": "Printer"}),
    ("find_objects", {"query": "SecretJoystick"}),
    ("find_objects", {"query": "WristSecret"}),
    ("find_objects", {"query": "secret", "category": "scripts"}),
    ("fsm_find", {"text": "printSecretMessage"}),
    ("fsm_find", {"text": "Printer"}),
)

class ProtocolError(RuntimeError):
    pass


def validate_output_path(output: Path) -> Path:
    destination = output.resolve()
    repo = Path(__file__).resolve().parents[1]
    if destination == repo or repo in destination.parents:
        raise ValueError("Live game observations must be stored OUTSIDE this repository")
    return destination


class LocalInsideDev:
    """No customizable URL, host or executable transport, only loopback."""
    def __init__(self, port: int, *, timeout: float = 10.0):
        if type(port) is not int or not 1 <= port <= 65535:
            raise ValueError("Port must be 1 through 65535")
        self.port = port
        self.timeout = timeout
        self.session = None
        self.sequence = 0
        self.available = {}

    def request(self, method: str, params: dict | None = None) -> dict:
        self.sequence += 1
        payload = {
            "jsonrpc": "2.0", "id": self.sequence, "method": method,
            "params": params or {},
        }
        encoded = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Origin": "http://localhost",
            "MCP-Protocol-Version": "2025-06-18",
            "User-Agent": "GRA-EDISNI-local-readonly-recon/1",
        }
        if self.session:
            headers["Mcp-Session-Id"] = self.session
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=self.timeout)
        try:
            conn.request("POST", "/mcp", encoded, headers)
            reply = conn.getresponse()
            raw = reply.read(MAX_RESPONSE_BYTES + 1)
            if len(raw) > MAX_RESPONSE_BYTES:
                raise ProtocolError("MCP response over fixed 8 MiB bound")
            if reply.status != 200:
                raise ProtocolError("MCP HTTP status %d; is InsideDev running?" % reply.status)
            sid = reply.getheader("Mcp-Session-Id")
            if sid:
                if len(sid) > 128:
                    raise ProtocolError("Oversized MCP session header")
                self.session = sid
        except OSError as exc:
            raise ProtocolError(
                "InsideDev not reachable on 127.0.0.1:%d; game/plugin not connected"
                % self.port
            ) from exc
        finally:
            conn.close()
        try:
            obj = json.loads(raw)
        except (ValueError, UnicodeDecodeError) as exc:
            raise ProtocolError("Invalid MCP JSON") from exc
        if not isinstance(obj, dict) or obj.get("jsonrpc") != "2.0":
            raise ProtocolError("Invalid MCP JSON-RPC object")
        if obj.get("id") != payload["id"]:
            raise ProtocolError("MCP response ID mismatch")
        if "error" in obj:
            raise ProtocolError("MCP response error: %s" % str(obj["error"])[:300])
        result = obj.get("result")
        if not isinstance(result, dict):
            raise ProtocolError("Missing MCP result object")
        return result

    def initialize(self) -> dict:
        response = self.request("initialize", {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "GRA-EDISNI-local-evidence", "version": "1"},
        })
        name = (response.get("serverInfo") or {}).get("name")
        if name != "insidedev":
            raise ProtocolError("Unexpected MCP server identity: %r" % name)
        tools = self.request("tools/list").get("tools")
        if not isinstance(tools, list):
            raise ProtocolError("MCP tool list is missing")
        self.available = {
            tool["name"]: tool for tool in tools
            if isinstance(tool, dict) and isinstance(tool.get("name"), str)
        }
        return {"reported_server": response.get("serverInfo"),
                "reported_protocol": response.get("protocolVersion")}

    def call(self, name: str, args: dict, *, opt_in_logic: bool = False) -> dict:
        if name not in SAFE_CALLS:
            if name != "command" or not opt_in_logic:
                raise ValueError("Tool is not on read-only allowlist")
            if set(args) != {"command"} or args["command"] not in FIXED_LOGIC_COMMANDS:
                raise ValueError("Only four frozen inspection commands are permitted")
        if name not in self.available:
            raise ProtocolError("Tool not advertised by InsideDev: " + name)
        read_only = (self.available[name].get("annotations") or {}).get("readOnlyHint")
        if name in SAFE_CALLS and read_only is not True:
            raise ProtocolError("Tool lacks readOnlyHint=true: " + name)
        if name == "command" and read_only is not False:
            raise ProtocolError("Upstream command annotation changed; re-audit before use")
        # Validate shapes, so caller-supplied arguments can never bypass tool control.
        expected = {
            "game_state": set(),
            "find_objects": {"query", "category"},
            "inspect": {"object", "deep"},
            "fsm_find": {"text"},
            "log": {"lines"},
        }
        if name in expected and not set(args).issubset(expected[name]):
            raise ValueError("Unrecognized arguments for " + name)
        result = self.request("tools/call", {"name": name, "arguments": args})
        if result.get("isError") is True:
            raise ProtocolError("InsideDev tool failed: " + name)
        content = result.get("content")
        if not isinstance(content, list) or any(
            not isinstance(x, dict) or x.get("type") != "text"
            for x in content
        ):
            raise ProtocolError("Non-text result; refusing to ingest binary or screenshot")
        return {"tool": name, "args": args,
                "text": "\n".join(str(x.get("text", "")) for x in content)}


def collect(client: LocalInsideDev, *, with_logic: bool = False) -> dict:
    intro = client.initialize()
    observations = [client.call(name, args) for name, args in SNAPSHOT_CALLS]
    if with_logic:
        observations.extend(
            client.call("command", {"command": line}, opt_in_logic=True)
            for line in FIXED_LOGIC_COMMANDS
        )
    return {
        "schema": "inside-local-live-consumer-v1",
        "captured_utc": datetime.now(timezone.utc).isoformat(),
        "upstream_project": UPSTREAM,
        "upstream_source_commit": PINNED_REVISION,
        "source": "user-controlled running game + optional third-party injected editor",
        "localhost_only": True,
        "default_only_upstream_readonly_tools": not with_logic,
        "optional_logic_uses_nonreadonly_mcp_command": with_logic,
        "binary_witness_authenticated": False,
        "sticker_consumer_identified": False,
        "transport": intro,
        "observations": observations,
        "limits": [
            "An MCP server name/version is self-reported, not cryptographic authentication",
            "Read-only tool hints are upstream claims, not security guarantees",
            "All results are scoped to currently loaded scenes and available code",
            "Logic commands optionally change the editor display and run code scans",
            "Negative results do not establish absence in other scenes/builds",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=47811)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--with-logic", action="store_true",
                        help="OPT-IN: run four fixed inspect-only commands using upstream non-readonly command tool")
    a = parser.parse_args()
    try:
        path = validate_output_path(a.output)
        report = collect(LocalInsideDev(a.port), with_logic=a.with_logic)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    except (OSError, ValueError, ProtocolError) as exc:
        print("No snapshot produced: "+str(exc), file=sys.stderr)
        return 2
    print("Local snapshot written to "+str(path))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
