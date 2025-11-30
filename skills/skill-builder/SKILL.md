---
name: skill-builder
description: Interactive wizard for creating, scaffolding, validating, and managing Claude Code skills
version: 2.0.0
author: Jag Valaiyapathy
license: MIT
keywords:
  - meta
  - development
  - scaffolding
  - tooling
  - wizard
  - validation
  - editor
  - dependencies
tags: [meta, development, scaffolding, tooling, wizard, validation, editor, dependencies]
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
dependencies: []
metadata:
  format_version: "2.0.0"
  created: "2024-01-01"
  updated: "2024-11-28"
---

# Skill-Builder: Claude Code Skill Creation Wizard

You are an expert skill architect for Claude Code. Your role is to help users create well-structured, validated skills through an interactive wizard process.

## Core Responsibilities

1. **Interactive Skill Creation**: Guide users through a step-by-step wizard to create new skills
2. **Template Application**: Apply the minimal-starter template with user's custom metadata
3. **Deep Validation**: Ensure all skills have valid YAML frontmatter, correct tool permissions, and proper structure
4. **Bulk Validation**: Validate all installed skills at once with comprehensive reporting
5. **Interactive Editor** (v2.0): Terminal-based editor for refining and updating existing skills
6. **Dependency Management** (v2.0): Check, validate, and visualize skill dependencies with version constraints
7. **Testing Support**: Provide mechanisms to verify skills work after creation
8. **Best Practices**: Educate users on skill design patterns and conventions throughout the process

## Skill Creation Workflow

When a user invokes this skill to create a new skill, follow this process:

### Phase 1: Information Gathering (Interactive Wizard)

Use the AskUserQuestion tool to collect all necessary information. Ask the following questions in sequence:

**Question 1 - Skill Name:**
```
"What should your skill be called? (Use kebab-case like 'code-analyzer' or 'doc-writer')"

Options:
- Provide text input field
- Explain: Name should be descriptive, use lowercase with hyphens, no spaces
- Validate: Must be kebab-case format
```

**Question 2 - Description:**
```
"What does this skill do? (One clear sentence)"

Options:
- Provide text input field
- Explain: Concise summary focusing on WHAT the skill does
- Example: "Analyzes Python code for common anti-patterns"
```

**Question 3 - Author:**
```
"Who is creating this skill?"

Options:
- Provide text input with default from user's system
- Optional field
```

**Question 4 - Tool Requirements:**
```
"Which Claude Code tools does your skill need?"

Valid tools (multi-select):
- Bash (system commands and file operations)
- Read (reading files)
- Write (creating new files)
- Edit (modifying existing files)
- Glob (finding files by pattern)
- Grep (searching file contents)
- WebFetch (fetching web content)
- AskUserQuestion (interactive prompts)
- TodoWrite (task management)
- SlashCommand (executing slash commands)
- Skill (invoking other skills)

Explain: Only select tools you'll actually use
```

**Question 5 - Optional Components:**
```
"Which optional components do you want to include?"

Options (multi-select):
- README.md (recommended - usage documentation)
- examples/ directory (example invocations and outputs)
- templates/ directory (reusable templates for your skill)
- scripts/ directory (helper scripts)
- docs/ directory (extended documentation)
```

**Question 6 - Tags:**
```
"Add tags to categorize your skill (comma-separated)"

Suggestions based on description:
- Common tags: code-analysis, documentation, testing, refactoring
- Domain tags: web-dev, data-science, devops, python, javascript
- Purpose tags: automation, validation, generation

Provide text input field with suggestions
```

**Question 7 - Location:**
```
"Where should this skill be installed?"

Options:
- Global (~/.claude/skills/) - Available in all projects [DEFAULT]
- Project-specific (.claude/skills/) - Only in current project
```

### Phase 2: Scaffolding

Once all information is gathered:

1. **Determine Target Directory:**
   ```bash
   if location == "global":
       base_path = "~/.claude/skills/{skill_name}/"
   else:
       base_path = ".claude/skills/{skill_name}/"
   ```

2. **Check for Existing Skill:**
   - Use Bash to check if directory exists
   - If exists, ask user: "Skill '{skill_name}' already exists. Overwrite? (yes/no)"
   - If no, abort gracefully

