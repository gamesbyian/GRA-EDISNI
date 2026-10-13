#!/usr/bin/env python3
"""A fake loopback MCP server, never actual game or mod code."""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
import tempfile
import threading
import unittest

from acquire_insidedev_consumer_snapshot import (
    LocalInsideDev, ProtocolError, SAFE_CALLS, SNAPSHOT_CALLS,
    collect, validate_output_path,
)

class FakeHandler(BaseHTTPRequestHandler):
    def log_message(self, *args): pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(n))
        self.server.events.append({
            "path": self.path, "method": data.get("method"),
            "params": data.get("params", {}), "origin": self.headers.get("Origin"),
        })
        method = data["method"]
        if method == "initialize":
            result = {"protocolVersion": "2025-06-18",
                      "serverInfo": {"name": self.server.identity, "version": "fake"}}
        elif method == "tools/list":
            result = {"tools": [
                {"name": name, "annotations": {"readOnlyHint": name != "command"}}
                for name in [*sorted(SAFE_CALLS), "command", "signal", "set_active"]
            ]}
            if self.server.unsafe:
                for tool in result["tools"]:
                    if tool["name"] == "game_state":
                        tool["annotations"]["readOnlyHint"] = False
        elif method == "tools/call":
            call = data["params"]
            result = {"isError": False,
                      "content": [{"type": "text", "text": "fixture response: "+call["name"]}]}
        else:
            self.send_error(400)
            return
        raw = json.dumps({"jsonrpc": "2.0", "id": data["id"], "result": result}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        if method == "initialize":
            self.send_header("Mcp-Session-Id", "fake-session")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


class LocalTests(unittest.TestCase):
    def setUp(self):
        self.server = HTTPServer(("127.0.0.1", 0), FakeHandler)
        self.server.events = []
        self.server.identity = "insidedev"
        self.server.unsafe = False
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.port = self.server.server_port

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)

    def test_default_only_readonly_tool_calls(self):
        report = collect(LocalInsideDev(self.port))
        self.assertTrue(report["default_only_upstream_readonly_tools"])
        self.assertEqual(len(report["observations"]), len(SNAPSHOT_CALLS))
        events = self.server.events
        self.assertTrue(all(e["path"] == "/mcp" for e in events))
        self.assertTrue(all(e["origin"] == "http://localhost" for e in events))
        calls = [e["params"]["name"] for e in events if e["method"] == "tools/call"]
        self.assertTrue(set(calls).issubset(SAFE_CALLS))
        self.assertNotIn("command", calls)
        self.assertNotIn("signal", calls)

    def test_fixed_optin_logic_commands(self):
        report = collect(LocalInsideDev(self.port), with_logic=True)
        self.assertTrue(report["optional_logic_uses_nonreadonly_mcp_command"])
        command_calls = [
            e["params"]["arguments"]["command"]
            for e in self.server.events
            if e["method"] == "tools/call" and e["params"]["name"] == "command"
        ]
        self.assertEqual(command_calls, [
            "gamecode", "logic PrintingPaperEasterEgg",
            "logic SecretJoystick", "logic shared secret"
        ])
        self.assertFalse(report["sticker_consumer_identified"])

    def test_disallow_arbitrary_command_and_tools(self):
        client = LocalInsideDev(self.port)
        client.initialize()
        for name, params in [
            ("signal", {"object": "Printer", "output": "printSecretMessage"}),
            ("set_active", {"object": "Secret", "active": False}),
            ("command", {"command": "signal Printer printSecretMessage"}),
            ("command", {"command": "setactive Secret on"}),
        ]:
            with self.assertRaises(ValueError):
                client.call(name, params)
        with self.assertRaises(ValueError):
            client.call("command", {"command": "setactive Secret on"},
                        opt_in_logic=True)
        with self.assertRaises(ValueError):
            client.call("find_objects", {"query": "x", "action": "setactive"})
        self.assertEqual(len([e for e in self.server.events
                              if e["method"] == "tools/call"]), 0)

    def test_fail_closed_if_tool_hint_changed(self):
        self.server.unsafe = True
        client = LocalInsideDev(self.port)
        client.initialize()
        with self.assertRaises(ProtocolError):
            client.call("game_state", {})
        self.assertEqual(len([e for e in self.server.events
                              if e["method"] == "tools/call"]), 0)

    def test_unexpected_mcp_identity(self):
        self.server.identity = "some-other-mcp-server"
        with self.assertRaises(ProtocolError):
            LocalInsideDev(self.port).initialize()

    def test_refuse_repository_write(self):
        dest = Path(__file__).resolve().parents[1]/"data"/"game-capture.json"
        with self.assertRaises(ValueError):
            validate_output_path(dest)
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(validate_output_path(Path(d)/"snapshot.json"),
                             Path(d,"snapshot.json").resolve())

    def test_reject_invalid_ports(self):
        for port in (-1, 0, 65536, "47811", True):
            with self.assertRaises(ValueError):
                LocalInsideDev(port)

if __name__ == "__main__":
    unittest.main()
