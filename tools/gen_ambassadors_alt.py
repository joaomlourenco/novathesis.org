#!/usr/bin/env python3
"""Alternative ambassadors page: institutions rather than templates.

    python3 tools/gen_ambassadors_alt.py

Writes en/ambassadors-alt.html and pt/ambassadors-alt.html, to be compared
against the ambassadors.html that lists one row per repository. Two differences:
NOVA FCT's three models and Lusófona's two collapse into one row each, because
an ambassador watches an institution's regulations and not a template; and the
cover thumbnail gives way to the institution's own mark, which is what a reader
recognises when scanning for their own school.

Everything else -- the copy, the duties, who holds what -- is shared with
gen_ambassadors.py, so the two pages cannot drift apart on anything but the
thing being compared.
"""
import sys, pathlib, html, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import nt_overrides as ov
from nt_schools import SITE, REPOS
from gen_ambassadors import COPY, ISSUE, portrait

LOGOS = SITE / 'logos'

def institutions():
    """REPOS folded to one entry per institution, in the order REPOS gives."""
    grouped, out, seen = {}, [], set()
    for g in ov.INSTITUTIONS_ALT:
        for r in g['repos']:
            grouped[r] = g
    for r in REPOS:
        g = grouped.get(r['repo'])
        key = g['key'] if g else r['repo']
        if key in seen:
            continue
        seen.add(key)
        repos = [x for x in REPOS if (grouped.get(x['repo'], {}).get('key') if grouped.get(x['repo']) else x['repo']) == key]
        out.append(dict(key=key, group=g, repos=repos, label=r['label']))
    return out

def logo(inst, c):
    """The institution's own mark. A missing file leaves a marked placeholder
    rather than a hole, so it is obvious which ones still need one."""
    f = LOGOS / f'{inst["key"]}.svg'
    name = html.escape(title(inst, c))
    if not f.exists():
        return (f'<span class="amb-logo amb-logo-missing" title="{name}">'
                f'<span>{html.escape(c["logo_missing"])}</span></span>')
    return (f'<a class="amb-logo" href="../logos/{f.name}" aria-label="{name}" title="{name}">'
            f'<img loading="lazy" alt="" src="../logos/{f.name}"></a>')

def title(inst, c):
    i = 0 if c['lang'] == 'en' else 1
    return inst['group']['name'][i] if inst['group'] else inst['label']

def holder(inst):
    for r in inst['repos']:
        a = ov.AMBASSADORS.get(r['repo'])
        if a:
            return a
    return None

def row(inst, c):
    a = holder(inst)
    models = ' · '.join(html.escape(r['repo']) for r in inst['repos'])
    if a:
        who = html.escape(a['name'])
        if a.get('github'):
            gh = html.escape(a['github'])
            who = f'<a href="https://github.com/{gh}">{who}</a><span class="amb-gh">{gh}</span>'
        body = f'{portrait(a)}<span class="amb-person">{who}</span>'
    else:
        body = (f'<span class="amb-face amb-mono amb-empty" aria-hidden="true">+</span>'
                f'<span class="amb-person">'
                f'<a href="{ISSUE}{html.escape(title(inst, c))}">{c["open_cta"]}</a>'
                f'<span class="amb-state">{c["open_label"]}</span></span>')
    return (f'<div class="amb-row">'
            f'<div class="amb-id">{logo(inst, c)}<div class="amb-school">'
            f'{html.escape(title(inst, c))}<span class="repo">{models}</span></div></div>'
            f'<div class="amb-who">{body}</div></div>')

def main():
    insts = institutions()
    for lang in ('en', 'pt'):
        c = dict(COPY[lang])
        c['logo_missing'] = 'logo?' if lang == 'en' else 'logótipo?'
        src = (SITE / lang / 'index.html').read_text(encoding='utf-8')
        head = ''.join(re.findall(r'<link rel="(?:preconnect|stylesheet|icon|me)"[^>]*>', src))
        head += ''.join(re.findall(r'<meta name="color-scheme"[^>]*>', src))
        head += ''.join(re.findall(r'<script>try\{var t=localStorage[^<]*</script>', src))
        head += ''.join(re.findall(r'<script src="\.\./theme\.js"></script>', src))
        header = re.search(r'<header class="hd">.*?</header>', src, re.S).group(0)
        header = header.replace('class="on"', 'class=""')
        header = header.replace('<a class="" href="contributing.html">',
                                '<a class="on" href="contributing.html">')
        header = re.sub(r'(<a class="lang" href=")[^"]*(")',
                        rf'\1../{c["other"]}/ambassadors-alt.html\2', header)
        footer = re.search(r'<footer class="ft">.*?</footer>', src, re.S).group(0)
        rows = ''.join(row(i, c) for i in insts)
        missing = sum(1 for i in insts if not (LOGOS / f'{i["key"]}.svg').exists())
        note = ('Alternative layout: one row per institution rather than per template, '
                'with the institution\'s own mark in place of a cover.'
                if lang == 'en' else
                'Disposição alternativa: uma linha por instituição em vez de por modelo, '
                'com o símbolo da instituição em vez da capa.')
        out = (f'<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
               f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
               f'<title>{c["title"]} · novathesis</title>\n'
               f'<meta name="robots" content="noindex">\n{head}\n</head>\n'
               f'<body>\n{header}\n<main class="page">\n'
               f'<div class="lede"><h1>{c["h1"]}</h1><p>{c["lede"]}</p></div>\n'
               f'<p class="amb-note">{note}</p>\n'
               f'<div class="sec-hd"><h2>{c["roll_h"]}</h2></div>\n'
               f'<div class="amb-g">{rows}</div>\n'
               f'</main>\n{footer}\n</body>\n</html>\n')
        p = SITE / lang / 'ambassadors-alt.html'
        old = p.read_text(encoding='utf-8') if p.exists() else None
        if old == out:
            print(f'{lang}/ambassadors-alt.html: already up to date')
        else:
            p.write_text(out, encoding='utf-8')
            print(f'{lang}/ambassadors-alt.html: written  ({len(insts)} instituições, '
                  f'{missing} sem logótipo)')

if __name__ == '__main__':
    main()
