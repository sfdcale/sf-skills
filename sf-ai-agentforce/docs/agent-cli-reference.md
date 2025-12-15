# Agent CLI Command Reference

> Complete reference for Salesforce CLI commands used with Agentforce agents

## Overview

This document covers all SF CLI commands for working with Agentforce agents. Commands are organized by workflow stage.

---

## Command Quick Reference

| Command | Purpose | Stage |
|---------|---------|-------|
| `sf afdx agent validate` | Validate Agent Script syntax | Authoring |
| `sf agent publish` | Publish authoring bundle | Authoring |
| `sf agent preview` | Preview agent behavior | Testing |
| `sf agent activate` | Activate published agent | Deployment |
| `sf agent deactivate` | Deactivate agent for changes | Deployment |
| `sf org open agent` | Open in Agentforce Builder | Management |
| `sf project retrieve start --metadata Agent:Name` | Sync agent from org | Sync |
| `sf project deploy start --metadata Agent:Name` | Deploy agent to org | Sync |

---

## Authoring Commands

### sf afdx agent validate

Validates Agent Script syntax before publishing.

```bash
sf afdx agent validate [flags]
```

**Flags:**

| Flag | Description | Required |
|------|-------------|----------|
| `--api-name` | Agent API name to validate | Yes |
| `--target-org` | Org username or alias | No (uses default) |

**Examples:**

```bash
# Validate specific agent
sf afdx agent validate --api-name Customer_Support_Agent --target-org myorg

# Validate using default org
sf afdx agent validate --api-name My_Agent
```

**Common Errors:**

| Error | Cause | Solution |
|-------|-------|----------|
| `SyntaxError: Unexpected token` | Invalid Agent Script syntax | Check indentation, colons, quotes |
| `ReferenceError: Unknown variable` | Variable not defined | Add variable to variables block |
| `TypeError: Invalid type` | Wrong data type used | Use valid type (string, number, boolean, etc.) |

---

### sf agent publish

Publishes the authoring bundle to create or update the agent in the org.

```bash
sf agent publish [flags]
```

**Flags:**

| Flag | Description | Required |
|------|-------------|----------|
| `--api-name` | Agent API name | Yes |
| `--target-org` | Org username or alias | No (uses default) |
| `--async` | Don't wait for completion | No |
| `--wait` | Minutes to wait (default: 33) | No |

**Examples:**

```bash
# Publish agent and wait for completion
sf agent publish --api-name Customer_Support_Agent --target-org myorg

# Publish async (don't wait)
sf agent publish --api-name Customer_Support_Agent --async --target-org myorg

# Publish with custom wait time
sf agent publish --api-name Customer_Support_Agent --wait 60 --target-org myorg
```

**What Gets Published:**

The publish command creates/updates these metadata types:
- `Bot` - Top-level chatbot definition
- `BotVersion` - Version configuration
- `GenAiPlannerBundle` - Reasoning engine configuration
- `GenAiPlugin` - Topics
- `GenAiFunction` - Actions

---

## Testing Commands

### sf agent preview

Preview agent behavior before production deployment. See [Agent Preview Guide](./agent-preview-guide.md) for detailed setup.

```bash
sf agent preview [flags]
```

**Flags:**

| Flag | Description | Required |
|------|-------------|----------|
| `--api-name` | Agent API name (skips selection prompt) | No |
| `--target-org` | Org username or alias | No (uses default) |
| `--use-live-actions` | Enable live mode (uses real Apex/Flows) | No |
| `--client-app` | Connected app name (required for live mode) | For live mode |
| `--output-dir` | Directory to save transcript/response files | No |
| `--apex-debug` | Generate Apex debug logs | No |
| `--authoring-bundle` | Specify authoring bundle API name | No |

**Examples:**

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

**Preview Modes:**

| Mode | Flag | Description |
|------|------|-------------|
| Simulated | (default) | LLM simulates action responses |
| Live | `--use-live-actions` | Uses actual Apex/Flows in org |

---

### sf agent test create

