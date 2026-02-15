# Contributing to The Best Workplace

## What This Is

A curated knowledge base on agile leadership, team culture, and workplace transformation. Content is written in [xWiki 2.1 markup](https://www.xwiki.org/xwiki/bin/view/Documentation/UserGuide/Features/XWikiSyntax/) and published via GitHub Pages.

## How to Contribute

### Editing Content

Pages live under `Docs/xwiki-pages/The Best Workplace/` as `.xwiki` files. Each page is a folder containing `WebHome.xwiki` and optionally an `_attachments/` directory for images.

Quick xWiki syntax reference:
```
= Heading 1 =
== Heading 2 ==
**bold**  //italic//  --strikethrough--
[[Link Label>>doc:PageName.WebHome]]
[[External Link>>https://example.com]]
[[image:filename.png]]
{{info}}Info box{{/info}}
((( grouped content )))
```

### Adding a New Page

1. Create a folder under `The Best Workplace/` (e.g., `Knowledge/New Topic/`)
2. Add `WebHome.xwiki` with your content
3. Place images in `_attachments/` next to the `.xwiki` file

### Local Preview

```
Docs\xwiki-pages\View.cmd
```

### Deployment

Content deploys to GitHub Pages automatically on push to `main`.

## Prerequisites

- Python 3.10+ (build scripts)
- PowerShell (local preview)
- Git

## Commit Style

Conventional commits: `type(scope): description`

```
docs(knowledge): add Team Topologies page
fix(viewer): handle colspan in table cells
feat(scripts): add attachment support to xar export
```

## AI Agents

If you are an AI agent, read [AGENTS.md](AGENTS.md) before making changes.

## Questions?

Open a [GitHub issue](https://github.com/robertschaub/BestWorkplace/issues).
