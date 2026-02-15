# AGENTS.md

How AI agents should operate in the BestWorkplace repository.

---

## Fundamental Rules

### Generic by Design
- **No assumptions about content structure.** Agents must not assume specific page hierarchies, topics, or content patterns.
- **Preserve existing content.** Do not rewrite, summarize, or restructure content unless explicitly asked.
- **Parameterize, don't specialize.** Use configuration over conditionals when building scripts or workflows.

---

## Reading .xwiki Files

Documentation lives in xWiki 2.1 format under `Docs/xwiki-pages/The Best Workplace/`. Quick syntax: `= H1 =`, `== H2 ==`, `**bold**`, `//italic//`, `[[Link>>Target]]`, `{{info}}...{{/info}}`, `{{mermaid}}...{{/mermaid}}`, `{{code language="..."}}...{{/code}}`.

Preserve existing syntax when editing. Full rules: `Docs/AGENTS/GlobalMasterKnowledge_for_xWiki.md`.

**Format rule:** Each document exists in exactly ONE authoritative format. If a `.md` file shows "Moved to xWiki", read the `.xwiki` file instead.

---

## Commands

| Action | Command |
|--------|---------|
| Preview locally | `Docs\xwiki-pages\View.cmd` |
| Build gh-pages | `python Docs/xwiki-pages/scripts/build_ghpages.py` |
| Deploy gh-pages | `powershell Docs/xwiki-pages/scripts/deploy-ghpages.ps1` |
| XAR to xWiki tree | `python Docs/xwiki-pages/scripts/xar_to_xwiki_tree.py <file.xar> --output Docs/xwiki-pages` |
| xWiki tree to XAR | `python Docs/xwiki-pages/scripts/xwiki_tree_to_xar.py Docs/xwiki-pages --output BestWorkplace.xar` |
| Download attachments | `python Docs/xwiki-pages/scripts/download_attachments.py` |

---

## Safety

- Do not change secrets/credentials or commit them.
- Do not modify generated files or build output (`gh-pages-build/`) unless requested.
- Avoid destructive git commands unless explicitly asked.
- Platform is Windows. Use PowerShell-compatible commands.

---

## Agent Handoff Protocol

When starting any new task, every agent MUST:

1. **Assess fit**: Is this task best suited for the current agent/tool, or would another be more effective?
2. **Check role and model**: Identify your current role and underlying LLM model. If either is a poor match for the task, inform the Captain and propose a better-suited role, model tier, or both. Reference the Model-Class Guidelines in `Docs/AGENTS/Multi_Agent_Collaboration_Rules.md` §6 for tier strengths.
3. **Recommend if not**: Tell the user which agent/tool to use, why, what context it needs (files to read, decisions already made), and any work completed so far.

### Role Activation Protocol

When the user starts with "As \<Role\>" or assigns you a role mid-conversation:

1. **Look up the role** in the alias table below → find the canonical role name
2. **Read required documents** listed for that role in `Docs/AGENTS/Multi_Agent_Collaboration_Rules.md` §2 Role Registry
3. **Check learnings**: Scan your role's section in `Docs/AGENTS/Role_Learnings.md` for tips and gotchas from previous agents
4. **Acknowledge**: State your role, focus areas, and which docs you've loaded
5. **Stay in role**: Focus on that role's concerns. Flag (don't act on) issues outside your scope.
6. **On handoff/completion**: Summarize work done, decisions made, open items, files touched. If you learned something useful, append it to `Role_Learnings.md`.

**Role Alias Quick-Reference:**

| User Says | Maps To | Registry Section |
|-----------|---------|-----------------|
| "Tech Writer", "xWiki Expert", "xWiki Developer" | Technical Writer | §2.1 |
| "Product Manager", "Product Owner", "Sponsor", "Content Strategist" | Product Strategist | §2.2 |
| "GIT Expert", "GitHub Expert", "DevOps" | DevOps Expert | §2.3 |
| "Agents Supervisor" | Captain (human role) | §2.4 |

**If the role is NOT in the table above:**
1. Tell the user which existing role is closest (if any) and ask whether to use that one
2. If no close match: read `/AGENTS.md` as baseline, then ask the user what documents and source files are relevant for this role
3. Proceed with steps 3-5 above once clarified

Full role definitions, required reading, and area-to-document mapping: `Docs/AGENTS/Multi_Agent_Collaboration_Rules.md`

