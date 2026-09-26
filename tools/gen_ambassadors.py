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
from nt_schools import SITE, GROUPS, REPOS, cover_stem, find

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
   open_label='Open', open_cta='Take this one', cover_label='Cover of',
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
   open_label='Por preencher', open_cta='Assumir este', cover_label='Capa de',
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

def cover(r, c):
    """A thumbnail of the school's own front cover, linking to the full drawing.
    The image itself stays decorative -- the school's name is right beside it --
    so the accessible name goes on the link instead, where a screen reader needs
    it. uminho's art is a wrap-around, clipped to the front face as the school
    cards clip it."""
    stem = cover_stem(r)
    f = find(stem, '1') if stem else None
    if not f:
        return ''
    cls = 'amb-cover crop' if r.get('crop') else 'amb-cover'
    label = html.escape(f'{c["cover_label"]} {r["label"]}')
    return (f'<a class="{cls}" href="../covers/SVG/{f.name}" aria-label="{label}" title="{label}">'
            f'<img loading="lazy" alt="" src="../covers/SVG/{f.name}"></a>')

def row(r, c):
    a = ov.AMBASSADORS.get(r['repo'])
    label = html.escape(r['label'])
    if a:
        who = html.escape(a['name'])
        if a.get('github'):
            gh = html.escape(a['github'])
            who = (f'<a href="https://github.com/{gh}">{who}</a>'
                   f'<span class="amb-gh">{gh}</span>')
        body = f'{portrait(a)}<span class="amb-person">{who}</span>'
    else:
        body = (f'<span class="amb-face amb-mono amb-empty" aria-hidden="true">+</span>'
                f'<span class="amb-name"><span class="tag">{c["open_label"]}</span> '
                f'<a href="{ISSUE}{html.escape(r["label"])}">{c["open_cta"]}</a></span>')
    return (f'<div class="amb-row">'
            f'<div class="amb-id">{cover(r, c)}<div class="amb-school">{label}'
            f'<span class="repo">{html.escape(r["repo"])}</span></div></div>'
            f'<div class="amb-who">{body}</div></div>')

def build(lang):
    c = COPY[lang]
    duties = ''.join(f'<div><h3>{h}</h3><p>{p}</p></div>' for h, p in c['duties'])
    groups = ''
    for key, gname in GROUPS:
        rows = [row(r, c) for r in REPOS if r['group'] == key]
        if not rows: continue
        groups += (f'<section class="amb-g"><div class="show-hd"><h2>{html.escape(gname)}</h2>'
                   f'<span class="show-tags"><span class="tag">{len(rows)}</span></span></div>'
                   + ''.join(rows) + '</section>')
    return (duties, groups)

def main():
    for lang in ('en', 'pt'):
        c = COPY[lang]
        src = (SITE / lang / 'index.html').read_text(encoding='utf-8')
        head = ''.join(re.findall(r'<link rel="(?:preconnect|stylesheet|icon|me)"[^>]*>', src))
        head += ''.join(re.findall(r'<meta name="color-scheme"[^>]*>', src))
        head += ''.join(re.findall(r'<script>try\{var t=localStorage[^<]*</script>', src))
        head += ''.join(re.findall(r'<script src="\.\./theme\.js"></script>', src))
        header = re.search(r'<header class="hd">.*?</header>', src, re.S).group(0)
        header = header.replace('class="on"', 'class=""')
        header = header.replace(f'<a class="" href="ambassadors.html">',
                                f'<a class="on" href="ambassadors.html">')
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
            filled = sum(1 for r in REPOS if r['repo'] in ov.AMBASSADORS)
            print(f'{lang}/ambassadors.html: written  ({filled}/{len(REPOS)} preenchidos)')

if __name__ == '__main__':
    main()
