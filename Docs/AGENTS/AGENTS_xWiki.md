# AGENTS.md - xWiki Documentation Work (BestWorkplace)

## Purpose

This file directs AI agents working on BestWorkplace xWiki documentation.

---

## Required Reading

Before working on xWiki content, agents MUST read and follow:

1. **[GlobalMasterKnowledge_for_xWiki.md](GlobalMasterKnowledge_for_xWiki.md)** (same folder)
   - Core rules and constraints (GLOBAL-R-*)
   - Document handling rules (DOC-R-*)
   - Diagram rules (Mermaid preferred)

2. **Content root:** `Docs/xwiki-pages/The Best Workplace/`
   - All xWiki pages live under this directory
   - Each page is a `WebHome.xwiki` file in its named directory

---

## Workflow: Direct .xwiki Editing

Agents edit `.xwiki` files directly — no conversion needed.

### Edit Pages

```bash
# Edit any page (pure xWiki 2.1 syntax)
code "Docs/xwiki-pages/The Best Workplace/Knowledge/Team Topologies/WebHome.xwiki"
code "Docs/xwiki-pages/The Best Workplace/Culture and Change/WebHome.xwiki"

# Commit changes
git add Docs/xwiki-pages/
git commit -m "docs: update team topologies and culture pages"
```

### Preview Locally (WYSIWYG)

```bash
# Double-click or run:
Docs\xwiki-pages\View.cmd
```

### Build GitHub Pages

```bash
# Build the static site
python Docs/xwiki-pages/scripts/build_ghpages.py

# Deploy to gh-pages branch
powershell Docs/xwiki-pages/scripts/deploy-ghpages.ps1
```

### Export to XAR (for xWiki import)

```bash
# From repo root
python Docs/xwiki-pages/scripts/xwiki_tree_to_xar.py Docs/xwiki-pages --output BestWorkplace.xar
```

### Import from XAR (from xWiki export)

```bash
# From repo root
python Docs/xwiki-pages/scripts/xar_to_xwiki_tree.py exported.xar --output Docs/xwiki-pages
```

---

## xWiki Mermaid Syntax

**Critical:** Empty lines required before AND after the mermaid block!

```
Text before diagram.

{{mermaid}}
flowchart TD
    A[Start] --> B[Process]
{{/mermaid}}

Text after diagram.
```

Do NOT use `{{code language="mermaid"}}` — it doesn't work.

**ERD Diagrams:** See **[Mermaid_ERD_Quick_Reference.md](Mermaid_ERD_Quick_Reference.md)** for critical syntax rules.

---

## Key Rules Summary

- Edit `.xwiki` files directly — no JSON conversion needed
- Mermaid preferred for new diagrams (DOC-R-028)
- No changes without explicit request (GLOBAL-R-017)
- Preserve xWiki markup exactly (GLOBAL-R-030)
- Commit frequently to git for version control

---

## File Locations

| Path | Purpose |
|------|---------|
| `Docs/xwiki-pages/The Best Workplace/` | Master documentation tree |
| `Docs/xwiki-pages/scripts/xar_to_xwiki_tree.py` | XAR → .xwiki tree |
| `Docs/xwiki-pages/scripts/xwiki_tree_to_xar.py` | .xwiki tree → XAR |
| `Docs/xwiki-pages/scripts/build_ghpages.py` | Build GitHub Pages static site |
| `Docs/xwiki-pages/scripts/deploy-ghpages.ps1` | Deploy to gh-pages branch |
| `Docs/xwiki-export/` | Dated XAR snapshots |

---

## Metadata Derivation (How Scripts Work)

The conversion scripts derive pageId, parent, and title from file paths:

- **WebHome pages**: Title = parent directory name (e.g., `The Best Workplace/Knowledge/Team Topologies/WebHome.xwiki` → title "Team Topologies")
- **Non-WebHome pages**: Title = first xWiki heading (`= Title =`)
- **Escaped dots**: Directory names with dots are escaped in pageIds as `\.`

---

## Relationship to FactHarbor

BestWorkplace's tooling was created from FactHarbor's (`C:\DEV\FactHarbor`) xWiki pipeline. Key relationships:

