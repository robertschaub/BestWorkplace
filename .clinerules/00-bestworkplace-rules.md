# BestWorkplace — Cline Rules

> **Canonical source:** `/AGENTS.md`. This file is a summary. If rules diverge, follow AGENTS.md.

**Read `/AGENTS.md` first** — it contains all project rules, safety rules, and workflow reference. This file adds Cline-specific notes.

## Project Overview

Documentation-only project — no source code. xWiki 2.1 pages about agile leadership and workplace culture, published via GitHub Pages.
- `Docs/xwiki-pages/The Best Workplace/` — xWiki content pages (single source of truth)
- `Docs/xwiki-pages/scripts/` — Build and deployment scripts

## Safety (Critical for Autonomous Operation)

- **Always confirm destructive actions with the user** before executing.
- Do not change secrets/credentials or commit them.
- Do not modify build output (`gh-pages-build/`) unless asked.
- Avoid destructive git commands unless explicitly asked.
- Platform: Windows. Use PowerShell-compatible commands.

## Cline-Specific Notes

- Prefer reading .xwiki files before editing — do not guess at page structure or content.
- Preserve existing xWiki 2.1 syntax when editing pages.
- Full xWiki rules: `Docs/AGENTS/GlobalMasterKnowledge_for_xWiki.md`.

## Commands

- Preview: `Docs\xwiki-pages\View.cmd`
- Build: `python Docs/xwiki-pages/scripts/build_ghpages.py`
- Deploy: `powershell Docs/xwiki-pages/scripts/deploy-ghpages.ps1`

## Roles

When the user starts with "As \<Role\>" (e.g., "As Tech Writer, update..."), follow the **Role Activation Protocol** in `/AGENTS.md`. It tells you which role definition to load from `Docs/AGENTS/Multi_Agent_Collaboration_Rules.md` §2 and which documents to read.

**Context-budget note:** If loading all Required Reading exceeds your context window, load only the role entry from §2 and defer document reads until needed for the specific task.

## Agent Handoff

If a task would be better handled by another tool, say so:
- **Claude Code (Opus)**: complex multi-step reasoning, plan mode.
- **Cursor Composer**: multi-file edits with visual diff.
- **GitHub Copilot**: inline completions.
See `/AGENTS.md` Agent Handoff Protocol for full reference.

## Conventions

- Commit messages: conventional commits `type(scope): description`.
- Solo developer + AI agents. Direct push to main is normal.
