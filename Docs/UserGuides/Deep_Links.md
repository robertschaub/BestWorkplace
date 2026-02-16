# Deep Links

Short URLs for sharing specific pages of the Best Workplace documentation.

## Base URL

```
https://robertschaub.github.io/BestWorkplace/
```

## Available Links

| Short URL | Target Page | Language |
|-----------|-------------|----------|
| [/guide](https://robertschaub.github.io/BestWorkplace/guide) | How to Use This Blueprint | EN |
| [/de](https://robertschaub.github.io/BestWorkplace/de) | Der beste Arbeitsplatz (root) | DE |
| [/de/guide](https://robertschaub.github.io/BestWorkplace/de/guide) | Gestalte deinen besten Arbeitsplatz! | DE |

The root page (EN) is accessible directly at the base URL.

## How It Works

Deep links are defined in `Docs/xwiki-pages/_redirects.json`. Each entry maps a slug to a `#ref` hash fragment in the viewer. The build script generates a redirect HTML file for each slug during gh-pages deployment.

### Adding a New Deep Link

1. Edit `Docs/xwiki-pages/_redirects.json`
2. Add an entry: `"slug": "#PageRef.WebHome"`
3. Rebuild and deploy gh-pages
