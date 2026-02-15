# Agent Instructions Index

**Purpose**: This folder contains role-specific instructions and tooling for AI agents working on BestWorkplace.

---

## By Role

| Role | Start Here | Description |
|------|-----------|-------------|
| **Any agent (docs)** | [/AGENTS.md](/AGENTS.md) | Fundamental rules, safety, workflow — read first |
| **Documentation / Tech Writer** | [TECH_WRITER_START_HERE.md](TECH_WRITER_START_HERE.md) | xWiki documentation workflow and content editing |
| **xWiki Editor** | [AGENTS_xWiki.md](AGENTS_xWiki.md) | Rules for editing .xwiki files directly |

---

## Multi-Agent Coordination

| Document | Purpose |
|----------|---------|
| [Multi_Agent_Collaboration_Rules.md](Multi_Agent_Collaboration_Rules.md) | Roles, workflow, area-to-document mapping, handoff protocol |
| [Multi_Agent_Meta_Prompt.md](Multi_Agent_Meta_Prompt.md) | Template for spawning task-specific agents with correct context |

---

## Tool-Specific Config Files

All tool configs reference `/AGENTS.md` as the single source of truth.

| Tool | Config Location | Notes |
|------|----------------|-------|
| Claude Code | `/CLAUDE.md` | Auto-loaded into system prompt |
| GitHub Copilot | `/.github/copilot-instructions.md` | Auto-loaded in VS Code |
| Cursor | `/.cursor/rules/*.mdc` | Glob-scoped rules, auto-attached per file type |
| Cline / RooCode | `/.clinerules/*.md` | Inserted into system prompt |
| Windsurf | `/.windsurfrules` | 6000 char limit, condensed rules inline |

---

## Tooling & Reference

| Document | Purpose |
|----------|---------|
| [GlobalMasterKnowledge_for_xWiki.md](GlobalMasterKnowledge_for_xWiki.md) | Core rules and document handling for xWiki work |
| [InitializeBWchat_for_xWiki.md](InitializeBWchat_for_xWiki.md) | Chat initialization prompt for xWiki-focused sessions |
| [Mermaid_ERD_Quick_Reference.md](Mermaid_ERD_Quick_Reference.md) | Syntax reference for Mermaid diagrams in documentation |
| [Role_Learnings.md](Role_Learnings.md) | Agent-contributed tips, gotchas, and patterns per role |
