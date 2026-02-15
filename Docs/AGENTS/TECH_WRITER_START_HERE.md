# Tech Writer Start Here - Documentation Maintenance

**For: AI agents working on BestWorkplace documentation**
**Last Updated**: 2026-02-15

---

## Mission

Maintain and extend BestWorkplace's documentation in xWiki 2.1 format, published via GitHub Pages.

The content covers agile leadership, team culture, coaching, and workplace transformation. All pages are the single source of truth — there is no separate xWiki server for public access.

---

## Your Access & Capabilities

**You ARE an AI agent in VS Code with:**
- Full read/write access to `c:\DEV\BestWorkplace`
- Can read, edit, create, delete local files
- Can run Python scripts and git commands
- Can preview xWiki pages locally (see below)
- Can build and deploy to GitHub Pages

**You CANNOT:**
- Access any xWiki web interface (the project lead handles imports/exports if needed)

---

## Documentation Structure

### xWiki Pages (Single Source of Truth)

```
Docs/xwiki-pages/
├── The Best Workplace/               (main documentation tree)
│   ├── WebHome.xwiki                 (root page — vision & principles)
│   ├── Culture and Change/           (culture transformation topics)
│   ├── Knowledge/                    (agile knowledge base)
│   │   ├── Agile Decision Making/
│   │   ├── Agile Hardware Development/
│   │   ├── Agile Transition and Change Management/
│   │   ├── Agile with Medical Regulations/
│   │   ├── Business agility/
│   │   ├── Cross-Functional Teamwork and T-Shaped Skills/
│   │   ├── Essential information collection on 'Agile'/
│   │   ├── Leadership to foster Innovation/
│   │   ├── Product Owner Role/
│   │   ├── Team Topologies/
│   │   └── User Centered Design & Design Thinking/
│   └── License and Disclaimer/
│
├── scripts/                          (build & conversion tools)
│   ├── build_ghpages.py              (builds GitHub Pages site)
│   ├── deploy-ghpages.ps1            (deploys to gh-pages branch)
│   ├── xar_to_xwiki_tree.py          (XAR → .xwiki tree)
│   ├── xwiki_tree_to_xar.py          (.xwiki tree → XAR)
│   ├── xar_to_fulltree.py            (XAR → JSON fulltree)
│   ├── fulltree_to_xar.py            (JSON → XAR)
│   └── download_attachments.py       (download images from xWiki)
│
├── viewer-impl/                      (local preview infrastructure)
│   ├── Open-XWikiViewer.ps1          (PowerShell HTTP server)
│   └── xwiki-viewer.html             (HTML viewer template)
│
└── View.cmd                          (local WYSIWYG viewer launcher)
```

**File format:** `.xwiki` files contain **pure xWiki 2.1 syntax** — headings with `= Title =`, bold with `**text**`, italic with `//text//`, links with `[[Label>>Space.Page]]`.

### Supporting Files

```
Docs/
├── xwiki-export/                     (XAR snapshot files)
├── AGENTS/                           (agent collaboration rules — THIS FILE)
```

---

## Essential Documents to Read First

| Document | Purpose |
|----------|---------|
| `/AGENTS.md` | Fundamental rules, safety, workflow |
| `/Docs/AGENTS/GlobalMasterKnowledge_for_xWiki.md` | xWiki syntax rules and document handling |
| `/Docs/AGENTS/AGENTS_xWiki.md` | xWiki editing workflow reference |

---

## Key Rules

### Format Authority
- **xWiki pages** are the authoritative source for all content
- **Markdown files** are authoritative for agent collaboration rules and project configuration
- **Never duplicate** content across both formats — each topic lives in ONE place

### Content Integrity
- **Preserve existing content** — do not rewrite, summarize, or restructure without explicit request
- **Preserve xWiki syntax** — maintain the exact formatting style of each page
- All content is under CC BY-SA 4.0 license, copyright Robert Schaub

---

## Common Workflows

### Editing xWiki Pages

1. Edit `.xwiki` files directly in `Docs/xwiki-pages/The Best Workplace/`
2. Preview locally: run `Docs\xwiki-pages\View.cmd`
3. Commit changes to git

### Building & Deploying to GitHub Pages

```bash
# Build the static site
python Docs/xwiki-pages/scripts/build_ghpages.py

# Deploy to gh-pages branch
powershell Docs/xwiki-pages/scripts/deploy-ghpages.ps1
```

The GitHub Actions workflow (`.github/workflows/deploy-docs.yml`) also deploys automatically on push to main when content files change.

### Converting XAR ↔ xWiki Tree

```bash
# Project lead provides .xar file → convert to .xwiki tree
python Docs/xwiki-pages/scripts/xar_to_xwiki_tree.py path/to/export.xar --output Docs/xwiki-pages

# After editing → convert back to .xar for xWiki import
python Docs/xwiki-pages/scripts/xwiki_tree_to_xar.py Docs/xwiki-pages --output BestWorkplace.xar
```

### Working with Attachments (Images)

Images are stored in `_attachments/` subdirectories alongside their parent page:
```
Knowledge/Product Owner Role/
├── WebHome.xwiki
└── _attachments/
    ├── image1.png
    └── image2.png
```

Reference images in xWiki with: `[[image:attach:filename.png]]`

---

## What You ARE Authorized To Do

- Read all files in `Docs/`
- Edit `.xwiki` files directly (pure xWiki 2.1 syntax)
- Edit `.md` documentation files in `Docs/AGENTS/`
- Run build and conversion scripts
- Create, reorganize, and archive documentation
- Fix formatting, links, and content
- Commit changes to git (local only)

## Ask Project Lead Before

- Deleting content that seems important but unclear
- Making decisions about content accuracy or direction
- Pushing to remote or creating PRs
- Any operation involving a live xWiki web interface
- Major structural reorganizations of the page hierarchy

---

## xWiki 2.1 Quick Syntax Reference

```
= Heading 1 =
== Heading 2 ==
=== Heading 3 ===

**bold**  //italic//  ##inline code##

* Bullet list
** Nested bullet

1. Numbered list
1. Second item (always use "1.")

[[Link Label>>Space.Page.WebHome]]
[[External Link>>https://example.com]]

|=Header 1|=Header 2|
|Cell 1|Cell 2|

{{code language="typescript"}}
const x = 1;
{{/code}}

{{mermaid}}
graph TD
  A --> B
{{/mermaid}}
```

**No metadata headers** — pageId, parent, title are derived from file paths.

---

**Maintained by**: Project Team
**Review frequency**: Update when documentation structure changes
