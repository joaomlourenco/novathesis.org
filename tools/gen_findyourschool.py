#!/usr/bin/env python3
"""Regenerate the repository-card grid in en/schools.html and pt/schools.html.

Only the grid is rewritten; each language's lede and closing note are left
exactly as they are, because they are hand-written prose.

School data lives in nt_schools.py -- edit there, not here.
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from nt_schools import (SITE, GROUPS, REPOS, ORG, overleaf, find, ratio,
                        cover_stem, check_or_exit)

TAGS = {'en': ('ZIP', 'Git', 'Overleaf'), 'pt': ('ZIP', 'Git', 'Overleaf')}
GRID_RE = re.compile(r'<div style="display:flex;flex-direction:column;gap:40px">.*?(?=\s*<div class="note">)', re.S)

def card(r, lang):
    cover = find(cover_stem(r), '1')
    url = f"{ORG}/{r['repo']}"
    zip_, git, ovl = TAGS[lang]
    # uminho's cover is a wrap-around, so it is cropped to the front face
    if r.get('crop'):
        h, w = 248, 175
        frame = (f'<span class="frame"><span class="crop g" style="display:block;height:{h}px;'
                 f'width:{w}px"><img src="../covers/SVG/{cover.name}" alt="{r["repo"]} cover" '
                 f'style="height:{h}px"></span></span>')
    else:
        frame = (f'<span class="frame"><img src="../covers/SVG/{cover.name}" '
                 f'alt="{r["repo"]} cover"></span>')
    return (f'<div class="card"><div class="repo">{r["repo"]}</div>{frame}'
            f'<div class="school">{r["label"]}</div>'
            f'<div class="tags">'
            f'<a class="tag" href="{url}/archive/refs/heads/main.zip">{zip_}</a>'
            f'<a class="tag" href="{url}">{git}</a>'
            f'<a class="tag" href="{overleaf(r["repo"])}">{ovl}</a></div></div>')

def grid(lang):
    out = ['<div style="display:flex;flex-direction:column;gap:40px">']
    for gid, heading in GROUPS:
        rows = [r for r in REPOS if r['group'] == gid]
        if not rows:
            continue
        out.append(f'<div class="group"><div class="gh"><h2>{heading}</h2></div><div class="grid">')
        out += [card(r, lang) for r in rows]
        out.append('</div></div>')
    out.append('</div>')
    return ''.join(out)

check_or_exit()

for lang in ('en', 'pt'):
    p = SITE / lang / 'schools.html'
    src = p.read_text(encoding='utf-8')
    new, n = GRID_RE.subn(lambda m: grid(lang), src)
    assert n == 1, f'{p}: card grid not found ({n} matches)'
    print(f'{p.relative_to(SITE)}: ' + ('already up to date' if new == src else 'written')
          + f'  ({len(REPOS)} cards)')
    if new != src:
        p.write_text(new, encoding='utf-8')

wide = [r['repo'] for r in REPOS
        if (f := find(cover_stem(r), '1')) and ratio(f) > 1 and not r.get('crop')]
if wide:
    print('\nWrap-around covers shown uncropped (consider crop=True):', ', '.join(wide))