### Working Principles

- **Stay focused.** Do the task you were given. Do not wander into adjacent improvements unless asked.
- **Plan before non-trivial changes.** For multi-file changes or unfamiliar content: explore the relevant pages, draft an approach, then implement. Skip planning only for single-file, obvious changes.
- **Don't guess — read or ask.** If unsure what a page contains, read it. Don't assume from page titles or training knowledge. If still unsure, ask the human.
- **Quality over quantity.** A small, correct change beats a large, sloppy one. Read before you edit. Verify after you change.
- **Verify your work.** After implementing, preview locally or check output. Don't mark work done without verification.
- **Be cost-aware.** Minimize unnecessary file reads and token usage. Don't re-read files you already have in context. Don't generate verbose output when concise will do.
- **Don't gold-plate.** Deliver what was requested — don't also restructure the page, add sections, and update other docs unrequested. But DO report issues, inconsistencies, or improvement opportunities you notice along the way — just flag them, don't act on them without asking.
- **Cross-check content against docs.** When editing one page, check related pages for consistency. Report any mismatches — stale cross-references and diverged content are high-value catches.
- **Summarize when done.** List files touched, note assumptions, and flag if verification was not run and why.

### Consolidate WIP Procedure

When the Captain requests "Consolidate WIP", follow this procedure to clean up `Docs/WIP/` (if it exists). The goal is to keep WIP lean: only active proposals and in-progress work remain; everything else moves to ARCHIVE or gets absorbed into documentation.

#### Step 1: Audit each WIP file

For every file in `Docs/WIP/` (excluding `README.md`):

1. **Read the file** completely.
2. **Cross-check against content and status:**
   - Has the proposed work been implemented? (Check git log, documentation pages)
   - Is the document superseded by a newer document?
   - Are pending items still relevant?
3. **Classify the file** into one of these categories:

| Category | Criteria | Action |
|----------|----------|--------|
| **DONE** | All items implemented; no open decisions remain | Archive (Step 2) |
| **SUPERSEDED** | A newer document replaces this | Archive (Step 2) |
| **PARTIALLY DONE** | Some items done, some still pending | Update in place (Step 3) |
| **STILL ACTIVE** | Work not started or actively in progress | Keep as-is |
| **STALE** | Not referenced in 3+ months, not blocking any decision | Ask Captain: archive or revive? |

#### Step 2: Archive completed files

For each file classified as DONE or SUPERSEDED:

1. **Extract any forward-looking content** (future goals, deferred decisions, open questions) before archiving. Ask the Captain where this content should live.
2. **Move the file** to `Docs/ARCHIVE/`.
3. **Update** `Docs/WIP/README.md`: remove the entry and add to "Cleanup History".

#### Step 3: Update partially-done files

For each file classified as PARTIALLY DONE:

1. **Mark completed items** with a completion date.
2. **Mark remaining items** with their current status.
3. **Remove obsolete content** (outdated approaches, rejected alternatives).
4. **Update** the file's header status line to reflect current state.

#### Step 4: Report to Captain

Provide a summary:
- Files archived (with reason)
- Files updated (what changed)
- Files kept as-is (confirm still active)
- Items needing Captain decision (stale files, ambiguous status, content placement)

**Important:** When unsure whether a file is done or where extracted content belongs, **ask the Captain** — don't guess. This procedure is interactive, not autonomous.

---

### Tool Strengths Reference

| Task Type | Best Tool | Why |
|-----------|-----------|-----|
| Complex multi-step reasoning | Claude Code (Opus) | Deep reasoning, plan mode |
| Inline completions | GitHub Copilot | Fast, context-aware |
| Multi-file edits with preview | Cursor (Composer) | Visual diff, multi-file edits |
| Autonomous multi-step workflows | Cline | Runs commands, creates files autonomously |
| Documentation + diagrams | Agent with TECH_WRITER role | See `Docs/AGENTS/TECH_WRITER_START_HERE.md` |
| xWiki documentation | Any agent | Read `Docs/AGENTS/AGENTS_xWiki.md` first |
| gh-pages deployment | Agent with DEVOPS role | See `Docs/AGENTS/Multi_Agent_Collaboration_Rules.md` §2.3 |

---

## Workflow

- Solo developer + AI agents. Direct push to main is normal.
- Commits: conventional commits `type(scope): description`.
