# BestWorkplace Multi-Agent Collaboration Rules

**Version:** 1.0
**Date:** 2026-02-15
**Status:** Active
**Owner:** Robert Schaub

---

## Purpose

This document defines the rules, roles, and workflow for multi-agent collaboration on BestWorkplace documentation tasks. It establishes a structured approach where multiple LLM agents (via Claude Code, Cursor, Cline, GitHub Copilot, and other tools) work collaboratively through defined roles to plan, review, author, and publish xWiki content about agile leadership via GitHub Pages.

---

## 1. Global References

All agents MUST read and adhere to these foundational documents before starting any task:

### 1.1 Mandatory Knowledge Sources

| Document | Location | Purpose |
|----------|----------|---------|
| **AGENTS.md** | `/AGENTS.md` | Fundamental rules, safety, workflow |
| **GlobalMasterKnowledge for xWiki** | `/Docs/AGENTS/GlobalMasterKnowledge_for_xWiki.md` | xWiki rules and document handling |
| **Root Documentation Page** | `/Docs/xwiki-pages/The Best Workplace/WebHome.xwiki` | Root documentation page |

### 1.2 Area-to-Documents Mapping

When a task specifies an **Area**, read the corresponding documents:

| Area | Required Documents |
|------|-------------------|
| **Documentation** | `Docs/AGENTS/TECH_WRITER_START_HERE.md`, `Docs/AGENTS/GlobalMasterKnowledge_for_xWiki.md` |
| **Content** | `Docs/xwiki-pages/The Best Workplace/` (the actual xWiki pages) |
| **Deployment** | `.github/workflows/deploy-docs.yml`, `Docs/xwiki-pages/scripts/` |
| **Structure** | `Docs/AGENTS/AGENTS_xWiki.md` |

**If no Area is specified:** Agent should intelligently identify relevant documents based on the task description.

### 1.3 Role-to-Area Mapping

When activated in a role, use this table to identify which areas are within your scope:

| Role | Primary Areas | Secondary Areas |
|------|--------------|-----------------|
| Technical Writer | Documentation, Content | Structure |
| Content Strategist | Content | Documentation |
| DevOps Expert | Deployment | — |
| Viewer Developer | Structure, Deployment | Documentation |

### 1.4 WIP Folder Protocol

- **Location:** `/Docs/WIP/`
- **Purpose:** Active collaborative documents, plans, reviews in progress
- **On Completion:** Move finalized documents to appropriate `Docs/` subfolder or `Docs/ARCHIVE/REVIEWS/`

---

## 2. Role Registry

> **Activation:** When the user says "As \<Role\>", look up the role alias in `AGENTS.md` → Role Activation Protocol to find the canonical role below. Read that role's Required Reading before starting work.
>
> **Lite mode:** Lightweight models with limited context — see §6.3 for a graduated loading strategy that defers non-essential reads.

### 2.1 Technical Writer

**Aliases:** Tech Writer, xWiki Expert, Content Editor
**Mission:** Documentation quality, consistency, maintainability

**Start Here:** Read `/Docs/AGENTS/TECH_WRITER_START_HERE.md` for a comprehensive onboarding guide specific to this role.

**Focus Areas:**
- Documentation accuracy and completeness
- Cross-reference integrity
- Terminology consistency (see AGENTS.md terminology table)
- User-facing documentation
- xWiki syntax and page structure

**Authority:**
- Documentation standards enforcement
- Terminology corrections
- Archive decisions for outdated docs

**Required Reading** (on activation):
| Document | Why |
|----------|-----|
| `/AGENTS.md` | Fundamental rules, .xwiki reading rules |
| `/Docs/AGENTS/TECH_WRITER_START_HERE.md` | Comprehensive role-specific guide |
| `/Docs/AGENTS/GlobalMasterKnowledge_for_xWiki.md` | xWiki syntax rules |

**Key Source Files:**
- `Docs/xwiki-pages/The Best Workplace/` — All xWiki documentation
- `Docs/xwiki-pages/scripts/` — Conversion tools (xar_to_xwiki_tree.py, xwiki_tree_to_xar.py)

