# Links Inventory — BestWorkplace

Live site: https://robertschaub.github.io/BestWorkplace/

---

## Redirect Aliases (`_redirects.json`)

Each entry creates both an HTML redirect page (`/slug/` clean URL) and a bundle alias (`#slug` hash URL).

| Slug | Target Page Ref | URL |
|------|----------------|-----|
| `guide` | `How to Use This Blueprint.WebHome` | `/guide/` or `#guide` |
| `de` | `WebHome.de` | `/de/` or `#de` |
| `de/guide` | `How to Use This Blueprint.WebHome.de` | `/de/guide/` or `#de/guide` |

**File:** `Docs/xwiki-pages/_redirects.json` (object format: `{ "slug": "#encodedRef" }`)

---

## Internal Cross-Links (doc: references)

18 internal links across xWiki pages. Key patterns:

### Language Switchers

| Source | Link | Target |
|--------|------|--------|
| `WebHome.xwiki` | `[[DE>>doc:WebHome.de]]` | German home |
| `WebHome.de.xwiki` | `[[EN>>doc:WebHome]]` | English home |
| `How to Use This Blueprint/WebHome.xwiki` | `[[DE>>doc:How to Use This Blueprint.WebHome.de]]` | German guide |
| `How to Use This Blueprint/WebHome.de.xwiki` | `[[EN>>doc:How to Use This Blueprint.WebHome]]` | English guide |

### Navigation Links

| Source | Link Text | Target |
|--------|-----------|--------|
| `WebHome.xwiki` | "Read, Reflect, Discuss, Grow..." | `How to Use This Blueprint.WebHome` |
| `WebHome.xwiki` | "The Song of Significance..." | `Knowledge.Culture and Change.Creating the best work place we can imagine.WebHome` |
| `WebHome.xwiki` | "Content under CC BY-SA 4.0..." | `License and Disclaimer.WebHome` |
| `Knowledge/WebHome.xwiki` | "Best Workplace Blueprint" | `WebHome` |
| `Knowledge/Product Owner Role/WebHome.xwiki` | "Team Topologies" | `Knowledge.Team Topologies.WebHome` |
| `Knowledge/Leadership to foster Innovation/Lean-Agile KPI's...` | "OKR - Objectives and Key Results" | `Knowledge.Leadership to foster Innovation.OKR - Objectives and Key Results.WebHome` |

German pages (`WebHome.de.xwiki`, `How to Use This Blueprint/WebHome.de.xwiki`) mirror the same targets with German labels.

---

## Translation Pages

| Page | English | German |
|------|---------|--------|
| Home | `WebHome.xwiki` | `WebHome.de.xwiki` |
| Guide | `How to Use This Blueprint/WebHome.xwiki` | `How to Use This Blueprint/WebHome.de.xwiki` |

Translation metadata stored in `_meta.json` files:
- `The Best Workplace/_meta.json` — `"de": { "title": "Der beste Arbeitsplatz" }`
- `How to Use This Blueprint/_meta.json` — `"de": { "title": "Anleitung zum Wegweiser" }`

---

## Deep-Link Mechanisms

Both mechanisms work for every redirect entry:

1. **HTML redirect pages** — `/guide/index.html` serves `<script>window.location.replace("../#ref")</script>`
2. **Bundle aliases** — `loadBundle()` adds `pageIndex["guide"] = pageIndex["How to Use This Blueprint.WebHome"]`
3. **Hash navigation** — `#How%20to%20Use%20This%20Blueprint.WebHome` resolves directly via `hashchange` listener

---

## CI/CD & Analytics

| Setting | Value |
|---------|-------|
| Workflow | `.github/workflows/deploy-docs.yml` |
| Trigger | Push to `main` (watched paths) + `workflow_dispatch` |
| Analytics secret | `DOCS_ANALYTICS_URL` (injected via CI) |
| Site ID | `BW` |
| Deploy tool | `peaceiris/actions-gh-pages@v4` (`force_orphan: true`) |
| Re-trigger | `gh workflow run "Deploy Docs to GitHub Pages" --ref main` |

---

## External Dependencies (viewer)

| Resource | URL |
|----------|-----|
| Mermaid.js | `https://cdnjs.cloudflare.com/ajax/libs/mermaid/10.9.1/mermaid.min.js` |
| Google Fonts | `https://fonts.googleapis.com/css2?family=Crimson+Pro&family=JetBrains+Mono&family=Outfit` |
| GitHub API | `https://api.github.com/repos/{repo}/contents/{path}` (for `{{github-files}}` macro) |

---

## External URLs in Content

~176 external URLs across Knowledge pages. Categories:
- **Educational frameworks:** Agile Alliance, SAFe, McKinsey, Sociocracy 3.0
- **Books & courses:** Amazon, Medium, O'Reilly, Pluralsight
- **Domain-specific:** Johner Institute (medical), Team Topologies, Cynefin
- **Standards:** Creative Commons BY-SA 4.0

---

*Last updated: 2026-02-21*
