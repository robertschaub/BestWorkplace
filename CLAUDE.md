# Claude Code instructions — BestWorkplace

Project rules and workflow: @AGENTS.md

## Project overview

Documentation-only project — no source code. xWiki 2.1 pages about agile leadership, team culture, and workplace transformation, published via GitHub Pages.

- `Docs/xwiki-pages/The Best Workplace/` — xWiki content pages (single source of truth)
- `Docs/xwiki-pages/scripts/` — Python build scripts and PowerShell deployment
- `Docs/xwiki-pages/viewer-impl/` — HTML viewer for local preview
- `Docs/xwiki-export/` — XAR snapshot files
- `.github/workflows/deploy-docs.yml` — CI/CD for gh-pages deployment

## Commands

- Preview: `Docs\xwiki-pages\View.cmd`
- Build gh-pages locally: `python Docs/xwiki-pages/scripts/build_ghpages.py`
- XAR → tree: `python Docs/xwiki-pages/scripts/xar_to_xwiki_tree.py <file.xar> --output Docs/xwiki-pages`
- Tree → XAR: `python Docs/xwiki-pages/scripts/xwiki_tree_to_xar.py Docs/xwiki-pages --output BestWorkplace.xar`
- Platform: Windows. Use PowerShell-compatible commands.

## Publishing (gh-pages)

**CI owns gh-pages. Agents must NEVER push to the gh-pages branch directly.**

- To publish: `git push` to `main` — CI (`.github/workflows/deploy-docs.yml`) deploys automatically with the `DOCS_ANALYTICS_URL` secret injected.
- `deploy-ghpages.ps1` is for **local preview only** — it builds but does NOT push. Running it and then pushing to gh-pages manually will overwrite the CI build and break analytics.
- To re-trigger CI without a content commit: `gh workflow run "Deploy Docs to GitHub Pages" --ref main`

## Safety

- No secrets in commits.
- No destructive git commands unless explicitly asked.
- Do not modify build output (`gh-pages-build/`) unless asked.

## Roles & Multi-Agent Workflow

When user assigns a role with "As \<Role\>", follow the Role Activation Protocol in `AGENTS.md`.
Role definitions and required reading: `Docs/AGENTS/Multi_Agent_Collaboration_Rules.md` §2.

## Agent handoff

If another tool would be better, say so and explain what context it needs:
- **Cursor Composer**: multi-file edits with visual diff.
- **GitHub Copilot**: inline completions.
- **Cline**: autonomous multi-step workflows.
Full reference: `/AGENTS.md` Agent Handoff Protocol.

## Workflow

- Solo developer + AI agents. Direct push to main is normal.
- Commits: conventional commits `type(scope): description`.
