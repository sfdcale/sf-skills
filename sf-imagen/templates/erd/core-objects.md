# ERD Template: Core Salesforce Objects

## Prompt Template

```
Professional Salesforce ERD diagram showing:

OBJECTS:
- Account (blue box, center position)
  - Type: Standard Object
  - Role: Master record for customers/partners

- Contact (green box, linked to Account)
  - Type: Standard Object
  - Relationship: Lookup to Account (optional parent)

- Opportunity (yellow box, linked to Account)
  - Type: Standard Object
  - Relationship: Master-Detail to Account (required parent)

- Case (orange box, linked to Account and Contact)
  - Type: Standard Object
  - Relationship: Lookup to Account, Lookup to Contact

RELATIONSHIPS:
- Lookup: Dashed arrow (---->)
- Master-Detail: Solid thick arrow (====>)

STYLING:
- Clean white background
- Pastel fill colors with dark borders
- Clear labels on relationship arrows
- Professional diagram layout
- Include legend in corner

FORMAT:
- Landscape orientation
- Centered composition
- Readable text at normal zoom
```

## Usage

```bash
# Draft at 1K (iterate here)
gemini --yolo "/generate '[paste prompt above with customizations]'"
open ~/nanobanana-output/*.png  # Review and refine

# Final at 4K (when satisfied)
uv run scripts/generate_image.py \
  -p "[your refined prompt]" \
  -f "core-objects-erd.png" \
  -r 4K
open ~/nanobanana-output/*core-objects*.png
```

## Resolution Guide

| Phase | Resolution | Use Case |
|-------|------------|----------|
| Draft | 1K (CLI) | Quick iteration, prompt refinement |
| Final | 4K (Python) | Documentation, presentations |

**Tip**: Iterate at 1K until layout is correct, then generate 4K final.
