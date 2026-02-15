# Initialize Chat for BestWorkplace xWiki work

**Version:** 1.0
**Date:** 2026-02-15
**Purpose:** Initialize a new AI assistant chat session to work on BestWorkplace xWiki documentation

---

> **NOTE: PRIMARY WORKFLOW**
>
> The primary workflow is **direct `.xwiki` file editing** in `Docs/xwiki-pages/The Best Workplace/`.
> Agents edit `.xwiki` files directly, commit to git, and use scripts to convert to/from XAR.
>
> See **[AGENTS_xWiki.md](AGENTS_xWiki.md)** for the current workflow.

---

## What This Is

This document initializes a **new AI assistant chat session** to safely work on **BestWorkplace's XWiki documentation**.

**BestWorkplace** is a curated knowledge base on agile leadership, team topologies, coaching, and creating great workplaces. The documentation is maintained in **XWiki 2.1 format** and published via **GitHub Pages**. This workflow allows AI assistants to help improve and maintain these documents.

---

## Current Workflow: Direct .xwiki Editing

1. **Edit .xwiki files** directly in `Docs/xwiki-pages/The Best Workplace/`
2. **Commit to git** for version control
3. **Preview locally**: `Docs\xwiki-pages\View.cmd`
4. **Build gh-pages**: `python Docs/xwiki-pages/scripts/build_ghpages.py`
5. **Deploy**: `powershell Docs/xwiki-pages/scripts/deploy-ghpages.ps1`
6. **Convert to XAR** when ready for xWiki import:
   ```bash
   python Docs/xwiki-pages/scripts/xwiki_tree_to_xar.py Docs/xwiki-pages --output BestWorkplace.xar
   ```
7. **Import XAR** to xWiki (Administration → Import)

**Key Principle:** Git is the master source; GitHub Pages is the public-facing site; xWiki is synchronized via XAR import/export when needed.

---

## Legacy: Claude Projects JSON Workflow (Reference Only)

### How It Worked

1. **Export from XWiki** → Fulltree JSON snapshot (pages + diagrams)
2. **AI Assistant** reads snapshot, proposes/applies improvements following strict rules
3. **AI Assistant** exports delta (only changed pages) as Python script
4. **Convert back** → XAR file for XWiki import
5. **Import to XWiki** → Changes are now in the master system

### Legacy: Cursor IDE xar-to-xar Workflow

### Export Commands
- `"Export"` or `"Export delta"` → Only changed pages since last export
- `"Export full"` → Complete corpus

### Markdown Conversion
- `"Import MD <filepath> as page <pageId>"` → Convert .md file to xWiki markup, add to corpus
- `"Export page <pageId> as MD"` → Convert xWiki page to standard Markdown file

Mermaid diagrams are automatically converted in both directions (GLOBAL-R-037/038).

### Versioning
- Each export auto-increments patch: 0.9.70 → 0.9.71 → 0.9.72
- Exception: delta then full without changes = same version

### Differences from Claude Projects
- **No handshake needed** – files available immediately
- **xar-to-xar** – you only deal with .xar files
- **Auto-versioning** – no manual version tracking needed
- **Direct file editing** – no generator scripts required

See GLOBAL-R-034, GLOBAL-R-035, GLOBAL-R-036 in GlobalMasterKnowledge for full rules.

---

## Files You (The User) Must Attach (Claude Projects)

Attach these files to initialize the session. **Filenames may vary** - use newest versions:

### 1. **Global Rules (Required)**
- **Placeholder:** `<GLOBAL_MASTERKNOWLEDGE>`
- **Example:** `GlobalMasterKnowledge_for_xWiki.md`
- **Contains:** All behavioral rules and constraints for the AI assistant
- **Action:** The assistant must read this and adopt all rules via `MergeIntoYourKnowledge`

### 2. **Baseline Fulltree JSON Snapshot (Required)**
- **Placeholder:** `<FULLTREE_JSON_BASELINE>`
- **Contains:** Complete XWiki corpus (pages in `xwiki/2.1` markup, diagrams in Mermaid)
- **Purpose:** Starting point for all work in this session

### 3. **Working Delta (Optional but Recommended)**
- **Placeholder:** `<FULLTREE_JSON_DELTA_WORKING_STATE>` or `<DELTA_GENERATOR_SCRIPT>`
- **Purpose:** If continuing from a previous chat that made changes, this contains only the modified pages
- **Effect:** Assistant will treat **baseline + delta** as the current working state

### 4. **Conversion Scripts (Optional - Reference Only)**
- **Placeholders:** `<XAR_TO_JSON_SCRIPT>`, `<JSON_TO_XAR_SCRIPT>`
- **Purpose:** Reference for understanding the data format; assistant does NOT modify these

---

## Required Startup Handshake

**The assistant MUST complete this handshake before doing any work:**

### Step 1: Confirm Files Loaded
State exactly which files were loaded:
```
Loaded GlobalMasterKnowledge: [exact filename and version]
Loaded Baseline Corpus: [exact filename]
Loaded Working Delta: [exact filename] OR [No delta provided]
```

### Step 2: State Working State Policy
```
Current Working State:
- If delta provided: Baseline + Delta = Working Version
- If no delta: Baseline = Working Version
```

