#!/usr/bin/env python3
"""Regenerate the repository-card grid in en/schools.html and pt/schools.html.

Only the grid is rewritten; each language's lede and closing note are left
exactly as they are, because they are hand-written prose.

School data lives in nt_schools.py -- edit there, not here.
"""
import re, sys, json, pathlib, html
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import nt_overrides as ov
from nt_schools import (SITE, GROUPS, REPOS, repo_url, zip_url, overleaf, inscrive, find, ratio,
                        cover_stem, check_or_exit)

# Functional icons, not brand marks: an approximation of someone's logo drawn by
# hand is worse than an honest arrow, and these say what the button does.
# Services that cannot be handed a school's ZIP through a URL, each with the
# shape of the detour it needs. `upload` takes the ZIP in by hand; `preset`
# opens a project the service already holds, which is why it needs the school
# id instead of the ZIP -- on letx the ZIP route is the one that does not work,
# so offering it would teach the single thing that fails.
MANUAL = {
 'scienhub': dict(name='ScienHub', site='https://scienhub.com', steps='upload'),
 'letx':     dict(name='letx', site='https://letx.app/open?template=novathesis',
                  steps='preset'),
}

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

def row(r, c, lk, cont=False, last=False):
    """`cont` marks a row whose institution is the same as the one above it: the
    mark is shown once and the rows below keep its width as empty space, so the
    name column stays on its line."""
    key = lk.get(r['repo'], r['repo'])
    f = LOGOS / f'{key}.svg'
    name = html.escape(r['label'])
    if cont:
        mark = f'<span class="amb-logo-gap{" is-last" if last else ""}" aria-hidden="true"></span>'
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
    # these have no import-by-URL, so their chip opens the steps rather than a
    # page that cannot do what the others do in one click. A `preset` service
    # holds one general project, so it can only serve a school the template
    # itself defines -- an external one has no id to type and gets no chip.
    btns += ''.join(
        f'<button class="tag tag-i tag-steps" type="button" data-manual="{svc}" '
        f'data-service="{html.escape(m["name"])}" data-site="{m["site"]}" '
        f'data-zip="{zip_url(r)}" data-school="{name}" '
        f'data-ntschool="{html.escape(r.get("school") or "")}">'
        f'{icon("steps")}<span>{html.escape(m["name"])}</span></button>'
        for svc, m in MANUAL.items()
        if m['steps'] != 'preset' or r.get('school'))
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
# %s is the service, %S the school's name, %I the id to type in the template.
STEPS = {
 'en': dict(title='Open in', zip='Download the ZIP', go='Open %s', close='Close',
   upload=dict(
     lead='%s cannot import a repository from a link, so the template goes in '
          'by hand. Four steps:',
     steps=['Download the ZIP for %S.', 'Open %s and sign in.',
            'Create a new, empty project and upload the ZIP.',
            'Set <code>template.tex</code> as the main document.']),
   preset=dict(
     lead='%s is free and opens in one click, but the project it keeps is the '
          'general template rather than one school’s. You point it at %S '
          'yourself. Three steps:',
     steps=['Open the novathesis project on %s. It is free, and asks you to '
            'sign in.',
            'In <code>0-Config/1_novathesis.tex</code>, set '
            '<code>\\ntsetup{school=%I}</code>.',
            'Compile.'],
     note='%s updates this copy with each release, so now and then it is a '
          'version behind — but not for long.')),
 'pt': dict(title='Abrir no', zip='Descarregar o ZIP', go='Abrir o %s', close='Fechar',
   upload=dict(
     lead='O %s não consegue importar um repositório a partir de um link, por '
          'isso o template entra à mão. Quatro passos:',
     steps=['Descarrega o ZIP da %S.', 'Abre o %s e entra na conta.',
            'Cria um projeto novo, vazio, e carrega o ZIP.',
            'Define <code>template.tex</code> como documento principal.']),
   preset=dict(
     lead='O %s é gratuito e abre num clique, mas guarda o template geral e '
          'não o de uma escola: a configuração para %S fica para ti. '
          'Três passos:',
     steps=['Abre o projeto novathesis no %s. É gratuito e pede-te que entres '
            'na conta.',
            'No <code>0-Config/1_novathesis.tex</code>, define '
            '<code>\\ntsetup{school=%I}</code>.',
            'Compila.'],
     note='O %s actualiza esta cópia a cada nova versão, por isso por vezes '
          'está uma atrás — mas não por muito tempo.')),
}

def dialog(lang):
    s = STEPS[lang]
    kinds = json.dumps({k: m['steps'] for k, m in MANUAL.items()})
    copy = json.dumps({k: s[k] for k in ('upload', 'preset')})
    ext = EXT[lang][0]
    return (
      f'<dialog id="manual" closedby="any" aria-labelledby="manual-t">'
      f'<h3 id="manual-t">{s["title"]} <span data-f="service"></span></h3>'
      f'<p class="manual-lead"></p>'
      f'<ol class="manual-steps"></ol>'
      f'<p class="manual-note" hidden><span class="tag ext">{ext}</span> '
      f'<span data-f="note"></span></p>'
      f'<div class="manual-do">'
      f'<a class="btn btn-p" data-f="zip" href="#">{s["zip"]}</a>'
      f'<a class="btn" data-f="site" href="#" target="_blank" rel="noopener"></a>'
      f'<button class="btn manual-x" type="button">{s["close"]}</button></div>'
      f'</dialog>'
      f'<script>(function(){{'
      f'var d=document.getElementById("manual");if(!d)return;'
      f'var K={kinds},C={copy},GO={s["go"]!r};'
      f'function fill(t,b){{return t.split("%s").join(b.dataset.service)'
      f'.split("%S").join(b.dataset.school)'
      f'.split("%I").join(b.dataset.ntschool||"");}}'
      f'document.addEventListener("click",function(e){{'
      f'var b=e.target.closest&&e.target.closest("[data-manual]");if(!b)return;'
      f'var svc=b.dataset.service,c=C[K[b.dataset.manual]];'
      f'd.querySelector(\'[data-f="service"]\').textContent=svc;'
      f'd.querySelector(".manual-lead").textContent=fill(c.lead,b);'
      # the steps carry <code>, so they are our own markup, not reader input
      f'd.querySelector(".manual-steps").innerHTML='
      f'c.steps.map(function(t){{return "<li>"+fill(t,b)+"</li>";}}).join("");'
      f'var n=d.querySelector(".manual-note");n.hidden=!c.note;'
      f'if(c.note)n.querySelector(\'[data-f="note"]\').textContent=fill(c.note,b);'
      # a service that holds its own prepared project has no use for the ZIP,
      # and on letx that route is precisely the broken one
      f'var z=d.querySelector(\'[data-f="zip"]\');z.hidden=!c.steps.some('
      f'function(t){{return t.indexOf("ZIP")>=0;}});z.href=b.dataset.zip;'
      f'var g=d.querySelector(\'[data-f="site"]\');g.href=b.dataset.site;'
      f'g.textContent=GO.replace("%s",svc);'
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
        keys = [lk.get(r['repo'], r['repo']) for r in rows]
        for n, r in enumerate(rows):
            cont = n > 0 and keys[n] == keys[n-1]
            last = cont and (n+1 == len(rows) or keys[n+1] != keys[n])
            out.append(row(r, c, lk, cont=cont, last=last))
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