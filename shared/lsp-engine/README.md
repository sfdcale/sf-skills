# LSP Engine for sf-skills

Language Server Protocol integration for Salesforce development skills in Claude Code.

## Overview

This module provides a shared LSP engine that enables real-time validation of Salesforce files during Claude Code authoring sessions. Currently supports:

- **Agent Script** (`.agent` files) - via Salesforce VS Code extension

## Prerequisites

1. **VS Code with Agent Script Extension**
   - Open VS Code
   - Go to Extensions (Cmd+Shift+X)
   - Search: "Agent Script" by Salesforce
   - Install

2. **Node.js 18+**
   - Required by the LSP server
   - Check: `node --version`

## Usage

### In Hooks (Recommended)

```python
#!/usr/bin/env python3
import sys
import json
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "shared" / "lsp-engine"))

from lsp_client import get_diagnostics
from diagnostics import format_diagnostics_for_claude

# Read hook input
hook_input = json.load(sys.stdin)
file_path = hook_input.get("tool_input", {}).get("file_path", "")

# Validate .agent files
if file_path.endswith(".agent"):
    result = get_diagnostics(file_path)
    output = format_diagnostics_for_claude(result)
    if output:
        print(output)
```

### Standalone CLI

```bash
# Test LSP validation
python3 lsp_client.py /path/to/file.agent
```

## Module Structure

```
lsp-engine/
├── __init__.py              # Package exports
├── agentscript_wrapper.sh   # Shell wrapper for LSP server
├── lsp_client.py            # Python LSP client
├── diagnostics.py           # Diagnostic formatting
└── README.md               # This file
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LSP_LOG_FILE` | Path to log file | `/dev/null` |
| `NODE_PATH` | Custom Node.js path | Auto-detected |

## Troubleshooting

### "LSP server not found"

The VS Code Agent Script extension is not installed:
1. Install from VS Code Marketplace
2. Verify: `ls ~/.vscode/extensions/salesforce.agent-script-*`

### "Node.js not found"

Install Node.js 18+:
- macOS: `brew install node`
- Or download from https://nodejs.org

### "Node.js version too old"

Upgrade to Node.js 18+:
- macOS: `brew upgrade node`

## How It Works

```
1. Hook triggers after Write/Edit on .agent file
         │
         ▼
2. lsp_client.py discovers VS Code extension
         │
         ▼
3. Spawns LSP server via agentscript_wrapper.sh
         │
         ▼
4. Sends textDocument/didOpen with file content
         │
         ▼
5. Parses textDocument/publishDiagnostics response
         │
         ▼
6. Formats errors for Claude → Auto-fix loop
```

## License

MIT - See LICENSE file in repository root.
