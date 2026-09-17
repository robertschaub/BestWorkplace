# The Best Workplace

A curated knowledge base on agile leadership, team topologies, coaching, and creating great workplaces.

Published as a static documentation site via GitHub Pages using xWiki 2.1 markup.

## View online

**[https://robertschaub.github.io/BestWorkplace/](https://robertschaub.github.io/BestWorkplace/)**

Privacy: [draft notice prepared for review](Docs/xwiki-pages/The%20Best%20Workplace/Privacy%20Policy/WebHome.xwiki). It is not yet effective; the private controller is identified, while the privacy contact, analytics consent/retention design, and provider records remain approval gates.

## Local preview

```
Docs\xwiki-pages\View.cmd
```

This starts a lightweight local server and opens the xWiki viewer in your browser.

## Structure

```
Docs/
  xwiki-pages/
    The Best Workplace/   ← xWiki content pages (.xwiki files)
    viewer-impl/          ← xWiki viewer (HTML + PowerShell server)
    scripts/              ← Build and deployment scripts
    View.cmd              ← Local preview launcher
  xwiki-export/
    *.xar                 ← Original xWiki export archive
```

## Deployment

Documentation is automatically deployed to GitHub Pages when changes are pushed to `main`.

Manual deployment:
```powershell
powershell Docs/xwiki-pages/scripts/deploy-ghpages.ps1
```