**Deliverables:** Documentation updates, terminology audits, documentation reorganization plans

**Anti-patterns:**
- Duplicating content across xWiki and Markdown (each topic lives in ONE place)
- Using domain-specific examples in documentation
- Modifying viewer, scripts, or deployment workflows (delegate to Viewer Developer or DevOps Expert)

---

### 2.2 Content Strategist

**Aliases:** Product Manager, Product Owner, Sponsor
**Mission:** Content direction, topic prioritization, audience alignment

**Focus Areas:**
- Content strategy and topic prioritization
- Audience needs assessment
- Acceptance criteria for documentation topics
- Scope decisions

**Authority:**
- Content prioritization
- Topic acceptance/rejection
- Scope and milestone decisions
- Stakeholder communication strategy

**Required Reading** (on activation):
| Document | Why |
|----------|-----|
| `/AGENTS.md` | Project overview and current state |
| `/Docs/xwiki-pages/The Best Workplace/WebHome.xwiki` | Root documentation page — current content landscape |

**Key Source Files:** None (this role reviews and directs, does not edit)

**Deliverables:** Content direction documents, acceptance criteria, prioritization decisions, scope definitions

**Anti-patterns:**
- Editing xWiki pages directly (delegate to Technical Writer)
- Making structural changes without consulting Technical Writer
- Modifying deployment configuration (delegate to DevOps Expert)
- Modifying viewer or scripts (delegate to Viewer Developer)

---

### 2.3 DevOps Expert

**Aliases:** GIT Expert, GitHub Expert, DevOps
**Mission:** Repository hygiene, CI/CD, deployment

**Focus Areas:**
- Git workflows and branch management
- GitHub Actions configuration and deployment
- Repository settings and security
- gh-pages deployment pipeline

**Authority:**
- Git workflow decisions
- Deployment configuration changes
- Repository and branch protection settings

**Required Reading** (on activation):
| Document | Why |
|----------|-----|
| `/AGENTS.md` | Commands, safety rules, current state |
| `.github/workflows/deploy-docs.yml` | Deployment workflow |

**Key Source Files:**
- `.github/workflows/deploy-docs.yml` — GitHub Actions workflow
- `Docs/xwiki-pages/scripts/deploy-ghpages.ps1` — Manual deployment script

**Deliverables:** Deployment configuration, CI/CD pipeline setup, repository management

**Anti-patterns:**
- Editing content pages (delegate to Technical Writer)
- Force-pushing or destructive git operations without explicit user approval
- Making content direction decisions (delegate to Content Strategist)
- Modifying viewer or build scripts (delegate to Viewer Developer)

---

### 2.4 Viewer Developer

**Aliases:** Developer, xWiki Developer, Extension Developer
**Mission:** Develop and maintain the xWiki viewer, VS Code extension, and build tooling

**Focus Areas:**
- xWiki viewer (xwiki-viewer.html) — HTML, JavaScript, CSS
- VS Code xWiki Preview extension — TypeScript
- Build and conversion scripts — Python
- PowerShell local server
- Viewer sync between BestWorkplace and FactHarbor repos

**Authority:**
- Viewer architecture and rendering decisions
- Parser and CSS changes
- Script improvements and bug fixes

**Required Reading** (on activation):
| Document | Why |
|----------|-----|
| `/AGENTS.md` | Project rules, safety |
| `/Docs/AGENTS/AGENTS_xWiki.md` | Viewer architecture, gh-pages pipeline |
| `/Docs/AGENTS/Role_Learnings.md` | DevOps/Viewer tips and gotchas |

**Key Source Files:**
- `Docs/xwiki-pages/viewer-impl/xwiki-viewer.html` — Shared viewer (identical in BestWorkplace and FactHarbor)
- `Docs/xwiki-pages/viewer-impl/Open-XWikiViewer.ps1` — Local preview server
- `Docs/xwiki-pages/scripts/build_ghpages.py` — gh-pages build (applies patches to viewer)
- FactHarbor: `tools/vscode-xwiki-preview/` — VS Code extension source

