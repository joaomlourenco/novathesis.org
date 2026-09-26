#!/usr/bin/env python3
"""Stamp styles.css and theme.js with a content hash in every page.

    python3 tools/stamp_assets.py

Cloudflare serves these with max-age=14400, so for four hours a browser does
not even ask whether they changed. With a single fixed address that means a CSS
change is invisible to anyone who visited recently -- including whoever is
reviewing it minutes after publishing. Adding ?v=<hash of the file> gives each
version its own address: unchanged file, unchanged address, cache still works;
changed file, new address, nobody sees the old one.

Run it after changing either asset, and after the generators, since those lift
the <link> tags from index.html. It is idempotent.
"""
import hashlib, pathlib, re, sys

SITE = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ('styles.css', 'theme.js')

def digest(name):
    return hashlib.sha256((SITE / name).read_bytes()).hexdigest()[:8]

def main():
    v = {a: digest(a) for a in ASSETS}
    # any path ending in the asset name, with or without a stamp already on it
    rx = re.compile(r'((?:href|src)=")([^"]*?(' + '|'.join(a.replace('.', r'\.') for a in ASSETS)
                    + r'))(?:\?v=[0-9a-f]+)?(")')
    touched = 0
    for p in sorted(SITE.rglob('*.html')):
        if '.git' in p.parts:
            continue
        s = p.read_text(encoding='utf-8')
        new = rx.sub(lambda m: f'{m.group(1)}{m.group(2)}?v={v[m.group(3)]}{m.group(4)}', s)
        if new != s:
            p.write_text(new, encoding='utf-8')
            touched += 1
    print(f'stamp_assets: ' + ', '.join(f'{a}?v={h}' for a, h in v.items()))
    print(f'stamp_assets: {touched} page(s) updated'
          if touched else 'stamp_assets: already up to date')

if __name__ == '__main__':
    main()