Creates agent tests from a YAML specification.

```bash
sf agent test create [flags]
```

**Flags:**

| Flag | Description | Required |
|------|-------------|----------|
| `--target-org` | Org username or alias | No (uses default) |
| `--spec-file` | Path to test specification YAML | Yes |

**Test Spec YAML Structure:**

```yaml
testCases:
  - name: "Order Status Check"
    utterance: "What is my order status?"
    expectedTopic: "order_management"
    expectedActions:
      - "get_order_status"

  - name: "Escalation Request"
    utterance: "I want to speak to a human"
    expectedTopic: "escalation"
    expectedActions:
      - "escalate"
```

**Examples:**

```bash
# Create tests from spec file
sf agent test create --spec-file ./tests/agent-tests.yaml --target-org myorg
```

---

## Deployment Commands

### sf agent activate

Activates a published agent, making it available to users.

```bash
sf agent activate [flags]
```

**Flags:**

| Flag | Description | Required |
|------|-------------|----------|
| `--api-name` | Agent API name | Yes |
| `--target-org` | Org username or alias | No (uses default) |

**Examples:**

```bash
# Activate agent
sf agent activate --api-name Customer_Support_Agent --target-org myorg
```

**Requirements:**
- Agent must be published first (`sf agent publish`)
- All required Apex classes and Flows must be deployed
- `default_agent_user` must be a valid org user

**Post-Activation:**
- Agent is immediately available to users
- Preview command can be used for testing
- Changes require deactivation first

---

### sf agent deactivate

Deactivates an agent, required before making changes.

```bash
sf agent deactivate [flags]
```

**Flags:**

| Flag | Description | Required |
|------|-------------|----------|
| `--api-name` | Agent API name | Yes |
| `--target-org` | Org username or alias | No (uses default) |

**Examples:**

```bash
# Deactivate agent before making changes
sf agent deactivate --api-name Customer_Support_Agent --target-org myorg
```

**When Deactivation is Required:**
- Adding or removing topics
- Modifying action configurations
- Changing system instructions
- Updating variable definitions

**Workflow:**
```bash
# 1. Deactivate
sf agent deactivate --api-name My_Agent --target-org myorg

# 2. Make changes to Agent Script

# 3. Re-publish
sf agent publish --api-name My_Agent --target-org myorg

# 4. Re-activate
sf agent activate --api-name My_Agent --target-org myorg
```

---

## Management Commands

### sf org open agent

Opens the agent in Agentforce Builder (web UI).

```bash
sf org open agent [flags]
```

**Flags:**

| Flag | Description | Required |
|------|-------------|----------|
| `--api-name` | Agent API name | Yes |
| `--target-org` | Org username or alias | No (uses default) |

**Examples:**

```bash
# Open agent in builder
sf org open agent --api-name Customer_Support_Agent --target-org myorg
```

---

## Sync Commands

### Retrieve Agent from Org

Uses the `Agent` pseudo metadata type to retrieve agent and dependencies.

```bash
sf project retrieve start --metadata Agent:<AgentName> --target-org [alias]
```

**What Gets Retrieved:**
- `Bot` - Top-level chatbot
- `BotVersion` - Version configuration
- `GenAiPlannerBundle` - Reasoning engine
- `GenAiPlugin` - Topics
- `GenAiFunction` - Actions
- Supporting Apex classes and Flows (if in same package)

**Examples:**

```bash
# Retrieve agent and dependencies
sf project retrieve start --metadata Agent:Customer_Support_Agent --target-org myorg

# Retrieve to specific directory
sf project retrieve start --metadata Agent:Customer_Support_Agent --output-dir ./retrieved --target-org myorg
```

---

### Deploy Agent to Org

Uses the `Agent` pseudo metadata type to deploy agent metadata.

```bash
sf project deploy start --metadata Agent:<AgentName> --target-org [alias]
```

**What Gets Deployed:**
- Agent metadata types (Bot, BotVersion, GenAiPlannerBundle, GenAiPlugin, GenAiFunction)
- Does NOT deploy Apex classes or Flows (deploy separately)

