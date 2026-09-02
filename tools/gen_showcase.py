#!/usr/bin/env python3
"""Regenerate the <main> of en/showcase.html and pt/showcase.html.

Layout per block:   [N] [1] [2] [L1]   pages, centred as a row
                       ==== S ====     spine, three pages wide

School data lives in nt_schools.py -- edit there, not here.
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from nt_schools import SITE, INSTITUTIONS, find, ratio

PAGE_ALT = {'N':  ('back cover', 'contracapa'),
            '1':  ('front cover', 'capa'),
            '2':  ('front page', 'página de título'),
            'L1': ('example chapter', 'capítulo de exemplo'),
            'S':  ('spine', 'lombada')}

CREDIT_LEAD = {'en': 'Support for this school contributed by',
               'pt': 'Suporte para esta escola contribuído por'}

LEDE = {
 'en': ('<h1>Showcase</h1>'
        '<p>Every page the template produces, for each school and degree: back cover, front cover, '
        'front page, an example chapter, and the spine underneath. Missing panels simply mean that '
        'school does not use that page.</p>'
        '<p>All samples are compiled from the current template with LuaLaTeX, in English.</p>'),
 'pt': ('<h1>Galeria</h1>'
        '<p>Todas as páginas que o template produz, para cada escola e grau: contracapa, capa, '
        'página de título, um capítulo de exemplo e, em baixo, a lombada. A ausência de uma página '
        'significa que essa escola não a usa.</p>'
        '<p>Todos os exemplos são compilados com o template actual em LuaLaTeX, em inglês.</p>'),
}

SIZES = [('560', 'S'), ('720', 'M'), ('960', 'L')]
CTL_LBL  = {'en': 'Size', 'pt': 'Tamanho'}
CTL_NAME = {'en': {'S': 'Small', 'M': 'Medium', 'L': 'Large'},
            'pt': {'S': 'Pequeno', 'M': 'Médio', 'L': 'Grande'}}

SCRIPT = """<script>
(function(){var show=document.querySelector('.show'),key='nt-showcase-size';
var btns=Array.prototype.slice.call(document.querySelectorAll('.sz'));
function set(w){show.style.setProperty('--bw',w+'px');
btns.forEach(function(b){b.setAttribute('aria-pressed',b.dataset.w===w?'true':'false');});}
btns.forEach(function(b){b.addEventListener('click',function(){set(b.dataset.w);
try{localStorage.setItem(key,b.dataset.w);}catch(e){}});});
try{var s=localStorage.getItem(key);
if(s&&btns.some(function(b){return b.dataset.w===s;}))set(s);}catch(e){}})();
</script>"""

def control(lang):
    btns = ''.join(
        f'<button type="button" class="sz" data-w="{w}" aria-pressed="{str(w == "720").lower()}"'
        f' title="{CTL_NAME[lang][s]}">{s}</button>' for w, s in SIZES)
    return f'<div class="show-ctl"><span>{CTL_LBL[lang]}</span>{btns}</div>'

def credit_line(inst, i, lang):
    who, gh = inst['credit']
    lead = CREDIT_LEAD[lang]
    # the handle is optional; without one there is nothing to link to
    if gh:
        return (f'<p class="credit">{lead} <a href="https://github.com/{gh}">{who}</a> '
                f'(<span class="mono">{gh}</span>)</p>')
    return f'<p class="credit">{lead} {who}</p>'

def build(lang):
    i = 0 if lang == 'en' else 1
    out, missing = [], []
    for inst in INSTITUTIONS:
        out.append('<section class="show-g">')
        if inst['key'] == 'manual':
            head = 'The template itself' if i == 0 else 'O próprio template'
        else:
            uni, school = inst['uni'][i], inst['school'][i]
            head = f'{uni} — {school}' if school and school != uni else uni
        out.append(f'<div class="show-hd"><h2>{head}</h2><span class="tag">{inst["tag"]}</span></div>')
        if inst.get('credit'):
            out.append(credit_line(inst, i, lang))
        out.append('<div class="blocks">')
        for stem, lbl_en, lbl_pt in inst['blocks']:
            label = lbl_en if i == 0 else lbl_pt
            hi = ' hi' if inst['key'] == 'manual' else ''
            out.append(f'<div class="block{hi}"><div class="block-lbl">{label}</div><div class="pages">')
            present = [(p, f) for p in ('N', '1', '2', 'L1') if (f := find(stem, p))]
            out.append('<div class="prow">')
            for p, f in present:
                wide = ' wide' if ratio(f) > 1 else ''
                out.append(f'<span class="pg{wide}"><img src="../covers/SVG/{f.name}" '
                           f'alt="{stem} {PAGE_ALT[p][i]}" loading="lazy"></span>')
            out.append('</div>')
            if (sp := find(stem, 'S')):
                out.append(f'<span class="pg sp"><img src="../covers/SVG/{sp.name}" '
                           f'alt="{stem} {PAGE_ALT["S"][i]}" loading="lazy"></span>')
            else:
                missing.append(f'{stem}: no spine')
            out.append('</div></div>')
            if not present:
                missing.append(f'{stem}: no pages at all')
        out.append('</div></section>')
    return '\n'.join(out), missing

for lang in ('en', 'pt'):
    p = SITE / lang / 'showcase.html'
    src = p.read_text(encoding='utf-8')
    body, missing = build(lang)
    new_main = (f'<main class="page">\n<div class="lede">{LEDE[lang]}</div>\n'
                f'{control(lang)}\n<div class="show">\n{body}\n</div>\n{SCRIPT}\n</main>')
    out, n = re.subn(r'<main class="page">.*?</main>', lambda m: new_main, src, flags=re.S)
    assert n == 1, f'{p}: <main> not found ({n} matches)'
    print(f'{p.relative_to(SITE)}: ' + ('already up to date' if out == src else 'written'))
    if out != src:
        p.write_text(out, encoding='utf-8')

print('\nAssets not available (panel simply omits them):')
for m in dict.fromkeys(missing):
    print('  ·', m)
