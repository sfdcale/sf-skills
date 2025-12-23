#!/usr/bin/env python3
"""
LSP Client for Agent Script Language Server
============================================

This module provides a Python interface to the Agent Script LSP server
for use in Claude Code hooks.

Features:
- Auto-discovers VS Code Agent Script extension
- Communicates via JSON-RPC over stdio
- Returns parsed diagnostics for validation hooks
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, List, Any


class LSPClient:
    """Client for communicating with the Agent Script LSP server."""

    def __init__(self, wrapper_path: Optional[str] = None):
        """
        Initialize the LSP client.

        Args:
            wrapper_path: Path to the LSP wrapper script. If None, auto-discovers.
        """
        self.wrapper_path = wrapper_path or self._find_wrapper()
        self._server_process: Optional[subprocess.Popen] = None
        self._request_id = 0

    def _find_wrapper(self) -> str:
        """Find the LSP wrapper script relative to this module."""
        module_dir = Path(__file__).parent
        wrapper = module_dir / "agentscript_wrapper.sh"
        if wrapper.exists():
            return str(wrapper)

        # Fallback: check common locations
        fallbacks = [
            Path.home() / ".claude" / "lsp" / "agentscript-lsp-wrapper.sh",
            Path.home() / ".claude" / "plugins" / "marketplaces" / "sf-skills" / "shared" / "lsp-engine" / "agentscript_wrapper.sh",
        ]
        for fallback in fallbacks:
            if fallback.exists():
                return str(fallback)

        raise FileNotFoundError(
            "LSP wrapper script not found. Ensure the Agent Script extension is installed."
        )

    def is_available(self) -> bool:
        """Check if the LSP server is available."""
        try:
            # Quick check: can we find the wrapper?
            if not os.path.exists(self.wrapper_path):
                return False

            # Quick check: is it executable?
            if not os.access(self.wrapper_path, os.X_OK):
                return False

            return True
        except Exception:
            return False

    def _next_request_id(self) -> int:
        """Generate the next request ID."""
        self._request_id += 1
        return self._request_id

    def _create_message(self, method: str, params: Dict[str, Any]) -> str:
        """Create a JSON-RPC message with Content-Length header."""
        request = {
            "jsonrpc": "2.0",
            "id": self._next_request_id(),
            "method": method,
            "params": params,
        }
        content = json.dumps(request)
        return f"Content-Length: {len(content)}\r\n\r\n{content}"

    def validate_file(self, file_path: str, content: Optional[str] = None) -> Dict[str, Any]:
        """
        Validate a file using the LSP server.

        Args:
            file_path: Path to the file to validate
            content: Optional file content (if None, reads from disk)

        Returns:
            Dict with 'success' boolean and 'diagnostics' list
        """
        import select
        import time

        if content is None:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Could not read file: {e}",
                    "diagnostics": [],
                }

        try:
            # Start the LSP server with unbuffered I/O
            process = subprocess.Popen(
                [self.wrapper_path, "--stdio"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=0,
            )

            def send_message(method: str, params: Dict, req_id: Optional[int] = None):
                """Send a JSON-RPC message to the LSP server."""
                msg = {"jsonrpc": "2.0", "method": method, "params": params}
                if req_id is not None:
                    msg["id"] = req_id
                content_bytes = json.dumps(msg).encode("utf-8")
                header = f"Content-Length: {len(content_bytes)}\r\n\r\n".encode("utf-8")
                process.stdin.write(header + content_bytes)
                process.stdin.flush()

            def read_responses(timeout: float = 3.0) -> List[Dict]:
                """Read LSP responses with Content-Length header parsing."""
                responses = []
                buffer = b""
                start = time.time()

                while time.time() - start < timeout:
                    ready, _, _ = select.select([process.stdout], [], [], 0.1)
                    if ready:
                        chunk = process.stdout.read(4096)
                        if not chunk:
                            break
                        buffer += chunk

                        # Parse complete messages
                        while b"Content-Length:" in buffer:
                            header_end = buffer.find(b"\r\n\r\n")
                            if header_end == -1:
                                break
                            header = buffer[:header_end].decode("utf-8")
                            try:
                                content_length = int(header.split(":")[1].strip())
                            except (ValueError, IndexError):
                                break
                            msg_start = header_end + 4
                            msg_end = msg_start + content_length
                            if len(buffer) < msg_end:
                                break
                            msg = buffer[msg_start:msg_end].decode("utf-8")
                            try:
                                responses.append(json.loads(msg))
                            except json.JSONDecodeError:
                                pass
                            buffer = buffer[msg_end:]
                    time.sleep(0.05)
                return responses

            # Initialize LSP
            init_params = {
                "processId": os.getpid(),
                "rootUri": f"file://{os.path.dirname(file_path)}",
                "capabilities": {
                    "textDocument": {
                        "publishDiagnostics": {"relatedInformation": True},
                    }
                },
            }
            send_message("initialize", init_params, self._next_request_id())
            time.sleep(0.3)
            read_responses(timeout=1)  # Read initialize response

            # Send initialized notification
            send_message("initialized", {})

            # Open document
            file_uri = f"file://{os.path.abspath(file_path)}"
            did_open_params = {
                "textDocument": {
                    "uri": file_uri,
                    "languageId": "agentscript",
                    "version": 1,
                    "text": content,
                }
            }
            send_message("textDocument/didOpen", did_open_params)

            # Wait for diagnostics (async from server)
            time.sleep(0.5)
            responses = read_responses(timeout=3)

            # Extract diagnostics from responses
            diagnostics = []
            for resp in responses:
                if resp.get("method") == "textDocument/publishDiagnostics":
                    params = resp.get("params", {})
                    for diag in params.get("diagnostics", []):
                        diagnostics.append({
                            "severity": diag.get("severity", 1),
                            "message": diag.get("message", "Unknown error"),
                            "range": diag.get("range", {}),
                            "source": diag.get("source", "agentscript"),
                            "code": diag.get("code", ""),
                        })

            # Clean shutdown
            send_message("shutdown", {}, self._next_request_id())
            send_message("exit", {})
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()

            return {
                "success": len(diagnostics) == 0,
                "diagnostics": diagnostics,
                "file_path": file_path,
            }

        except FileNotFoundError:
            return {
                "success": False,
                "error": "LSP wrapper script not found. Install VS Code Agent Script extension.",
                "diagnostics": [],
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "diagnostics": [],
            }

    def _parse_diagnostics(self, response: str) -> List[Dict[str, Any]]:
        """Parse diagnostics from LSP response."""
        diagnostics = []

        # Look for JSON-RPC responses
        try:
            # Split by Content-Length headers
            parts = response.split("Content-Length:")
            for part in parts:
                if not part.strip():
                    continue

                # Find JSON content after headers
                json_start = part.find("{")
                if json_start == -1:
                    continue

                json_content = part[json_start:]

                # Handle multiple JSON objects
                decoder = json.JSONDecoder()
                pos = 0
                while pos < len(json_content):
                    try:
                        obj, end_pos = decoder.raw_decode(json_content[pos:])
                        pos += end_pos

                        # Check for diagnostics notification
                        if obj.get("method") == "textDocument/publishDiagnostics":
                            params = obj.get("params", {})
                            for diag in params.get("diagnostics", []):
                                diagnostics.append({
                                    "severity": diag.get("severity", 1),
                                    "message": diag.get("message", "Unknown error"),
                                    "range": diag.get("range", {}),
                                    "source": diag.get("source", "agentscript"),
                                })
                    except json.JSONDecodeError:
                        break

        except Exception:
            pass  # Ignore parsing errors

        return diagnostics


def is_lsp_available() -> bool:
    """Check if the Agent Script LSP is available."""
    try:
        client = LSPClient()
        return client.is_available()
    except Exception:
        return False


def get_diagnostics(file_path: str, content: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to get diagnostics for a file.

    Args:
        file_path: Path to the .agent file
        content: Optional file content

    Returns:
        Dict with validation results
    """
    try:
        client = LSPClient()
        return client.validate_file(file_path, content)
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "diagnostics": [],
        }


if __name__ == "__main__":
    # CLI usage for testing
    if len(sys.argv) < 2:
        print("Usage: python lsp_client.py <file.agent>")
        sys.exit(1)

    result = get_diagnostics(sys.argv[1])
    print(json.dumps(result, indent=2))