| Component | Relationship |
|-----------|-------------|
| `viewer-impl/xwiki-viewer.html` | **Shared identically** — changes must be synced to both repos |
| `scripts/build_ghpages.py` | **Independent copy** — BestWorkplace has extra patches (#12, #13 for image/attachment handling) |
| `scripts/xar_to_xwiki_tree.py` | Identical copy |
| `scripts/xwiki_tree_to_xar.py` | Identical copy |
| `scripts/download_attachments.py` | **BestWorkplace-only** — downloads images from live xWiki instance |
| `.github/workflows/deploy-docs.yml` | Independent copy (different path triggers) |

### Content Origin

Content was extracted from `Docs/xwiki-export/The Best Workplace Full 14.Feb.2026.xar` using `xar_to_xwiki_tree.py`. The original xWiki space name was "The Best Workplace - Our Vision", renamed to "The Best Workplace" locally. Non-content spaces (Macros, Scheduler, XWiki) were removed during extraction.

### Image Attachments

Images are stored in `_attachments/` directories alongside each page's `WebHome.xwiki`. They were downloaded from the live xWiki instance at `https://schaubgroup.ch/wiki/bestworkplace` using `download_attachments.py`. The build script copies them to `attachments/` in the gh-pages output.

**Gotcha:** The Agile page has double quotes in the xWiki space name (`"Agile"`) but single quotes locally (Windows restriction). The `download_attachments.py` script maps local names back to original xWiki names for URL construction, but this specific case required manual download with `%22` encoding.

---

## xWiki Viewer (`viewer-impl/xwiki-viewer.html`)

The viewer is a ~2000-line standalone HTML file that renders xWiki 2.1 markup in the browser. It is **shared identically** with the FactHarbor repository. Any changes must be copied to both repos.

### Rendering Pipeline

1. `extractBlockMacros(source)` — replaces block macros (`{{code}}`, `{{mermaid}}`, `{{info}}`, `{{children/}}`, etc.) with numbered placeholders
2. `parse(source)` — line-by-line parsing: headings, lists, tables, `(((` groups, `(% ... %)` params, paragraphs
3. `resolvePlaceholders(html)` — replaces placeholders with rendered HTML
4. `resolveIncludes(html)` — async: fetches and inlines `{{include}}` content
5. `resolveChildren` (in `renderPreview()`) — populates `{{children/}}` from the page tree

### Supported Macros

| Macro | Rendered as |
|-------|-----------|
| `{{code language="..."}}...{{/code}}` | `<pre><code>` with language label |
| `{{mermaid}}...{{/mermaid}}` | Mermaid diagram (rendered via mermaid.js) |
| `{{info}}`, `{{warning}}`, `{{error}}`, `{{success}}` | Colored message boxes |
| `{{toc/}}` | Auto-generated table of contents |
| `{{include reference="..."}}` | Transcluded page content |
| `{{children/}}` | Clickable list of child pages |
| `{{{verbatim}}}` | Pre-formatted code block |

### Key Gotchas

- **`(% ... %)` parameter lines**: A standalone line `(% class="x" %)` sets `pendingParams` for the NEXT element. A prefix `(% class="x" %)|(((` is stripped and the remainder (`|(((`) is re-processed. Table-level pendingParams are passed to `<table>` via `renderTable(rows, tblAttrs)`.
- **External links**: Use `[[label>>https://url]]` — the viewer auto-adds `target="_blank" rel="noopener"` for all `https://` links. Do NOT use `url:` prefix or `||target="_blank"` parameter — the viewer doesn't parse those.
- **Image rendering in `inl()`**: The wiki-link regex has a negative lookahead for `image:` so `[[image:...]]` patterns aren't consumed as wiki links.
- **`colspan`/`rowspan`**: Supported via `(% colspan="2" %)` in table cells — parsed by `buildAttrs()`.

---

## GitHub Pages Pipeline (`build_ghpages.py`)

The build script generates a static deployment from the xWiki content tree:

1. `scan_tree()` → builds page hierarchy + reads content into `pages` dict
2. `inject_titles()` → adds H1 headings for pages lacking them (derives title from directory name)
3. Outputs `pages.json` (bundled content) + `index.html` (patched viewer) + `.nojekyll`
4. `collect_attachments()` → copies `_attachments/` files to `attachments/` in build output

### How `generate_viewer_html()` Works

The build script applies **exact string replacements** to the viewer HTML. If you modify the viewer, verify that all patch target strings still exist. BestWorkplace-specific patches:

| # | What it patches | Purpose |
|---|----------------|---------|
| 1 | `<title>` | "The Best Workplace" branding |
| 2 | Logo text | "Best Workplace Docs" |
| 4 | Welcome `<h1>` | Branding |
| 5 | `loadPage()` | Hash-based deep linking |
| 8 | Init block | `loadBundle()` replacing `loadFromServer()` |
| 9 | `</style>` | Hide interactive controls |
| 10 | Watch badge | Bundle metadata element |
| 11 | Main area div | Remove `hidden` class |
| **12** | Wiki-link regex | Add `\|image:` to negative lookahead (prevents `[[image:...]]` from being consumed as links) |
| **13** | Image regex | Prefix `attachments/` for local images, preserve width/height params |

Patches #12 and #13 are **BestWorkplace-only** (not in FactHarbor's build script).

### Auto-Deploy

GitHub Actions workflow (`.github/workflows/deploy-docs.yml`) triggers on push to `main` when content/scripts/viewer files change. Uses `peaceiris/actions-gh-pages@v4` with `force_orphan: true`.

Published at: **https://robertschaub.github.io/BestWorkplace/**

---

**Last Updated:** 2026-02-15