**Deliverables:** Viewer fixes, new rendering features, parser improvements, script enhancements

**Anti-patterns:**
- Editing content pages (delegate to Technical Writer)
- Making content direction decisions (delegate to Content Strategist)
- Changing viewer HTML without verifying `build_ghpages.py` patches still match
- Forgetting to sync viewer changes between BestWorkplace and FactHarbor repos

---

### 2.5 Captain (Human Role)

**Note:** This is the human user's meta-role, not an agent role. Documented here so agents understand the human's authority and responsibilities.

**Aliases:** Agents Supervisor
**Mission:** Overall project direction, conflict resolution, final authority

**Responsibilities:**
- Assigning roles and tasks to agents
- Resolving disagreements between agents/roles
- Making strategic decisions (scope, timeline, priorities)
- Approving deployment changes and structural reorganizations
- Managing git operations (push to remote, branch management)

**What agents should expect from the Captain:**
- Task assignments via "As \<Role\>" pattern
- Approval/rejection of plans and proposals
- Context from previous agent sessions
- Resolution of escalated decisions

**When to escalate to the Captain:** See §7 Escalation Protocol.

---

## 3. Workflow Patterns

> **Usage:** The workflow below is active for complex or significant content tasks. For simple changes, use the Quick Fix Workflow (3.2).
>
> **Pre-task fitness check:** Before starting any workflow, every agent must verify that their current role and LLM model tier are appropriate for the task. If not, inform the Captain and propose a better fit. See the Agent Handoff Protocol in `/AGENTS.md` and Model-Class Guidelines in §6.

### 3.1 Standard Feature Workflow

```mermaid
flowchart TB
    subgraph Phase1["Phase 1: Planning"]
        P1[Technical Writer<br/>Creates Content Plan]
        P2[Content Strategist<br/>Reviews Content Direction]
    end

    subgraph Phase2["Phase 2: Review"]
        R1[Content Strategist<br/>Approves Plan]
        R2[Technical Writer<br/>Revises Based on Feedback]
    end

    subgraph Phase3["Phase 3: Implementation"]
        I1[Technical Writer<br/>Authors xWiki Content]
        I2[Technical Writer<br/>Verifies Cross-References]
    end

    subgraph Phase4["Phase 4: Deployment"]
        D1[DevOps Expert or Viewer Developer<br/>Builds and Deploys to gh-pages]
        D2[Content Strategist<br/>Final Content Verification]
    end

    P1 --> P2 --> R1 --> R2 --> I1 --> I2 --> D1 --> D2
```

### 3.2 Quick Fix Workflow

For small, well-understood changes:

1. **Technical Writer** proposes fix with rationale
2. **Content Strategist** reviews and approves
3. **Technical Writer** implements
4. **Content Strategist** verifies

### 3.3 Complex Investigation Workflow

For issues requiring deep analysis by a **single investigator** with sequential review:

1. **Technical Writer**, **Viewer Developer**, or **DevOps Expert** investigates root cause
2. **Content Strategist** validates findings
3. **Technical Writer** proposes solution options
4. **All roles** discuss trade-offs (async via document)
5. Proceed to Standard Feature Workflow

> **§3.3 vs §3.4:** Use §3.3 when one expert can investigate and the team reviews sequentially. Use §3.4 when you want **independent parallel perspectives** from multiple agents on the same problem.

### 3.4 Multi-Agent Investigation Workflow

For complex tasks where the Captain wants multiple agents to independently investigate, propose solutions, and produce a consolidated plan.

**When to use:** The Captain assigns the same investigation task to 2+ agents (potentially different roles, tools, or models) and wants a single unified output document.

**Concurrency model: Hub-and-Spoke.** Each agent writes to their own spoke file (zero contention). The consolidator is the only agent that reads all spoke files and merges them into the hub.

**Workflow:**

