"""Regenerate the <main> of en/showcase.html and pt/showcase.html.

Layout per block:   [N] [1] [2] [L1]        (4-column grid, pages fill in order)
                    ==== spine ====         (spans all 4 columns -> same width everywhere)

Institution names come from the template's own \\SetUniversity / \\SetSchool
strings so EN and PT are authoritative rather than hand-translated.
"""
import re, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent
SVG = SITE / 'covers' / 'SVG'

# (uni_en, uni_pt, school_en, school_pt, tag)
G = {
 'manual':   ('', '', '', '', ''),
 'nova-fct': ('NOVA University Lisbon', 'Universidade NOVA de Lisboa',
              'NOVA School of Science and Technology', 'Faculdade de Ciências e Tecnologia', 'NOVA FCT'),
 'nova-fcsh':('NOVA University Lisbon', 'Universidade NOVA de Lisboa',
              'School of Social Sciences and Humanities', 'Faculdade de Ciências Sociais e Humanas', 'NOVA FCSH'),
 'nova-itqb':('NOVA University Lisbon', 'Universidade NOVA de Lisboa',
              'Instituto de Tecnologia Química e Biológica António Xavier',
              'Instituto de Tecnologia Química e Biológica António Xavier', 'NOVA ITQB'),
 'nova-ensp':('NOVA University Lisbon', 'Universidade NOVA de Lisboa',
              'National School of Public Health', 'Escola Nacional de Saúde Pública', 'NOVA ENSP'),
 'ulisboa-ist': ('Universidade de Lisboa', 'Universidade de Lisboa',
              'Instituto Superior Técnico', 'Instituto Superior Técnico', 'ULISBOA IST'),
 'ulisboa-fcul':('Universidade de Lisboa', 'Universidade de Lisboa',
              'Faculty of Sciences', 'Faculdade de Ciências', 'ULISBOA FCUL'),
 'ulisboa-iseg':('Universidade de Lisboa', 'Universidade de Lisboa',
              'Lisbon School of Economics &amp; Management', 'Instituto Superior de Economia e Gestão', 'ULISBOA ISEG'),
 'ulisboa-fmv': ('Universidade de Lisboa', 'Universidade de Lisboa',
              'Faculty of Veterinary Medicine', 'Faculdade de Medicina Veterinária', 'ULISBOA FMV'),
 'ulisboa-ff': ('Universidade de Lisboa', 'Universidade de Lisboa',
              'Faculty of Pharmacy', 'Faculdade de Farmácia', 'ULISBOA FF'),
 'uminho':   ('Universidade do Minho', 'Universidade do Minho',
              'School of Engineering', 'Escola de Engenharia', 'UMINHO'),
 'iscteiul-eta': ('Iscte – University Institute of Lisbon', 'Iscte — Instituto Universitário de Lisboa',
              'School of Technology and Architecture', 'Escola de Tecnologia e Arquitectura', 'ISCTE-IUL ETA'),
 'ulht-deisi':('Universidade Lusófona de Humanidades e Tecnologias', 'Universidade Lusófona de Humanidades e Tecnologias',
              'Departamento de Engenharia Informática e Sistemas de Informação',
              'Departamento de Engenharia Informática e Sistemas de Informação', 'ULHT DEISI'),
 'ulht-mge': ('Universidade Lusófona de Humanidades e Tecnologias', 'Universidade Lusófona de Humanidades e Tecnologias',
              'Escola de Ciências Econômicas e das Organizações',
              'Escola de Ciências Econômicas e das Organizações', 'ULHT MGE'),
 'uporto-fcup': ('Universidade do Porto', 'Universidade do Porto',
              'Faculdade de Ciências', 'Faculdade de Ciências', 'UPORTO FCUP'),
 'ipl-isel': ('Instituto Politécnico de Lisboa', 'Instituto Politécnico de Lisboa',
              'Instituto Superior de Engenharia de Lisboa', 'Instituto Superior de Engenharia de Lisboa', 'IPL ISEL'),
 'ips-ests': ('Polytechnic Institute of Setúbal', 'Instituto Politécnico de Setúbal',
              'Escola Superior de Tecnologia de Setúbal', 'Escola Superior de Tecnologia de Setúbal', 'IPS ESTS'),
 'other-esep':('Nursing School of Porto', 'Escola Superior de Enfermagem do Porto',
              '', '', 'ESEP'),
}

