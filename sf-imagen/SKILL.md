---
name: sf-imagen
description: >
  AI-powered visual content generation for Salesforce development.
  Generates ERD diagrams, LWC mockups, architecture visuals using Nano Banana Pro.
  Also provides Gemini as a parallel sub-agent for code review and research.
license: MIT
metadata:
  version: "1.1.0"
  author: "Jag Valaiyapathy"
  scoring: "80 points across 5 categories"
---

# sf-imagen: Salesforce Visual AI Skill

Visual content generation and AI sub-agent for Salesforce development using
Gemini CLI with Nano Banana Pro extension.

## ⚠️ IMPORTANT: Prerequisites Check

**Before using this skill, ALWAYS run the prerequisites check first:**

```bash
~/.claude/plugins/marketplaces/sf-skills/sf-imagen/scripts/check-prerequisites.sh
```

**If the check fails, DO NOT invoke this skill.** The user must fix the missing prerequisites first.

## Requirements

| Requirement | Description | How to Get |
|-------------|-------------|------------|
| **macOS** | Required for Preview app image display | Built-in |
| **GEMINI_API_KEY** | Personal API key for Nano Banana Pro | https://aistudio.google.com/apikey |
| **Gemini CLI** | Command-line interface for Gemini | `npm install -g @google/gemini-cli` |
| **Nano Banana Extension** | Image generation extension | `gemini extensions install nanobanana` |

### Optional (for terminal display)
| Requirement | Description | How to Get |
|-------------|-------------|------------|
| Ghostty Terminal | For Kitty graphics protocol | https://ghostty.org |
| timg | Terminal image viewer | `brew install timg` |

### Setting Up API Key

Add to `~/.zshrc` (DO NOT commit to version control):
```bash
export GEMINI_API_KEY="your-personal-api-key"
export NANOBANANA_MODEL=gemini-3-pro-image-preview
```

## Core Capabilities

### 1. Visual ERD Generation
Generate actual rendered ERD diagrams (not just Mermaid code):
- Query object metadata via sf-metadata
- Generate visual diagram with Nano Banana Pro
- **Display in macOS Preview app** (default)

### 2. LWC/UI Mockups
Generate wireframes and component mockups:
- Data tables, record forms, dashboard cards
- Experience Cloud page layouts
- Mobile-responsive designs following SLDS

### 3. Gemini Code Review (Sub-Agent)
Parallel code review while Claude continues working:
- Apex class/trigger review for best practices
- LWC component review for accessibility
- SOQL query optimization suggestions

### 4. Documentation Research (Sub-Agent)
Parallel Salesforce documentation research:
- Look up API references and limits
- Find best practices and patterns
- Research release notes

---

## Workflow Patterns

### Pattern A: Visual ERD Generation

**Trigger**: User asks for visual ERD, rendered diagram, or image-based data model

**Workflow**:
1. Run prerequisites check
2. Query object metadata via sf-metadata (if org connected)
3. Build Nano Banana prompt with object relationships
4. Execute Gemini CLI with `/generate` command (requires --yolo flag)
5. **Open result in macOS Preview app using `open` command**

**Example**:
```bash
# Generate image
gemini --yolo "/generate 'Professional Salesforce ERD diagram showing:
   - Account (blue box, center)
   - Contact (green box, linked to Account with lookup arrow)
   - Opportunity (yellow box, linked to Account with master-detail thick arrow)
   Include legend. Clean white background, Salesforce Lightning style.'"

# Open in macOS Preview (DEFAULT)
open ~/nanobanana-output/[generated-file].png
```

### Pattern B: LWC Mockup

**Trigger**: User asks for component mockup, wireframe, or UI design

**Workflow**:
1. Load appropriate template from `templates/lwc/`
2. Customize prompt with user requirements
3. Execute via Nano Banana
4. Open in Preview app

### Pattern C: Parallel Code Review

**Trigger**: User asks for code review, second opinion, or "review while I work"

**Workflow**:
1. Run Gemini in background with JSON output
2. Claude continues with current task
3. Return Gemini's findings when ready

**Example**:
```bash
gemini "Review this Apex trigger for:
   - Bulkification issues
   - Best practices violations
   - Security concerns (CRUD/FLS)
   Code: [trigger code]" -o json
```

### Pattern D: Documentation Research

**Trigger**: User asks to look up, research, or find documentation

**Workflow**:
1. Run Gemini with documentation query
2. Return findings with sources

---

## Commands Reference

### Image Generation

```bash
# Generate image from prompt (MUST use --yolo for non-interactive)
gemini --yolo "/generate 'description'"

# Images are saved to ~/nanobanana-output/
```

### Image Display

```bash
# DEFAULT: Open in macOS Preview app
open /path/to/image.png

# Open most recent generated image
open ~/nanobanana-output/$(ls -t ~/nanobanana-output/*.png | head -1)
```

### Alternative Display Methods

```bash
# View inline in Claude Code conversation (multimodal vision)
# Use the Read tool → /path/to/image.png

# Terminal display with Kitty graphics (requires Ghostty + timg)
timg -pk -g 120x40 /path/to/image.png

# Open in new Ghostty window
~/bin/show-image-window /path/to/image.png
```

---

## Cross-Skill Integration

| Skill | Integration | Usage |
|-------|-------------|-------|
| sf-diagram | Enhance Mermaid with visual rendering | "Convert this Mermaid ERD to a visual diagram" |
| sf-metadata | Get object/field data for ERDs | Query org before generating ERD |
| sf-lwc | Generate component mockups | "Mockup for the AccountList component" |
| sf-apex | Review Apex code via Gemini | "Get Gemini's opinion on this trigger" |

---

## Helper Scripts

| Script | Location | Purpose |
|--------|----------|---------|
| `check-prerequisites.sh` | `scripts/` | Verify all requirements before use |
| `show-image.sh` | `scripts/` | Display images in current terminal (optional) |

---

## Template Usage

### ERD Templates (`templates/erd/`)
- `core-objects.md` - Standard CRM objects
- `custom-objects.md` - Custom data model

### LWC Templates (`templates/lwc/`)
- `data-table.md` - Lightning datatable mockups
- `record-form.md` - Record form mockups
- `dashboard-card.md` - Dashboard card mockups

### Architecture Templates (`templates/architecture/`)
- `integration-flow.md` - Integration architecture diagrams

### Review Templates (`templates/review/`)
- `apex-review.md` - Apex code review prompts
- `lwc-review.md` - LWC review prompts

---

## Troubleshooting

### Prerequisites Check Failed
Run `scripts/check-prerequisites.sh` and fix each issue:
- **No API Key**: Set GEMINI_API_KEY in ~/.zshrc (personal key from aistudio.google.com)
- **No Gemini CLI**: Install with npm
- **No Nano Banana**: Install extension via gemini CLI

### Image Not Opening
- Ensure you're on macOS (Preview app is macOS-only)
- Check the file path exists: `ls ~/nanobanana-output/`
- Try opening manually: `open ~/nanobanana-output/[filename].png`

### API Key Errors
- Ensure GEMINI_API_KEY is exported in current shell
- Verify key is valid at https://aistudio.google.com/apikey
- Check billing is enabled on Google Cloud project

---

## Security Notes

⚠️ **NEVER commit your GEMINI_API_KEY to version control**

- Store API key in `~/.zshrc` only (not in project files)
- The key is personal and tied to your Google account billing

---

## License

MIT License. Copyright (c) 2024-2025 Jag Valaiyapathy
