# Role Learnings Log

**Purpose:** Agents append learnings here during or after task completion. The Captain periodically reviews and promotes valuable entries into the Role Registry (`Multi_Agent_Collaboration_Rules.md` §2).

**Format:** Append new entries at the bottom of the relevant role section. Do NOT edit or delete existing entries — only the Captain curates this file.

---

## How to Contribute

After completing a task, if you discovered something that would help future agents in your role, append an entry:

```markdown
### {Date} — {Brief Title}
**Role:** {your role}  **Agent/Tool:** {e.g., Claude Code, Cursor, Cline}
**Category:** {tip | gotcha | missing-doc | wrong-assumption | useful-pattern | new-file}
**Learning:** {1-3 sentences: what you learned, why it matters, what to do differently}
**Files:** {relevant file paths, if any}
```

**Categories explained:**
- **tip**: Useful technique or shortcut for this role
- **gotcha**: Something that tripped you up or wasted time
- **missing-doc**: Documentation gap you had to work around
- **wrong-assumption**: An assumption from the role guidance that turned out to be incorrect
- **useful-pattern**: A workflow pattern worth reusing
- **new-file**: A new file was created that future agents should know about

---

## Technical Writer

### 2026-02-15 — External link syntax for the xWiki viewer
**Role:** Technical Writer / xWiki Expert  **Agent/Tool:** Claude Code (Opus 4.6)
**Category:** gotcha
**Learning:** The xwiki-viewer.html detects external links by checking if the href starts with `https://`. Use `[[label>>https://url]]` syntax. Do NOT use xWiki's `url:` prefix (`[[label>>url:https://...]]`) or `||target="_blank"` parameter — the viewer doesn't parse those. The viewer automatically adds `target="_blank" rel="noopener"` to all https:// links. Bold wrapping works: `**[[label>>https://url]]**`.
**Files:** `Docs/xwiki-pages/viewer-impl/xwiki-viewer.html` (line ~721, `inl()` method)

### 2026-02-15 — Pages without headings get auto-injected titles
**Role:** Technical Writer  **Agent/Tool:** Claude Code (Opus 4.6)
**Category:** tip
**Learning:** `build_ghpages.py` has `inject_titles()` which prepends an `= Title =` heading to pages that don't start with one. The title is derived from the parent directory name for WebHome files. 14 of 20 BestWorkplace pages needed injected titles. If you want a different title, add your own `= My Title =` as the first line — the injector skips pages that already have a heading.
**Files:** `Docs/xwiki-pages/scripts/build_ghpages.py` (`inject_titles`, `_derive_title`, `_has_heading`)

## Content Strategist

_(No entries yet)_

## Viewer Developer

_(No entries yet)_

## DevOps Expert