```mermaid
flowchart TB
    subgraph Init["Phase 0: Initiation"]
        C1[Captain sends INVESTIGATE to first agent]
        C2[First agent creates hub document]
        C3[Captain sends INVESTIGATE to remaining agents]
    end

    subgraph Investigate["Phase 1: Independent Investigation"]
        A1[Agent 1<br/>Writes to own spoke file]
        A2[Agent 2<br/>Writes to own spoke file]
        AN[Agent N<br/>Writes to own spoke file]
    end

    subgraph Consolidate["Phase 2: Consolidation"]
        CON[Consolidator Agent<br/>Reads all spoke files<br/>Writes consolidated output to hub]
    end

    subgraph Review["Phase 3: Review & Approval"]
        REV[Reviewer / Implementer<br/>Reads hub document]
        CAP[Captain approves plan]
    end

    C1 --> C2 --> C3 --> A1 & A2 & AN --> CON --> REV --> CAP
```

**Phase 0 — Initiation (Captain)**

1. Send the **INVESTIGATE** command to the **first agent** and wait for confirmation that the hub document has been created
2. Once confirmed, send **INVESTIGATE** to the remaining agents — they can all run in parallel

This two-step dispatch eliminates the document-creation race condition. No other manual preparation is needed.

**Phase 1 — Independent Investigation (each agent)**

1. **If the hub document does not exist** (first agent only):
   a. Create it from the Investigation Document Template (§4.5), populate the **Investigation Brief** from the Captain's task description
   b. Set document status to `INVESTIGATING`
   c. Add your row to the **Participant Tracker** with your spoke file path
2. **If the hub document exists** (subsequent agents):
   a. Read the Investigation Brief
   b. Add your row to the **Participant Tracker** with your spoke file path
3. **Create your spoke file**: `Docs/WIP/{Topic}_Report_{Role}_{Agent}.md` using the Spoke File Format (§4.5)
4. Perform investigation (read docs, analyze content, research) — write everything to **your spoke file**
5. When done: update your Participant Tracker row to `DONE`
6. Do NOT read other agents' spoke files (anti-anchoring rule — reports are in separate files, making this naturally enforced)
7. Do NOT attempt consolidation — that is Phase 2

**Phase 2 — Consolidation (designated agent)**

1. Captain assigns a consolidator agent (typically a high-capability model)
2. Consolidator sets hub document status to `CONSOLIDATING`
3. Consolidator reads ALL spoke files listed in the Participant Tracker (where status = `DONE`)
4. Consolidator writes the following sections in the hub document under `# CONSOLIDATED OUTPUT`:
   - **Consolidated Analysis**: Summary, Agreement Matrix (which investigators confirmed each finding), Strongest Contributions per investigator
   - **Consolidated Plan**: Phased implementation plan with files, risks, and effort indicators — with **Open Questions** subsection for unresolved disagreements requiring Captain decision
5. Consolidator appends each spoke file's content under `# INVESTIGATION REPORTS` in the hub for traceability
6. Set document status to `READY_FOR_REVIEW`

**Phase 3 — Review & Implementation**

1. Captain (or assigned reviewer) reads the hub document
2. Captain approves, requests changes, or escalates open questions
3. Decisions are recorded in the **Decision Record** section of the hub
4. Once approved: set status to `APPROVED` → implementer proceeds using Standard Feature Workflow (§3.1) or Quick Fix Workflow (§3.2)

**Rules:**
- Participants, their roles, and their number vary per task — the Captain decides who participates
- Each agent writes to their own spoke file — no shared-file contention during Phase 1
- Anti-anchoring: agents must NOT read other agents' spoke files during Phase 1 (file separation makes this naturally enforced)
- The consolidator must not discard minority findings — disagreements are valuable signal
- If an agent discovers something outside the investigation scope, it flags it in an `**Out of Scope**` note in their spoke file but does not investigate further
- The hub document is the single source of truth for the downstream reviewer/implementer
- Agents MUST update their row in the **Participant Tracker** when changing state
- If a participant remains in `INVESTIGATING` or `WRITING` status and their agent session is no longer active, the Captain may set their status to `ABANDONED` and proceed with consolidation using available reports. The consolidator should note the missing perspective.

#### Decision Authority & Escalation