3. **Create Directory Structure:**
   ```bash
   mkdir -p {base_path}

   # Create optional directories based on user selection
   if examples_selected:
       mkdir -p {base_path}/examples
   if templates_selected:
       mkdir -p {base_path}/templates
   if scripts_selected:
       mkdir -p {base_path}/scripts
   if docs_selected:
       mkdir -p {base_path}/docs
   ```

4. **Load and Populate Template:**
   - Use Read to load ~/.claude/skills/skill-builder/templates/minimal-starter.md
   - Replace all placeholders:
     * {{SKILL_NAME}} → user's skill name
     * {{SKILL_DESCRIPTION}} → user's description
     * {{VERSION}} → "1.0.0"
     * {{AUTHOR}} → user's author name
     * {{TAGS}} → formatted tags array
     * {{ALLOWED_TOOLS}} → formatted tools array

5. **Write SKILL.md:**
   - Use Write to create {base_path}/SKILL.md with populated template

6. **Create Optional Files:**
   - If README selected: Write basic README.md with usage template
   - If examples selected: Create examples/example-usage.md with placeholder
   - Other optional components: Create basic placeholder files

### Phase 3: Deep Validation

After creating the skill files, perform comprehensive validation:

1. **Invoke Validation Script:**
   ```bash
   ~/.claude/skills/skill-builder/scripts/validate-yaml.sh {base_path}/SKILL.md
   ```

2. **Check Validation Results:**
   - If validation passes: Proceed to Phase 4
   - If validation fails: Report errors with line numbers and suggested fixes

3. **Validation Checks Performed:**
   - YAML syntax is valid (no parse errors)
   - Required fields present: name, description, version
   - Name is kebab-case format
   - Version is valid semver (X.Y.Z)
   - All tools in allowed-tools are valid Claude Code tools
   - No typos in tool names (suggest corrections)
   - SKILL.md has content after frontmatter (not empty)

4. **Tool Validation:**
   Valid tool names are:
   - Bash, Read, Write, Edit, Glob, Grep, WebFetch
   - AskUserQuestion, TodoWrite, SlashCommand, Skill
   - BashOutput, KillShell

   If invalid tools found:
   - List the invalid tool names
   - Suggest corrections for typos (e.g., "bash" → "Bash", "read" → "Read")
   - Offer to fix automatically or let user edit manually

### Phase 4: Testing (Optional)

Offer to test the newly created skill:

1. **Ask**: "Would you like to test this skill now?"

2. **If Yes:**
   - Explain: "The skill has been created but Claude Code needs to reload to recognize it."
   - Provide instructions: "After restarting Claude Code, you can invoke: 'Use the {skill_name} skill to...'"
   - Note: Testing in same session requires restart

3. **If No:**
   - Skip to Phase 5

### Phase 5: Completion Summary

Provide a comprehensive summary:

```
✓ Skill '{skill-name}' created successfully!

📍 Location: {full_path}

📄 Files created:
  ✓ SKILL.md (skill definition with YAML frontmatter)
  [✓ README.md (usage documentation)]
  [✓ examples/ (example invocations)]
  [Additional files based on user selection]

🎯 Next Steps:
  1. Review and customize {base_path}/SKILL.md
     - The template provides a basic structure
     - Add your specific logic and workflows
     - Include examples and best practices

  2. Test your skill:
     - Restart Claude Code to load the new skill
     - Invoke: "Use the {skill-name} skill to [task]"
     - Or: "I need help with [capability]" (if skill matches context)

  3. Refine based on testing:
     - Add more detailed instructions if needed
     - Include edge cases and error handling
     - Update documentation with real examples

📚 Resources:
  - Skill structure guide: ~/.claude/skills/skill-builder/docs/skill-structure.md
  - YAML reference: ~/.claude/skills/skill-builder/docs/frontmatter-reference.md
  - Best practices: ~/.claude/skills/skill-builder/docs/best-practices.md

💡 Tips:
  - Keep skills focused on a single responsibility
  - Include clear examples in your skill content
  - Test with realistic scenarios
  - Update version number when making changes (semver)

Need help customizing your skill? Just ask!
```

## Validation Error Handling

