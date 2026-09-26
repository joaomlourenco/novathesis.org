#!/usr/bin/env python3
"""Write en/ambassadors.html and pt/ambassadors.html.

    python3 tools/gen_ambassadors.py

The roll is built from REPOS, the same list behind "Find your school", so the
two pages cannot disagree about which schools exist. Who holds each post comes
from AMBASSADORS in nt_overrides.py; a school with no entry is shown as open,
which is the honest state and doubles as the ask.

Unlike the other generators this one writes the whole page: there is no
hand-written prose to preserve yet. Edit the COPY below, not the HTML.
"""
import sys, pathlib, html, re
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import nt_overrides as ov
from nt_schools import SITE, GROUPS, REPOS

LOGOS = SITE / 'logos'

ISSUE = ('https://github.com/joaomlourenco/novathesis/issues/new'
         '?title=%5BAMBASSADOR%5D%20')

COPY = {
 'en': dict(
   lang='en', other='pt', title='Ambassadors', nav='Ambassadors',
   desc='One volunteer per institution, keeping the novathesis template honest '
        'against their school\'s current thesis regulations.',
   h1='Ambassadors',
   lede='Every school in <b>nova</b>thesis was built from a regulation someone read once. '
        'Regulations change, and the template only finds out when somebody notices. '
        'An ambassador is that somebody, for one institution.',
   duties_h='What an ambassador does',
   duties=[('Watch the rules',
            'Keep an eye on your school\'s thesis regulations and formatting guidelines, '
            'and say when they change. This is the part nobody else can do.'),
           ('Check the output',
            'Once in a while, build your school\'s template and confirm the cover, the spine '
            'and the front matter still match what your institution asks for.'),
           ('Report, or fix',
            'Open an issue with what you found. A pull request is welcome but never expected '
            '— a precise report is worth more than a rushed patch.')],
   not_h='What it is not',
   not_p='It is not support duty. You are not expected to answer other students\' LaTeX '
         'questions, to maintain code, or to be available on any schedule. If your own '
         'thesis gets busy, hand the post back — that is a normal thing to do.',
   join_h='Take a school',
   join_p='Pick your institution below and open an issue. If your school is not listed yet, '
          'it needs a template before it needs an ambassador — start there instead.',
   join_btn='Volunteer for a school',
   roll_h='The schools',
   roll_p='One post per repository. Open posts are not a gap to be embarrassed about: '
          'the template works without them, it just learns about changes more slowly.',
   open_label='Open', open_cta='Take this one', logo_missing='logo?',
   repo_label='repository'),
 'pt': dict(
   lang='pt', other='en', title='Embaixadores', nav='Embaixadores',
   desc='Um voluntário por instituição, que mantém o template novathesis fiel aos '
        'regulamentos de tese em vigor na sua escola.',
   h1='Embaixadores',
   lede='Cada escola do <b>nova</b>thesis foi construída a partir de um regulamento que '
        'alguém leu uma vez. Os regulamentos mudam, e o template só fica a saber quando '
        'alguém repara. Um embaixador é esse alguém, para uma instituição.',
   duties_h='O que faz um embaixador',
   duties=[('Vigiar as regras',
            'Estar atento ao regulamento de teses e às normas de formatação da tua escola, '
            'e avisar quando mudam. Esta é a parte que mais ninguém pode fazer.'),
           ('Verificar o resultado',
            'De vez em quando, compilar o template da tua escola e confirmar que a capa, a '
            'lombada e os elementos iniciais continuam conformes ao que a instituição exige.'),
           ('Reportar, ou corrigir',
            'Abrir um issue com o que encontraste. Um pull request é bem-vindo mas nunca '
            'esperado — um relato preciso vale mais do que uma correcção à pressa.')],
   not_h='O que não é',
   not_p='Não é serviço de apoio. Não se espera que respondas a dúvidas de LaTeX de outros '
         'estudantes, que mantenhas código, nem que estejas disponível a horas certas. Se a '
         'tua própria tese apertar, devolve o lugar — é uma coisa perfeitamente normal.',
   join_h='Assume uma escola',
   join_p='Escolhe a tua instituição na lista e abre um issue. Se a tua escola ainda não '
          'estiver listada, primeiro precisa de um template e só depois de um embaixador — '
          'começa por aí.',
   join_btn='Voluntariar-me por uma escola',
   roll_h='As escolas',
   roll_p='Um lugar por repositório. Os lugares por preencher não são motivo de vergonha: '
          'o template funciona sem eles, apenas fica a saber das alterações mais devagar.',
   open_label='Por preencher', open_cta='Assumir este', logo_missing='logótipo?',
   repo_label='repositório'),
}