Decisions during investigation and consolidation follow a tiered authority model based on impact and risk. Escalate upward when the threshold is exceeded. See also the general Escalation Protocol (§7).

| Level | Who decides | Scope | When applicable | Examples |
|-------|------------|-------|-----------------|---------|
| **1 — Lead agent** | The individual agent decides alone | Low impact, easily reversible, within own report | All phases | Investigation methodology, which files to analyze, report structure, internal findings |
| **2 — Agent consent** | Lead agent + one relevant agent agree | Medium impact, affects shared output | Phase 2–3 only (agents cannot communicate during Phase 1) | Proposing a specific content approach, recommending a tool, flagging a finding as critical |
| **3 — Agent consensus** | All participating agents agree (via document) | High impact, affects multiple areas | Phase 2–3, orchestrated by Captain | Consolidation priorities, plan phasing, recommending structural changes, disagreement resolution between agents |
| **4 — Captain approval** | Captain must explicitly approve | Very high impact, irreversible, or outside investigation scope | Any phase | Content reorganization, deployment changes, removing documentation, expanding investigation scope, approving the final plan |

**Escalation rules:**
- When in doubt, escalate one level up — over-escalating is safer than under-escalating
- An agent who identifies a Level 4 decision must flag it in **Open Questions** and NOT proceed without Captain approval
- The consolidator operates at Level 3: they synthesize and structure, but cannot make Level 4 decisions unilaterally
- Level 2–3 decisions must be documented in the report or consolidated plan with rationale
- The Captain can override any lower-level decision

#### Captain Commands

The Captain uses these standardized prompts to direct agents. Copy, fill in the blanks, and paste to the agent.

**INVESTIGATE** — Assign an agent to investigate (Phase 1):
```
As {Role}, investigate using the Multi-Agent Investigation Workflow (§3.4).
Document: Docs/WIP/{filename}.md
Task: {what to investigate — clear questions to answer}
Inputs: {files, data, reports, or artifacts to examine}
Scope: {what is NOT in scope}
Focus on: {optional specific focus area or questions for this agent}

If the hub document does not exist, create it from the §4.5 template and populate the Investigation Brief.
Add yourself to the Participant Tracker, create your spoke file (§4.5), and write your report there.
```

**CONSOLIDATE** — Assign the consolidator (Phase 2):
```
As {Role}, consolidate the investigation in Docs/WIP/{filename}.md
Set document status to CONSOLIDATING.
Read ALL spoke files listed in the Participant Tracker (where Status = DONE), then write:
- ## Consolidated Analysis (summary, agreement matrix, strongest contributions)
- ## Consolidated Plan (phased, with files and risks)
- ### Open Questions (unresolved disagreements needing Captain decision)
Copy each spoke file's content under # INVESTIGATION REPORTS for traceability.
Set document status to READY_FOR_REVIEW when done.
```

**REVIEW** — Assign a reviewer (Phase 3):
```
As {Role}, review the consolidated plan in Docs/WIP/{filename}.md
Assess the plan for completeness, feasibility, and risks.
Add your review under ## Review Log using the Review Comment Format (§4.4).
```

**STATUS** — Check investigation progress (any phase):
```
Read Docs/WIP/{filename}.md and report:
- Document status
- Participant Tracker state (who is done, who is still working)
- Any agents with ABANDONED status or stale sessions
```

**PROPOSE** — Ask an agent to propose next steps (after any phase):
```
As {Role}, read Docs/WIP/{filename}.md and propose next steps.
Consider the current document status, completed reports, and open questions.
Append your proposal as a new report under # INVESTIGATION REPORTS:
### Proposal: {Role} ({Agent/Model}) — {Date}
Include: what to do next, who should do it, priorities, and any blockers.
Do NOT write into the # CONSOLIDATED OUTPUT sections — those are reserved for the consolidator.
```

**IMPLEMENT** — Assign an agent to execute the approved plan (after Phase 3):
```
As {Role}, implement the approved plan in Docs/WIP/{filename}.md
Read ## Consolidated Plan and execute it phase by phase.
After each phase: verify the build, update the document status, and report progress.
If you encounter blockers or deviations from the plan, stop and report to the Captain.
```

