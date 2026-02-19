#!/usr/bin/env python3
"""
build_ghpages.py

Generate GitHub Pages deployment for xWiki documentation.

Scans the .xwiki page tree under Docs/xwiki-pages/The Best Workplace/, generates:
  - pages.json   : All page content bundled as JSON
  - index.html   : Modified xwiki-viewer.html for static hosting (no file picker)
  - .nojekyll    : Tells GitHub Pages to skip Jekyll processing

Usage (from repo root):
    python Docs/xwiki-pages/scripts/build_ghpages.py
    python Docs/xwiki-pages/scripts/build_ghpages.py -o my-output-dir
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

WIKI_EXTS = {'.xwiki', '.wiki', '.txt', '.md'}
SORT_FILE = '_sort'


def _read_sort_order(directory: Path) -> List[str] | None:
    """Read a _sort file from a directory, returning ordered names or None."""
    sort_path = directory / SORT_FILE
    if not sort_path.is_file():
        return None
    try:
        lines = sort_path.read_text(encoding='utf-8').splitlines()
        return [line.strip() for line in lines if line.strip() and not line.strip().startswith('#')]
    except (OSError, UnicodeDecodeError):
        return None


def _apply_sort_order(entries: List[Dict[str, Any]], sort_order: List[str] | None) -> None:
    """Sort entries in-place: items in sort_order first (in that order), then rest alphabetically.
    Folders always come before files within each group."""
    if sort_order:
        order_map = {name.lower(): i for i, name in enumerate(sort_order)}
        entries.sort(key=lambda e: (
            0 if e['type'] == 'folder' else 1,                          # folders first
            0 if e['name'].lower().replace('.xwiki', '') in order_map    # listed items first
                or e['name'].lower() in order_map else 1,
            order_map.get(e['name'].lower().replace('.xwiki', ''),
                          order_map.get(e['name'].lower(), float('inf'))),
            e['name'].lower()
        ))
    else:
        entries.sort(key=lambda e: (0 if e['type'] == 'folder' else 1, e['name'].lower()))


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")


def _git_short_hash() -> str:
    """Get the current git short commit hash, or empty string."""
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--short', 'HEAD'],
            capture_output=True, text=True, timeout=5
        )
        return result.stdout.strip() if result.returncode == 0 else ''
    except Exception:
        return ''


def find_repo_root() -> Path:
    """Walk up from script location to find .git directory."""
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / '.git').exists():
            return p
        p = p.parent
    # Fallback: current working directory
    return Path.cwd()


def scan_tree(base_dir: Path, prefix: list | None = None) -> Tuple[List[Dict[str, Any]], Dict[str, str], Dict[str, Any]]:
    """
    Recursively scan directory for .xwiki files.

    Returns (tree_structure, pages_dict, metas_dict) where:
      - tree_structure: hierarchical list matching the viewer's scanDirectory() format
      - pages_dict: flat dict mapping ref -> content string
      - metas_dict: dict mapping folder_path -> parsed _meta.json content

    The output matches what the JavaScript viewer produces when you open a folder,
    so renderTree() and buildPageIndex() can consume it directly.
    """
    if prefix is None:
        prefix = []

    entries: List[Dict[str, Any]] = []
    pages: Dict[str, str] = {}
    metas: Dict[str, Any] = {}

    try:
        items = sorted(base_dir.iterdir(), key=lambda p: p.name.lower())
    except OSError:
        return entries, pages, metas

    sort_order = _read_sort_order(base_dir)

    # Read _meta.json for translation metadata
    meta_path = base_dir / '_meta.json'
    meta = None
    if meta_path.is_file():
        try:
            meta = json.loads(meta_path.read_text(encoding='utf-8'))
            folder_path = '/'.join(prefix) if prefix else ''
            metas[folder_path] = meta
        except (OSError, json.JSONDecodeError):
            pass

    for item in items:
        if item.name.startswith('.') or item.name == SORT_FILE or item.name == '_meta.json':
            continue

        if item.is_file() and item.suffix.lower() in WIKI_EXTS:
            base_name = item.stem
            segments = prefix + [base_name]
            ref = '.'.join(segments)
            rel_path = '/'.join(prefix + [item.name])

            try:
                content = item.read_text(encoding='utf-8')
            except (OSError, UnicodeDecodeError) as e:
                print(f'  Warning: skipping {item}: {e}', file=sys.stderr)
                continue

            pages[ref] = content

            entry = {
                'type': 'file',
                'name': item.name,
                'baseName': base_name,
                'ref': ref,
                'segments': segments,
                'relPath': rel_path,
                'parentPath': '.'.join(prefix)
            }
            # Apply translation title from _meta.json
            if meta and meta.get('translations'):
                for lang, info in meta['translations'].items():
                    if base_name == f'WebHome.{lang}' and info.get('title'):
                        entry['displayTitle'] = info['title']
            entries.append(entry)

        elif item.is_dir():
            children, sub_pages, sub_metas = scan_tree(item, prefix + [item.name])
            if children:
                entries.append({
                    'type': 'folder',
                    'name': item.name,
                    'segments': prefix + [item.name],
                    'children': children
                })
                pages.update(sub_pages)
                metas.update(sub_metas)

    # Sort: respect _sort file if present, otherwise folders first then alphabetical
    _apply_sort_order(entries, sort_order)

    return entries, pages, metas


def find_root_ref(pages: Dict[str, str]) -> str:
    """Find the best root page reference."""
    if 'WebHome' in pages:
        return 'WebHome'
    # Look for any WebHome
    for ref in pages:
        if ref.endswith('.WebHome') and ref.count('.') == 1:
            return ref
    return next(iter(pages)) if pages else ''


def _derive_title(file_path: Path) -> str:
    """Derive a page title from the file path.
    For WebHome.xwiki, use the parent directory name.
    For other files, use the file stem."""
    if file_path.stem == 'WebHome':
        return file_path.parent.name
    return file_path.stem


def _has_heading(content: str) -> bool:
    """Check if the content contains a heading within the first 30 lines.

    Pages may start with xWiki style directives like (%...%) or table
    markup before the actual heading appears inside a cell.  Scanning
    a few dozen lines catches headings embedded in styled tables.
    """
    for line in content.splitlines()[:30]:
        stripped = line.strip()
        if not stripped:
            continue
        # xWiki heading: starts with = (H1) or == (H2) etc.
        if re.match(r'^={1,6}\s', stripped):
            return True
    return False


def inject_titles(pages: Dict[str, str], content_dir: Path) -> int:
    """Prepend page titles as H1 headings for pages that lack them."""
    count = 0
    for ref, content in list(pages.items()):
        if _has_heading(content):
            continue
        # Reconstruct file path from ref to derive title
        segments = ref.split('.')
        file_path = content_dir
        for seg in segments[:-1]:
            file_path = file_path / seg
        file_path = file_path / (segments[-1] + '.xwiki')
        title = _derive_title(file_path)
        pages[ref] = f'= {title} =\n\n{content}'
        count += 1
    return count


def collect_attachments(content_dir: Path, output_dir: Path) -> int:
    """Find all _attachments/ directories and copy files to output_dir/attachments/."""
    att_out = output_dir / 'attachments'
    count = 0
    for att_dir in content_dir.rglob('_attachments'):
        if not att_dir.is_dir():
            continue
        for f in att_dir.iterdir():
            if f.is_file():
                att_out.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, att_out / f.name)
                count += 1
    return count


def generate_viewer_html(template_path: Path, analytics_url: str = '') -> str:
    """
    Read the existing xwiki-viewer.html and produce a modified version
    for static GitHub Pages deployment.

    Applies targeted patches to:
    - Replace welcome screen with auto-loading
    - Add loadBundle() function
    - Patch loadPage() and resolveIncludes() to read from page.content
    - Add hash-based deep linking
    - Hide inapplicable UI elements
    - Update branding
    """
    html = template_path.read_text(encoding='utf-8')

    # 1. Title
    html = html.replace('<title>XWiki Viewer</title>',
                        '<title>The Best Workplace</title>')

    # 2. Logo branding
    html = html.replace(
        'XWiki<span>Viewer</span>',
        'Best Workplace<span>Docs</span>'
    )

    # 4. Welcome screen title
    html = html.replace(
        '<h1>XWiki Viewer</h1>',
        '<h1>The Best Workplace</h1>'
    )

    # 5. Add hash update to loadPage() - after currentPageRef = ref
    html = html.replace(
        "    currentPageRef = ref;\n    Analytics.trackPageView(ref);\n    currentFileHandle = page.handle || null;",
        "    currentPageRef = ref;\n    Analytics.trackPageView(ref);\n    if(history.replaceState) history.replaceState(null,'','#'+ref);\n    currentFileHandle = page.handle || null;"
    )

    # 8. Inject loadBundle() function and replace init block
    load_bundle_js = """