def initials(name):
    parts = [w for w in re.split(r'\s+', name) if w]
    return html.escape((parts[0][:1] + (parts[-1][:1] if len(parts) > 1 else '')).upper())

def portrait(a):
    """GitHub avatars are public, stable and chosen by the person themselves.
    A local file covers someone without GitHub who agreed to a picture. With
    neither, a monogram keeps the row the same shape instead of leaving a hole."""
    if a.get('github'):
        return (f'<img class="amb-face" loading="lazy" alt="" '
                f'src="https://avatars.githubusercontent.com/{html.escape(a["github"])}?s=160">')
    if a.get('photo'):
        return f'<img class="amb-face" loading="lazy" alt="" src="../people/{html.escape(a["photo"])}">'
    return f'<span class="amb-face amb-mono" aria-hidden="true">{initials(a["name"])}</span>'

def institutions():
    """REPOS folded to one entry per institution, keeping REPOS' order. An
    ambassador watches an institution's regulations, not a template, so NOVA
    FCT's three models and Lusofona's two are one post each, not five."""
    grouped = {r: g for g in ov.INSTITUTIONS_ALT for r in g['repos']}
    out, seen = [], set()
    for r in REPOS:
        g = grouped.get(r['repo'])
        key = g['key'] if g else r['repo']
        if key in seen:
            continue
        seen.add(key)
        repos = [x for x in REPOS
                 if (grouped[x['repo']]['key'] if x['repo'] in grouped else x['repo']) == key]
        out.append(dict(key=key, group=g, repos=repos, label=r['label'], section=r['group']))
    return out

def title(inst, c):
    i = 0 if c['lang'] == 'en' else 1
    return inst['group']['name'][i] if inst['group'] else inst['label']

def mark(inst, c):
    """The institution's own logo -- what a reader scanning for their school
    actually recognises. A missing file leaves a marked placeholder rather than
    a hole, so it is obvious which one still needs one."""
    f = LOGOS / f'{inst["key"]}.svg'
    name = html.escape(title(inst, c))
    if not f.exists():
        return (f'<span class="amb-logo amb-logo-missing" title="{name}">'
                f'<span>{html.escape(c["logo_missing"])}</span></span>')
    return (f'<a class="amb-logo" href="../logos/{f.name}" aria-label="{name}" title="{name}">'
            f'<img loading="lazy" alt="" src="../logos/{f.name}"></a>')

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
        # Mirrors the filled row: what the name occupies above, what the handle
        # occupies below.
        body = (f'<span class="amb-face amb-mono amb-empty" aria-hidden="true">+</span>'
                f'<span class="amb-person">'
                f'<a href="{ISSUE}{html.escape(title(inst, c))}">{c["open_cta"]}</a>'
                f'<span class="amb-state">{c["open_label"]}</span></span>')
    return (f'<div class="amb-row">'
            f'<div class="amb-id">{mark(inst, c)}<div class="amb-school">'
            f'{html.escape(title(inst, c))}<span class="repo">{models}</span></div></div>'
            f'<div class="amb-who">{body}</div></div>')

