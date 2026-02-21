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

### `deploy-ghpages.ps1` — local preview only, NOT for publishing

**File:** `Docs/xwiki-pages/scripts/deploy-ghpages.ps1`

**What it does now:**
1. Runs `build_ghpages.py` to generate `index.html` + `pages.json` in `gh-pages-build/`
2. Switches to the local `gh-pages` branch
3. Copies generated files (including attachments and redirect directories)
4. Commits locally
5. Switches back to the original branch — **does NOT push**

**What it used to do (before 2026-02-21):**
The original script included `git push origin gh-pages` as step 6. AI agents ran this script when asked to "publish" or "deploy" docs. This overwrote the CI-built `gh-pages` branch with a locally-built version that **lacked the `DOCS_ANALYTICS_URL` secret** (only available in CI). Result: the Stats button stopped working on the live site.

**Why the push was removed:**
- CI (`.github/workflows/deploy-docs.yml`) uses `peaceiris/actions-gh-pages@v4` with `force_orphan: true`, which replaces the entire `gh-pages` branch on every deploy.
- CI injects `DOCS_ANALYTICS_URL` into the build via `--analytics-url`, so the deployed `index.html` has `Analytics.configure(url, 'BW')` baked in.
- A manual `git push origin gh-pages` from the local script overwrites this CI build. Since the secret isn't available locally, the rebuilt `index.html` has no analytics configuration — the Stats button is hidden.
- This happened multiple times before the push step was removed.

**How to publish:** Push to `main`. CI deploys automatically.
**How to re-trigger without a content change:** `gh workflow run "Deploy Docs to GitHub Pages" --ref main`

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
