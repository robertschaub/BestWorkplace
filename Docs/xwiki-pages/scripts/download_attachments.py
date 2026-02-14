#!/usr/bin/env python3
"""
download_attachments.py

Scan .xwiki files for image:FILENAME references and download attachments
from a live xWiki instance. Saves images into _attachments/ folders
next to each page's WebHome.xwiki.

Usage:
    python Docs/xwiki-pages/scripts/download_attachments.py
    python Docs/xwiki-pages/scripts/download_attachments.py --base-url https://schaubgroup.ch/wiki/bestworkplace
    python Docs/xwiki-pages/scripts/download_attachments.py --dry-run
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path


# xWiki space name in the live instance (before we renamed it locally)
XWIKI_SPACE_ORIGINAL = 'The Best Workplace - Our Vision'
# Local directory name (after rename)
LOCAL_SPACE_NAME = 'The Best Workplace'

# Pattern: [[image:FILENAME||params]] where FILENAME does not start with http
IMAGE_PATTERN = re.compile(r'\[\[image:([^|\]]+?)(?:\|\|[^\]]*?)?\]\]')


def find_repo_root() -> Path:
    p = Path(__file__).resolve().parent
    while p != p.parent:
        if (p / '.git').exists():
            return p
        p = p.parent
    return Path.cwd()


def scan_for_images(content_dir: Path) -> list[tuple[Path, str]]:
    """Scan all .xwiki files and return (page_dir, filename) pairs for local attachments."""
    results = []
    for xwiki_file in content_dir.rglob('*.xwiki'):
        text = xwiki_file.read_text(encoding='utf-8')
        for match in IMAGE_PATTERN.finditer(text):
            filename = match.group(1).strip()
            # Skip external URLs
            if filename.startswith('http://') or filename.startswith('https://'):
                continue
            results.append((xwiki_file.parent, filename))
    return results


def build_download_url(base_url: str, page_dir: Path, content_dir: Path, filename: str) -> str:
    """Build xWiki download URL for an attachment."""
    # Get relative path from content root to the page directory
    rel_path = page_dir.relative_to(content_dir)
    # Convert local path to xWiki space path (replace local name with original)
    parts = list(rel_path.parts)
    # The first part should be the local space name root (e.g. empty if content_dir IS the space)
    # Since content_dir is "The Best Workplace", rel_path is relative from there
    space_path = XWIKI_SPACE_ORIGINAL + '/' + '/'.join(parts) if parts else XWIKI_SPACE_ORIGINAL

    # URL-encode each path segment
    encoded_parts = [urllib.parse.quote(p, safe='') for p in space_path.split('/')]
    encoded_path = '/'.join(encoded_parts)

    return f'{base_url}/download/{encoded_path}/WebHome/{urllib.parse.quote(filename, safe="")}'


def download_image(url: str, dest: Path, dry_run: bool = False) -> bool:
    """Download a single image. Returns True on success."""
    if dry_run:
        print(f'  [DRY RUN] Would download: {url}')
        print(f'            To: {dest}')
        return True

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'BestWorkplace-Sync/1.0'})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            size_kb = len(data) / 1024
            print(f'  OK  {dest.name} ({size_kb:.1f} KB)')
            return True
    except urllib.error.HTTPError as e:
        print(f'  FAIL {dest.name}: HTTP {e.code}', file=sys.stderr)
        return False
    except Exception as e:
        print(f'  FAIL {dest.name}: {e}', file=sys.stderr)
        return False


def main():
    parser = argparse.ArgumentParser(description='Download xWiki attachments for local pages')
    parser.add_argument('--base-url', default='https://schaubgroup.ch/wiki/bestworkplace',
                        help='Base URL of xWiki instance')
    parser.add_argument('--content-dir', default=None,
                        help='Path to content directory (default: auto-detect)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Show what would be downloaded without downloading')
    args = parser.parse_args()

    repo_root = find_repo_root()
    content_dir = Path(args.content_dir) if args.content_dir else \
                  repo_root / 'Docs' / 'xwiki-pages' / LOCAL_SPACE_NAME

    if not content_dir.is_dir():
        print(f'Error: content directory not found: {content_dir}', file=sys.stderr)
        sys.exit(1)

    print(f'Scanning {content_dir} for image references...')
    images = scan_for_images(content_dir)

    # Deduplicate (same image might be referenced multiple times)
    unique = {}
    for page_dir, filename in images:
        key = (page_dir, filename)
        if key not in unique:
            unique[key] = True

    print(f'Found {len(unique)} unique local attachments\n')

    success = 0
    skipped = 0
    failed = 0

    for (page_dir, filename) in unique:
        dest = page_dir / '_attachments' / filename

        # Skip if already downloaded
        if dest.exists() and not args.dry_run:
            print(f'  SKIP {filename} (already exists)')
            skipped += 1
            continue

        url = build_download_url(args.base_url, page_dir, content_dir, filename)
        if download_image(url, dest, dry_run=args.dry_run):
            success += 1
        else:
            failed += 1

        # Be polite to the server
        if not args.dry_run:
            time.sleep(0.3)

    print(f'\nDone! Downloaded: {success}, Skipped: {skipped}, Failed: {failed}')
    if failed > 0:
        print('Re-run to retry failed downloads.', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