#### Activation Walkthrough (Captain Quick Reference)

No manual document preparation needed — agents handle it.

**Step 1 — Dispatch first agent**

Paste the **INVESTIGATE** command into the first agent. Wait for confirmation that the hub document has been created and the Investigation Brief is populated.

**Step 2 — Dispatch remaining agents** (in parallel)

Paste the **INVESTIGATE** command into each additional agent. They find the hub document, self-register in the Participant Tracker, and create their own spoke files. All agents write to their own files — no contention.

**Step 3 — Monitor progress**

Paste the **STATUS** command into any available agent to check the Participant Tracker. When all participants show `DONE`, proceed to consolidation.

**Step 4 — Consolidate**

Paste the **CONSOLIDATE** command into a high-capability agent (e.g., Opus). The consolidator reads all spoke files, writes the unified analysis + plan into the hub, and copies spoke content under Investigation Reports for traceability.

**Step 5 — Review, Propose, or Implement**

Use **REVIEW**, **PROPOSE**, or **IMPLEMENT** commands as needed. These can go to the same or different agents.

---

### 3.5 Role Handoff Protocol

When the user switches roles mid-conversation or continues work from a previous session:

**Outgoing role provides (in final message):**
1. **Summary**: What was accomplished
2. **Decisions**: Key choices made and rationale
3. **Open items**: Unresolved questions, blocked tasks
4. **Files touched**: Modified/created files list
5. **Warnings**: Gotchas, fragile areas, things to verify
6. **Learnings** (if any): Append to `/Docs/AGENTS/Role_Learnings.md` under your role section — tips, gotchas, wrong assumptions, or missing docs you discovered

**Incoming role should:**
1. Read the handoff summary (if provided by user or in conversation context)
2. Read Required Reading for their role (from §2 Role Registry)
3. Scan your role's section in `/Docs/AGENTS/Role_Learnings.md` for tips and gotchas from previous agents
4. Check `Docs/WIP/` for active task documents related to the current work
5. Acknowledge role activation before starting work

---

## 4. Collaboration Document Protocol

### 4.1 Document Naming Convention

```
Docs/WIP/{TaskTitle}_{DocumentType}.md

Examples:
- Docs/WIP/Leadership_Principles_Content_Plan.md
- Docs/WIP/Content_Structure_Review.md
- Docs/WIP/Deployment_Pipeline_Investigation.md
- Docs/WIP/Agile_Practices_Topic_Investigation_2026-02-15.md  (§3.4 multi-agent investigation)
```

### 4.2 Document Structure

Every collaborative document MUST include:

```markdown
# {Task Name} - {Document Type}

**Status:** DRAFT | IN_REVIEW | APPROVED | IMPLEMENTED | ARCHIVED
**Created:** {date}
**Last Updated:** {date}
**Author Role:** {role name}

---

## Context
{Brief description of the task and why this document exists}

## References
{Links to related documents, requirements, existing content}

---

## Content
{Main content of the document}

---

## Review Log

| Date | Reviewer Role | Status | Comments |
|------|---------------|--------|----------|
| {date} | {role} | {Approved/Changes Requested/Comment} | {summary} |

---

## Decision Record
{Final decisions made, with rationale}
```

### 4.3 Concurrent Editing

- **§3.4 investigations:** No contention — each agent writes to their own spoke file. Only the Participant Tracker in the hub is shared, and updates are brief appends.
- **Other shared documents:** One writer at a time. If two agents need to edit the same document, the Captain sequences them. Always re-read a shared file before editing it — another agent may have changed it since you last read it.

### 4.4 Review Comment Format

When adding review comments:

```markdown
### Review: {Reviewer Role} - {Date}

**Overall Assessment:** {APPROVE | REQUEST_CHANGES | COMMENT_ONLY}

#### Strengths
- {positive observation}

#### Concerns
- **[CRITICAL]** {must fix before proceeding}
- **[SUGGESTION]** {optional improvement}
- **[QUESTION]** {clarification needed}

#### Specific Comments
- Line/Section X: {comment}
```

