# Copilot / AI agent instructions — BestWorkplace

> **Canonical source:** `/AGENTS.md`. This file is a summary. If rules diverge, follow AGENTS.md.

Purpose: short, actionable notes to help an AI agent be immediately productive in this repo.

- **Big picture**: This is a documentation-only project — no source code. xWiki 2.1 pages about agile leadership and workplace culture, published via GitHub Pages.
  - `Docs/xwiki-pages/The Best Workplace/` — xWiki content pages (single source of truth)
  - `Docs/xwiki-pages/scripts/` — Python build + PowerShell deployment scripts
  - `Docs/xwiki-pages/viewer-impl/` — Local HTML viewer

- **xWiki syntax** (2.1): `= H1 =`, `== H2 ==`, `**bold**`, `//italic//`, `[[Link>>Target]]`, `{{info}}...{{/info}}`, `{{mermaid}}...{{/mermaid}}`.

- **Commands**:
  - Preview: `Docs\xwiki-pages\View.cmd`
  - Build: `python Docs/xwiki-pages/scripts/build_ghpages.py`
  - Deploy: `powershell Docs/xwiki-pages/scripts/deploy-ghpages.ps1`

- **Safety**:
  - Do not change secrets/credentials or commit them.
  - Avoid destructive git commands unless explicitly asked.
  - Do not modify build output (`gh-pages-build/`) unless asked.

- **Roles**: When the user starts with "As \<Role\>" (e.g., "As Tech Writer, update…"), follow the **Role Activation Protocol** in `/AGENTS.md`. It tells you which role to load from `Docs/AGENTS/Multi_Agent_Collaboration_Rules.md` §2 and which documents to read.

- **Agent handoff**: For large multi-file edits, suggest Cursor Composer or Claude Code. See `/AGENTS.md` Agent Handoff Protocol for full reference.

- **Conventions**:
  - Commit messages: conventional commits `type(scope): description`.
  - Solo developer + AI agents. Direct push to main is normal.