### 2026-02-15 — Viewer is shared between BestWorkplace and FactHarbor
**Role:** DevOps Expert / xWiki Expert  **Agent/Tool:** Claude Code (Opus 4.6)
**Category:** gotcha
**Learning:** `xwiki-viewer.html` is identical in both BestWorkplace and FactHarbor repos (`C:\DEV\FactHarbor`). Any change to the viewer must be copied to both repos, then both must be pushed to trigger their respective GitHub Actions gh-pages deployments. The `build_ghpages.py` scripts differ between repos (BestWorkplace has extra image/attachment patches #12 and #13), so only the viewer HTML is shared — the build scripts are independent.
**Files:** `Docs/xwiki-pages/viewer-impl/xwiki-viewer.html` (both repos)

### 2026-02-15 — build_ghpages.py uses exact string patches on the viewer
**Role:** DevOps Expert  **Agent/Tool:** Claude Code (Opus 4.6)
**Category:** gotcha
**Learning:** `build_ghpages.py` applies changes to the viewer HTML via Python `str.replace()` with exact string matching. If you modify lines in the viewer that are also patch targets, the patches will silently fail (no error, just no replacement). After modifying the viewer, always verify that all `html.replace(...)` calls in `build_ghpages.py` still find their target strings. BestWorkplace has 2 extra patches (#12 for wiki-link image exclusion, #13 for attachment path prefix) not present in FactHarbor's build script.
**Files:** `Docs/xwiki-pages/scripts/build_ghpages.py`, `Docs/xwiki-pages/viewer-impl/xwiki-viewer.html`

### 2026-02-15 — Attachment download: double-quote directory names
**Role:** DevOps Expert  **Agent/Tool:** Claude Code (Opus 4.6)
**Category:** gotcha
**Learning:** The xWiki space name for Agile contains double quotes (`"Agile"`) but Windows can't have `"` in directory names, so extraction uses single quotes (`'Agile'`). The `download_attachments.py` script maps local directory names back to original xWiki space names for URL construction, but this quote mismatch required manual intervention — downloading with `%22` (double quote) encoding instead of `%27` (single quote). If adding new pages with special characters, verify the download URLs manually with `--dry-run` first.
**Files:** `Docs/xwiki-pages/scripts/download_attachments.py`

### 2026-02-15 — GitHub Actions force_orphan and local gh-pages branch conflict
**Role:** DevOps Expert  **Agent/Tool:** Claude Code (Opus 4.6)
**Category:** gotcha
**Learning:** The GitHub Actions workflow uses `force_orphan: true` which recreates the gh-pages branch each time. If you also have a local gh-pages branch (from manual deployment), it will be behind the remote and `git push` will fail with non-fast-forward. Solution: delete the local gh-pages branch (`git branch -D gh-pages`) and let GitHub Actions handle all deployments. Do NOT use `deploy-ghpages.ps1` after GitHub Actions is set up — they conflict.
**Files:** `.github/workflows/deploy-docs.yml`, `Docs/xwiki-pages/scripts/deploy-ghpages.ps1`

### 2026-02-15 — XAR scripts now support image attachments round-trip
**Role:** DevOps Expert  **Agent/Tool:** Claude Code (Opus 4.6)
**Category:** new-file
**Learning:** All 4 XAR conversion scripts now handle `_attachments/` directories. Export (`xwiki_tree_to_xar.py`) scans for `_attachments/` alongside each `.xwiki` file, base64-encodes them, and `fulltree_to_xar.py` writes `<attachment>` XML elements into the XAR. Import (`xar_to_fulltree.py`) parses `<attachment>` elements (skipping empty ones), and `xar_to_xwiki_tree.py` writes decoded files to `_attachments/`. Round-trip tested: 28 BestWorkplace attachments (8.5 MB) survived export-import with exact byte-for-byte integrity. Scripts are identical in both FactHarbor and BestWorkplace repos.
**Files:** `Docs/xwiki-pages/scripts/xwiki_tree_to_xar.py`, `Docs/xwiki-pages/scripts/fulltree_to_xar.py`, `Docs/xwiki-pages/scripts/xar_to_fulltree.py`, `Docs/xwiki-pages/scripts/xar_to_xwiki_tree.py`

### 2026-02-15 — GitHub security settings must match FactHarbor
**Role:** DevOps Expert  **Agent/Tool:** Claude Code (Opus 4.6)
**Category:** tip
**Learning:** BestWorkplace GitHub security should mirror FactHarbor. As of 2026-02-15 both repos have: Dependabot security updates (enabled), secret scanning + push protection (enabled), two rulesets — "BlockDefault" (prevents deletion and force-push of main) and "Branch Protection for Main" (PRs required with 1 approver, dismiss stale reviews, admin bypass). BestWorkplace omits FactHarbor's required "CI" status check since it has no CI workflow. Use `gh api repos/robertschaub/BestWorkplace/rulesets` to verify.
**Files:** (GitHub API — no local files)

---

## Handover — 2026-02-15

**Agent:** Claude Code (Opus 4.6)
**Sessions:** 2 (continued session, context carried over)
**Duration:** BestWorkplace repository creation through security hardening

### Work Completed

| Area | What was done |
|------|--------------|
| **Repo creation** | Created BestWorkplace GitHub repo from xWiki .xar export |
| **Content extraction** | Extracted 20 pages from .xar to `.xwiki` file tree |
| **Image attachments** | Downloaded 28 images from xWiki server to `_attachments/` dirs |
| **Viewer** | Shared `xwiki-viewer.html` from FactHarbor with rendering fixes: `(% %)` prefix handling, `{{children/}}` macro, colspan/rowspan, table-level styling |
| **GitHub Pages** | Auto-deploy via GitHub Actions (`deploy-docs.yml`), `build_ghpages.py` with BW-specific patches |
| **XAR round-trip** | 4 scripts updated to support attachment export/import (verified 28 files, 8.5 MB) |
| **Cross-links** | FactHarbor xWiki pages link to BestWorkplace gh-pages site |
| **GitHub security** | Dependabot, secret scanning, push protection, branch rulesets — all matching FactHarbor |
| **Agent docs** | `AGENTS.md`, `AGENTS_xWiki.md`, `Role_Learnings.md` fully populated |
| **GitHub entry pages** | `LICENSE.md`, `CONTRIBUTING.md`, `SECURITY.md` created (uncommitted) |

### Uncommitted Changes

The following files are staged but NOT committed (left for successor):

- `LICENSE.md` — CC BY-SA 4.0 license (matching xWiki content license page)
- `CONTRIBUTING.md` — How to edit content, preview, deploy, use XAR scripts
- `SECURITY.md` — Scope, what to report, enabled GitHub features

**Action needed:** Review, adjust if desired, commit and push.

### Pending / Future Work

1. **Verify live site** — Check https://robertschaub.github.io/BestWorkplace/ renders correctly with images, table styling, and children lists
2. **Create a dated .xar snapshot** — Now that export includes attachments: `python Docs/xwiki-pages/scripts/xwiki_tree_to_xar.py Docs/xwiki-pages --output "Docs/xwiki-export/BestWorkplace_15.Feb.2026.xar"`
3. **Sync scripts if viewer changes** — Any change to `xwiki-viewer.html` must be copied between FactHarbor and BestWorkplace repos
4. **FactHarbor has uncommitted changes** — `Docs/DEVELOPMENT/Coding Agent Prompts.md` (modified), `Docs/REVIEWS/` and `Docs/WIP/` (new files). These are FactHarbor-only, not BestWorkplace-related.

### Key Architecture Decisions

- **Viewer is shared** between repos (identical HTML), but `build_ghpages.py` differs (BW has extra patches #12, #13 for images)
- **Scripts are shared** (all 4 XAR scripts are identical in both repos)
- **GitHub Actions deploys** on every push to main — no manual deployment needed
- **Admin bypass** on branch protection allows direct push to main (solo developer workflow)
- **CC BY-SA 4.0** license for content (from original xWiki), MIT for scripts

---

## Captain Review Log

When the Captain reviews and promotes learnings, record it here:

| Date | Entries Reviewed | Promoted to Registry | Discarded | Notes |
|------|-----------------|---------------------|-----------|-------|
| _(none yet)_ | | | | |