### Step 3: State Delta Baseline for Exports
```
Delta Baseline for Exports:
- Exports will be "delta since [baseline filename]"
- Version will auto-increment: [current] → [next]
```

### Step 4: Confirm Operating Rules
```
Will NOT change any page/diagram without explicit request or confirmed proposal
Will ASK for confirmation when scope/intent is ambiguous
Will default to DELTA-ONLY in messages and exports
Will export via PYTHON GENERATOR SCRIPT (no raw JSON in chat)
Will keep "Show" commands READ-ONLY (displays current working version)
Will follow all rules from GlobalMasterKnowledge v[X]
```

### Step 5: Wait for Instruction
```
Ready. What would you like me to work on?
```

**The assistant must complete ALL 5 steps before doing any work.**

---

## How to Request Work (Recommended Phrases)

Use these clear, unambiguous commands:

### Viewing Content (Read-Only)
- `"Show page <NODE_ID>"`
- `"Show diagram <NODE_ID>"`
- `"List all pages in <SPACE>"`

### Proposing Changes (No Modifications Yet)
- `"Propose improvements to page <NODE_ID>"`
- `"Analyze <NODE_ID> and suggest changes"`
- `"Review <NODE_ID> for consistency with <OTHER_PAGE>"`

### Applying Changes (Modifications)
- `"Apply proposal A to page <NODE_ID>"`
- `"Apply these specific changes to pages: [list]"`
- `"Move section X from page Y to page Z"`

### Exporting Work
- `"Export delta"` → Only changed pages since baseline
- `"Export full"` → Complete corpus (use sparingly)
- `"Export"` → Defaults to delta

---

## Key Rules Summary (From GlobalMasterKnowledge)

The assistant must follow all rules in `<GLOBAL_MASTERKNOWLEDGE>`. Key highlights:

### Change Control
- **GLOBAL-R-016:** Non-lossy editing (>=98% length unless explicitly requested to reduce)
- **GLOBAL-R-017:** No changes without explicit request or confirmed proposal
- **GLOBAL-R-021:** "Show" is always read-only (never modifies content)
- **GLOBAL-R-023:** Changes only allowed if explicitly requested or proposal confirmed

### Export Rules
- **GLOBAL-R-015:** Default to delta-only (not full exports)
- **GLOBAL-R-018:** Export via Python generator script (no raw JSON in chat)
- **GLOBAL-R-033:** Auto-increment version on each export

### Display Rules
- **Anti-truncation:** Never use "..." ellipses in page displays unless explicitly requested
- **Current working version:** Always show baseline + applied deltas, not stale baseline
- **Full content:** If page is long, ask whether to show full page or selected sections

---

## Common Workflows

### Workflow 1: Review and Improve a Page
```
User: "Show page The Best Workplace.Knowledge.Team Topologies.WebHome"
Assistant: [Displays full page content, read-only]

User: "Propose improvements focusing on clarity"
Assistant: [Analyzes, proposes specific changes, NO modifications yet]

User: "Apply proposal 2 and 4"
Assistant: [Applies only those changes, confirms completion]

User: "Export delta"
Assistant: [Creates Python generator script with version increment]
```

### Workflow 2: Major Reorganization
```
User: "Move the OKR section from Leadership to its own top-level Knowledge page"
Assistant: [Confirms understanding] "This will modify 2 pages. Proceed?"

User: "Yes"
Assistant: [Makes changes, reports what was modified]

User: "Export delta"
Assistant: [Creates generator script]
```

### Workflow 3: Create New Page
```
User: "Create new page 'Psychological Safety' under Knowledge"
Assistant: [Creates page with proper structure]

User: "Add content about team psychological safety and its impact"
Assistant: [Adds content following xWiki 2.1 syntax]

User: "Export delta"
Assistant: [Exports only the new page]
```

---

## Troubleshooting

### If Assistant Violates Rules
```
User: "Rule Violation: Read GLOBAL-R-[Number]"
```

### If Assistant Shows Stale Content
```
User: "You're showing baseline, not current working version. Apply the delta first."
```

### If Assistant Truncates Content
```
User: "Show full page without truncation"
```

### If Assistant Changes Without Permission
```
User: "STOP. You modified without my explicit request. Rule Violation: Read GLOBAL-R-017 and GLOBAL-R-023"
```

---

## Success Criteria

A properly initialized session should have:

- **Handshake completed** (all 5 steps confirmed)
- **Rules acknowledged** (GlobalMasterKnowledge adopted)
- **Working state clear** (baseline + delta understood)
- **Delta baseline known** (for version tracking)
- **Operating constraints confirmed** (read-only show, delta-only export, etc.)
- **Ready state** (waiting for first instruction)

---

## For The Assistant: Quick Start Checklist

When you see this initialization document, immediately:

1. Read `<GLOBAL_MASTERKNOWLEDGE>` and type internally: `MergeIntoYourKnowledge`
2. Load `<FULLTREE_JSON_BASELINE>` (note exact filename)
3. Load `<FULLTREE_JSON_DELTA_WORKING_STATE>` if provided
4. Complete the 5-step handshake (listed above)
5. WAIT for user's first instruction (do NOT propose anything yet)

**DO NOT:**
- Start working before completing handshake
- Propose changes without being asked
- Assume you know what needs fixing
- Modify anything without explicit request
- Export raw JSON (use generator script)
- Truncate content with "..."