PHD = ('PhD Dissertation', 'Dissertação de Doutoramento')
MSC = ('MSc Thesis', 'Tese de Mestrado')

# ordered: (group, asset stem, label_en, label_pt)
BLOCKS = [
 ('manual',    'other-novathesis-phd-en-lua', 'The <b>nova</b>thesis manual', 'O manual <b>nova</b>thesis'),
 ('nova-fct',  'nova-fct-phd-en-lua', *PHD),
 ('nova-fct',  'nova-fct-msc-en-lua', *MSC),
 ('nova-fct',  'nova-fct-cbbi-msc-en-lua',
     'MSc in Computational Biology &amp; Bioinformatics', 'Mestrado em Biologia Computacional &amp; Bioinformática'),
 ('nova-fct',  'nova-fct-di-adc-bsc-en-lua', 'BSc in Computer Science', 'Licenciatura em Informática'),
 ('nova-fcsh', 'nova-fcsh-phd-en-lua', *PHD),
 ('nova-itqb', 'nova-itqb-gray-phd-en-lua', 'PhD Dissertation — Gray', 'Dissertação de Doutoramento — Cinza'),
 ('nova-itqb', 'nova-itqb-green-phd-en-lua', 'PhD Dissertation — Green', 'Dissertação de Doutoramento — Verde'),
 ('nova-ensp', 'nova-ensp-phd-en-lua', *PHD),
 ('ulisboa-ist',  'ulisboa-ist-phd-en-lua', *PHD),
 ('ulisboa-fcul', 'ulisboa-fcul-phd-en-lua', *PHD),
 ('ulisboa-iseg', 'ulisboa-iseg-phd-en-lua', *PHD),
 ('ulisboa-fmv',  'ulisboa-fmv-phd-en-lua', *PHD),
 ('ulisboa-ff',   'ulisboa-ff-phd-en-lua', *PHD),
 ('uminho',    'uminho-eeng-phd-en-lua', *PHD),
 ('iscteiul-eta', 'iscteiul-eta-phd-en-lua', *PHD),
 ('ulht-deisi','ulht-deisi-phd-en-lua', *PHD),
 ('ulht-mge',  'ulht-mge-phd-en-lua', *PHD),
 ('uporto-fcup','uporto-fcup-phd-en-lua', *PHD),
 ('ipl-isel',  'ipl-isel-msc-en-lua', *MSC),
 ('ipl-isel',  'ipl-isel-meb-msc-en-lua', 'MSc in Biomedical Engineering', 'Mestrado em Engenharia Biomédica'),
 ('ips-ests',  'ips-ests-msc-en-lua', *MSC),
 ('other-esep','other-esep-msc-en-lua', *MSC),
]

# group -> (display name, github handle)
CREDITS = {
 'ulisboa-ff':  ('Afonso Nóbrega', 'nobrega8'),
 'uporto-fcup': ('Guilherme Borges', 'sgtpepperpt'),
 'ipl-isel':    ('Gonçalo N. Duarte', 'MrDuartePT'),
}
CREDIT_LEAD = {'en': 'Support for this school contributed by',
               'pt': 'Suporte para esta escola contribuído por'}

PAGE_ALT = {  # (en, pt)
 'N':  ('back cover', 'contracapa'),
 '1':  ('front cover', 'capa'),
 '2':  ('front page', 'página de título'),
 'L1': ('example chapter', 'capítulo de exemplo'),
 'S':  ('spine', 'lombada'),
}

def find(stem, page):
    """Resolve stem-page.svg, tolerating an export-tool page suffix (-N-1.svg)."""
    exact = SVG / f'{stem}-{page}.svg'
    if exact.exists():
        return exact
    extra = sorted(SVG.glob(f'{stem}-{page}-[0-9].svg'))
    return extra[0] if extra else None

def ratio(path):
    """width/height from the SVG viewBox."""
    head = path.read_text(encoding='utf-8', errors='ignore')[:600]
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
    return float(m.group(1)) / float(m.group(2)) if m else 0.707

