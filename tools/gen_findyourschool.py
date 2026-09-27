#!/usr/bin/env python3
"""Regenerate the repository-card grid in en/schools.html and pt/schools.html.

Only the grid is rewritten; each language's lede and closing note are left
exactly as they are, because they are hand-written prose.

School data lives in nt_schools.py -- edit there, not here.
"""
import re, sys, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import nt_overrides as ov
from nt_schools import (SITE, GROUPS, REPOS, repo_url, zip_url, overleaf, inscrive, find, ratio,
                        cover_stem, check_or_exit)

# Functional icons, not brand marks: an approximation of someone's logo drawn by
# hand is worse than an honest arrow, and these say what the button does.
MANUAL = {'scienhub': ('ScienHub', 'https://scienhub.com'),
          'prism':    ('Prism',    'https://prism.openai.com')}

ICONS = {
 'zip':  '<path d="M12 3v11M7.5 10l4.5 4 4.5-4M4 19h16"/>',
 'git':  '<circle cx="7" cy="6" r="2.4"/><circle cx="7" cy="18" r="2.4"/>'
         '<circle cx="17" cy="9.5" r="2.4"/><path d="M7 8.4v7.2M17 12v1.2c0 2-1.6 2.9-3.4 3.2'
         'C11.3 16.9 9.6 17.4 8.9 18"/>',
 'open': '<path d="M14 4h6v6M20 4l-8.5 8.5M18 13.5V19a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5.5"/>',
 'steps':'<circle cx="12" cy="12" r="8.6"/><path d="M12 11.2v5M12 7.9v.1"/>',
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


TAGS = {'en': ('ZIP', 'Git', 'Overleaf', 'Inscrive'),
        'pt': ('ZIP', 'Git', 'Overleaf', 'Inscrive')}

# A card is marked external when the entry names its own `org`: that is exactly
# what "kept outside the novathesis organisation" means, so no separate flag can
# fall out of step with the URLs.
COPY = {'en': dict(lang='en', zip='ZIP', git='Git', cover_label='Cover of',
                   logo_missing='logo?'),
        'pt': dict(lang='pt', zip='ZIP', git='Git', cover_label='Capa de',
                   logo_missing='logótipo?')}

EXT = {'en': ('External', 'Maintained outside the novathesis organisation, '
              'on its own release cycle'),
       'pt': ('Externo', 'Mantido fora da organização novathesis, '
              'com o seu próprio ciclo de lançamentos')}
LOGOS = SITE / 'logos'

GRID_RE = re.compile(r'<div style="display:flex;flex-direction:column;gap:40px">.*?(?=\s*<div class="note">)', re.S)

def row(r, c, lk, cont=False):
    """`cont` marks a row whose institution is the same as the one above it: the
    mark is shown once and the rows below keep its width as empty space, so the
    name column stays on its line."""
    key = lk.get(r['repo'], r['repo'])
    f = LOGOS / f'{key}.svg'
    name = html.escape(r['label'])
    if cont:
        mark = '<span class="amb-logo-gap" aria-hidden="true"></span>'
    elif f.exists():
        mark = f'<span class="amb-logo"><img loading="lazy" alt="" src="../logos/{f.name}"></span>'
    else:
        mark = f'<span class="amb-logo amb-logo-missing"><span>{c["logo_missing"]}</span></span>'
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
    # ScienHub and Prism have no import-by-URL, so their chip opens the steps
    # rather than a page that cannot do what the others do in one click
    btns += ''.join(
        f'<button class="tag tag-i tag-steps" type="button" data-manual="{svc}" '
        f'data-service="{html.escape(sname)}" data-site="{surl}" '
        f'data-zip="{zip_url(r)}" data-school="{name}">'
        f'{icon("steps")}<span>{html.escape(sname)}</span></button>'
        for svc, (sname, surl) in MANUAL.items())
    # the externally maintained school keeps its marker here too: it is the same
    # warning, and a row without it would send people off as if it were ours
    ext = ''
    if r.get('org'):
        label, tip = EXT[c['lang']]
        ext = f' <span class="tag ext" title="{tip}">{label}</span>'
    return (f'<div class="sch-row{" sch-cont" if cont else ""}">'
            f'<div class="sch-id">{mark}<div class="amb-school">{name}'
            f'<span class="repo">{html.escape(r["repo"])}{ext}</span></div></div>'
            f'<div class="sch-cover">{cover}</div>'
            f'<div class="sch-get">{btns}</div></div>')


# One dialog per page, filled from the clicked chip. closedby="any" gives
# light dismiss and Esc for free; Safari has neither yet, hence the fallback.
STEPS = {
 'en': dict(title='Open in', lead='%s cannot import a repository from a link, so the '
                  'template goes in by hand. Four steps:',
            s1='Download the ZIP for %s.', s2='Open %s and sign in.',
            s3='Create a new, empty project and upload the ZIP.',
            s4='Set <code>template.tex</code> as the main document.',
            zip='Download the ZIP', go='Open %s', close='Close'),
 'pt': dict(title='Abrir no', lead='O %s não consegue importar um repositório a partir de '
                  'um link, por isso o template entra à mão. Quatro passos:',
            s1='Descarrega o ZIP da %s.', s2='Abre o %s e entra na conta.',
            s3='Cria um projeto novo, vazio, e carrega o ZIP.',
            s4='Define <code>template.tex</code> como documento principal.',
            zip='Descarregar o ZIP', go='Abrir o %s', close='Fechar'),
}

def dialog(lang):
    s = STEPS[lang]
    return (
      f'<dialog id="manual" closedby="any" aria-labelledby="manual-t">'
      f'<h3 id="manual-t">{s["title"]} <span data-f="service"></span></h3>'
      f'<p class="manual-lead"></p>'
      f'<ol><li data-s="1"></li><li data-s="2"></li><li>{s["s3"]}</li><li>{s["s4"]}</li></ol>'
      f'<div class="manual-do">'
      f'<a class="btn btn-p" data-f="zip" href="#">{s["zip"]}</a>'
      f'<a class="btn" data-f="site" href="#" target="_blank" rel="noopener"></a>'
      f'<button class="btn manual-x" type="button">{s["close"]}</button></div>'
      f'</dialog>'
      f'<script>(function(){{'
      f'var d=document.getElementById("manual");if(!d)return;'
      f'var L={{lead:{s["lead"]!r},s1:{s["s1"]!r},s2:{s["s2"]!r},go:{s["go"]!r}}};'
      f'document.addEventListener("click",function(e){{'
      f'var b=e.target.closest&&e.target.closest("[data-manual]");if(!b)return;'
      f'var svc=b.dataset.service;'
      f'd.querySelector(\'[data-f="service"]\').textContent=svc;'
      f'd.querySelector(".manual-lead").textContent=L.lead.replace("%s",svc);'
      f'd.querySelector(\'[data-s="1"]\').textContent=L.s1.replace("%s",b.dataset.school);'
      f'd.querySelector(\'[data-s="2"]\').textContent=L.s2.replace("%s",svc);'
      f'var z=d.querySelector(\'[data-f="zip"]\');z.href=b.dataset.zip;'
      f'var g=d.querySelector(\'[data-f="site"]\');g.href=b.dataset.site;'
      f'g.textContent=L.go.replace("%s",svc);'
      f'd.showModal();}});'
      f'd.querySelector(".manual-x").addEventListener("click",function(){{d.close();}});'
      f'if(!("closedBy" in HTMLDialogElement.prototype)){{'          # Safari
      f'd.addEventListener("click",function(e){{if(e.target!==d)return;'
      f'var r=d.getBoundingClientRect();'
      f'if(e.clientY>=r.top&&e.clientY<=r.bottom&&e.clientX>=r.left&&e.clientX<=r.right)return;'
      f'd.close();}});}}'
      f'}})();</script>')

def grid(lang):
    """The wrapper is unchanged so GRID_RE keeps finding it on the next run;
    only what goes inside it became rows instead of cards."""
    c = COPY[lang]
    lk = logo_key()
    out = ['<div style="display:flex;flex-direction:column;gap:40px">']
    for gid, heading in GROUPS:
        rows = [r for r in REPOS if r['group'] == gid]
        if not rows:
            continue
        out.append(f'<div class="group"><div class="gh"><h2>{heading}</h2></div><div class="amb-g">')
        prev = None
        for r in rows:
            key = lk.get(r['repo'], r['repo'])
            out.append(row(r, c, lk, cont=(key == prev)))
            prev = key
        out.append('</div></div>')
    out.append('</div>')
    out.append(dialog(lang))
    return ''.join(out)

def main():
    check_or_exit()

    for lang in ('en', 'pt'):
        p = SITE / lang / 'schools.html'
        src = p.read_text(encoding='utf-8')
        new, n = GRID_RE.subn(lambda m: grid(lang), src)
        assert n == 1, f'{p}: card grid not found ({n} matches)'
        print(f'{p.relative_to(SITE)}: ' + ('already up to date' if new == src else 'written')
              + f'  ({len(REPOS)} rows)')
        if new != src:
            p.write_text(new, encoding='utf-8')

    wide = [r['repo'] for r in REPOS
            if (f := find(cover_stem(r), '1')) and ratio(f) > 1 and not r.get('crop')]
    if wide:
        print('\nWrap-around covers shown uncropped (consider crop=True):', ', '.join(wide))


if __name__ == '__main__':
    main()