**Examples:**

```bash
# Deploy agent metadata
sf project deploy start --metadata Agent:Customer_Support_Agent --target-org myorg

# Deploy with validation only (no actual deployment)
sf project deploy start --metadata Agent:Customer_Support_Agent --dry-run --target-org myorg
```

**Full Deployment Workflow:**

```bash
# 1. Deploy Apex classes first
sf project deploy start --metadata ApexClass --target-org myorg

# 2. Deploy Flows
sf project deploy start --metadata Flow --target-org myorg

# 3. Deploy Agent metadata
sf project deploy start --metadata Agent:Customer_Support_Agent --target-org myorg

# 4. Activate agent
sf agent activate --api-name Customer_Support_Agent --target-org myorg
```

---

## Agent Metadata Types

When working with agent metadata directly, these are the relevant types:

| Metadata Type | Description | Example API Name |
|---------------|-------------|------------------|
| `Bot` | Top-level chatbot definition | `Customer_Support_Agent` |
| `BotVersion` | Version configuration | `Customer_Support_Agent.v1` |
| `GenAiPlannerBundle` | Reasoning engine (LLM config) | `Customer_Support_Agent_Planner` |
| `GenAiPlugin` | Topic definition | `Order_Management_Plugin` |
| `GenAiFunction` | Action definition | `Get_Order_Status_Function` |

**Retrieving Specific Metadata:**

```bash
# Retrieve just the bot definition
sf project retrieve start --metadata Bot:Customer_Support_Agent --target-org myorg

# Retrieve just the planner bundle
sf project retrieve start --metadata GenAiPlannerBundle:Customer_Support_Agent_Planner --target-org myorg

# Retrieve all plugins
sf project retrieve start --metadata GenAiPlugin --target-org myorg
```

---

## Common Workflows

### New Agent Development

```bash
# 1. Create Agent Script file (.agent)
# 2. Validate syntax
sf afdx agent validate --api-name My_Agent --target-org myorg

# 3. Deploy dependencies (Apex, Flows)
sf project deploy start --source-dir force-app/main/default/classes --target-org myorg
sf project deploy start --source-dir force-app/main/default/flows --target-org myorg

# 4. Publish agent
sf agent publish --api-name My_Agent --target-org myorg

# 5. Preview (simulated mode)
sf agent preview --api-name My_Agent --target-org myorg

# 6. Activate
sf agent activate --api-name My_Agent --target-org myorg

# 7. Preview (live mode)
sf agent preview --api-name My_Agent --use-live-actions --client-app MyApp --target-org myorg
```

### Modifying Existing Agent

```bash
# 1. Deactivate
sf agent deactivate --api-name My_Agent --target-org myorg

# 2. Edit Agent Script file

# 3. Validate
sf afdx agent validate --api-name My_Agent --target-org myorg

# 4. Re-publish
sf agent publish --api-name My_Agent --target-org myorg

# 5. Test with preview
sf agent preview --api-name My_Agent --target-org myorg

# 6. Re-activate
sf agent activate --api-name My_Agent --target-org myorg
```

### Syncing Agent Between Orgs

```bash
# 1. Retrieve from source org
sf project retrieve start --metadata Agent:My_Agent --target-org source-org

# 2. Deploy to target org (dependencies first)
sf project deploy start --source-dir force-app/main/default/classes --target-org target-org
sf project deploy start --source-dir force-app/main/default/flows --target-org target-org

# 3. Deploy agent metadata
sf project deploy start --metadata Agent:My_Agent --target-org target-org

# 4. Activate in target org
sf agent activate --api-name My_Agent --target-org target-org
```

---

## Related Documentation

- [Agent Preview Guide](./agent-preview-guide.md) - Detailed preview setup including Connected App
- [Agent Script Syntax](./agent-script-syntax.md) - Complete syntax reference
- [Agent Actions Guide](./agent-actions-guide.md) - Action configuration
- [Testing and Validation Guide](./testing-validation-guide.md) - Testing workflows