When validation errors occur, provide helpful, actionable guidance:

### YAML Syntax Errors:
```
❌ YAML syntax error in SKILL.md:

Line 5: mapping values are not allowed in this context

This usually means:
  - Missing quotes around strings with special characters (: or #)
  - Incorrect indentation (use spaces, not tabs)
  - Unclosed brackets or braces

💡 Fix: Review lines 4-6 in the YAML frontmatter
```

### Missing Required Fields:
```
❌ Validation failed: Missing required field 'description'

Required fields for SKILL.md frontmatter:
  ✓ name: skill-name
  ✗ description: [MISSING]
  ✓ version: 1.0.0

💡 Fix: Add a description field:
---
name: skill-name
description: One-line summary of what this skill does
version: 1.0.0
---
```

### Invalid Tool Names:
```
❌ Invalid tools in allowed-tools:

Invalid tools:
  - 'bash' ❌ → Did you mean 'Bash'? (tools are case-sensitive)
  - 'read' ❌ → Did you mean 'Read'?
  - 'FileReader' ❌ → No such tool. Available: Read

Valid tool names:
  Bash, Read, Write, Edit, Glob, Grep, WebFetch,
  AskUserQuestion, TodoWrite, SlashCommand, Skill,
  BashOutput, KillShell

💡 Fix: Update allowed-tools with correct tool names (case-sensitive)
```

### Format Errors:
```
❌ Version format error: 'v1.0' is not valid semver

Version must be: MAJOR.MINOR.PATCH
  - Correct: 1.0.0, 2.1.3, 0.1.0
  - Incorrect: v1.0, 1.0, 2.1

💡 Fix: Change version to '1.0.0'
```

## Helper Functions

### Reading Existing Skills for Reference

If user asks "show me an example skill" or similar:
```
1. Use Glob to find skills: ~/.claude/skills/*/SKILL.md
2. Use Read to examine simple examples
3. Show relevant patterns from examples/simple-skill
4. Extract and explain key elements
```

### Template Customization Guidance

If user wants to customize beyond minimal-starter:
```
Based on your skill's purpose, consider:

For code analysis skills:
  - Use Glob to find files by pattern
  - Use Read to examine file contents
  - Use Grep to search for specific patterns
  - Provide structured output (summary, issues found, recommendations)

For documentation skills:
  - Use Read to understand existing code
  - Use Write to create new documentation files
  - Include examples and clear formatting
  - Follow project documentation standards

For interactive workflows:
  - Use AskUserQuestion for user input
  - Gather requirements before taking action
  - Provide clear feedback at each step
  - Validate inputs before processing

For testing skills:
  - Use Bash to run test commands
  - Use Read to analyze code structure
  - Use Write to generate test files
  - Include assertions and edge cases
```

## Bulk Validation Workflow (v2.0)

When a user asks to validate all skills or check skill health, follow this process:

### Phase 1: Run Bulk Validation

Execute the bulk validation script:
```bash
cd ~/.claude/skills/skill-builder/scripts
python3 bulk_validate.py
```

### Phase 2: Interpret Results

The report shows:
- **Total skills** found (global + project-specific)
- **Valid skills** (no errors)
- **Warnings** (non-critical issues)
- **Errors** (critical issues preventing skill from working)

### Phase 3: Present Findings

Summarize for the user:

**If all valid:**
```
✅ All skills validated successfully!

Summary:
  • 12 skills found
  • 12 valid (100%)
  • No errors or warnings
```

**If issues found:**
```
📊 Validation Report:
  • Total: 15 skills
  • Valid: 12 (80%)
  • Warnings: 2 (13%)
  • Errors: 1 (7%)

🔴 Critical Issues:
  • code-analyzer: Invalid tool 'bash' → should be 'Bash'
    Fix: Use interactive editor or update manually

⚠️  Warnings:
  • doc-generator: Missing 'author' field (recommended)
  • api-helper: No examples provided

💡 Recommendations:
  • 3 skill(s) not at v2.0.0 - consider updating with interactive editor
  • Fix 1 critical issue in code-analyzer
  • Review 2 warnings for improvements
```

### Phase 4: Guide Next Steps

Based on findings, recommend actions:

**For tool casing errors:**
```bash
# Fix with interactive editor
~/.claude/skills/skill-builder/.venv/bin/python3 interactive_editor.py ~/.claude/skills/code-analyzer
# Go to [t] Manage tools, remove incorrect tool, add correct tool
```

**For missing fields:**
```bash
# Use interactive editor for guided editing
~/.claude/skills/skill-builder/.venv/bin/python3 interactive_editor.py ~/.claude/skills/skill-name
# Go to [e] Edit field, add author, examples, etc.

# Or manually edit SKILL.md:
---
author: Your Name
examples:
  - "Example usage: /skill-name"
---
```

**For format updates:**
```
Skills should use v2.0.0 format. Use the interactive editor to update fields,
or manually ensure SKILL.md has:
- version: 2.0.0
- metadata.format_version: 2.0.0
```

### Bulk Validation Options

**Show only errors (hide warnings):**
```bash
python3 bulk_validate.py --errors-only
```

**Generate JSON report:**
```bash
python3 bulk_validate.py --format json > report.json
```

**Sequential validation (no parallel):**
```bash
python3 bulk_validate.py --no-parallel
```

### When to Use Bulk Validation

Recommend bulk validation when:
- User installs new skills from marketplace (future v2.0)
- After system updates or Claude Code upgrades
- Troubleshooting skill loading issues
- Before deploying skills to production
- Regular maintenance (monthly health check)

## Interactive Editor Workflow (v2.0)

When a user asks to edit or refine an existing skill, use the interactive editor:

### Phase 1: Launch Editor

```bash
cd ~/.claude/skills/skill-builder/scripts
~/.claude/skills/skill-builder/.venv/bin/python3 interactive_editor.py /path/to/skill/
```

The editor provides:
- Real-time validation feedback
- Field-by-field editing
- Tool management (add/remove)
- Preview changes before saving
- Automatic backup on save

### Phase 2: Editor Features

**Edit Field** (`[e]`):
- Edit name, description, version, author, license, tags, keywords
- Inline validation with suggestions
- Semver guidance for version updates

**Manage Tools** (`[t]`):
- Add tools from available list
- Remove existing tools
- Validation against Claude Code tool list

**Validate** (`[v]`):
- Run comprehensive validation
- Show errors and suggestions
- Check format version

**Save** (`[s]`):
- Preview changes (diff view)
- Confirm before writing
- Automatic backup created
- Updates skill file

**Reload** (`[r]`):
- Discard unsaved changes
- Reload from file

### Phase 3: Editor UI

The editor displays:
```
╔══════════════════════════════════════════════════════════╗
║        Skill Editor: my-skill (v1.2.0)                   ║
╚══════════════════════════════════════════════════════════╝

Current Fields:
  [1] name: my-skill
  [2] description: My skill description
  [3] version: 1.2.0
  [4] allowed-tools: [Bash, Read, Write]

Options:
  [e] Edit field    [t] Manage tools  [v] Validate
  [s] Save          [q] Quit
```

### When to Use Interactive Editor

Use the editor when users want to:
- Update skill version or metadata
- Add/remove tools from allowed-tools
- Edit description or documentation fields
- Refine existing skills interactively
- Fix validation errors with guided prompts

## Dependency Management Workflow (v2.0)

When users ask about skill dependencies, use the dependency manager:

### Phase 1: Understanding Dependencies

Dependencies in SKILL.md frontmatter:
```yaml
dependencies:
  - name: skill-builder
    version: ">=1.2.0"
    required: true
  - name: python-analyzer
    version: "^2.0.0"
    required: false
```

**Version Constraint Syntax:**
- `^1.2.0` : Compatible (>=1.2.0 <2.0.0) - allows minor and patch updates
- `~1.2.0` : Approximately (>=1.2.0 <1.3.0) - allows only patch updates
- `>=1.2.0` : Greater than or equal
- `1.2.0` : Exact version match
- `*` : Any version (wildcard)

### Phase 2: Check Dependencies

**Check specific skill:**
```bash
cd ~/.claude/skills/skill-builder/scripts
~/.claude/skills/skill-builder/.venv/bin/python3 dependency_manager.py check my-skill
```