// =================================================================
// Bundle Loading (GitHub Pages static mode)
// =================================================================
async function loadBundle(){
  try {
    // Cache-busting: append timestamp to force fresh fetch
    const cacheBust = new Date().getTime();
    const resp = await fetch('pages.json?v='+cacheBust);
    if(!resp.ok) throw new Error('HTTP '+resp.status);
    const bundle = await resp.json();
    pageTree = bundle.tree;
    pageIndex = buildPageIndex(pageTree);
    // Attach content strings to page index entries
    for(const[ref,entry] of Object.entries(pageIndex)){
      entry.content = bundle.pages[ref] || '';
    }
    // Alias root WebHome under wrapper folder name so folder click works
    if(bundle.tree[0] && pageIndex['WebHome'] && !pageIndex[bundle.tree[0].name+'.WebHome']){
      pageIndex[bundle.tree[0].name+'.WebHome'] = pageIndex['WebHome'];
    }
    const count = Object.keys(pageIndex).length;
    document.getElementById('treeBody').innerHTML = renderTree(pageTree);
    document.getElementById('treeCount').textContent = '('+count+')';
    document.getElementById('treeSidebar').classList.remove('collapsed');
    showEditor();
    // Navigate to ?page= param, hash target, or root page
    const params = new URLSearchParams(location.search);
    const pageParam = params.get('page');
    const hashRef = decodeURIComponent(location.hash.slice(1));
    const initRef = (pageParam && pageIndex[pageParam]) ? pageParam
      : (hashRef && pageIndex[hashRef]) ? hashRef
      : (bundle.rootRef || Object.keys(pageIndex)[0]);
    if(initRef) await loadPage(initRef);
    // Show metadata
    const meta = document.getElementById('bundleMeta');
    if(meta){
      const d = bundle.generated ? bundle.generated.slice(0,10) : '';
      const h = bundle.commitHash || '';
      meta.textContent = 'Updated: '+d+(h?' ('+h+')':'');
      meta.style.display = '';
    }
  } catch(e){
    console.error('Bundle load failed:',e);
    document.getElementById('welcomeScreen').classList.remove('hidden');
    document.getElementById('mainArea').classList.add('hidden');
    const card = document.querySelector('.welcome-card');
    if(card) card.innerHTML = '<h1 style="color:#c9915a">The Best Workplace</h1><p style="color:#d8d8de">Failed to load documentation bundle.</p><p style="color:#7c7c8a;font-size:.9em">Make sure <code>pages.json</code> exists alongside this file.<br>Error: '+e.message+'</p>';
  }
}