### 4.5 Investigation Document Template

Used with the Multi-Agent Investigation Workflow (§3.4). File naming: `Docs/WIP/{Topic}_Investigation_{date}.md`

#### Hub Document (shared)

```markdown
# {Topic} — Multi-Agent Investigation

**Status:** INVESTIGATING | CONSOLIDATING | READY_FOR_REVIEW | APPROVED | IMPLEMENTED
**Created:** {date}
**Captain:** {name or role}

---

## Participant Tracker

Each agent adds their own row when joining. No manual setup needed.

| # | Role | Agent/Tool/Model | Report File | Status | Updated |
|---|------|-----------------|-------------|--------|---------|

Status values: `INVESTIGATING` → `WRITING` → `DONE` | `ABANDONED` | `CONSOLIDATING` → `DONE` | `REVIEWING` → `DONE`
Report File: path to the agent's spoke file (e.g., `Docs/WIP/{Topic}_Report_{Role}_{Agent}.md`).

---

## Investigation Brief

**Task:** {What needs to be investigated — clear questions to answer}
**Inputs:** {Files, data, reports, or artifacts agents should examine}
**Scope boundaries:** {What is NOT in scope for this investigation}

---
---

# CONSOLIDATED OUTPUT

> **Reading guide:** Everything below this line is the authoritative, consolidated result.
> It is written by the consolidator in Phase 2 and reviewed/approved in Phase 3.
> During Phase 1 (investigation) these sections are empty — do not fill them in during investigation.

## Consolidated Analysis

### Summary
*(empty until Phase 2)*

### Agreement Matrix

| Finding | Agent 1 | Agent 2 | Agent N |
|---------|---------|---------|---------|

### Strongest Contributions
*(empty until Phase 2)*

---

## Consolidated Plan

*(empty until Phase 2)*

### Open Questions
*(empty until Phase 2)*

---

## Review Log

| Date | Reviewer Role | Assessment | Comments |
|------|---------------|------------|----------|

---

## Decision Record

*(Decisions made by the Captain after review, with rationale)*

---
---

# INVESTIGATION REPORTS

> **Reading guide:** Everything below this line contains reports copied from spoke files by the consolidator.
> After consolidation, these serve as historical reference and traceability — the consolidated output above is authoritative.

*(Consolidator copies each spoke file's content here in Phase 2 for traceability)*

---
```

#### Spoke File Format (one per agent)

File naming: `Docs/WIP/{Topic}_Report_{Role}_{Agent}.md`

```markdown
# {Topic} — Report: {Role} ({Agent/Model})

**Date:** {date}
**Hub Document:** Docs/WIP/{Topic}_Investigation_{date}.md
**Status:** INVESTIGATING | WRITING | DONE

---

## Files Analyzed
- {file path} — {what was examined and why}

## Findings
{Detailed findings from the investigation}

## Proposals
{Proposed solutions, approaches, or next steps}

## Risks / Concerns
{Identified risks, edge cases, caveats}

## Out of Scope
{Items discovered but outside the investigation scope — flagged for awareness}

---
```

**Status transitions (hub document):**
- `INVESTIGATING` → First agent sets on document creation; agents are writing spoke files
- `CONSOLIDATING` → Set when all investigators are `DONE`; consolidator is working
- `READY_FOR_REVIEW` → Consolidator sets when synthesis is complete
- `APPROVED` → Captain sets after review; implementation may begin
- `IMPLEMENTED` → Move to `Docs/ARCHIVE/` or appropriate subfolder

---

## 5. Global Rules

### 5.1 Terminology Consistency

All agents must use consistent terminology throughout documentation. Refer to `/AGENTS.md` for the authoritative terminology table. When writing or editing xWiki content, ensure terms are used precisely and consistently across all pages.

### 5.2 Documentation Sync

After any content change:
1. Check cross-references between xWiki pages
2. Verify terminology consistency across related pages
3. Update the root `WebHome.xwiki` table of contents if page structure changed
4. Ensure gh-pages build reflects latest content

---

