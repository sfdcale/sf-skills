# Agent Preview Guide

> Complete guide for previewing Agentforce agents using the SF CLI

## Overview

The `sf agent preview` command allows you to test your agent's behavior before deploying to production. Preview supports two modes:

| Mode | Description | Use When |
|------|-------------|----------|
| **Simulated** | Uses mocked action responses | Apex/Flows not ready, testing logic |
| **Live** | Uses actual Apex/Flows in org | Integration testing with real data |

---

## CLI Command Reference

### Basic Syntax

```bash
sf agent preview [flags]
```

### All Flags

| Flag | Description | Required |
|------|-------------|----------|
| `--api-name` | Agent API name (skips selection prompt) | No |
| `--target-org` | Org username or alias | No (uses default) |
| `--use-live-actions` | Enable live mode (uses real Apex/Flows) | No |
| `--client-app` | Connected app name (required for live mode) | For live mode |
| `--output-dir` | Directory to save transcript/response files | No |
| `--apex-debug` | Generate Apex debug logs | No |
| `--authoring-bundle` | Specify authoring bundle API name | No |

### Examples

```bash
# Preview with agent selection prompt
sf agent preview --target-org myorg

# Preview specific agent (simulated mode)
sf agent preview --api-name Customer_Support_Agent --target-org myorg

# Preview in live mode with connected app
sf agent preview --api-name Customer_Support_Agent --use-live-actions --client-app MyAgentApp --target-org myorg

# Preview with debug output saved
sf agent preview --api-name Customer_Support_Agent --output-dir ./preview-logs --apex-debug --target-org myorg
```

---

## Preview Modes

### Simulated Mode (Default)

**When to use:**
- Apex classes or Flows aren't deployed yet
- Testing agent logic without affecting org data
- Rapid iteration on agent design

**How it works:**
- LLM simulates action responses based on action descriptions
- No actual Apex/Flow execution
- Safe for testing - no org data changes

```bash
# Simulated mode (default)
sf agent preview --api-name My_Agent --target-org myorg
```

### Live Mode

**When to use:**
- Integration testing with real Apex/Flows
- Validating end-to-end functionality
- Testing with actual org data

**Requirements:**
- Connected app configured (see below)
- Apex classes and Flows deployed to org
- `default_agent_user` property set to valid org user
- Agent must be **active**

```bash
# Live mode
sf agent preview --api-name My_Agent --use-live-actions --client-app MyAgentApp --target-org myorg
```

---

## Connected App Setup (Required for Live Preview)

To use live preview mode, you must configure a Connected App:

### Step 1: Create Connected App in Salesforce

1. Go to **Setup → App Manager → New Connected App**
2. Configure these settings:

| Setting | Value |
|---------|-------|
| Connected App Name | `AgentPreviewApp` (or your choice) |
| API Name | Auto-generated |
| Contact Email | Your email |
| Enable OAuth Settings | ✅ Checked |
| Callback URL | `http://localhost:1717/OauthRedirect` |
| Selected OAuth Scopes | `Manage user data via Web browsers (web)` |

3. Save and wait for activation (can take a few minutes)

### Step 2: Get Consumer Key

1. After saving, click **Manage Consumer Details**
2. Verify your identity
3. Copy the **Consumer Key** (you'll need this)

### Step 3: Add Connected App to Agent

In your Agent Script, the connected app is linked during agent configuration in the org.

### Step 4: Link Connected App to CLI User

```bash
# First, ensure you're logged into the org
sf org login web --target-org myorg

# Link connected app to your authenticated user
sf org login web \
  --client-app AgentPreviewApp \
  --username your.user@org.com \
  --client-id YOUR_CONSUMER_KEY \
  --scopes web
```

### Step 5: Run Live Preview

```bash
sf agent preview --api-name My_Agent --use-live-actions --client-app AgentPreviewApp --target-org myorg
```

---

## Output Files

When using `--output-dir`, preview saves these files:

### transcript.json

Conversation record with all messages:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "What is my order status?",
      "timestamp": "2025-01-15T10:30:00Z"
    },
    {
      "role": "assistant",
      "content": "I'd be happy to help check your order status. Could you provide your order number?",
      "timestamp": "2025-01-15T10:30:02Z"
    }
  ]
}
```

### responses.json

Full API messages with internal details:

```json
{
  "responses": [
    {
      "type": "assistant_response",
      "content": "...",
      "internal_ids": {...},
      "actions_invoked": [...]
    }
  ]
}
```

---

## Debugging with Apex Logs

Enable Apex debugging to troubleshoot action execution:

```bash
sf agent preview --api-name My_Agent --use-live-actions --client-app MyApp --apex-debug --target-org myorg
```

This generates Apex debug logs that you can analyze with:
- Salesforce Developer Console
- SF CLI: `sf apex log get`
- Apex Replay Debugger (VS Code)

---

## Troubleshooting

### "No active agents found"

**Cause:** Agent not activated
**Solution:** Activate the agent first:
```bash
sf agent activate --api-name My_Agent --target-org myorg
```

### "Connected app not found"

**Cause:** Connected app not linked to CLI user
**Solution:** Run the `sf org login web` command with `--client-app` flag (see Step 4 above)

### "default_agent_user not found"

**Cause:** User specified in agent config doesn't exist
**Solution:** Update the `default_agent_user` property in your Agent Script config block to a valid org user

### Preview hangs or times out

**Cause:** Action taking too long or failing silently
**Solution:**
1. Use `--apex-debug` to capture logs
2. Check for SOQL limits or callout timeouts
3. Test the Flow/Apex independently first

### Actions not executing in live mode

**Cause:** Actions not deployed to org
**Solution:** Deploy dependencies before preview:
```bash
sf project deploy start --metadata ApexClass --target-org myorg
sf project deploy start --metadata Flow --target-org myorg
```

---

## Limitations

| Limitation | Details |
|------------|---------|
| Escalation testing | Not supported - publish agent and test via actual endpoint |
| Connection endpoints | Preview doesn't strictly adhere to connection configuration |
| Script changes | Require validation and preview restart to test |
| Active agent required | Agent must be active for preview (use `sf agent activate`) |

---

## Best Practices

1. **Start with simulated mode** - Iterate quickly on agent logic
2. **Deploy dependencies first** - Apex and Flows must be in org for live mode
3. **Use output files** - Save transcripts for debugging and review
4. **Test edge cases** - Try unexpected inputs to validate guardrails
5. **Validate before preview** - Run `sf afdx agent validate` first

---

## Related Commands

| Command | Description |
|---------|-------------|
| `sf agent activate` | Activate agent (required before preview) |
| `sf agent deactivate` | Deactivate agent |
| `sf afdx agent validate` | Validate Agent Script syntax |
| `sf agent publish` | Publish authoring bundle |

---

## Related Documentation

- [Agent CLI Reference](./agent-cli-reference.md)
- [Testing and Validation Guide](./testing-validation-guide.md)
- [Agent Actions Guide](./agent-actions-guide.md)
