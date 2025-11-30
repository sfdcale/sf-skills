# sf-flow-builder

Creates and validates Salesforce flows using best practices and metadata standards (API 62.0).

## Features

✨ **Comprehensive Flow Creation** (7 Flow Types)
- Screen Flows (user-guided forms and wizards)
- Record-Triggered Flows - After-Save (automation after create/update)
- **NEW**: Record-Triggered Flows - Before-Save (modify records before saving)
- **NEW**: Record-Triggered Flows - Before-Delete (validate or prevent deletion)
- **NEW**: Platform Event-Triggered Flows (real-time event processing)
- Autolaunched Flows (reusable logic for Apex/API)
- Scheduled Flows (time-based batch processing)

🔒 **Strict Validation & Scoring**
- Enhanced validation with 0-100 scoring system
- **Bulkification checks** - prevents DML in loops (CRITICAL)
- **Transform element recommendations** - 30-50% performance gains
- **NEW**: **Simulation mode** - tests with 200+ records before deployment
- API 62.0 (Winter '26) compliance
- Auto-fix suggestions for common issues
- Governor limit analysis

🚀 **Safe Deployment**
- Two-step deployment (validate → deploy)
- Integration with sf-deployment skill
- Activation control (always prompts before activating)
- Comprehensive error handling

📋 **Testing Guidance**
- Type-specific testing checklists
- Bulk testing recommendations (200+ records)
- Debug log analysis
- Production readiness verification

## Quick Start

### Basic Usage

```
"Create a screen flow to collect customer feedback and save it to a custom object"

"Create a record-triggered flow on Opportunity that updates related contacts when stage changes"

"Create an autolaunched flow that takes an account ID and returns the total opportunity value"
```

### Flow Types

**Screen Flow**
```
User: "Create a screen flow for account creation"

The skill will:
1. Ask for flow details (name, description, target org)
2. Generate interactive screens with form fields
3. Validate the flow structure
4. Deploy with two-step process
5. Provide testing checklist
```

**Record-Triggered Flow**
```
User: "Create a record-triggered flow on Account after save"

The skill will:
1. Ask for trigger object and conditions
2. Generate bulkified flow with <bulkSupport>true</bulkSupport>
3. Validate no DML in loops (CRITICAL check)
4. Add fault paths to DML operations
5. Deploy and provide bulk testing guidance
```

**Autolaunched Flow**
```
User: "Create an autolaunched flow with input/output variables"

The skill will:
1. Design input/output variables
2. Create reusable logic
3. Validate naming conventions
4. Deploy with testing recommendations
```

**Scheduled Flow**
```
User: "Create a scheduled flow to run nightly at 2am"

The skill will:
1. Set up schedule configuration
2. Create bulkified batch processing logic
3. Ensure DML is outside loops (best practice)
4. Deploy and provide monitoring guidance
```

## Validation Features

### Comprehensive Checks

**CRITICAL ERRORS** (Block deployment immediately):
- ❌ DML operations inside loops (causes bulk failures)
- ❌ Broken element references
- ❌ Missing required elements
- ❌ Invalid XML structure

**WARNINGS** (Block in strict mode):
- ⚠️  Missing <bulkSupport>true</bulkSupport> on record-triggered flows
- ⚠️  DML operations without fault paths
- ⚠️  Unused variables
- ⚠️  Loops that should use Transform element
- ⚠️  Naming convention violations

**BEST PRACTICES**:
- ✓ API version 62.0 (latest)
- ✓ Descriptive element names
- ✓ Flow description present
- ✓ Transform used for field mapping

### Enhanced Scoring System

Flows are scored 0-100 based on:
- **Errors**: -50 points each (blockers)
- **Warnings**: -5 to -15 points each
- **Best Practices**: +bonus points

**Example Report:**
```
Flow Validation Report: Account_Update_Flow (API 62.0)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ XML Structure: Valid
✓ API Version: 62.0 (current - Winter '26)
✓ Required Elements: Present
✓ Element References: All valid
✓ Bulkification: No DML in loops

⚠ Warnings (2):
  - Variable 'tempVar' declared but never used (-5 pts)
  - DML operation 'Update_Account' missing fault path (-10 pts)

✗ Errors: None

Best Practices Score: 85/100 (Good - needs improvement)

Auto-Fix Available:
  [1] Remove unused variable 'tempVar'
  [2] Add fault path to 'Update_Account'

Recommendations:
  1. 📝 Add flow description for documentation
  2. 🔒 Add error handling to DML operations
```

## Two-Step Deployment

The skill always uses a safe deployment process:

**Step 1: Validation (Check-Only)**
```
- Deploys with --check-only flag (dry-run)
- Verifies metadata structure
- Checks org-specific compatibility
- No actual deployment yet
```

**Step 2: Actual Deployment**
```
- Only proceeds if validation passes
- Deploys to target org
- Monitors deployment status
- Provides verification steps
```

**Step 3: Activation Prompt**
```
Always asks before activating:
- "Keep as Draft" (recommended for production)
- "Activate Now" (use after thorough testing)
```

## Best Practices Enforced

### Performance
- **Bulkification**: All record-triggered flows must handle collections
- **No DML in Loops**: CRITICAL ERROR if detected
- **Transform Element**: 30-50% faster than loops for field mapping
- **Minimize DML**: Batch operations where possible

### Design
- **Error Handling**: Fault paths on all DML operations
- **Meaningful Names**: Variables (camelCase), Elements (PascalCase_With_Underscores)
- **Descriptions**: Document complex logic
- **Subflows**: Reusable patterns

### Security
- **System vs User Mode**: Understand implications
- **Field-Level Security**: Validate permissions
- **No Hardcoded Data**: Use variables or custom settings

## Requirements

- **Salesforce CLI**: `sf` command installed and configured
- **sf-deployment skill**: Version ≥2.0.0 (for deployment operations)
- **Python 3**: For validation script (optional but recommended)
- **Target Org**: Authenticated org with appropriate permissions

## File Structure

```
~/.claude/skills/sf-flow-builder/
├── SKILL.md                              # Main skill definition
├── README.md                             # This file
├── templates/
│   ├── screen-flow-template.xml          # Screen flow base
│   ├── record-triggered-after-save.xml   # Record trigger base
│   ├── autolaunched-flow-template.xml    # Autolaunched base
│   └── scheduled-flow-template.xml       # Scheduled flow base
├── validators/
│   └── flow_validator.py                 # Python validation script
├── examples/
│   ├── screen-flow-example.md            # Screen flow walkthrough
│   ├── record-trigger-example.md         # Record trigger example
│   └── autolaunched-example.md           # Autolaunched example
└── docs/
    ├── flow-best-practices.md            # Salesforce Flow best practices
    └── troubleshooting.md                # Common issues and solutions
```

## Testing Your Flows

### Screen Flows
- Navigate to Setup → Flows → [FlowName]
- Click "Run" to test UI
- Verify all screens and decision paths
- Test with invalid data for validation

### Record-Triggered Flows
- Create test records that meet trigger criteria
- **CRITICAL**: Test with bulk data (200+ records)
- Check Debug Logs for execution
- Verify no governor limit errors

### Autolaunched Flows
- Create Apex test classes to invoke
- Test with various input parameters
- Verify output variables
- Check error handling

### Scheduled Flows
- Test logic manually before activating schedule
- Monitor first scheduled run
- Verify batch processing with expected volume

## Troubleshooting

### "Validation fails but I can't see the issue"
Run the Python validator directly:
```bash
python3 ~/.claude/skills/sf-flow-builder/validators/flow_validator.py \
  force-app/main/default/flows/YourFlow.flow-meta.xml
```

### "Flow works in sandbox but fails in production"
- Check field-level security differences
- Verify all dependent metadata deployed
- Review validation rules
- Test with production data volume

### "Performance issues with flow"
- Check for DML in loops (validator catches this)
- Use Transform element instead of loops
- Minimize DML operations
- Use Get Records with filters

### "Flow doesn't appear after deployment"
- Check deployment status: `sf project deploy report`
- Verify user permissions
- Refresh metadata in org

## Examples

See the `examples/` directory for detailed walkthroughs:
- `screen-flow-example.md` - Customer feedback form
- `record-trigger-example.md` - Opportunity stage updates
- `autolaunched-example.md` - Account total calculation

## Resources

- [Salesforce Flow Documentation](https://help.salesforce.com/s/articleView?id=sf.flow.htm)
- [Flow Best Practices](https://help.salesforce.com/s/articleView?id=sf.flow_prep_bestpractices.htm)
- [API 62.0 Release Notes](https://help.salesforce.com/s/articleView?id=release-notes.rn_forcecom_flow.htm)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the SKILL.md for detailed workflow
3. Run the Python validator for detailed diagnostics

## Version

**Current Version**: 1.2.0 (Phase 2 & 3 Complete)
**API Version**: 62.0 (Winter '26)
**Last Updated**: 2024-11-29

### What's New in 1.2.0

**Phase 2 - Simulation & Advanced Validation:**
- ✅ Bulk simulation mode (tests with 200+ records)
- ✅ Governor limit analysis and warnings
- ✅ Resource usage tracking (SOQL, DML, CPU time)

**Phase 3 - Extended Flow Types:**
- ✅ Platform Event-triggered flows
- ✅ Record-Triggered before-save flows
- ✅ Record-Triggered before-delete flows
- ✅ Enhanced template library (7 types total)

## License

This skill is part of Claude Code skill library.
