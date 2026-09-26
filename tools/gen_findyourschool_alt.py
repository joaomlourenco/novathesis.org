#!/usr/bin/env python3
"""Alternative "Find your school": a row per repository instead of a card grid.

    python3 tools/gen_findyourschool_alt.py

Writes en/schools-alt.html and pt/schools-alt.html, to compare against the card
grid. Each row reads left to right: the institution's mark, the school's name
and repository id, the front cover, then the four ways to get it.

The marks are per institution, so NOVA FCT's three repositories and Lusofona's
two repeat theirs -- correctly, since that is one institution with several
templates. The lede and note are taken from the live page, so the two versions
say the same thing about Overleaf's plans and the free alternatives.
"""
import sys, pathlib, html, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import nt_overrides as ov
from nt_schools import SITE, GROUPS, REPOS, cover_stem, find, repo_url, zip_url, overleaf, inscrive

LOGOS = SITE / 'logos'

# Functional icons, not brand marks: an approximation of someone's logo drawn by
# hand is worse than an honest arrow, and these say what the button does.
ICONS = {
 'zip':  '<path d="M12 3v11M7.5 10l4.5 4 4.5-4M4 19h16"/>',
 'git':  '<circle cx="7" cy="6" r="2.4"/><circle cx="7" cy="18" r="2.4"/>'
         '<circle cx="17" cy="9.5" r="2.4"/><path d="M7 8.4v7.2M17 12v1.2c0 2-1.6 2.9-3.4 3.2'
         'C11.3 16.9 9.6 17.4 8.9 18"/>',
 'open': '<path d="M14 4h6v6M20 4l-8.5 8.5M18 13.5V19a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5.5"/>',
}
def icon(kind):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[kind]}</svg>')

def logo_key():
    m = {}
    for g in ov.INSTITUTIONS_ALT:
        for r in g['repos']:
            m[r] = g['key']
    return m

def row(r, c, lk):
    key = lk.get(r['repo'], r['repo'])
    f = LOGOS / f'{key}.svg'
    name = html.escape(r['label'])
    mark = (f'<span class="amb-logo"><img loading="lazy" alt="" src="../logos/{f.name}"></span>'
            if f.exists() else
            f'<span class="amb-logo amb-logo-missing"><span>{c["logo_missing"]}</span></span>')
    stem = cover_stem(r)
    cf = find(stem, '1') if stem else None
    cls = 'amb-cover crop' if r.get('crop') else 'amb-cover'
    cover = (f'<a class="{cls}" href="../covers/SVG/{cf.name}" aria-label="{c["cover_label"]} {name}" '
             f'title="{c["cover_label"]} {name}">'
             f'<img loading="lazy" alt="" src="../covers/SVG/{cf.name}"></a>') if cf else ''
    btns = ''.join(
        f'<a class="tag tag-i" href="{href}">{icon(kind)}<span>{label}</span></a>'
        for kind, label, href in (
            ('zip',  c['zip'],  zip_url(r)),
            ('git',  c['git'],  repo_url(r)),
            ('open', 'Overleaf', overleaf(r)),
            ('open', 'Inscrive', inscrive(r))))
    return (f'<div class="sch-row">'
            f'<div class="sch-id">{mark}<div class="amb-school">{name}'
            f'<span class="repo">{html.escape(r["repo"])}</span></div></div>'
            f'<div class="sch-cover">{cover}</div>'
            f'<div class="sch-get">{btns}</div></div>')

def lifted(lang, what):
    """The lede and the note as the live page words them, so the alternative
    cannot end up making different promises about compile limits."""
    s = (SITE / lang / 'schools.html').read_text(encoding='utf-8')
    m = re.search(rf'<div class="{what}">(.*?)</div>\s*(?=<div|</main)', s, re.S)
    return m.group(1) if m else ''

COPY = {'en': dict(other='pt', title='Find your school', zip='ZIP', git='Git',
                   cover_label='Cover of', logo_missing='logo?',
                   note='Alternative layout: one row per repository instead of a card grid, '
                        'with the institution mark beside each cover.'),
        'pt': dict(other='en', title='A tua escola', zip='ZIP', git='Git',
                   cover_label='Capa de', logo_missing='logótipo?',
                   note='Disposição alternativa: uma linha por repositório em vez de uma '
                        'grelha de cartões, com o símbolo da instituição ao lado da capa.')}

def main():
    lk = logo_key()
    for lang in ('en', 'pt'):
        c = COPY[lang]
        src = (SITE / lang / 'index.html').read_text(encoding='utf-8')
        head = ''.join(re.findall(r'<link rel="(?:preconnect|stylesheet|icon|me)"[^>]*>', src))
        head += ''.join(re.findall(r'<meta name="color-scheme"[^>]*>', src))
        head += ''.join(re.findall(r'<script>try\{var t=localStorage[^<]*</script>', src))
        head += ''.join(re.findall(r'<script src="\.\./theme\.js"></script>', src))
        header = re.search(r'<header class="hd">.*?</header>', src, re.S).group(0)
        header = header.replace('class="on"', 'class=""')
        header = header.replace('<a class="" href="schools.html">', '<a class="on" href="schools.html">')
        header = re.sub(r'(<a class="lang" href=")[^"]*(")', rf'\1../{c["other"]}/schools-alt.html\2', header)
        footer = re.search(r'<footer class="ft">.*?</footer>', src, re.S).group(0)
        groups = ''
        for key, gname in GROUPS:
            rows = [row(r, c, lk) for r in REPOS if r['group'] == key]
            if not rows: continue
            groups += (f'<section class="amb-g"><div class="show-hd"><h2>{html.escape(gname)}</h2>'
                       f'<span class="show-tags"><span class="tag">{len(rows)}</span></span></div>'
                       + ''.join(rows) + '</section>')
        out = (f'<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
               f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
               f'<title>{c["title"]} · novathesis</title>\n'
               f'<meta name="robots" content="noindex">\n{head}\n</head>\n'
               f'<body>\n{header}\n<main class="page">\n'
               f'<div class="lede">{lifted(lang, "lede")}</div>\n'
               f'<p class="amb-note">{c["note"]}</p>\n{groups}\n'
               f'<div class="note">{lifted(lang, "note")}</div>\n'
               f'</main>\n{footer}\n</body>\n</html>\n')
        p = SITE / lang / 'schools-alt.html'
        old = p.read_text(encoding='utf-8') if p.exists() else None
        if old == out:
            print(f'{lang}/schools-alt.html: already up to date')
        else:
            p.write_text(out, encoding='utf-8')
            print(f'{lang}/schools-alt.html: written  ({len(REPOS)} linhas)')

if __name__ == '__main__':
    main()