// Hash-based deep linking
window.addEventListener('hashchange',()=>{
  const ref = location.hash.slice(1);
  if(ref && pageIndex[ref]) loadPage(ref);
});

"""

    # Replace the init block at the end of the file
    old_init = """// Auto-load: try server-provided wiki first, then fall back to folder picker
(async function(){
  const params = new URLSearchParams(window.location.search);
  const loaded = await loadFromServer();
  if(loaded){
    const pageParam = params.get('page');
    if(pageParam && pageIndex[pageParam]){
      await loadPage(pageParam);
    }
  } else if(params.get('open') === 'folder'){
    setTimeout(()=> openFolderPicker(), 300);
  }
})();"""

    new_init = """// Auto-load documentation bundle
loadBundle();"""

    html = html.replace(old_init, load_bundle_js + new_init)

    # 9. Hide inapplicable UI elements with CSS
    # Insert before closing </style>
    hide_css = """
/* GitHub Pages static mode: hide interactive-only controls */
.welcome-screen { display: none !important; }
.welcome-actions, #dropZone, .drop-zone { display: none !important; }
#fileInput, #folderInput { display: none !important; }
.toolbar .btn[onclick*="openFile"],
.toolbar .btn[onclick*="openFolder"],
#btnWatch, #btnReload { display: none !important; }
.view-toggle button[onclick*="source"] { display: none !important; }
.view-toggle button[onclick*="split"] { display: none !important; }
#dropOverlay { display: none !important; }
#bundleMeta { display: none; color: var(--text-dim); font-size: .75em; margin-left: 8px; }
"""
    html = html.replace('</style>', hide_css + '</style>')

    # 10. Add bundle metadata element to toolbar
    html = html.replace(
        '<span class="watch-badge" id="watchBadge">',
        '<span id="bundleMeta"></span><span class="watch-badge" id="watchBadge">'
    )

    # 11. Make main area visible by default (skip welcome screen)
    html = html.replace(
        '<div class="main-area hidden" id="mainArea">',
        '<div class="main-area" id="mainArea">'
    )

    # 12. Fix wiki-link regex to not consume [[image:...]] patterns
    #     The wiki-link regex [[(?!https?://)...]] runs before the image regex,
    #     so it grabs [[image:file.png||...]] as a link. Add image: to the exclusion.
    html = html.replace(
        r"text=text.replace(/\[\[(?!https?:\/\/)([^\]]+?)\]\]/g",
        r"text=text.replace(/\[\[(?!https?:\/\/|image:)([^\]]+?)\]\]/g"
    )

    # 13. Patch image rendering to resolve local attachments and preserve params
    old_img_line = "text=text.replace(/\\[\\[image:([^\\]|]+?)(?:\\|[^\\]]*)?" \
                   "\\]\\]/g,'<img src=\"$1\" alt=\"image\">');"
    new_img_line = """text=text.replace(/\\[\\[image:([^\\]|]+?)(?:\\|\\|([^\\]]*))?\\]\\]/g,function(m,src,params){
      var s=src.trim();
      if(!/^https?:\\/\\//.test(s)) s='attachments/'+encodeURIComponent(s);
      var a='';
      if(params){
        var wm=params.match(/width="(\\d+)"/);
        var hm=params.match(/height="(\\d+)"/);
        if(wm)a+=' width="'+wm[1]+'"';
        if(hm)a+=' height="'+hm[1]+'"';
      }
      return '<img src="'+s+'" alt="image"'+a+'>';
    });"""
    html = html.replace(old_img_line, new_img_line)

    # 14. Configure analytics endpoint (if provided)
    if analytics_url:
        safe_url = analytics_url.rstrip('/').replace("'", "\\'")
        analytics_init = f"\n// Configure analytics endpoint\nAnalytics.configure('{safe_url}');\n"
        html = html.replace(
            '// Auto-load documentation bundle\nloadBundle();',
            analytics_init + '// Auto-load documentation bundle\nloadBundle();'
        )

    return html


def generate_redirects(redirects_path: Path, output_dir: Path, base_url: str = '') -> int:
    """Read _redirects.json and generate HTML redirect pages.

    Each key is the alias slug (e.g. "guide" -> guide/index.html),
    each value is the target (hash fragment, relative path, or full URL).
    """
    if not redirects_path.is_file():
        return 0

    try:
        redirects = json.loads(redirects_path.read_text(encoding='utf-8'))
    except (OSError, json.JSONDecodeError) as e:
        print(f'  Warning: could not read {redirects_path}: {e}', file=sys.stderr)
        return 0

    count = 0
    for slug, target in redirects.items():
        # If target is a hash fragment, resolve relative to base
        if target.startswith('#'):
            depth = slug.count('/') + 1  # e.g. "de/guide" -> 2 levels up
            prefix = '../' * depth
            full_target = f'{prefix}{target}' if not base_url else f'{base_url}{target}'
        else:
            full_target = target

        redirect_dir = output_dir / slug
        redirect_dir.mkdir(parents=True, exist_ok=True)
        redirect_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Redirecting…</title>
<script>window.location.replace("{full_target}");</script>
<noscript><meta http-equiv="refresh" content="0; URL={full_target}"></noscript>
</head>
<body>
<p>Redirecting to <a href="{full_target}">{full_target}</a>…</p>
</body>
</html>
'''
        (redirect_dir / 'index.html').write_text(redirect_html, encoding='utf-8')
        count += 1
        print(f'  Redirect: /{slug}/ -> {target}')

    return count


def main():
    parser = argparse.ArgumentParser(
        description='Generate GitHub Pages deployment for xWiki docs'
    )
    parser.add_argument('--content-dir',
        default=None,
        help='Path to xWiki content directory (default: Docs/xwiki-pages/The Best Workplace)')
    parser.add_argument('--viewer',
        default=None,
        help='Path to xwiki-viewer.html template (default: auto-detect)')
    parser.add_argument('--output', '-o',
        default='gh-pages-build',
        help='Output directory (default: gh-pages-build)')
    parser.add_argument('--analytics-url',
        default='',
        help='Cloudflare Worker URL for page view analytics')

    args = parser.parse_args()

    repo_root = find_repo_root()
    content_dir = Path(args.content_dir) if args.content_dir else \
                  repo_root / 'Docs' / 'xwiki-pages' / 'The Best Workplace'
    viewer_path = Path(args.viewer) if args.viewer else \
                  repo_root / 'Docs' / 'xwiki-pages' / 'viewer-impl' / 'xwiki-viewer.html'
    output_dir = Path(args.output)

    if not content_dir.is_dir():
        print(f'Error: content directory not found: {content_dir}', file=sys.stderr)
        sys.exit(1)
    if not viewer_path.is_file():
        print(f'Error: viewer template not found: {viewer_path}', file=sys.stderr)
        sys.exit(1)

    # Scan content
    print(f'Scanning {content_dir} ...')
    tree, pages, metas = scan_tree(content_dir)
    root_ref = find_root_ref(pages)
    print(f'  Found {len(pages)} pages, root: {root_ref}')
    if metas:
        print(f'  Found {len(metas)} _meta.json file(s)')

    # Inject titles for pages that don't have headings
    title_count = inject_titles(pages, content_dir)
    if title_count:
        print(f'  Injected titles for {title_count} pages')

    # Wrap tree in a root folder so the project name appears in the sidebar
    root_name = content_dir.name  # e.g. "The Best Workplace"
    tree = [{
        'type': 'folder',
        'name': root_name,
        'segments': [root_name],
        'children': tree
    }]

    # Get commit hash
    commit_hash = _git_short_hash()

    # Generate pages.json
    bundle = {
        'generated': _now_iso(),
        'generator': 'build_ghpages.py',
        'version': '1.0',
        'commitHash': commit_hash,
        'rootRef': root_ref,
        'pageCount': len(pages),
        'tree': tree,
        'pages': pages,
        'metas': metas
    }

    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / 'pages.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(bundle, f, ensure_ascii=False)
    json_size = json_path.stat().st_size
    print(f'  Wrote {json_path} ({json_size:,} bytes)')

    # Generate modified viewer HTML
    print(f'Generating viewer from {viewer_path} ...')
    viewer_html = generate_viewer_html(viewer_path, analytics_url=args.analytics_url)
    html_path = output_dir / 'index.html'
    html_path.write_text(viewer_html, encoding='utf-8')
    html_size = html_path.stat().st_size
    print(f'  Wrote {html_path} ({html_size:,} bytes)')

    # Collect attachments (images)
    att_count = collect_attachments(content_dir, output_dir)
    if att_count:
        att_size = sum(f.stat().st_size for f in (output_dir / 'attachments').iterdir())
        print(f'  Copied {att_count} attachments ({att_size:,} bytes)')

    # Generate redirects from _redirects.json
    redirects_path = repo_root / 'Docs' / 'xwiki-pages' / '_redirects.json'
    redirect_count = generate_redirects(redirects_path, output_dir)

    # Generate .nojekyll
    nojekyll_path = output_dir / '.nojekyll'
    nojekyll_path.write_text('', encoding='utf-8')

    total_size = json_size + html_size
    print(f'\nDone! {len(pages)} pages, {att_count} attachments, {redirect_count} redirects, {total_size:,} bytes total')
    print(f'Output: {output_dir.resolve()}')
    print(f'\nTo deploy, copy contents of {output_dir}/ to the gh-pages branch.')


if __name__ == '__main__':
    main()