## 6. Model-Class Guidelines

> **Note:** These are organized by capability tier, not specific model versions, to avoid staleness as models evolve.

### 6.1 High-Capability Models (e.g., Claude Opus, GPT-o3, Gemini 2.5 Pro)

**Strengths:** Deep reasoning, complex analysis, nuanced understanding, large context
**Best For:** Content strategy decisions, complex investigations, quality gates, structural reorganization
**Considerations:**
- Reserve for high-stakes decisions and ambiguous problem spaces
- Excellent for multi-step planning and content review
- Good at finding inconsistencies across documentation

### 6.2 Mid-Tier Models (e.g., Claude Sonnet, GPT-4.1, Gemini 2.5 Flash)

**Strengths:** Balanced cost/capability, good reasoning, fast iteration
**Best For:** Standard reviews, documentation authoring, routine content updates, iterative review cycles
**Considerations:**
- Well-suited for following structured protocols
- Efficient for documentation tasks
- Good default for most content work

### 6.3 Lightweight Models (e.g., Claude Haiku, GPT-4.1 mini, Kimi K2)

**Strengths:** Fast, cost-effective, good for bulk operations
**Best For:** Fast iterations, autonomous workflows (Cline), bulk operations, extract/understand tasks
**Considerations:**
- May need explicit reminders about project conventions — follow AGENTS.md strictly
- Best paired with clear, structured instructions

**Context Budget — Lite Activation:**

Lightweight models have smaller context windows. When activated with "As \<Role\>", use this graduated loading strategy instead of reading all Required Reading at once:

1. **Always load:** `/AGENTS.md` (terminology + safety — non-negotiable)
2. **Load the role entry** from §2 of this document (one subsection, ~40 lines)
3. **Scan** your role's section in `Docs/AGENTS/Role_Learnings.md` (brief)
4. **Defer** remaining Required Reading — load specific documents only when the task requires them
5. **State what you deferred:** In your acknowledgment, list which Required Reading you have NOT loaded yet so the human knows

This avoids consuming 60%+ of context on upfront reads that may not be relevant to a simple task.

---

## 7. Escalation Protocol

### 7.1 When to Escalate to Human

- Content direction decisions (new topics, removing content, changing audience)
- Structural reorganization (moving pages, changing hierarchy)
- Deployment configuration changes
- Disagreement between roles (e.g., Technical Writer and Content Strategist)
- Cost/performance trade-offs with significant impact
- Uncertainty about content accuracy or appropriateness

### 7.2 Escalation Format

```markdown
## Escalation Request

**From:** {Role} ({Agent})
**Urgency:** HIGH | MEDIUM | LOW
**Decision Needed By:** {date/condition}

### Situation
{What happened or was discovered}

### Options
1. **Option A:** {description}
   - Pros: {list}
   - Cons: {list}

2. **Option B:** {description}
   - Pros: {list}
   - Cons: {list}

### Recommendation
{Which option and why, if any}

### Impact of No Decision
{What happens if human doesn't respond}
```

---

## 8. Quality Checklist

Before marking any task complete:

- [ ] xWiki syntax preserved correctly
- [ ] Cross-references verified between pages
- [ ] Content reviewed for accuracy
- [ ] gh-pages build succeeds
- [ ] WIP document archived or updated
- [ ] Terminology consistent across all affected pages
- [ ] Review log complete in WIP document

---

## Related Documents

- [Meta-Prompt Template](./Multi_Agent_Meta_Prompt.md) - Reusable prompt for starting tasks
- [Role Learnings Log](./Role_Learnings.md) - Agent-contributed tips, gotchas, and patterns per role
- [GlobalMasterKnowledge for xWiki](./GlobalMasterKnowledge_for_xWiki.md) - xWiki-specific rules
- [AGENTS_xWiki.md](./AGENTS_xWiki.md) - xWiki agent configurations
- [TECH_WRITER_START_HERE.md](./TECH_WRITER_START_HERE.md) - Technical Writer onboarding guide

---

**Document Maintainer:** Captain
**Last Reviewed:** 2026-02-15