def build(lang):
    c = COPY[lang]
    duties = ''.join(f'<div><h3>{h}</h3><p>{p}</p></div>' for h, p in c['duties'])
    insts = institutions()
    groups = ''
    for key, gname in GROUPS:
        rows = [row(i, c) for i in insts if i['section'] == key]
        if not rows: continue
        groups += (f'<section class="amb-g"><div class="show-hd"><h2>{html.escape(gname)}</h2>'
                   f'<span class="show-tags"><span class="tag">{len(rows)}</span></span></div>'
                   + ''.join(rows) + '</section>')
    return (duties, groups)

def sync_home(filled, total):
    """Keep the home page's open-posts figure honest. It is a claim that goes
    stale the moment someone takes a school, so the generator that knows the
    number owns it rather than leaving it to be remembered."""
    import re as _re
    for lang in ('en', 'pt'):
        p = SITE / lang / 'index.html'
        if not p.exists():
            continue
        s = p.read_text(encoding='utf-8')
        s2, n = _re.subn(r'(<b data-amb-open>)\d+(</b>)', rf'\g<1>{total - filled}\g<2>', s)
        if n and s2 != s:
            p.write_text(s2, encoding='utf-8')
            print(f'{lang}/index.html: open posts -> {total - filled}')

def main():
    insts = institutions()
    for lang in ('en', 'pt'):
        c = COPY[lang]
        src = (SITE / lang / 'index.html').read_text(encoding='utf-8')
        head = ''.join(re.findall(r'<link rel="(?:preconnect|stylesheet|icon|me)"[^>]*>', src))
        head += ''.join(re.findall(r'<meta name="color-scheme"[^>]*>', src))
        head += ''.join(re.findall(r'<script>try\{var t=localStorage[^<]*</script>', src))
        head += ''.join(re.findall(r'<script src="\.\./theme\.js"></script>', src))
        header = re.search(r'<header class="hd">.*?</header>', src, re.S).group(0)
        header = header.replace('class="on"', 'class=""')
        # it sits under Contributing now, so that is the item that lights up
        header = header.replace('<a class="" href="contributing.html">',
                                '<a class="on" href="contributing.html">')
        footer = re.search(r'<footer class="ft">.*?</footer>', src, re.S).group(0)
        header = re.sub(r'(<a class="lang" href=")[^"]*(")',
                        rf'\1../{c["other"]}/ambassadors.html\2', header)
        duties, groups = build(lang)
        out = (f'<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
               f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
               f'<title>{c["title"]} · novathesis</title>\n'
               f'<meta name="description" content="{html.escape(c["desc"])}">\n{head}\n</head>\n'
               f'<body>\n{header}\n<main class="page">\n'
               f'<div class="lede"><h1>{c["h1"]}</h1><p>{c["lede"]}</p></div>\n'
               f'<div class="sec-hd"><h2>{c["duties_h"]}</h2></div>'
               f'<div class="cards3">{duties}</div>\n'
               f'<div class="note"><div><h3>{c["not_h"]}</h3>'
               f'<p style="margin-top:8px">{c["not_p"]}</p></div></div>\n'
               f'<div class="dark"><div><h2>{c["join_h"]}</h2>'
               f'<p style="margin-top:10px">{c["join_p"]}</p></div>'
               f'<a class="btn btn-p" href="{ISSUE}">{c["join_btn"]}</a></div>\n'
               f'<div class="sec-hd"><h2>{c["roll_h"]}</h2></div>'
               f'<p class="amb-note">{c["roll_p"]}</p>{groups}\n'
               f'</main>\n{footer}\n</body>\n</html>\n')
        p = SITE / lang / 'ambassadors.html'
        old = p.read_text(encoding='utf-8') if p.exists() else None
        if old == out:
            print(f'{lang}/ambassadors.html: already up to date')
        else:
            p.write_text(out, encoding='utf-8')
            held = sum(1 for i in insts if holder(i))
            print(f'{lang}/ambassadors.html: written  ({held}/{len(insts)} instituições)')
    sync_home(sum(1 for i in insts if holder(i)), len(insts))

if __name__ == '__main__':
    main()