def build(lang):
    i = 0 if lang == 'en' else 1
    out, missing = [], []
    for gkey, group in _grouped():
        uni, school, tag = (G[gkey][i], G[gkey][2 + i], G[gkey][4])
        out.append('<section class="show-g">')
        if gkey == 'manual':
            head = ('The template itself' if i == 0 else 'O próprio template')
            out.append(f'<div class="show-hd"><h2>{head}</h2><span class="tag">novathesis</span></div>')
        else:
            title = f'{uni} — {school}' if school and school != uni else uni
            out.append(f'<div class="show-hd"><h2>{title}</h2><span class="tag">{tag}</span></div>')
        if gkey in CREDITS:
            who, gh = CREDITS[gkey]
            lead = CREDIT_LEAD['en' if i == 0 else 'pt']
            out.append(f'<p class="credit">{lead} <a href="https://github.com/{gh}">{who}</a> '
                       f'(<span class="mono">{gh}</span>)</p>')
        out.append('<div class="blocks">')
        for stem, lbl_en, lbl_pt in group:
            label = lbl_en if i == 0 else lbl_pt
            hi = ' hi' if gkey == 'manual' else ''
            out.append(f'<div class="block{hi}"><div class="block-lbl">{label}</div><div class="pages">')
            present = [(p, f) for p in ('N', '1', '2', 'L1') if (f := find(stem, p))]
            out.append('<div class="prow">')
            for p, f in present:
                alt = f'{stem} {PAGE_ALT[p][i]}'
                wide = ' wide' if ratio(f) > 1 else ''
                out.append(f'<span class="pg{wide}"><img src="../covers/SVG/{f.name}" alt="{alt}" loading="lazy"></span>')
            out.append('</div>')
            if (sp := find(stem, 'S')):
                alt = f'{stem} {PAGE_ALT["S"][i]}'
                out.append(f'<span class="pg sp"><img src="../covers/SVG/{sp.name}" alt="{alt}" loading="lazy"></span>')
            else:
                missing.append(f'{stem}: no spine')
            out.append('</div></div>')
            if not present:
                missing.append(f'{stem}: no pages at all')
        out.append('</div></section>')
    return '\n'.join(out), missing

def _grouped():
    seen, order = {}, []
    for gkey, stem, en, pt in BLOCKS:
        if gkey not in seen:
            seen[gkey] = []
            order.append(gkey)
        seen[gkey].append((stem, en, pt))
    return [(k, seen[k]) for k in order]

LEDE = {
 'en': ('<h1>Showcase</h1>'
        '<p>Every page the template produces, for each school and degree: back cover, front cover, front page, '
        'an example chapter, and the spine underneath. Missing panels simply mean that school does not use that page.</p>'
        '<p>All samples are compiled from the current template with LuaLaTeX, in English.</p>'),
 'pt': ('<h1>Galeria</h1>'
        '<p>Todas as páginas que o template produz, para cada escola e grau: contracapa, capa, página de título, '
        'um capítulo de exemplo e, em baixo, a lombada. A ausência de uma página significa que essa escola não a usa.</p>'
        '<p>Todos os exemplos são compilados com o template actual em LuaLaTeX, em inglês.</p>'),
}

SIZES = [('560', 'S'), ('720', 'M'), ('960', 'L')]
CTL_LBL = {'en': 'Size', 'pt': 'Tamanho'}
CTL_NAME = {'en': {'S': 'Small', 'M': 'Medium', 'L': 'Large'},
            'pt': {'S': 'Pequeno', 'M': 'Médio', 'L': 'Grande'}}

def control(lang):
    btns = ''.join(
        f'<button type="button" class="sz" data-w="{w}" aria-pressed="{str(w == "720").lower()}"'
        f' title="{CTL_NAME[lang][s]}">{s}</button>' for w, s in SIZES)
    return f'<div class="show-ctl"><span>{CTL_LBL[lang]}</span>{btns}</div>'

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

for lang in ('en', 'pt'):
    p = SITE / lang / 'showcase.html'
    src = p.read_text(encoding='utf-8')
    body, missing = build(lang)
    new_main = (f'<main class="page">\n<div class="lede">{LEDE[lang]}</div>\n'
                f'{control(lang)}\n'
                f'<div class="show">\n{body}\n</div>\n{SCRIPT}\n</main>')
    out, n = re.subn(r'<main class="page">.*?</main>', lambda m: new_main, src, flags=re.S)
    assert n == 1, f'{p}: <main> not found ({n} matches)'
    if out == src:
        print(f'{p.relative_to(SITE)}: already up to date')
    else:
        p.write_text(out, encoding='utf-8')
        print(f'{p.relative_to(SITE)}: written')

print('\nAssets not available (panel simply omits them):')
for m in dict.fromkeys(missing):
    print('  ·', m)