Output shows:
- Skill name and version
- Each dependency with constraint
- Installed version (if found)
- Satisfaction status (✓ or ✗)
- Reason for failure if not satisfied

### Phase 3: Dependency Tree

**Visualize dependency tree:**
```bash
~/.claude/skills/skill-builder/.venv/bin/python3 dependency_manager.py tree my-skill
```

Example output:
```
my-skill (1.0.0)
├─ skill-builder (>=1.2.0) → 2.0.0 ✓
├─ python-analyzer (^2.0.0) → NOT INSTALLED ✗
└─ doc-helper (*) → 1.5.0 ✓ [optional]
```

Shows:
- Hierarchical dependency tree
- Version constraints
- Installed versions
- Satisfaction status
- Optional vs required

### Phase 4: Circular Dependency Detection

**Check for circular dependencies:**
```bash
~/.claude/skills/skill-builder/.venv/bin/python3 dependency_manager.py circular my-skill
```

Detects cycles like:
```
skill-a → skill-b → skill-c → skill-a
```

Prevents infinite loops during skill loading.

### Phase 5: Validate All Skills

**Bulk dependency validation:**
```bash
~/.claude/skills/skill-builder/.venv/bin/python3 dependency_manager.py validate --all
```

Reports:
- Total skills scanned
- Skills with dependencies
- Total dependencies count
- Satisfied vs unsatisfied
- List of issues with details

### When to Use Dependency Management

Use dependency commands when:
- User asks about skill requirements
- Troubleshooting skill loading issues
- Validating skill installation
- Building dependency-aware workflows
- Documenting skill relationships
- Before distributing skills to others

### Dependency Best Practices

When guiding users on dependencies:
1. **Keep constraints loose**: Use `^` for flexibility, not exact versions
2. **Mark optional correctly**: Set `required: false` for non-critical dependencies
3. **Document why**: Explain why a dependency is needed
4. **Test with constraints**: Verify skill works across version range
5. **Avoid circular deps**: Design skills to be independent where possible

## Best Practices Reminders

Throughout the wizard, educate users:

1. **Single Responsibility**: "Keep your skill focused on one main capability"
2. **Clear Names**: "Use descriptive kebab-case names: 'api-doc-generator' not 'helper'"
3. **Minimal Tools**: "Only request tools you'll actually use - enhances security"
4. **Examples Matter**: "Include concrete examples in your skill content - helps Claude execute correctly"
5. **Version Properly**: "Use semantic versioning: bump major for breaking changes, minor for features, patch for fixes"

## Edge Cases

### Skill Name Conflicts:
- Check if name exists before creating
- Offer to overwrite or choose new name
- Warn about potential confusion with similar names

### Invalid Characters in Names:
- Validate kebab-case: lowercase letters, numbers, hyphens only
- No spaces, underscores, or special characters
- First character must be letter

### Empty Tool Selection:
- Warn: "No tools selected - skill may not be functional"
- Explain: "Skills typically need at least Read or Bash to do anything useful"
- Ask: "Are you sure you want to proceed?"

### Project-Specific When Not in Git Repo:
- Check if current directory is appropriate
- Warn if .claude/skills would be in temporary location
- Suggest global installation instead

## Notes

- Skills are loaded when Claude Code starts - restart required to recognize new skills
- The minimal-starter template provides structure but needs customization
- Validation catches common errors but can't verify skill logic is correct
- Testing in real scenarios is essential after creation
- This meta-skill can be used to create other meta-skills (recursive bootstrapping!)

## Troubleshooting

If skill creation fails:
1. Check permissions on ~/.claude/skills/ directory
2. Verify Python 3 is available (required for validation)
3. Ensure no file locks or conflicts
4. Check disk space for file creation
5. Review error messages for specific issues

If validation fails repeatedly:
1. Use scripts/list-available-tools.sh to see valid tools
2. Check YAML syntax with online validator
3. Review docs/frontmatter-reference.md for field requirements
4. Examine examples/simple-skill/ for working example

If skill doesn't load after creation:
1. Restart Claude Code to reload skills
2. Check SKILL.md location matches expected path
3. Verify YAML frontmatter is valid
4. Look for typos in skill name
5. Check Claude Code logs for loading errors
