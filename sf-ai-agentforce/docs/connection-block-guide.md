# Connection Block Guide

> Configure external integrations and escalation routing for Agentforce agents

## Overview

The `connection` block in Agent Script describes how agents interact with external systems and human agents. It's essential for:

- **Escalation Routing**: Directing conversations to human agents via Omni-Channel
- **External Integrations**: Connecting to chat platforms like Enhanced Chat

---

## Connection Block Syntax

```agentscript
connection messaging:
   outbound_route_type: "queue"
   outbound_route_name: "Support_Queue"
```

### Properties

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| `outbound_route_type` | String | Yes | Routing type: `"queue"`, `"skill"`, or `"agent"` |
| `outbound_route_name` | String | Yes | API name of the Omni-Channel queue, skill, or agent |

### Route Types

| Type | Use Case | Example |
|------|----------|---------|
| `queue` | Route to a queue of agents | `"Support_Queue"` |
| `skill` | Route based on agent skills | `"Technical_Support"` |
| `agent` | Route to a specific agent | `"supervisor@company.com"` |

---

## Escalation Workflow

### Prerequisites

Before using `@utils.escalate`, you need:

1. **Omni-Channel Setup**: Configured queues/skills in Salesforce
2. **Connection Block**: Defined in your agent script
3. **Messaging Channel**: Active messaging channel (Enhanced Chat, etc.)

### Complete Example

```agentscript
system:
   instructions: "You are a helpful assistant. Transfer to a human agent when requested or when you cannot resolve an issue."
   messages:
      welcome: "Hello! How can I help you today?"
      error: "I apologize, but I encountered an issue."

config:
   agent_name: "Support_Agent"
   default_agent_user: "agent@company.com"
   agent_label: "Customer Support Agent"
   description: "Handles customer inquiries with human escalation"

variables:
   EndUserId: linked string
      source: @MessagingSession.MessagingEndUserId
      description: "Messaging End User ID"
   RoutableId: linked string
      source: @MessagingSession.Id
      description: "Messaging Session ID"
   ContactId: linked string
      source: @MessagingEndUser.ContactId
      description: "Contact ID"
   escalation_reason: mutable string
      description: "Reason for escalation"

language:
   default_locale: "en_US"
   additional_locales: ""
   all_additional_locales: False

# Connection block for escalation routing
connection messaging:
   outbound_route_type: "queue"
   outbound_route_name: "Customer_Support_Queue"

start_agent topic_selector:
   label: "Topic Selector"
   description: "Routes users to appropriate topics"

   reasoning:
      instructions: ->
         | Determine what the user needs.
         | If they ask for a human agent, route to escalation.
      actions:
         go_help: @utils.transition to @topic.help
         go_escalation: @utils.transition to @topic.escalation

topic help:
   label: "Help"
   description: "Provides assistance to users"

   reasoning:
      instructions: ->
         | Help the user with their question.
         | If you cannot resolve the issue, offer to connect them with a human.
      actions:
         escalate_if_needed: @utils.transition to @topic.escalation
            available when @variables.needs_human == True

topic escalation:
   label: "Escalation"
   description: "Transfers conversation to human agent"

   reasoning:
      instructions: ->
         | Acknowledge the transfer request.
         | Apologize for any inconvenience.
         | Transfer to a human agent.
      actions:
         # Basic escalation (works in both deployment methods)
         transfer_to_human: @utils.escalate
            description: "Transfer to human agent when customer requests or issue cannot be resolved"
```

---

## Escalation Syntax by Deployment Method

### AiAuthoringBundle (Basic Escalation)

```agentscript
# ✅ WORKS - Basic escalation with description
actions:
   escalate: @utils.escalate
      description: "Transfer to human agent"
```

### GenAiPlannerBundle (With Reason)

```agentscript
# ✅ WORKS - Escalation with reason parameter
actions:
   escalate: @utils.escalate with reason="Customer requested human assistance"
```

### ⚠️ Common Mistakes

```agentscript
# ❌ WRONG - 'with reason' in AiAuthoringBundle causes SyntaxError
actions:
   escalate: @utils.escalate with reason="..."  # FAILS in AiAuthoringBundle!

# ❌ WRONG - Inline description fails
actions:
   escalate: @utils.escalate "Transfer to human"  # FAILS!

# ✅ CORRECT - Description on separate line
actions:
   escalate: @utils.escalate
      description: "Transfer to human"
```

---

## Enhanced Chat Integration

When using Enhanced Chat as your messaging channel:

```agentscript
connection messaging:
   outbound_route_type: "queue"
   outbound_route_name: "Chat_Support_Queue"
```

### Setup Requirements

1. **Enable Enhanced Chat** in Setup → Chat Settings
2. **Create Omni-Channel Queue** with Chat routing
3. **Deploy Agent** with connection block
4. **Configure Embedded Service** to use the agent

---

## Skill-Based Routing

Route based on agent skills for specialized support:

```agentscript
connection messaging:
   outbound_route_type: "skill"
   outbound_route_name: "Technical_Support_Skill"
```

### Use Case

- Technical issues → Technical Support skill
- Billing questions → Billing skill
- Sales inquiries → Sales skill

---

## Troubleshooting

### Escalation Not Working

| Issue | Cause | Solution |
|-------|-------|----------|
| "escalate" not recognized | Missing connection block | Add `connection messaging:` block |
| Agent not transferring | Queue not configured | Verify Omni-Channel queue exists |
| "SyntaxError: Unexpected 'with'" | Using `with reason` in AiAuthoringBundle | Use basic escalation or GenAiPlannerBundle |
| Transfer fails silently | Agent user lacks permissions | Grant Omni-Channel permissions |

### Verifying Connection

1. Deploy agent
2. Test in Agentforce Testing Center
3. Request escalation
4. Verify transfer appears in Omni-Channel Supervisor

---

## Best Practices

| Practice | Description |
|----------|-------------|
| **Always include connection** | If your agent might need escalation, add the block |
| **Use clear descriptions** | Help the LLM decide when to escalate |
| **Test escalation flows** | Verify transfers work before production |
| **Configure fallback queue** | Have a default queue for unexpected escalations |
| **Monitor agent handoffs** | Track escalation reasons for improvement |

---

## Related Documentation

- [SKILL.md - Escalation Section](../skills/sf-ai-agentforce/SKILL.md)
- [Agent Script Syntax](./agent-script-syntax.md)
- [Salesforce Omni-Channel Documentation](https://help.salesforce.com/s/articleView?id=sf.omnichannel_intro.htm)
