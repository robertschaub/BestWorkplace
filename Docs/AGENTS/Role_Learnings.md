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

## Product Strategist

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

---

## Captain Review Log

When the Captain reviews and promotes learnings, record it here:

| Date | Entries Reviewed | Promoted to Registry | Discarded | Notes |
|------|-----------------|---------------------|-----------|-------|
| _(none yet)_ | | | | |
